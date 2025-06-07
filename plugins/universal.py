import os
import cloudscraper
from pyrogram.types import Message
from pyrogram import Client
from plugins.decoder import decode
import aiofiles

async def account_login(bot: Client, m: Message, host: str):
    import asyncio
    scraper = cloudscraper.create_scraper()
    editable = await m.reply_text("**Send ID*Password**\nOR\n**Token*UserID**")

    try:
        input1: Message = await bot.listen(m.chat.id)
        raw_text = input1.text.strip()
        await input1.delete()
    except Exception:
        return await editable.edit("❌ Failed to read input.")

    if len(raw_text.split("*")) != 2:
        return await editable.edit("❌ Invalid format. Use: `ID*Password` or `Token*UserID`")

    part1, part2 = raw_text.split("*")
    login_mode = "idpass" if "@" in part1 or part1.isdigit() else "token"

    token, userid = None, None
    try:
        if login_mode == "idpass":
            res = scraper.post(
                f"{host}/post/userLogin",
                data={"email": part1, "password": part2},
                headers={
                    "Auth-Key": "appxapi",
                    "User-Id": "-2",
                    "Authorization": "",
                    "User_app_category": "",
                    "Language": "en",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "okhttp/4.9.1"
                }
            ).json()
            token = res.get("data", {}).get("token")
            userid = res.get("data", {}).get("userid")
            if not token or not userid:
                return await editable.edit("❌ Login failed! Check credentials.")
            await editable.edit("✅ Login successful via ID & Password.")
        else:
            token, userid = part1, part2
            await editable.edit("✅ Login successful via Token.")
    except Exception as e:
        return await editable.edit(f"❌ Login request failed!\n{e}")

    headers = {
        "Host": host.replace("https://", "").replace("http://", ""),
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-Id": str(userid),
        "Authorization": str(token)
    }

    # Get courses
    try:
        course_list = scraper.get(f"{host}/get/mycourse?userid={userid}", headers=headers).json()
        courses = course_list.get("data", [])
        if not courses:
            return await editable.edit("❌ No courses found!")
    except Exception as e:
        return await editable.edit(f"❌ Failed to fetch courses.\n{e}")

    course_text = ""
    for course in courses:
        course_text += f"```{course['id']}``` - **{course['course_name']}**\n\n"
    await editable.edit(f"**Available Batches:**\n\n{course_text}")

    # Select course ID
    try:
        msg1 = await m.reply_text("📥 Now send the **Batch ID**:")
        input2 = await bot.listen(m.chat.id)
        batch_id = input2.text.strip()
        await msg1.delete()
        await input2.delete()
    except Exception:
        return await m.reply_text("❌ Failed to read batch ID.")

    try:
        course_info = scraper.get(f"{host}/get/course_by_id?id={batch_id}", headers=headers).json()
        course_title = course_info["data"][0]["course_name"]
    except Exception:
        return await m.reply_text("❌ Invalid Batch ID or fetch error.")

    # Subject fetch
    try:
        subs = scraper.get(f"{host}/get/allsubjectfrmlivecourseclass?courseid={batch_id}", headers=headers).json().get("data", [])
        if not subs:
            return await m.reply_text("❌ No subjects found for this batch.")
    except Exception:
        return await m.reply_text("❌ Failed to fetch subjects.")

    subj_text, subj_ids = "", ""
    for sub in subs:
        subj_text += f"```{sub['subjectid']}``` - **{sub['subject_name']}**\n\n"
        subj_ids += f"{sub['subjectid']}&"
    await m.reply_text(subj_text)

    # Topic selection
    try:
        msg2 = await m.reply_text(f"Send **Topic IDs** like: `1&2&3`\n\nTo download all: ```{subj_ids}```")
        input3 = await bot.listen(m.chat.id)
        topic_ids = [x.strip() for x in input3.text.strip().split("&") if x.strip()]
        await msg2.delete()
        await input3.delete()
    except Exception:
        return await m.reply_text("❌ Failed to read topic IDs.")

    prog = await m.reply_text("🔄 Extracting... Please wait.")
    video_links = ""
    try:
        for sub_id in topic_ids:
            topics = scraper.get(f"{host}/get/alltopicfrmlivecourseclass?courseid={batch_id}&subjectid={sub_id}", headers=headers).json().get("data", [])
            for topic in topics:
                tid = topic["topicid"]
                cname = topic["topic_name"]
                concepts = scraper.get(
                    f"{host}/get/allconceptfrmlivecourseclass",
                    params={
                        'courseid': batch_id,
                        'subjectid': sub_id,
                        'topicid': tid,
                        'start': '-1'
                    },
                    headers=headers
                ).json().get("data", [])
                for concept in concepts:
                    cid = concept["conceptid"]
                    videos = scraper.get(
                        f"{host}/get/livecourseclassbycoursesubtopconceptapiv3",
                        params={
                            'courseid': batch_id,
                            'subjectid': sub_id,
                            'topicid': tid,
                            'conceptid': cid,
                            'start': '-1'
                        },
                        headers=headers
                    ).json().get("data", [])
                    for v in videos:
                        title = v.get("Title", "Untitled")
                        url = decode(v.get("download_link", ""))
                        video_links += f"{title}: {url}\n"
    except Exception as e:
        await prog.delete()
        return await m.reply_text(f"❌ Extraction error: {e}")

    filename = f"AUBLIC - {course_title}.txt"
    try:
        async with aiofiles.open(filename, "w", encoding="utf-8") as f:
            await f.write(video_links)
        await prog.delete()
        await m.reply_document(filename, caption=f"`{filename}`")
    except Exception as e:
        await prog.delete()
        return await m.reply_text(f"❌ Failed to send file: {e}")
    finally:
        try:
            os.remove(filename)
        except Exception:
            pass
