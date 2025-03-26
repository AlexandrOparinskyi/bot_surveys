from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Survey
from filters.survey_filters import SurveySlugFilter
from keyboards.survey_keyboards import (create_all_surveys_keyboard,
                                        create_start_survey_keyboard,
                                        create_options_keyboard)
from services.survey_services import generate_question_text

survey_router = Router()
storage = MemoryStorage()


class SurveyState(StatesGroup):
    in_description = State()
    in_survey = State()


@survey_router.message(Command(commands="surveys"))
async def select_survey(message: Message,
                        session: AsyncSession,
                        state: FSMContext):
    """Срабатывает после команды /surveys и предлагает выбрать
    опрос для прохождения"""
    surveys_query = select(Survey).where(
        Survey.is_active == True
    )
    surveys = await session.scalars(surveys_query)

    keyboard = create_all_surveys_keyboard(surveys.all())
    text = ("Выберите, пожалуйста, опрос.\n\n"
            "После выбора нужного опроса вам будет доступно его описание"
            " и полное название, если оно не умещается в кнопке.\n\n"
            "Вы сможете вернуться к списку, нажав"
            " кнопку 'Назад к опросам', если выбранный опрос"
            "вам не подходит")

    await state.set_state(SurveyState.in_description)
    await message.answer(text, reply_markup=keyboard)


@survey_router.callback_query(StateFilter(SurveyState.in_description),
                              SurveySlugFilter())
async def get_survey_description(callback: CallbackQuery,
                                 session: AsyncSession,
                                 state: FSMContext):
    """Срабатывает после выбора опроса и показывает полное название
    опроса с его описанием. Предлагает либо пройти выбранный опрос,
    либо вернуться к списку опросов"""
    survey_query = select(Survey).where(
        and_(Survey.is_active == True,
             Survey.slug == callback.data)
    )
    survey = await session.scalar(survey_query)

    await state.update_data({"survey": survey})

    text = (f"<b>{survey.title}</b>\n\n"
            f"{survey.description}")
    keyboard = create_start_survey_keyboard()

    await callback.message.edit_text(text, reply_markup=keyboard)


@survey_router.callback_query(StateFilter(SurveyState.in_description),
                              lambda x: x.data in ["start_this_survey",
                                                   "back_to_surveys_list"])
async def start_survey_or_back_to_surveys_list(callback: CallbackQuery,
                                               session: AsyncSession,
                                               state: FSMContext):
    """Срабатывает после начала опроса, либо возврата к списку опросов.
    Если пользователь выбрал возврат к списку - вызывается метод
    select_survey. Иначе пользователь начинает проходить опрос"""
    if callback.data == "back_to_surveys_list":
        await state.clear()
        await select_survey(callback.message, session, state)
        return

    data = await state.get_data()
    survey = data.get("survey")
    await state.update_data({"n": 1})
    await state.set_state(SurveyState.in_survey)

    if not survey:
        await callback.message.answer("Какая-то ошибка...\n"
                                      "Опрос не найдет, попробуй "
                                      "начать заново")
        return

    text = generate_question_text(survey, 0)
    keyboard = create_options_keyboard()

    await callback.message.answer(text, reply_markup=keyboard)


@survey_router.callback_query(StateFilter(SurveyState.in_survey),
                              F.data.startswith("next_question_"))
async def continue_or_finish_survey(callback: CallbackQuery,
                                    session: AsyncSession,
                                    state: FSMContext):
    """Срабатывает на первый ответ любого опроса и на каждый следующий
    до завершения опроса. При продолжении возвращает следующий вопрос с
    ответами. При завершении считает очки и завершает опрос"""

    data = await state.get_data()
    survey, n = data.get("survey"), data.get("n")
    index = int(callback.data.split("_")[-1])
    point = int(survey.questions[n - 1].options[index].is_correct)

    if len(survey.questions) <= n:
        await callback.message.answer("finish bro")
        point_result = data.get("result") + point
        await callback.message.answer(f"Вы набрали {point_result} баллов")
        return

    text = generate_question_text(survey, n)
    keyboard = create_options_keyboard()

    if n == 1:
        await state.update_data({"n": n + 1, "result": point})
    else:
        await state.update_data({"n": n + 1,
                                 "result": data.get("result") + point})
    await callback.message.answer(text, reply_markup=keyboard)
