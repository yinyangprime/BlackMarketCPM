from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
import json
from datetime import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Ambil dari environment (Render / Replit)
KEYS_FILE = "YinYangKeys.json"
PROMO_CODE = "yinhensem"

# Fungsi semak key
def semak_key(user_key, telegram_id=None):
    try:
        with open(KEYS_FILE, 'r') as f:
            keys = json.load(f)
    except:
        return False, "❌ Database kunci tidak dijumpai."

    for key in keys:
        if key["key"] == user_key:
            if telegram_id and key.get("telegram_id") not in [None, telegram_id]:
                return False, "❌ Kunci sudah dikaitkan dengan pengguna lain."
            if key.get("expiry"):
                if datetime.strptime(key["expiry"], "%Y-%m-%d %H:%M:%S") < datetime.now():
                    return False, "❌ Kunci telah tamat tempoh."
            return True, "✅ Key sah & aktif!"
    return False, "❌ Key tidak sah atau telah tamat tempoh."

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"""
👑 Selamat Datang ke *Yin Yang Black Market Bot* 👑
💻 Sistem jual beli key CPM (Car Parking Multiplayer) tersedia secara automatik.

📦 Harga Key:
• 1 Hari – RM10
• 7 Hari – RM30
• 30 Hari – RM50
• Lifetime – RM150

🎁 Guna kod promosi: *{PROMO_CODE}* untuk key 1 hari percuma!

🔧 Arahan:
• /beli — Beli key
• /key — Semak key
• /status — Status key
• /hubungi_admin — Bantuan

⚠️ Semua urusan dipantau. Sistem ini hak milik eksklusif *Yin Yang / TikTok: Yin Yang*.
    """
    await update.message.reply_text(msg, parse_mode="Markdown")

# /key command
async def key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("❗ Sila masukkan key. Contoh: `/key abc123`", parse_mode="Markdown")
        return
    key = args[0]
    valid, msg = semak_key(key, update.effective_user.id)
    await update.message.reply_text(msg)

# /beli command
async def beli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪙 Untuk pembelian key, sila buat bayaran ke QR DuitNow dan hantarkan resit kepada admin. Harga:\n\n1 Hari – RM10\n7 Hari – RM30\n30 Hari – RM50\nLifetime – RM150\n\nKod promosi: *yinhensem* untuk 1 hari percuma!\n\nAdmin: @xiixmmi", parse_mode="Markdown")

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Bot aktif dan sedia menerima arahan.\nGunakan /start untuk melihat menu penuh.")

# /hubungi_admin
async def hubungi_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Hubungi admin di Telegram: @xiixmmi")

# Start bot
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("key", key))
    app.add_handler(CommandHandler("beli", beli))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("hubungi_admin", hubungi_admin))
    await app.run_polling()
