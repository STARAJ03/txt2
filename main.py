import os
from pyrogram import Client, idle
from flask import Flask
import asyncio
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

# Your Pyrogram bot code here
bot = Client(
    "StarkBot",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    plugins=dict(root="plugins"),
    workers=50,
)

async def start_bot():
    await bot.start()
    print("Bot started")
    await idle()
    await bot.stop()

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask server in a separate thread
    threading.Thread(target=run_flask).start()

    # Run pyrogram bot in asyncio event loop
    asyncio.run(start_bot())
