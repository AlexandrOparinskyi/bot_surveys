from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import FAQ
from keyboards.faq_keyboards import create_faq_keyboard

faq_router = Router()


@faq_router.message(Command(commands="faq"))
async def get_faq(message: Message, session: AsyncSession):
    all_faq = await session.scalars(select(FAQ))
    keyboard = create_faq_keyboard(all_faq)
    await message.answer("<b>Часто задаваемые вопросы</b>\n\n"
                         "Выберите вопрос, который вас интересует",
                         reply_markup=keyboard)


@faq_router.callback_query(F.data.startswith("detail_faq_"))
async def get_detail_faq(callback: CallbackQuery,
                         session: AsyncSession,
                         bot: Bot):
    _, _, faq_id = callback.data.split("_")
    faq = await session.scalar(select(FAQ).where(FAQ.id == int(faq_id)))
    document = FSInputFile(faq.file_path)
    await bot.send_document(callback.from_user.id, document=document)
    await callback.message.answer(faq.text)
