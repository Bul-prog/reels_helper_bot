from fastapi import APIRouter, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_BOT_TOKEN
from handlers.start import start
from handlers.generate import choose_type, generate, generate_more
from handlers.subscribe import subscribe

router = APIRouter()

# Telegram application (python-telegram-bot)
telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(choose_type, pattern="^(hook|script|ads)$"))
telegram_app.add_handler(CallbackQueryHandler(subscribe, pattern="^subscribe$"))
telegram_app.add_handler(CallbackQueryHandler(generate_more, pattern="^more$"))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
