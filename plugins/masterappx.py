from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from plugins.universal import account_login

@Client.on_message(filters.command("MasterAppx") & filters.private)
async def master_appx(bot, message: Message):
    buttons = [
        [InlineKeyboardButton("🔍 Find Appx URL", callback_data="find_appx")],
    ]
    await message.reply_text(
        "**Send Appx API URL:**\n\n"
        "If you don't know the Appx API URL, use the 'Find Appx URL' button below.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    try:
        input1 = await bot.listen(message.chat.id)
        api_url = input1.text.strip()
        await input1.delete()
    except Exception:
        return await message.reply_text("❌ Failed to read API URL input.")

    await account_login(bot, message, api_url)
