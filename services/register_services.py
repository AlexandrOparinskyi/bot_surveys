from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import RegisterCommand, User


async def get_register_command(session: AsyncSession, text: str):
    command_query = select(RegisterCommand).where(
        RegisterCommand.command == text
    )
    return await session.scalar(command_query)


async def exists_user(session: AsyncSession, user_id: int) -> bool:
    exists_user_query = select(User).where(
        User.user_id == user_id
    )
    user = await session.scalar(exists_user_query)
    return user is not None
