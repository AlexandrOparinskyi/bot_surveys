import os.path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from sqladmin import Admin, ModelView
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from wtforms.fields.simple import StringField, TextAreaField, FileField
from wtforms.form import Form
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea

from database.connect import engine
from database.models import (BotCommand, RegisterCommand, User, Survey,
                             Question, Option, SurveyResult, UserPoint, FAQ)

app = FastAPI()
admin = Admin(app, engine)
UPLOAD_FOLDER = "uploads"
app.mount("/files", StaticFiles(directory=UPLOAD_FOLDER), name="files")


class BotCommandAdmin(ModelView, model=BotCommand):
    name = "Команда бота"
    name_plural = "Команды бота"
    page_size = 25
    column_list = (BotCommand.id, BotCommand.command, BotCommand.text)


class RegisterCommandAdmin(ModelView, model=RegisterCommand):
    name = "Команда для регистрации"
    name_plural = "Команды для регистрации"
    page_size = 25
    column_list = (RegisterCommand.id,
                   RegisterCommand.command,
                   RegisterCommand.description)


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    page_size = 25
    column_list = (User.id, User.name, User.surname)


class SurveyAdmin(ModelView, model=Survey):
    name = "Опрос"
    name_plural = "Опросы"
    page_size = 25
    column_list = (Survey.id, Survey.title, Survey.is_active)
    form_columns = (Survey.title, Survey.description, Survey.is_active)


class QuestionAdmin(ModelView, model=Question):
    name = "Вопрос"
    name_plural = "Вопросы"
    page_size = 25
    column_list = (Question.id, Question.survey_id, Question.text)
    form_columns = (Question.survey, Question.text)
    column_default_sort = (Question.id, True)


class OptionAdmin(ModelView, model=Option):
    name = "Ответ"
    name_plural = "Ответы"
    page_size = 25
    column_list = (Option.id, Question.survey_id, Option.question_id,
                   Option.text, Option.is_correct)
    form_columns = (Option.survey, Option.question,
                    Option.text, Option.is_correct)


class SurveyResultAdmin(ModelView, model=SurveyResult):
    name = "Результат опроса"
    name_plural = "Результаты опросов"
    page_size = 25
    column_list = (SurveyResult.id, SurveyResult.text_result)


class UserPointAdmin(ModelView, model=UserPoint):
    name = "Количество баллов пользователя"
    name_plural = "Количество баллов пользователей"
    page_size = 25
    column_list = (UserPoint.id, UserPoint.user,
                   UserPoint.survey, UserPoint.points)


class FAQForm(Form):
    question = StringField("Вопрос", validators=[DataRequired()])
    text = TextAreaField("Ответ", widget=TextArea())
    file = FileField("Файл")


class FAQAdmin(ModelView, model=FAQ):
    name = "FAQ",
    name_plural = "FAQ"
    page_size = 25
    column_list = (FAQ.id, FAQ.question, FAQ.text, FAQ.file_path)
    form = FAQForm
    column_formatters = {
        "file_path": lambda m, a: (
            f"Скачать"
            if m.file_path
            else "Файл отсутствует"
        )
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        form = await request.form()
        file = form["file"]

        if file and file.filename:
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = str(uuid4())[:16] + file_extension
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            model.file_path = file_path


admin.add_view(BotCommandAdmin)
admin.add_view(RegisterCommandAdmin)
admin.add_view(UserAdmin)
admin.add_view(SurveyAdmin)
admin.add_view(QuestionAdmin)
admin.add_view(OptionAdmin)
admin.add_view(SurveyResultAdmin)
admin.add_view(UserPointAdmin)
admin.add_view(FAQAdmin)
