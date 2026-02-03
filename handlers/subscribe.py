from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from services.payments import create_subscription_payment


async def subscribe(update, context):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        payment_url = create_subscription_payment(user_id)

        await query.message.reply_text(
            "💳 *Подписка PRO*\n\n"
            "• 20 генераций в день\n"
            "• «Ещё вариант» без ограничений\n\n"
            "Цена: *250 ₽ / месяц*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Перейти к оплате", url=payment_url)]
            ]),
            parse_mode="Markdown"
        )

    except Exception as e:
        print("PAYMENT ERROR:", e)
        await query.message.reply_text(
            "❌ Не удалось создать платёж.\n"
            "Попробуй позже или напиши в поддержку."
        )
