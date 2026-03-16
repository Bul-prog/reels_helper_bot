# Описание проекта ReelsHookAI 🤖🎬

Telegram-бот для генерации идей и сценариев коротких видео (Reels / Shorts / TikTok) с помощью YandexGPT.

Бот помогает быстро создавать:
- 🔥 вирусные хуки
- 🎬 сценарии коротких видео
- 📢 рекламные скрипты

Проект реализует полный цикл работы AI-бота: генерация контента, лимиты использования, 
подписка и онлайн-деплой.

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
```text
ReelsHookAI
│
├── handlers/           # Telegram handlers
│   ├── start.py
│   ├── generate.py
│   └── subscribe.py
│
├── services/           # Бизнес-логика
│   ├── ai.py
│   ├── limits.py
│   └── payments.py
│
├── webhooks/
│   └── webhook_yookassa.py
│
├── ui/                 # тексты и клавиатуры
│
├── app.py              # FastAPI сервер
├── main.py             # запуск Telegram логики
├── config.py           # переменные окружения
├── db.py               # SQLite база
├── requirements.txt
└── Dockerfile
```

---
## Установка и запуск
### 1. Клонировать репозиторий
```bash
git clone https://github.com/Bul-prog/reels_helper_bot.git
cd reels_helper_bot
```

### 2. Установить зависимости
```bash
pip install -r requirements.txt
```

## ⚙️ Установить переменные окружения

| Переменная          | Назначение               |
| ------------------- | ------------------------ |
| TELEGRAM_BOT_TOKEN  | токен Telegram бота      |
| BOT_USERNAME        | username бота            |
| YC_OAUTH_TOKEN      | OAuth токен Yandex Cloud |
| YC_FOLDER_ID        | folder id Yandex Cloud   |
| YOOKASSA_SHOP_ID    | ID магазина YooKassa     |
| YOOKASSA_SECRET_KEY | секретный ключ YooKassa  |
| BASE_URL            | публичный URL сервиса    |
| MOCK_MODE           | режим тестовой генерации |


## Запуск через Docker (локально)
```bash
docker build -t reelshookai .
docker run -p 8080:8080 reelshookai
```

## Деплой (Railway)
Проект развёрнут через Railway.

Основные этапы:
- Push проекта в GitHub
- Подключение репозитория в Railway
- Добавление переменных окружения
- Настройка Telegram webhook
- Подключение YooKassa webhook


