import logging

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import load_config
from database.models import User, Survey

logger = logging.getLogger(__name__)


async def send_tg_result(session: AsyncSession, user_id: int,
                         point: int, bot: Bot, survey: Survey,
                         answers: list[int]) -> None:
    config = load_config()

    user_query = select(User).where(
        User.user_id == user_id
    )
    user = await session.scalar(user_query)
    text1 = (f"Пользователь {user.name} {user.surname} "
             f"заработал {point} баллов")

    text2 = f"Ответы пользователя {user.name} {user.surname}:\n\n"
    for i in range(len(survey.questions)):
        text2 += f"<b>Вопрос {i + 1}:</b>  {survey.questions[i].text}\n"
        if answers[i] == 0:
            text2 += (f"<b>   {survey.questions[i].options[answers[i]].text}"
                      f"</b>\n"
                      f"   {survey.questions[i].options[answers[1]].text}\n"
                      f"   {survey.questions[i].options[answers[2]].text}\n\n")
        elif answers[i] == 1:
            text2 += (f"   {survey.questions[i].options[answers[i]].text}\n"
                      f"   <b>{survey.questions[i].options[answers[1]].text}"
                      f"</b>\n"
                      f"   {survey.questions[i].options[answers[2]].text}\n\n")
        elif answers[i] == 2:
            text2 += (f"   {survey.questions[i].options[answers[i]].text}\n"
                      f"   {survey.questions[i].options[answers[1]].text}\n"
                      f"   <b>{survey.questions[i].options[answers[2]].text}"
                      f"</b>\n\n")

    for user_id in config.tg_bot.user_id:
        try:
            await bot.send_message(chat_id=user_id, text=text1)
            await bot.send_message(chat_id=user_id, text=text2)
        except Exception as e:
            logger.error(e)
