import telebot
import datetime
import pytz
import qrcode
from PIL import Image
from io import BytesIO

TOKEN = "INSERISCI_QUI_IL_TUO_TOKEN"   # ← CAMBIA DOPO con il tuo token!

bot = telebot.TeleBot(TOKEN)

dati_fissi = [
    "7_GIORNI", "ANM", "2026-02-22T17:42", "2026-02-28T23:59",
    "E3GGJ2BYZE", "15", "2", "4",
    "050e9ecf31070627ed6a06783002899a3059e5749040e7f77aeb18f80c"
]

variants = {"0.5cm": 59, "1cm": 118, "1.5cm": 177, "2cm": 236, "2.5cm": 295}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for size in variants:
        markup.add(telebot.types.InlineKeyboardButton(size, callback_data=size))
    
    bot.send_message(message.chat.id, 
        "👋 *Generatore QR ANM*\n\nClicca sulla dimensione:", 
        reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    size = call.data
    pixels = variants[size]

    tz = pytz.timezone('Europe/Rome')
    timestamp = datetime.datetime.now(tz).isoformat(timespec='seconds')

    dati = dati_fissi + [timestamp]
    testo = "\n".join(dati)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=1)
    qr.add_data(testo)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#000000", back_color="#FFFFFF")
    img = img.resize((pixels, pixels), Image.Resampling.NEAREST)

    bio = BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)

    bot.send_photo(call.message.chat.id, bio, 
                   caption=f"✅ QR {size} generato\n⏰ {timestamp}")

print("Bot avviato...")
bot.infinity_polling()
