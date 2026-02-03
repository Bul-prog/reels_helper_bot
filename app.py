from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from telegram_webhook import router as telegram_router
from webhooks.webhook_yookassa import router as yookassa_router

app = FastAPI()

app.include_router(yookassa_router, prefix="/webhooks")
app.include_router(telegram_router)


@app.get("/payment/success", response_class=HTMLResponse)
async def payment_success():
    return """
    <html>
      <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
        <h2>✅ Оплата принята</h2>
        <p>Подписка будет активирована в течение нескольких секунд.</p>
        <p>Вернитесь в Telegram и продолжайте пользоваться ботом 🚀</p>
      </body>
    </html>
    """
