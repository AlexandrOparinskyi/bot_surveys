from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Survey


def create_all_surveys_keyboard(surveys) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[InlineKeyboardButton(
            text=s.title,
            callback_data=s.slug
        ) for s in surveys],
        width=1
    )
    return kb_builder.as_markup()


def create_start_survey_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="Начать этот опрос",
            callback_data="start_this_survey"
        ),
        InlineKeyboardButton(
            text="Обратно к списку опросов",
            callback_data="back_to_surveys_list"
        ),
        width=1
    )
    return kb_builder.as_markup()


def create_options_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[InlineKeyboardButton(
            text=j,
            callback_data=f"next_question_{i}"
        ) for i, j in enumerate("ABC")]
    )
    return kb_builder.as_markup()
