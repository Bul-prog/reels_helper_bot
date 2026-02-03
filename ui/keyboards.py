from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Хук (3 секунды)", callback_data="hook")],
        [InlineKeyboardButton("🎬 Сценарий видео", callback_data="script")],
        [InlineKeyboardButton("📢 Рекламный скрипт", callback_data="ads")],
        [InlineKeyboardButton("⭐ Подписка", callback_data="subscribe")]
    ])


def subscribe_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Подписка", callback_data="subscribe")]
    ])


def more_variant_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Ещё вариант", callback_data="more")]
    ])
