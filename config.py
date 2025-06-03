import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_HASH = os.environ.get("API_HASH", "")

    # Safe conversion of API_ID
    API_ID = int(os.environ.get("API_ID", ""))  # default 0 agar set na ho

    # AUTH_USERS ko list me convert karo agar string ho comma separated
    AUTH_USERS = [int(x) for x in os.environ.get("AUTH_USERS", "").split(",") if x]
