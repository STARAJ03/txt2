from pyrogram import filters
from pyrogram import Client as stark
from pyrogram.types import Message


@stark.on_message(filters.command(["start"]))
async def Start_msg(bot: stark, m: Message):
    user_name = m.from_user.first_name if m.from_user else 'User'
    caption = (f"Hello {user_name}\n"
               "I'm a Powerful TXT Extractor Bot.\n"
               "For more details, send /help..\n\n"
               "Managed By : @Aublic\n\n"
               "Choose an app below 👇")
    await bot.send_photo(
        m.chat.id,
        photo=
        "https://i.ibb.co/cSyLcHNz/Chat-GPT-Image-Jun-3-2025-03-16-31-PM.png",
        caption=caption)


@stark.on_message(filters.command(["help"]))
async def help_msg(bot: stark, m: Message):
    help_text = (
        "📝 **Bot Commands Overview**\n\n"
        "• **/pw** – Physics Wallah\n"
        "• **/e1** – E1 Coaching App\n"
        "• **/vidya** – Vidya Bihar App\n"
        "• **/ocean** – Ocean Gurukul App\n"
        "• **/winners** – The Winners Institute\n"
        "• **/rgvikramjeet** – Rgvikramjeet App\n"
        "• **/txt** – Ankit With Rojgar, The Mission Institute, The Last Exam App\n"
        "• **/cp** – Classplus App\n"
        "• **/cw** – Careerwill App\n"
        "• **/khan** – Khan Gs App\n"
        "• **/exampur** – Exampur App\n"
        "• **/samyak** – Samyak IAS\n"
        "• **/chandra** – Chandra App\n"
        "• **/mgconcept** – MG Concept App\n"
        "• **/down** – Downloading URL lists\n"
        "• **/forward** – Forward from one channel to others\n\n"
        "**Usage:**\nSend the command as per your requirement to start extraction from that app."
    )
    await m.reply_text(help_text)
