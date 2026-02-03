# ReelsHookAI 🤖🎬

Telegram-бот для генерации:
- 🔥 хуков (3 секунды)
- 🎬 сценариев коротких видео (Reels / Shorts / TikTok)
- 📢 рекламных скриптов

## 🚀 Стек
- Python 3.11
- python-telegram-bot
- FastAPI
- SQLite
- YooKassa
- YandexGPT
- Docker
- Railway

---

## 📁 Структура проекта

.
├── app.py # FastAPI app (webhooks)
├── main.py # Telegram logic (webhook mode)
├── config.py # Env config
├── db.py # SQLite
├── handlers/ # Telegram handlers
├── services/ # AI, limits, payments
├── webhooks/ # YooKassa webhook
├── ui/ # Texts, keyboards, formatters
├── Dockerfile
├── requirements.txt
└── README.md


---

## ⚙️ Переменные окружения

```env
# Telegram
TELEGRAM_BOT_TOKEN=
BOT_USERNAME=

# App
BASE_URL=

# YandexGPT
YC_IAM_TOKEN=
YC_FOLDER_ID=
YC_OAUTH_TOKEN=

# YooKassa
YOOKASSA_SHOP_ID=
YOOKASSA_SECRET_KEY=

# Flags
MOCK_MODE=true
```

## Запуск через Docker (локально)
- docker build -t reelshookai .
- docker run -p 8080:8080 reelshookai

## Деплой (Railway)
- Подключить GitHub-репозиторий
- Railway автоматически соберёт Docker-образ
- Получить публичный домен .up.railway.app
- Добавить BASE_URL в Variables
- Redeploy

## Платежи
- Подтверждение оплаты происходит только через YooKassa webhook
- return_url используется только для UX
- Подписка активируется автоматически