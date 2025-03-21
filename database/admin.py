from fastapi import FastAPI
from sqladmin import Admin, ModelView

from database.connect import engine
from database.models import BotCommand

app = FastAPI()
admin = Admin(app, engine)


class BotCommandAdmin(ModelView, model=BotCommand):
    name = "Команда бота"
    name_plural = "Команды бота"
    page_size = 25
    column_list = (BotCommand.id, BotCommand.command, BotCommand.text)


admin.add_view(BotCommandAdmin)
