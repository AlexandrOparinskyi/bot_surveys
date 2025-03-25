from database.models import Survey, SurveyResult


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


async def get_result_for_survey(survey, result_point) -> SurveyResult:
    pass
