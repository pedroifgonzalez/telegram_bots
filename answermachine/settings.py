from decouple import config

try:
    API_ID = config("API_ID", default=0, cast=int)
    API_HASH = config("API_HASH")
    APP_TITLE = config("APP_TITLE", cast=str, default="answermachine")
    USERNAMES = config("USERNAMES")
    PHONE_NUMBERS = config("PHONE_NUMBERS")
except Exception:
    raise Exception("Missing env variables")
