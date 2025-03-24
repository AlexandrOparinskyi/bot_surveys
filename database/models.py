from sqlalchemy import (Column, Integer, String,
                        Text, BigInteger)
from sqlalchemy.orm import DeclarativeBase


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
    __tablename__ = "users"

    user_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(100), nullable=True, unique=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(70), nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String(100), nullable=False)
