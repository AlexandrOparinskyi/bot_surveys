from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import RegisterCommand


async def get_register_command(session: AsyncSession, message: Message):
    command_query = select(RegisterCommand).where(
        RegisterCommand.command == message.text.replace("/", "")
    )
    return await session.scalar(command_query)
