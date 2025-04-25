from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Survey, SurveyResult, User, UserPoint, SendResult


def generate_question_text(survey: Survey, n: int) -> str:
    data = {
        0: "A",
        1: "B",
        2: "C"
    }

    text = f"{survey.questions[n].text}\n\n"
    for i, o in enumerate(survey.questions[n].options):
        text += f"<b>{data[i]}.</b>  {o.text}\n"

    return text


async def get_result_for_survey(session: AsyncSession, survey: Survey,
                                result_point: int) -> SurveyResult:
    result_query = select(SurveyResult).where(
        and_(SurveyResult.min_point <= result_point,
             SurveyResult.max_point >= result_point,
             SurveyResult.survey_id == survey.id)
    )
    result = await session.scalar(result_query)
    return result


async def get_user_by_user_id(session: AsyncSession, user_id: int):
    user_query = select(User).where(
        User.user_id == user_id
    )
    user = await session.scalar(user_query)
    return user


async def exists_user_point_in_survey(session: AsyncSession, user_id: int,
                                      survey: Survey) -> bool:
    user = await get_user_by_user_id(session, user_id)

    user_point_query = select(UserPoint).where(
        and_(UserPoint.user_id == user.id,
             UserPoint.survey_id == survey.id)
    )
    user_point = await session.scalar(user_point_query)
    print(user_point, survey.id, user_id)
    return user_point is not None


async def get_send_results(session: AsyncSession):
    get_result = await session.execute(select(SendResult))
    return get_result.first()[0]
