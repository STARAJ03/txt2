import asyncio
import logging
import threading
from flask import Flask
from pyrogram import Client, idle
from pyromod import listen
from config import Config
from logging.handlers import RotatingFileHandler

# Setup logging
LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# Allowed users
AUTH_USERS = [int(x) for x in Config.AUTH_USERS.split(",") if x]

# Pyrogram Client setup
bot = Client(
    "StarkBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins"),
    sleep_threshold=20,
    workers=50,
)

# Flask app to prevent "no port detected" on Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# Bot main function
async def main():
    await bot.start()
    bot_info = await bot.get_me()
    LOGGER.info(f"<--- @{bot_info.username} Started Successfully (c) AublicxRobot --->")
    await idle()
    await bot.stop()
    LOGGER.info("<--- Bot Stopped --->")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
