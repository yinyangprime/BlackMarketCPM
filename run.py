import asyncio
import threading
import main  # API (Flask)
from yinyangbot import run_bot  # Telegram Bot

def start_flask():
    main.app.run(host="0.0.0.0", port=8080)

def start_telegram():
    asyncio.run(run_bot())

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
    start_telegram()
