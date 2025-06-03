import os
import requests
import cloudscraper
from pyrogram.types import Message
from pyrogram import Client
from plugins.decoder import decode

async def account_login(bot: Client, m: Message, host: str):
    s = requests.Session()
    scraper = cloudscraper.create_scraper()
    editable = await m.reply_text("**Send ID*Password**\nOR\n**Token*UserID**")

    input1: Message = await bot.listen(m.chat.id)
    raw_text = input1.text.strip()
    await input1.delete()

    if len(raw_text.split("*")) != 2:
        return await editable.edit("❌ Invalid format. Use: `ID*Password` or `Token*UserID`")

    part1, part2 = raw_text.split("*")
    if "@" in part1 or part1.isdigit():
        login_mode = "idpass"
        email, password = part1, part2
    else:
        login_mode = "token"
        token, userid = part1, part2

    if login_mode == "idpass":
        res = scraper.post(f"{host}/post/userLogin", data={"email": email, "password": password}, headers={
            "Auth-Key": "appxapi",
            "User-Id": "-2",
            "Authorization": "",
            "User_app_category": "",
            "Language": "en",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "okhttp/4.9.1"
        }).json()
        token = res["data"]["token"]
        userid = res["data"]["userid"]
        await editable.edit("✅ Login successful via ID & Password.")
    else:
        await editable.edit("✅ Login successful via Token.")

    headers = {
        "Host": host.replace("https://", "").replace("http://", ""),
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-Id": str(userid),
        "Authorization": str(token)
    }

    # Show courses
    course_list = requests.get(f"{host}/get/mycourse?userid={userid}", headers=headers).json()
    courses = course_list["data"]
    course_text = ""
    for course in courses:
        course_text += f"```{course['id']}``` - **{course['course_name']}**\n\n"
    await editable.edit(f"**Available Batches:**\n\n{course_text}")
    
    # Select course ID
    msg1 = await m.reply_text("📥 Now send the **Batch ID**:")
    input2 = await bot.listen(m.chat.id)
    batch_id = input2.text.strip()
    await msg1.delete()
    await input2.delete()

    course_info = requests.get(f"{host}/get/course_by_id?id={batch_id}", headers=headers).json()
    course_title = course_info["data"][0]["course_name"]

    # Subject fetch
    subs = requests.get(f"{host}/get/allsubjectfrmlivecourseclass?courseid={batch_id}", headers=headers).json()["data"]
    subj_text, subj_ids = "", ""
    for sub in subs:
        subj_text += f"```{sub['subjectid']}``` - **{sub['subject_name']}**\n\n"
        subj_ids += f"{sub['subjectid']}&"
    await m.reply_text(subj_text)

    msg2 = await m.reply_text(f"Send **Topic IDs** like: `1&2&3`\n\nTo download all: ```{subj_ids}```")
    input3 = await bot.listen(m.chat.id)
    topic_ids = input3.text.strip().split("&")
    await msg2.delete()
    await input3.delete()

    prog = await m.reply_text("🔄 Extracting... Please wait.")

    video_links = ""
    for sub_id in topic_ids:
        topics = scraper.get(f"{host}/get/alltopicfrmlivecourseclass?courseid={batch_id}&subjectid={sub_id}", headers=headers).json()["data"]
        for topic in topics:
            tid = topic["topicid"]
            cname = topic["topic_name"]
            concepts = scraper.get(f"{host}/get/allconceptfrmlivecourseclass", params={
                'courseid': batch_id,
                'subjectid': sub_id,
                'topicid': tid,
                'start': '-1'
            }, headers=headers).json()["data"]
            for concept in concepts:
                cid = concept["conceptid"]
                videos = scraper.get(f"{host}/get/livecourseclassbycoursesubtopconceptapiv3", params={
                    'courseid': batch_id,
                    'subjectid': sub_id,
                    'topicid': tid,
                    'conceptid': cid,
                    'start': '-1'
                }, headers=headers).json().get("data", [])
                for v in videos:
                    title = v["Title"]
                    url = decode(v["download_link"])
                    video_links += f"{title}: {url}\n"

    filename = f"AUBLIC - {course_title}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(video_links)

    await prog.delete()
    await m.reply_document(filename, caption=f"`{filename}`")
    os.remove(filename)
