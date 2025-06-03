from pyrogram import filters
from pyrogram import Client as stark
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from main import LOGGER, prefixes, AUTH_USERS
from config import Config
import os
import sys

@stark.on_message(filters.command(["start"]) & ~filters.edited)
async def Start_msg(bot: stark , m: Message):
    await bot.send_photo(
        m.chat.id,
        photo="https://i.ibb.co/cSyLcHNz/Chat-GPT-Image-Jun-3-2025-03-16-31-PM.png",
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    user_name = m.from_user.first_name if m.from_user else 'User'
    keyboard = [
        [InlineKeyboardButton("👑 OWNER", url="https://t.me/Aublic")],  # Owner button JPG ke niche
        [
            InlineKeyboardButton("Physics Wallah", callback_data="pw"),
            InlineKeyboardButton("E1 Coaching App", callback_data="e1"),
        ],
        [
            InlineKeyboardButton("Vidya Bihar App", callback_data="vidya"),
            InlineKeyboardButton("Ocean Gurukul App", callback_data="ocean"),
        ],
        [
            InlineKeyboardButton("The Winners Institute", callback_data="winners"),
            InlineKeyboardButton("Rgvikramjeet App", callback_data="rgvikramjeet"),
        ],
        [
            InlineKeyboardButton("Ankit With Rojgar", callback_data="txt"),
            InlineKeyboardButton("Classplus App", callback_data="cp"),
        ],
        [
            InlineKeyboardButton("Careerwill App", callback_data="cw"),
            InlineKeyboardButton("Khan Gs App", callback_data="khan"),
        ],
        [
            InlineKeyboardButton("Exampur App", callback_data="exampur"),
            InlineKeyboardButton("Samyak IAS", callback_data="samyak"),
        ],
        [
            InlineKeyboardButton("Chandra App", callback_data="chandra"),
            InlineKeyboardButton("MG Concept App", callback_data="mgconcept"),
        ],
        [
            InlineKeyboardButton("Download URL lists", callback_data="down"),
            InlineKeyboardButton("Forward", callback_data="forward"),
        ],
    ]
    caption = f"""Hello {user_name}
I'm a Powerful TXT Extractor Bot.
Note : App with Star Indicator Not For Public.

Managed By : @Aublic
"""
    

@stark.on_message(filters.command(["restart"]) & ~filters.edited)
async def restart_handler(_, m):
    await m.reply_text("Restarted!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@stark.on_message(filters.command(["log"]) & ~filters.edited)
async def log_msg(bot: stark , m: Message):   
    await bot.send_document(m.chat.id, "log.txt")
