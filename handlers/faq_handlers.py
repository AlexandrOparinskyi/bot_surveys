import os

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import FAQ, Move
from keyboards.faq_keyboards import create_faq_keyboard, create_move_keyboard

faq_router = Router()

DATA_FOLDER = "/app/data"


@faq_router.message(Command(commands="faq"))
async def get_faq(message: Message, session: AsyncSession):
    faq = await session.scalars(select(FAQ))
    keyboard = create_faq_keyboard(faq)
    await message.answer("<b>Часто задаваемые вопросы</b>\n\n"
                         "Выберите вопрос, который вас интересует",
                         reply_markup=keyboard)


@faq_router.callback_query(F.data.startswith("detail_faq_"))
async def get_detail_faq(callback: CallbackQuery,
                         session: AsyncSession,
                         bot: Bot):
    _, _, faq_id = callback.data.split("_")
    faq = await session.scalar(select(FAQ).where(FAQ.id == int(faq_id)))
    if faq.file_path_1:
        file_path = os.path.join(DATA_FOLDER, faq.file_path_1)
        _, file_exp = file_path.split(".")
        document = FSInputFile(file_path)

        if file_exp in ["jpeg", "jpg", "png", "webp", "gif"]:
            await bot.send_photo(callback.from_user.id, document)
        elif file_exp in ["mp4", "avi", "mov", "webm"]:
            await bot.send_video(callback.from_user.id, document)
        else:
            await bot.send_document(callback.from_user.id, document)
    if faq.file_path_2:
        file_path = os.path.join(DATA_FOLDER, faq.file_path_2)
        _, file_exp = file_path.split(".")
        document = FSInputFile(file_path)

        if file_exp in ["jpeg", "jpg", "png", "webp", "gif"]:
            await bot.send_photo(callback.from_user.id, document)
        elif file_exp in ["mp4", "avi", "mov", "webm"]:
            await bot.send_video(callback.from_user.id, document)
        else:
            await bot.send_document(callback.from_user.id, document)
    if faq.file_path_3:
        file_path = os.path.join(DATA_FOLDER, faq.file_path_3)
        _, file_exp = file_path.split(".")
        document = FSInputFile(file_path)

        if file_exp in ["jpeg", "jpg", "png", "webp", "gif"]:
            await bot.send_photo(callback.from_user.id, document)
        elif file_exp in ["mp4", "avi", "mov", "webm"]:
            await bot.send_video(callback.from_user.id, document)
        else:
            await bot.send_document(callback.from_user.id, document)

    if faq.text:
        await bot.send_message(callback.from_user.id, faq.text)


@faq_router.message(Command(commands="move"))
async def get_moves(message: Message, session: AsyncSession):
    move = await session.scalars(select(Move))
    keyboard = create_move_keyboard(move)
    await message.answer("<b>Уроки в движении</b>\n\n"
                         "Выберите вопрос, который вас интересует",
                         reply_markup=keyboard)


@faq_router.callback_query(F.data.startswith("detail_move_"))
async def get_detail_move(callback: CallbackQuery,
                         session: AsyncSession,
                         bot: Bot):
    _, _, faq_id = callback.data.split("_")
    file = await session.scalar(select(Move).where(Move.id == int(faq_id)))
    if file.file_path:
        file_path = os.path.join(DATA_FOLDER, file.file_path)
        _, file_exp = file_path.split(".")
        video = FSInputFile(file_path)

        await bot.send_video(callback.from_user.id, video)
