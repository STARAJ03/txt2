user_searching = set()

@Client.on_callback_query()
async def handle_callback(bot, callback):
    if callback.data == "find_appx":
        await callback.message.delete()
        await bot.send_message(callback.from_user.id, "🔍 Please send the **App Name** you want to search.\n\nFormat: `Exampur`")
        user_searching.add(callback.from_user.id)
        await callback.answer()

@Client.on_message(filters.text & filters.private)
async def find_appx_url(bot, message: Message):
    if message.from_user.id not in user_searching:
        return  # Ignore messages from users not in search mode

    query = message.text.strip().lower()

    matches = [f"{name} → {url}" for name, url in ACADEMY_HOSTS.items() if query in name.lower()]

    if not matches:
        await message.reply_text("❌ No matching academy found. Try another name.")
    else:
        results = "\n\n".join(matches[:30])
        await message.reply_text(f"🔍 **Matching Academies:**\n\n{results}\n\n👉 Paste any URL above to use with `/MasterAppx`.")

    user_searching.remove(message.from_user.id)  # reset search mode
