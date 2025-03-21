from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.connect import get_async_session


class ConnectDatabaseMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler:
            Callable[[TelegramObject, Dict[str, Any]],
                     Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with get_async_session() as session:
            data.setdefault("session", session)

            return await handler(event, data)
