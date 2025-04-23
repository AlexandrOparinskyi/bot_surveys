from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_sender_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="Отправить всем",
            callback_data="send_message_all_user"
        ),
        InlineKeyboardButton(
            text="Написать другое",
            callback_data="back_to_start_send_message"
        )
    )
    return kb_builder.as_markup()