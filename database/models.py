from uuid import uuid4

from slugify import slugify
from sqlalchemy import (Column, Integer, String, Text, BigInteger,
                        ForeignKey, Boolean, LargeBinary)
from sqlalchemy.event import listens_for
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class BotCommand(Base):
    """Модель для команд бота"""
    __tablename__ = "bot_commands"

    command = Column(String(20), nullable=False)
    text = Column(Text, nullable=False)


class RegisterCommand(Base):
    """Модель для команд регистрации"""
    __tablename__ = "register_commands"

    command = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    description = Column(String, nullable=True)


class User(Base):
    """Модель пользователей"""
    __tablename__ = "users"

    user_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(100), nullable=True, unique=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(70), nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String(100), nullable=False)

    user_points = relationship("UserPoint",
                               back_populates="user",
                               lazy="selectin")

    def __repr__(self):
        return f"{self.name} {self.surname}"


class Survey(Base):
    """Модель опросов"""
    __tablename__ = "surveys"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=False, nullable=False)

    questions = relationship("Question",
                             back_populates="survey",
                             lazy="selectin")
    options = relationship("Option",
                           back_populates="survey",
                           lazy="selectin")
    user_points = relationship("UserPoint",
                               back_populates="survey",
                               lazy="selectin")

    def __repr__(self):
        return self.title


@listens_for(Survey, "before_insert")
def generate_slug(mapper, connection, target):
    if not target.slug:
        target.slug = slugify(f"{target.title[:40]}-{str(uuid4())[:6]}")


class Question(Base):
    """Модель вопросов"""
    __tablename__ = "questions"

    text = Column(String, nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)

    survey = relationship("Survey",
                          back_populates="questions",
                          lazy="selectin")
    options = relationship("Option",
                           back_populates="question",
                           lazy="selectin")

    def __repr__(self):
        return self.text


class Option(Base):
    """Модель ответов на вопросы"""
    __tablename__ = "options"

    text = Column(String, nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)

    survey = relationship("Survey",
                          back_populates="options",
                          lazy="selectin")
    question = relationship("Question",
                            back_populates="options",
                            lazy="selectin")


class UserPoint(Base):
    """Модель итогоов"""
    __tablename__ = "user_points"

    points = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)

    user = relationship("User",
                        back_populates="user_points",
                        lazy="selectin")
    survey = relationship("Survey",
                          back_populates="user_points",
                          lazy="selectin")


class SurveyResult(Base):
    """Модель результатов опроса"""
    __tablename__ = "survey_results"

    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    min_point = Column(Integer, nullable=False)
    max_point = Column(Integer, nullable=False)
    text_result = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    survey = relationship("Survey", lazy="selectin")


class FAQ(Base):
    """Модель вопросов/ответов"""
    __tablename__ = "faq"

    question = Column(String(255), nullable=False)
    text = Column(Text, nullable=True)
    file_path_1 = Column(String(255), nullable=True)
    file_path_2 = Column(String(255), nullable=True)
    file_path_3 = Column(String(255), nullable=True)


class SendResult(Base):
    """Модель отправки результата"""
    __tablename__ = "send_results"

    send_telegram = Column(Boolean, nullable=False, default=True)
    send_email = Column(Boolean, nullable=False, default=True)
    save_google_sheet = Column(Boolean, nullable=False, default=True)
