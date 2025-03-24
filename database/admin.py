from fastapi import FastAPI
from pydantic_core.core_schema import model_field
from sqladmin import Admin, ModelView

from database.connect import engine
from database.models import (BotCommand,
                             RegisterCommand, User)

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


admin.add_view(BotCommandAdmin)
admin.add_view(RegisterCommandAdmin)
