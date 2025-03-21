from fastapi import FastAPI
from sqladmin import Admin, ModelView

from database.connect import engine
from database.models import (BotCommand,
                             RegisterCommand)

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


admin.add_view(BotCommandAdmin)
admin.add_view(RegisterCommandAdmin)
