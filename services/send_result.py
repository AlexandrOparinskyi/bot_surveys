from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from config import load_config
from database.models import User

logger = logging.getLogger(__name__)


async def send_tg_result(session: AsyncSession, user_id: int,
                         point: int, bot: Bot) -> None:
    user_query = select(User).where(
        User.user_id == user_id
    )
    user = await session.scalar(user_query)
    text = f"Пользователь {user.name} {user.surname} заработал {point} баллов"

    config = load_config()

    for user_id in config.tg_bot.user_id:
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            logger.error(e)
