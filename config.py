#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) ACE 

import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7091128043:AAF5q40JTQmn-0l1pOOf0cVCZhiLC3LEi4g")
    API_ID = int(os.environ.get("API_ID", "25352517"))
    API_HASH = os.environ.get("API_HASH", "2b7e6cf7752c3af91f958d67793a3e0b")
    AUTH_USERS = os.environ.get("AUTH_USERS", "7360968885")
