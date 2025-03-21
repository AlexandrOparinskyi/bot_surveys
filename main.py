import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import load_config, Config
from handlers.register_handlers import register_router
from handlers.user_handlers import user_router
from middlewares.connect_database_middleware import ConnectDatabaseMiddleware


async def main():
    logging.basicConfig(level=logging.DEBUG)

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    dp.update.middleware(ConnectDatabaseMiddleware())

    dp.include_router(user_router)
    dp.include_router(register_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
