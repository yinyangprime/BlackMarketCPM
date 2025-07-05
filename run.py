import os
import threading
import asyncio

def start_bot():
    from yybot import run_bot
    asyncio.run(run_bot())

def start_api():
    os.system("python3 main.py")

if __name__ == '__main__':
    print("🚀 Starting YinYang Black Market System...")
    api_thread = threading.Thread(target=start_api)
    api_thread.start()
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()
