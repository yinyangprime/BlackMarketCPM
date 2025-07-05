import os
import threading
import asyncio
from yinyangbot import run_bot  # Fungsi async sebenar dari yinyangbot
import main  # Flask API

def start_api():
    main.app.run(host="0.0.0.0", port=int(os.getenv("SERVER_PORT", 8080)))

def start_bot():
    asyncio.run(run_bot())  # ✅ Hanya satu asyncio.run()

if __name__ == "__main__":
    print("🚀 Starting YinYang Black Market System...")

    api_thread = threading.Thread(target=start_api)
    api_thread.start()

    start_bot()
