from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy import select, and_

from database.connect import get_async_session
from database.models import BotCommand


class SurveySlugAndActiveFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with get_async_session() as session:
            commands = await session.scalars(select(BotCommand))
            return message.text in commands.all()

