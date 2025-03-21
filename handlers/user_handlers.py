from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BotCommand

user_router = Router()


@user_router.message(F.text.startswith("/"))
async def process_another_command(message: Message, session: AsyncSession):
    command_query = select(BotCommand).where(
        BotCommand.command == message.text.replace("/", "")
    )
    command = await session.scalar(command_query)

    if not command:
        await message.answer("Я не знаю такой команды 😕")
        return

    await message.answer(command.text)
