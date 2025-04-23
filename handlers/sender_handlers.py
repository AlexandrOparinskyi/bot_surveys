from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import load_config
from database.models import User
from keyboards.sender_keyboards import create_sender_keyboard

sender_router = Router()
storage = MemoryStorage()
config = load_config()


class SenderState(StatesGroup):
    in_process = State()
    confirm = State()


@sender_router.message(Command(commands="q"))
async def start_send_message_all_user(message: Message, state: FSMContext):
    if message.from_user.id not in config.tg_bot.user_id:
        return

    await state.set_state(SenderState.in_process)
    await message.answer("Введите сообщение, которое хотите отправить всем "
                         "пользователям")


@sender_router.callback_query(StateFilter(SenderState.confirm),
                              F.data == "back_to_start_send_message")
async def start_send_message_all_user_cb(callback: CallbackQuery,
                                         state: FSMContext):
    await state.set_state(SenderState.in_process)
    await callback.message.answer("Введите сообщение, которое хотите "
                                  "отправить всем пользователям")


@sender_router.message(StateFilter(SenderState.in_process))
async def finish_send_message_all_user(message: Message, state: FSMContext):
    await state.set_state(SenderState.confirm)
    await state.update_data(message=message.text)
    keyboard = create_sender_keyboard()
    await message.answer(f"Сообщение для всех пользователей:\n"
                         f"    <b>{message.text}</b>",
                         reply_markup=keyboard)


@sender_router.callback_query(StateFilter(SenderState.confirm),
                              F.data == "send_message_all_user")
async def send_message_all_user(callback: CallbackQuery,
                                state: FSMContext,
                                session: AsyncSession,
                                bot: Bot):
    data = await state.get_data()
    await state.clear()
    users = await session.scalars(select(User))
    await callback.answer("Отправлено")
    await callback.message.delete()

    for user in users:
        if user.user_id not in config.tg_bot.user_id:
            try:
                await bot.send_message(chat_id=user.user_id,
                                       text=data.get("message"))
            except Exception:
                pass
