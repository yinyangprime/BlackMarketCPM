import os
import threading
import asyncio

# Jalankan bot Telegram
def start_bot():
    from yinyangbot import main as bot_main
    asyncio.run(bot_main())

# Jalankan Flask API
def start_api():
    os.system("python3 main.py")

if __name__ == '__main__':
    print("🚀 Starting YinYang Black Market System...")

    # Thread untuk API Flask
    api_thread = threading.Thread(target=start_api)
    api_thread.start()

    # Thread untuk Telegram Bot
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()
