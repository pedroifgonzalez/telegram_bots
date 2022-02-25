from decouple import config


try:
    API_ID = config("API_ID", default=0, cast=int)
    API_HASH = config("API_HASH")
    APP_TITLE = config("APP_TITLE", cast=str)
    BOT_TOKEN = config("BOT_TOKEN", cast=str)
    USERNAMES = config("USERNAMES")
    PHONE_NUMBERS = config("PHONE_NUMBERS")
except:
    raise Exception("Missing env variables")
