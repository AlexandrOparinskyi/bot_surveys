from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from keyboards.register_keyboards import create_confirm_register_keyboard
from services.register_services import get_register_command, exists_user

register_router = Router()
storage = MemoryStorage()


class RegisterState(StatesGroup):
    name = State()
    age = State()
    city = State()
    confirm = State()


@register_router.message(Command(commands="register"))
async def start_register(message: Message,
                         session: AsyncSession,
                         state: FSMContext):
    """Срабатывает после ввода команды /register.
    Создает состояние name и предлагает ввести имя и фамилию"""
    if await exists_user(session, message.from_user.id):
        command = await get_register_command(session, "user_exists")
        await message.answer(command.text)
        return

    await state.set_state(RegisterState.name)
    command = await get_register_command(session, "register")
    await message.answer(command.text)


@register_router.message(StateFilter(RegisterState.name),
                         lambda x: len(x.text.split(" ")) == 2)
async def register_name(message: Message,
                        session: AsyncSession,
                        state: FSMContext):
    """Срабатывает после корректного ввода имени и фамилии.
    Меняет состояние name на age и предлагает ввести возраст"""
    name, surname = message.text.split(" ")
    await state.set_state(RegisterState.age)
    await state.update_data({"name": name.title(),
                             "surname": surname.title()})

    command = await get_register_command(session, "register_name")
    await message.answer(command.text)


@register_router.message(StateFilter(RegisterState.name))
async def fail_register_name(message: Message,
                             session: AsyncSession):
    command = await get_register_command(session, "fail_register_name")
    await message.answer(command.text)


@register_router.message(StateFilter(RegisterState.age),
                         lambda x: x.text.isdigit() and
                                   0 < int(x.text) < 100)
async def register_age(message: Message,
                       session: AsyncSession,
                       state: FSMContext):
    await state.set_state(RegisterState.city)
    await state.update_data({"age": int(message.text)})

    command = await get_register_command(session, "register_age")
    await message.answer(command.text)


@register_router.message(StateFilter(RegisterState.age))
async def fail_register_age(message: Message,
                            session: AsyncSession):
    command = await get_register_command(session, "fail_register_age")
    await message.answer(command.text)


@register_router.message(StateFilter(RegisterState.city))
async def register_city(message: Message,
                        session: AsyncSession,
                        state: FSMContext):
    await state.set_state(RegisterState.confirm)
    await state.update_data({"city": message.text.title()})

    data = await state.get_data()
    command = await get_register_command(session, "register_city")

    text = (f"{command.text}\n\n"
            f"Имя: {data.get('name')}\n"
            f"Фамилия: {data.get('surname')}\n"
            f"Возраст: {data.get('age')}\n"
            f"Город: {message.text.title()}")
    keyboard = create_confirm_register_keyboard()

    await message.answer(text, reply_markup=keyboard)


@register_router.callback_query(StateFilter(RegisterState.confirm),
                                lambda x: x.data in ("error_register_data",
                                                     "confirm_register_data"))
async def confirm_register(callback: CallbackQuery,
                           session: AsyncSession,
                           state: FSMContext):
    if callback.data == "error_register_data":
        await state.clear()
        await start_register(callback.message, session, state)
        return

    data = await state.get_data()
    user_query = insert(User).values(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        name=data.get("name"),
        surname=data.get("surname"),
        age=data.get("age"),
        city=data.get("city")
    )
    await session.execute(user_query)
    await session.commit()

    command = await get_register_command(session, "register_confirm")
    await callback.message.answer(command.text)
