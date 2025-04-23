from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_faq_keyboard(faq) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[InlineKeyboardButton(
            text=f.text,
            callback_data=f"detail_faq_{f.id}"
        ) for f in faq],
        width=1
    )
    return kb_builder.as_markup()
