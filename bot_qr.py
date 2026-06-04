import telebot
import datetime
import pytz
import qrcode
from PIL import Image
from io import BytesIO

TOKEN = "8239347929:AAEGr4xywdLShOGiAywcwJlCiODGExZ7nQ0"   # ← Cambia con il tuo token

bot = telebot.TeleBot(TOKEN)

dati_fissi = [
    "MENSILE",
    "ANM",
    "2026-06-02T11:40",
    "2026-06-30T23:59",
    "MGZET9AUBP",
    "11",
    "2",
    "4",
    "05c36d9fce339ec6dc8711e828433a27bd3ff535a49b2abe7f6a02927f"
]

variants = {
    "0.5cm": 59,
    "1cm": 118,
    "1.5cm": 177,
    "2cm": 236
}

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
    genera_qr_code(call.message.chat.id, size)
    bot.answer_callback_query(call.id)

def genera_qr_code(chat_id, size):
    pixels = variants[size]

    tz = pytz.timezone('Europe/Rome')
    timestamp = datetime.datetime.now(tz).isoformat(timespec='seconds')

    dati = dati_fissi + [timestamp]
    testo = "\n".join(dati)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=16, border=1)
    qr.add_data(testo)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#000000", back_color="#FFFFFF")
    img = img.resize((pixels, pixels), Image.Resampling.NEAREST)

    bio = BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)

    bot.send_photo(chat_id, bio, caption=f"✅ QR {size} generato\n⏰ {timestamp}")

print("🤖 Bot aggiornato avviato...")
bot.infinity_polling()
