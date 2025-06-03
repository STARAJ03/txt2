from pyrogram import Client, filters
from pyrogram.types import Message
from appx_api import ACADEMY_HOSTS

@Client.on_message(filters.text & filters.private)
async def find_appx_url(bot, message: Message):
    query = message.text.strip().lower()
    
    # Filter API URLs by matching academy name
    matches = [f"{name} → {url}" for name, url in ACADEMY_HOSTS.items() if query in name.lower()]
    
    if not matches:
        return await message.reply_text("❌ No matching academy found. Try another name.")
    
    results = "\n\n".join(matches[:30])  # Show only first 30 matches
    await message.reply_text(f"🔍 **Matching Academies:**\n\n{results}\n\n👉 Paste any URL above to use with `/MasterAppx`.")
