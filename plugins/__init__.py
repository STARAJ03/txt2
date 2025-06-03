from pyrogram import filters
from pyrogram import Client as stark
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from main import LOGGER, prefixes, AUTH_USERS
from config import Config
import os
import sys


@stark.on_message(filters.command(["start"]))
async def Start_msg(bot: stark, m: Message):
    await bot.send_photo(
        m.chat.id,
        photo="https://telegra.ph/file/cef3ef6ee69126c23bfe3.jpg",
        caption=(
            "**Hi I am All in One Extractor Bot**.\n"
            "Press **/pw** for **Physics Wallah**..\n\n"
            "Press **/e1** for **E1 Coaching App**..\n\n"
            "Press **/vidya** for **Vidya Bihar App**..\n\n"
            "Press **/ocean** for **Ocean Gurukul App**..\n\n"
            "Press **/winners** for **The Winners Institute**..\n\n"
            "Press **/rgvikramjeet** for **Rgvikramjeet App**..\n\n"
            "Press **/txt** for  **Ankit With Rojgar,**\n**The Mission Institute,**\n**The Last Exam App**..\n\n"
            "Press **/cp** for **Classplus App**..\n\n"
            "Press **/cw** for **Careerwill App**..\n\n"
            "Press **/khan** for **Khan GS App**..\n\n"
            "Press **/exampur** for **Exampur App**..\n\n"
            "Press **/samyak** for **Samyak IAS**..\n\n"
            "Press **/chandra** for **Chandra App**..\n\n"
            "Press **/mgconcept** for **MG Concept App**..\n\n"
            "Press **/down** for **Downloading URL lists**..\n\n"
            "Press **/forward** to **Forward from one channel to others**..\n\n"
            "**𝗕𝗼𝘁 𝗢𝘄𝗻𝗲𝗿 : @Aublic**"
        )
    )


@stark.on_message(filters.command(["restart"]) & filters.create(lambda _, __, msg: not msg.edit_date))
async def restart_handler(_, m):
    await m.reply_text("Restarted!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@stark.on_message(filters.command(["log"]) & filters.create(lambda _, __, msg: not msg.edit_date))
async def log_msg(bot: stark, m: Message):   
    await bot.send_document(m.chat.id, "log.txt")
