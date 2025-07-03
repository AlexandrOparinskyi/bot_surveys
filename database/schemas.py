from pydantic import BaseModel


class OptionBase(BaseModel):
    text: str
    is_correct: bool


class QuestionBase(BaseModel):
    text: str
    answers: list[OptionBase]


class ResultBase(BaseModel):
    min_point: int
    max_point: int
    text: str
    description: str


class SurveyBase(BaseModel):
    title: str
    description: str | None = None
    is_active: bool = False
    questions: list[QuestionBase]
    results: list[ResultBase]
