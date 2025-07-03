from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command="/help",
            description="Помощь"
        ),
        BotCommand(
            command="/register",
            description="Регистрация"
        ),
        BotCommand(
            command="/surveys",
            description="Выбрать опрос"
        ),
        BotCommand(
            command="/faq_raif",
            description="FAQ Райф"
        ),
        BotCommand(
            command="/faq_vtb",
            description="FAQ ВТБ"
        ),
        BotCommand(
            command="/move",
            description="Уроки в движении"
        )
    ]

    await bot.set_my_commands(main_menu_commands)
