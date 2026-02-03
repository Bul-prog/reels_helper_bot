import uuid

import requests

from config import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY, YOOKASSA_PRICE_RUB, MOCK_MODE, BASE_URL

YOOKASSA_API_URL = "https://api.yookassa.ru/v3/payments"


def create_subscription_payment(user_id: int, plan: str = "pro"):
    if MOCK_MODE:
        # фейковая тестовая ссылка
        return "https://example.com/mock-payment-success"
    idempotency_key = str(uuid.uuid4())

    payload = {
        "amount": {
            "value": f"{YOOKASSA_PRICE_RUB:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{BASE_URL}/payment/success"
        },
        "capture": True,
        "description": "Подписка PRO на ReelsHookAI",
        "metadata": {
            "user_id": str(user_id),
            "plan": plan
        }
    }

    response = requests.post(
        YOOKASSA_API_URL,
        json=payload,
        auth=(YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY),
        headers={
            "Idempotence-Key": idempotency_key
        },
        timeout=10
    )

    response.raise_for_status()
    data = response.json()

    return data["confirmation"]["confirmation_url"]
