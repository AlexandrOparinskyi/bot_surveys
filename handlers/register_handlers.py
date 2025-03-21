from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from services.command_services import get_register_command

register_router = Router()
storage = MemoryStorage()


class RegisterState(StatesGroup):
    name = State()


@register_router.message(Command(commands="register"))
async def start_register(message: Message,
                         session: AsyncSession,
                         state: FSMContext):
    """Отрабатывает после ввода команды /register.
    Создает состояние name и ожидает ввода имени и фамилии"""
    await state.set_state(RegisterState.name)
    command = await get_register_command(session, message)
    await message.answer(command.text)
