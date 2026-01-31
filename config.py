from os import getenv

from dotenv import load_dotenv

load_dotenv()

SUBSONIC_SERVER = getenv("SUBSONIC_SERVER")
SUBSONIC_USERNAME = getenv("SUBSONIC_USERNAME")
SUBSONIC_PASSWORD = getenv("SUBSONIC_PASSWORD")
DISCORD_CLIENT_ID = getenv("DISCORD_CLIENT_ID")
EXCLUDED_GENRES = getenv("EXCLUDED_GENRES", "").split(",")
COVER_IMAGES = getenv("COVER_IMAGES", "").split(",")
