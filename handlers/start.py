from db import create_user
from ui.keyboards import main_menu
from ui.messages import START_TEXT


async def start(update, context):
    user_id = update.message.from_user.id
    create_user(user_id)

    await update.message.reply_text(
        START_TEXT,
        reply_markup=main_menu()
    )
