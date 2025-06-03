from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    import asyncio
    from pyrogram import Client, idle
    from config import Config
    import logging
    from logging.handlers import RotatingFileHandler

    # Setup logging as you have

    AUTH_USERS = [int(chat) for chat in Config.AUTH_USERS.split(",") if chat != ""]

    bot = Client(
        "StarkBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=20,
        plugins=dict(root="plugins"),
        workers=50,
    )

    async def main():
        await bot.start()
        bot_info = await bot.get_me()
        logging.info(f"<--- @{bot_info.username} Started (c) AublicXRobot --->")
        await idle()
        await bot.stop()
        logging.info("<--- Bot Stopped --->")

    # Run flask app in a separate thread
    threading.Thread(target=run_flask).start()

    # Run bot event loop
    asyncio.run(main())
