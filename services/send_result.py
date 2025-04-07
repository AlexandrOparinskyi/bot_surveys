from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def send_tg_result(session: AsyncSession, user_id: int,
                         point: int, bot: Bot) -> None:
    user_query = select(User).where(
        User.user_id == user_id
    )
    user = await session.scalar(user_query)
    text = f"Пользователь {user.name} {user.surname} заработал {point} баллов"

    await bot.send_message(chat_id=882095669, text=text)
