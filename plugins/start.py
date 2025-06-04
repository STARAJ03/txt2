from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(bot, message: Message):
    user = message.from_user.first_name
    await message.reply_photo(
        photo="https://i.ibb.co/cSyLcHNz/Chat-GPT-Image-Jun-3-2025-03-16-31-PM.png",  # replace with your thumbnail link
        caption=(
            f"**Hello {user}** 👋\n"
            "I'm a Powerful TXT Extractor Bot.\n"
            "__Note: App with Star Indicator Not For Public.__\n\n"
            "**Managed By : @Aublic**\n\n"
            "**Usage:** First Select the App Listed Below."
        ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔑 Master Appx", callback_data="master_appx"),
                InlineKeyboardButton("🔍 Find API", callback_data="find_appx")
            ],
            [
                InlineKeyboardButton("📲 Appx OTP Login", callback_data="otp_login")
            ]
        ])
    )

# Callback handler to route button clicks
@Client.on_callback_query()
async def handle_callback(bot, callback):
    data = callback.data

    if data == "master_appx":
        await callback.message.delete()
        await bot.send_message(callback.from_user.id, 
            "🔑 **Send Appx API URL:**\n\nIf you don't know it, click 'Find API' from the menu.")
        input1 = await bot.listen(callback.from_user.id)
        api_url = input1.text.strip()
        await input1.delete()
        from plugins.universal import account_login
        await account_login(bot, callback.message, api_url)

    elif data == "find_appx":
        await callback.message.delete()
        await bot.send_message(callback.from_user.id, 
            "🔍 Please send the **App Name** you want to search.\n\nFormat: `Exampur`")

    elif data == "otp_login":
        await callback.message.delete()
        from plugins.otp_login import otp_login_flow
        await otp_login_flow(bot, callback.message)

    await callback.answer()
