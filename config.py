import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", "0"))          # Default 0 agar set nahi ho to
    API_HASH = os.environ.get("API_HASH", "")
    AUTH_USERS = os.environ.get("AUTH_USERS", "7360968885")        # Comma separated user IDs, e.g. "123456,7891011"
