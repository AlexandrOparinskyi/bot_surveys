from typing import List

import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy.ext.asyncio import AsyncSession

from config import load_config
from database.models import Survey
from services.survey_services import get_user_by_user_id

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(
    'findostavka.json',
    scopes=SCOPES
)

config = load_config()

gc = gspread.service_account(filename='findostavka.json',
                             scopes=SCOPES)
sh = gc.open_by_key(config.google_sheet.g_id)


async def create_user_result(user_id: int,
                             survey: Survey,
                             answers: List[int],
                             session: AsyncSession,
                             points: int) -> None:
    user = await get_user_by_user_id(session, user_id)
    survey_questions = [q.text for q in survey.questions]
    text_answers = []
    for i in range(len(survey.questions)):
        text_answers.append(survey.questions[i].options[answers[i]].text)

    try:
        worksheet = sh.worksheet(survey.title)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(survey.title, rows=300, cols=len(survey.questions) + 5)
        worksheet.append_row(["Имя пользователя"] + survey_questions + ["Общее кол-во баллов"])

    user_id_list = worksheet.col_values(1)
    try:
        row_index = user_id_list.index(f"{user.id}. {user.name} {user.surname}") + 1
        worksheet.delete_rows(row_index, row_index)
        worksheet.append_row([f"{user.id}. {user.name} {user.surname}"] + text_answers + [points])

    except ValueError:
        worksheet.append_row([f"{user.id}. {user.name} {user.surname}"] + text_answers + [points])
