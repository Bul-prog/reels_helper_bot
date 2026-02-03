import json

from fastapi import APIRouter, Request, HTTPException

from config import YOOKASSA_PRICE_RUB
from db import (
    activate_subscription,
    payment_exists,
    save_payment
)

router = APIRouter()


@router.post("/yookassa")
async def yookassa_webhook(request: Request):
    event = await request.json()

    if event.get("event") != "payment.succeeded":
        return {"ok": True}

    payment = event["object"]
    payment_id = payment["id"]

    # 1️⃣ идемпотентность
    if payment_exists(payment_id):
        return {"ok": True}

    metadata = payment.get("metadata", {})
    # user_id = int(metadata.get("user_id"))
    user_id_raw = metadata.get("user_id")
    if not user_id_raw:
        raise HTTPException(status_code=400, detail="Missing user_id in metadata")

    try:
        user_id = int(user_id_raw)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id in metadata")

    plan = metadata.get("plan")

    amount = float(payment["amount"]["value"])
    currency = payment["amount"]["currency"]

    # 2️⃣ валидация
    if currency != "RUB" or amount != float(YOOKASSA_PRICE_RUB):
        raise HTTPException(status_code=400, detail="Invalid amount")

    # 3️⃣ сохраняем платёж
    save_payment(
        user_id=user_id,
        payment_id=payment_id,
        amount=int(YOOKASSA_PRICE_RUB),
        currency="RUB",
        plan=plan or "pro",
        status="succeeded",
        raw_event=json.dumps(event, ensure_ascii=False)
    )
    # 4️⃣ активируем подписку
    activate_subscription(user_id, plan or "pro")

    return {"ok": True}
