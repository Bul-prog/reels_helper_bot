import os

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
BOT_USERNAME = os.getenv("BOT_USERNAME")

# Режимы
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

# Backend

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL and not MOCK_MODE:
    raise RuntimeError("BASE_URL is not set")
# для продакшена
# if not BASE_URL:
#     raise RuntimeError("BASE_URL is not set")

# Yandex Cloud
YC_IAM_TOKEN = os.getenv("YC_IAM_TOKEN")
YC_FOLDER_ID = os.getenv("YC_FOLDER_ID")

# Лимиты
FREE_DAILY_LIMIT = 1
PRO_DAILY_LIMIT = 20

# Подписка
SUBSCRIPTION_PRICE_RUB = 250

YOOKASSA_PRICE_RUB = 250

YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
