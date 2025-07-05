from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from datetime import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
KEYS_FILE = "YinYangKeys.json"
PROMO_CODE = "yinhensem"
ADMIN_ID = 754978535

def semak_key(user_key, telegram_id=None):
    try:
        with open(KEYS_FILE, ' 'r') as f:
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"""
👑 Selamat Datang ke *Yin Yang Black Market Bot* 👑
📦 Harga Key:
• 1 Hari – RM10
• 7 Hari – RM30
• 30 Hari – RM50
• Lifetime – RM150

🎁 Kod promosi: *{PROMO_CODE}* untuk 1 hari percuma!

🔧 Arahan:
/beli — Beli key
/key — Semak key
/status — Status bot
/hubungi_admin — Bantuan
    """
    await update.message.reply_text(msg, parse_mode="Markdown")

async def key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("❗ Masukkan key. Contoh: /key ABC123", parse_mode="Markdown")
        return
    user_key = args[0]
    valid, msg = semak_key(user_key, update.effective_user.id)
    await update.message.reply_text(msg)

async def beli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪙 Beli key:
Bayar ke QR DuitNow & hantar resit ke admin: @xiixmmi")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Bot aktif dan berfungsi.")

async def hubungi_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Admin: @xiixmmi")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("key", key))
    app.add_handler(CommandHandler("beli", beli))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("hubungi_admin", hubungi_admin))
    await app.run_polling()
