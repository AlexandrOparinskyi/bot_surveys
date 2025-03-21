from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class BotCommand(Base):
    __tablename__ = "bot_commands"

    command = Column(String(20), nullable=False)
    text = Column(Text, nullable=False)
