from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

load_dotenv()
from config import TELEGRAM_BOT_TOKEN

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN не задан. "
        "Проверь .env или переменные окружения."
    )

from handlers.start import start
from handlers.generate import choose_type, generate, generate_more
from handlers.subscribe import subscribe


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(choose_type, pattern="^(hook|script|ads)$"))
    app.add_handler(CallbackQueryHandler(subscribe, pattern="^subscribe$"))
    app.add_handler(CallbackQueryHandler(generate_more, pattern="^more$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))

    print("🚀 HookBot запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
