from fastapi import FastAPI
from sqladmin import Admin, ModelView

from database.connect import engine
from database.models import (BotCommand, RegisterCommand, User, Survey,
                             Question, Option, SurveyResult, UserPoint)

app = FastAPI()
admin = Admin(app, engine)


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


admin.add_view(BotCommandAdmin)
admin.add_view(RegisterCommandAdmin)
admin.add_view(UserAdmin)
admin.add_view(SurveyAdmin)
admin.add_view(QuestionAdmin)
admin.add_view(OptionAdmin)
admin.add_view(SurveyResultAdmin)
admin.add_view(UserPointAdmin)
