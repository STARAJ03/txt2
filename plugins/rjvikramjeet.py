#  MIT License
#
#  Copyright (c) 2019-present Dan <https://github.com/delivrance>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE
#  Code edited By Cryptostark
import urllib
import urllib.parse
import requests
import json
import subprocess
from pyrogram.types.messages_and_media import message
import helper
from pyromod import listen
from pyrogram.types import Message
import tgcrypto
import pyrogram
from requests_toolbelt.utils import dump
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
import time
from pyrogram.types import User, Message
from p_bar import progress_bar
from subprocess import getstatusoutput
import logging
import os
import sys
import re
from pyrogram import Client as bot
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
def decode(tn):
  key = "638udh3829162018".encode("utf8")
  iv = "fedcba9876543210".encode("utf8")
  ciphertext = bytearray.fromhex(b64decode(tn.encode()).hex())
  cipher = AES.new(key, AES.MODE_CBC, iv)
  plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
  url=plaintext.decode('utf-8')
  return url
@bot.on_message(filters.command(["rgvikramjeet"]))
async def account_login(bot: Client, m: Message):
    s = requests.Session()
    scraper = cloudscraper.create_scraper()
    global cancel
    cancel = False

    editable = await m.reply_text(
        "**Send ID*Password**\nOR\n**Token*UserID**\n\nCorrect format is required or bot will not respond.")

    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text
    await input1.delete(True)

    # Determine login method
    if len(raw_text.split("*")) != 2:
        return await editable.edit("❌ Invalid format. Use: `ID*Password` or `Token*UserID`")

    part1, part2 = raw_text.split("*")
    if "@" in part1 or part1.isdigit():
        login_mode = "idpass"
        email = part1
        password = part2
    else:
        login_mode = "token"
        token = part1
        userid = part2

    host = "https://rgvikramjeetapi.classx.co.in"

    if login_mode == "idpass":
        rwa_url = f"{host}/post/userLogin"
        hdr = {
            "Auth-Key": "appxapi",
            "User-Id": "-2",
            "Authorization": "",
            "User_app_category": "",
            "Language": "en",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "okhttp/4.9.1"
        }
        info = {"email": email, "password": password}
        res = scraper.post(rwa_url, data=info, headers=hdr).content
        output = json.loads(res)
        userid = output["data"]["userid"]
        token = output["data"]["token"]
        await editable.edit("✅ Login successful via ID & Password.")

    else:
        await editable.edit("✅ Login successful via Token.")

    # Common headers after login
    hdr1 = {
        "Host": "rgvikramjeetapi.classx.co.in",
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-Id": userid,
        "Authorization": token
    }

    # Fetch courses
    cour_url = f"{host}/get/mycourse?userid={userid}"
    res1 = s.get(cour_url, headers=hdr1)
    b_data = res1.json()['data']
    cool = ""
    for data in b_data:
        aa = f"```{data['id']}``` - **{data['course_name']}**\n\n"
        if len(f'{cool}{aa}') > 4096:
            await m.reply_text(cool)
            cool = ""
        cool += aa
    await editable.edit(f"**You have these batches:**\n\n```BATCH ID``` - **BATCH NAME**\n\n{cool}")

    editable1 = await m.reply_text("📥 Now send the **Batch ID** to continue:")
    input2 = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    await editable1.delete(True)

    html = scraper.get(f"{host}/get/course_by_id?id={raw_text2}", headers=hdr1).json()
    course_title = html["data"][0]["course_name"]

    html = scraper.get(f"{host}/get/allsubjectfrmlivecourseclass?courseid={raw_text2}", headers=hdr1).content
    output0 = json.loads(html)
    subjID = output0["data"]
    cool = ""
    vj = ""
    for sub in subjID:
        subjid = sub["subjectid"]
        subjname = sub["subject_name"]
        aa = f"```{subjid}``` - **{subjname}**\n\n"
        cool += aa
        vj += f"{subjid}&"
    await editable.edit(cool)

    editable1 = await m.reply_text(f"Now send **Topic IDs** like this: `1&2&3`\n\nTo download full batch use:\n```{vj}```")
    input3 = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    await editable1.delete(True)
    prog = await editable.edit("📥 Extracting video links... Please wait.")

    try:
        output_dict = {}
        videos_dict = {}
        mm = "Rgvikramjeet"
        xv = raw_text3.split('&')
        for raw_text3 in xv:
            res3 = requests.get(f"{host}/get/alltopicfrmlivecourseclass?courseid={raw_text2}&subjectid={raw_text3}", headers=hdr1)
            b_data2 = res3.json()['data']
            for data in b_data2:
                t_name = data["topic_name"]
                tid = data["topicid"]
                par = {
                    'courseid': raw_text2,
                    'subjectid': raw_text3,
                    'topicid': tid,
                    'start': '-1'
                }
                res6 = requests.get(f'{host}/get/allconceptfrmlivecourseclass', params=par, headers=hdr1).json()
                b_data3 = res6['data']
                for data in b_data3:
                    cid = data["conceptid"]
                    par2 = {
                        'courseid': raw_text2,
                        'subjectid': raw_text3,
                        'topicid': tid,
                        'conceptid': cid,
                        'start': '-1'
                    }
                    res4 = requests.get(f'{host}/get/livecourseclassbycoursesubtopconceptapiv3', params=par2, headers=hdr1).json()
                    try:
                        topicid = res4["data"]
                        for data in topicid:
                            tn = data["download_link"]
                            title = data["Title"]
                            url = decode(tn)
                            videos_dict[title] = url
                            with open(f"{mm} - {course_title}.txt", "a", encoding="utf-8") as f:
                                f.write(f"{title}: {url}\n")
                        output_dict[t_name] = videos_dict
                    except Exception as e:
                        await m.reply_text(f"{tid}: {e}")
                        continue
        await prog.delete(True)
        await m.reply_document(f"{mm} - {course_title}.txt", caption=f"```{mm} - {course_title}```")
        os.remove(f"{mm} - {course_title}.txt")
    except Exception as e:
        await m.reply_text(str(e))

    
