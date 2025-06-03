from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

@Client.on_message(filters.command("MasterAppx"))
async def master_appx_handler(client, message: Message):
    buttons = [
        [InlineKeyboardButton("🔍 Find Appx URL", callback_data="find_appx")]
    ]
    text = (
        "**Send Appx API Url :**\n\n"
        "🔹 **If you don’t know Appx API URL**, then use the button below 👇"
    )
    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("find_appx"))
async def find_appx_callback(client, callback_query):
    await callback_query.message.edit_text(
        "**Please Send App Name You want to Search**\n\n"
        "**Format:-** `Exampur`"
    )
