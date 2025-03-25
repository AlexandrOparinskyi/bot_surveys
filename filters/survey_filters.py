from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from sqlalchemy import select

from database.connect import get_async_session
from database.models import Survey


class SurveySlugFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, *args, **kwargs):
        async with get_async_session() as session:
            survey_query = select(Survey).where(
                Survey.is_active == True
            )
            surveys = await session.scalars(survey_query)

            return callback.data in [s.slug for s in surveys]
