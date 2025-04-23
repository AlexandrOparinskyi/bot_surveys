import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config, Config
from handlers.register_handlers import register_router
from handlers.sender_handlers import sender_router
from handlers.survey_handlers import survey_router
from handlers.user_handlers import user_router
from keyboards.main_menu import set_main_menu
from middlewares.connect_database_middleware import ConnectDatabaseMiddleware


async def main():
    logging.basicConfig(level=logging.DEBUG)

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token,
                   default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher()

    dp.update.middleware(ConnectDatabaseMiddleware())

    dp.include_router(user_router)
    dp.include_router(register_router)
    dp.include_router(survey_router)
    dp.include_router(sender_router)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
