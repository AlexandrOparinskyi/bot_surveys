from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import select

from database.connect import get_async_session
from database.models import BotCommand

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer("Hello bro")


@user_router.message()
async def process_another_command(message: Message):
    async with get_async_session() as session:
        command_query = select(BotCommand).where(
            BotCommand.command == message.text.replace("/", "")
        )
        command = await session.scalar(command_query)
        if not command:
            await message.answer("Command not found!")
            return

        await message.answer(command.text)
