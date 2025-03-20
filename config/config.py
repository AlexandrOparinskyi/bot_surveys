from dataclasses import dataclass
from environs import env


@dataclass
class TgBot:
    token: str
    user_id: list[int]


@dataclass
class DataBase:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DataBase


def load_config(path: str | None = None) -> Config:
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env("TOKEN"),
            user_id=[int(uid) for uid in env("USER_ID").split(", ")]
        ),
        db=DataBase(
            db_host=env("DB_HOST"),
            db_port=env("DB_PORT"),
            db_name=env("DB_NAME"),
            db_user=env("DB_USER"),
            db_pass=env("DB_PASS"),
        )
    )
