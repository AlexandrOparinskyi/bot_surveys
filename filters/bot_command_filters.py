from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy import select

from database.connect import get_async_session
from database.models import BotCommand


class BotCommandFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with get_async_session() as session:
            commands = await session.scalars(select(BotCommand))
            res = [c.command for c in commands.all()]
            return message.text.replace("/", "") in res
