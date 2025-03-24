from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_confirm_register_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="Данные верны",
            callback_data="confirm_register_data"
        ),
        InlineKeyboardButton(
            text="Есть ошибки. Начну регистрацию заново",
            callback_data="error_register_data"
        ),
        width=1
    )
    return kb_builder.as_markup()
