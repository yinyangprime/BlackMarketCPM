from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from datetime import datetime
import os

KEYS_FILE = 'YinYangKeys.json'
BOT_OWNER = 7370949688  # Ganti dengan Telegram ID owner

def is_key_valid(user_key, user_id):
    try:
        with open(KEYS_FILE, 'r') as f:
            keys = json.load(f)
    except FileNotFoundError:
        return False, "Key database tidak dijumpai."

    for key in keys:
        if key["key"] == user_key:
            if key.get("telegram_id") not in [None, user_id]:
                return False, "Key ini sudah didaftarkan kepada ID lain."
            if key.get("expiry") and datetime.strptime(key["expiry"], "%Y-%m-%d %H:%M:%S") < datetime.now():
                return False, "Kunci telah tamat tempoh."
            return True, "Key sah! Anda boleh akses sistem."
    return False, "Key tidak sah atau telah tamat tempoh."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(
        [["/beli", "/key"], ["/hubungi_admin", "/status"]], resize_keyboard=True
    )
    await update.message.reply_text(
        "Selamat datang ke Yin Yang Black Market\n\n"
        "- 1 Hari = RM10\n"
        "- 7 Hari = RM30\n"
        "- 30 Hari = RM50\n"
        "- Lifetime = RM150\n\n"
        "Promo code: yinhensem untuk 1 hari PERCUMA\n"
        "Command tersedia:\n"
        "/beli – Untuk beli key\n"
        "/key – Untuk semak key\n"
        "/status – Status sistem\n"
        "/hubungi_admin – Bantuan & pertanyaan",
        reply_markup=reply_markup
    )

async def beli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Untuk beli key, buat bayaran ke DuitNow QR & hantar bukti ke admin: @xiixmmi")

async def key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if not args:
        await update.message.reply_text("Sila masukkan key. Contoh: /key ABC123")
        return
    user_key = args[0]
    valid, msg = is_key_valid(user_key, user_id)
    await update.message.reply_text(msg)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sistem aktif dan stabil. Semua fungsi OK.")

async def hubungi_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hubungi admin di Telegram: @xiixmmi")

def run_bot(token):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("beli", beli))
    app.add_handler(CommandHandler("key", key))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("hubungi_admin", hubungi_admin))
    print("Telegram bot berjalan...")
    app.run_polling()
