import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = 27131304
    API_HASH = "e1701bd589138de2dc127ceb6922561b"
    BOT_TOKEN = "8308568349:AAF8uf5CmoGRt0OZy9K2llDkh50ugd31Z0o"
    OWNER_ID = 6958670242
    STORAGE_CHANNEL = -1003519685683
    BASE_URL = os.environ.get("BASE_URL", "https://ghost-streamer-2.onrender.com").rstrip('/')
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    FORCE_SUB_CHANNEL = 0
    BOT_USERNAME = ""
