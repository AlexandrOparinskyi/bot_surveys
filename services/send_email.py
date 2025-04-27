import asyncio
from email.mime.text import MIMEText

import aiosmtplib
from sqlalchemy.ext.asyncio import AsyncSession

from config import load_config
from database.models import Survey, User
from services.survey_services import get_user_by_user_id

config = load_config()


def generate_text_for_email(user: User, survey: Survey,
                            answers: list[int], points: int) -> str:
    html = f"""
        <html>
        <head></head>
        <body>
            <h2>Отчет пользователя {user.name} {user.surname} по 
            опросу "{survey.title}"</h2>
            <p><b>Общее количество баллов:</b> {points}</p>
            <hr>
            <h3>Ответы на вопросы:</h3>
            <ol>
        """

    for i in range(len(survey.questions)):
        html += f"""
            <li>
                <b>{survey.questions[i]}</b>
        """
        if answers[i] == 0:
            html += f"""
                <p>-> {survey.questions[i].options[0].text}</p>
                <p>{survey.questions[i].options[1].text}</p>
                <p>{survey.questions[i].options[2].text}</p>
                </li>
            """
        elif answers[i] == 1:
            html += f"""
                <p>{survey.questions[i].options[0].text}</p>
                <p>-> {survey.questions[i].options[1].text}</p>
                <p>{survey.questions[i].options[2].text}</p>
                </li>
            """
        elif answers[i] == 2:
            html += f"""
                <p>{survey.questions[i].options[0].text}</p>
                <p>{survey.questions[i].options[1].text}</p>
                <p>-> {survey.questions[i].options[2].text}</p>
                </li>
            """

    html += """
            </ol>
        </body>
        </html>
        """

    return html


async def send_email(user_id: int, survey: Survey, answers: list[int],
                     session: AsyncSession, points: int) -> None:
    user = await get_user_by_user_id(session, user_id)
    text = generate_text_for_email(user, survey, answers, points)

    message = MIMEText(text, "html", _charset='utf-8')
    message['Subject'] = 'Hello World!'
    message['From'] = config.smtp.username
    message['To'] = 'surveys@example.com'

    async with aiosmtplib.SMTP(hostname=config.smtp.host,
                               port=config.smtp.port) as smtp:
        await smtp.login(config.smtp.username, config.smtp.password)
        await smtp.send_message(message)
