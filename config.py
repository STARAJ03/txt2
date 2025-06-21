import os

class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    API_ID = int(os.environ.get("27765349"))
    API_HASH = os.environ.get("9df1f705c8047ac0d723b29069a1332b")
    AUTH_USERS = os.environ.get("AUTH_USERS", "1116405290")
