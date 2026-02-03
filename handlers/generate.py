from db import get_or_create_user
from services.ai import generate_text
from services.limits import check_and_use_limit
from ui.formatter import format_answer
from ui.keyboards import subscribe_keyboard, main_menu, more_variant_keyboard
from ui.messages import CHOOSE_PROMPT, LIMIT_REACHED_TEXT, PROMPTS, START_TEXT


async def choose_type(update, context):
    query = update.callback_query

    # корректный немедленный ACK
    await query.answer()

    content_type = query.data
    context.user_data["type"] = content_type

    await query.message.reply_text(
        CHOOSE_PROMPT[content_type]
    )


async def generate(update, context):
    user_id = update.message.from_user.id

    user = get_or_create_user(user_id)
    can_use, used, limit = check_and_use_limit(user)

    if not can_use:
        await update.message.reply_text(
            LIMIT_REACHED_TEXT,
            reply_markup=subscribe_keyboard()
        )
        return

    content_type = context.user_data.get("type")

    if not content_type:
        await update.message.reply_text(
            "Сначала выбери, что ты хочешь сделать 👇"
        )
        await update.message.reply_text(
            START_TEXT,
            reply_markup=main_menu()
        )
        return

    topic = update.message.text
    prompt = PROMPTS[content_type].format(topic=topic)

    # 🔐 сохраняем prompt для "Ещё вариант"
    context.user_data["last_prompt"] = prompt

    raw_text = generate_text(prompt)
    formatted_text = format_answer(content_type, raw_text)

    await update.message.reply_text(
        formatted_text,
        reply_markup=more_variant_keyboard(),
        parse_mode="Markdown"
    )

    # (по желанию) сбрасываем состояние
    # context.user_data.pop("type", None)


async def generate_more(update, context):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    user = get_or_create_user(user_id)

    can_use, used, limit = check_and_use_limit(user)

    if not can_use:
        await query.message.reply_text(
            LIMIT_REACHED_TEXT,
            reply_markup=subscribe_keyboard()
        )
        return

    prompt = context.user_data.get("last_prompt")

    if not prompt:
        await query.message.reply_text(
            "Не удалось повторить генерацию 😔\nПопробуй начать заново через меню."
        )
        return

    raw_text = generate_text(prompt)

    content_type = context.user_data.get("type") or "hook"
    formatted_text = format_answer(content_type, raw_text)

    await query.message.reply_text(
        formatted_text,
        reply_markup=more_variant_keyboard(),
        parse_mode="Markdown"
    )
