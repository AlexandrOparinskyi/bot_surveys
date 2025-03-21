from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BotCommand
from filters.bot_command_filters import BotCommandFilter

user_router = Router()


@user_router.message(BotCommandFilter())
async def process_another_command(message: Message, session: AsyncSession):
    command_query = select(BotCommand).where(
        BotCommand.command == message.text.replace("/", "")
    )
    command = await session.scalar(command_query)

    await message.answer(command.text)
