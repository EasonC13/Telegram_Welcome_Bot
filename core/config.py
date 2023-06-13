import os

try:
    from dotenv import load_dotenv

    load_dotenv(".env")
except ModuleNotFoundError:
    # No dotenv
    print("[warning ModuleNotFoundError] .env not found. ")
    pass

# Host Information
DOMAIN_NAME = os.getenv("DOMAIN_NAME", "example.com")


MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
# SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "GroupChatAdminHelperBot")
PROJECT_VERSION = os.getenv("PROJECT_VERSION", "0.1")
ALLOWED_HOSTS = ["*"]

API_PORT = os.getenv("API_PORT", 8899)
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_WORKER = os.getenv("API_WORKER", 2)

DEBUG = False

# MongoDB
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_USERNAME = os.getenv("MONGO_USER", "user")
MONGODB_USERNAME = os.getenv("MONGO_USER", "")
MONGODB_PASSWORD = os.getenv("MONGO_PASSWORD", "")

MAX_BACKUP_COUNT = 50

MONGODB_URL = os.getenv(
    "MONGODB_URI",
    f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}",
)

DATABASE_NAME = "GroupChatAdminHelperBot"
# API Version
API_V1_PREFIX = "/api/v1"

AUTH_V1_PREFIX = "/api/auth"
MAINTAINER_TOKEN_HASH = os.getenv("MAINTAINER_TOKEN_HASH", "")

# SMTP
SMTP_SSL_HOST = os.getenv("SMTP_SSL_HOST", "localhost")
SMTP_ACCOUNT = os.getenv("SMTP_ACCOUNT", "localhost")
SMTP_PW = os.getenv("SMTP_PW", "localhost")
SMTP_FROM = os.getenv("SMTP_FROM", "localhost")

# Security
EMAIL_EXPIRE_MINUTE = 24 * 60  # Email url expire after 1 day as default

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "")
