import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)

from config import load_config

logger = logging.getLogger(__name__)

config = load_config()
DB_HOST = config.db.db_host
DB_PORT = config.db.db_port
DB_NAME = config.db.db_name
DB_USER = config.db.db_user
DB_PASS = config.db.db_pass

db_url = (f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@"
          f"{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_async_engine(url=db_url, echo=False)
async_session = async_sessionmaker(bind=engine,
                                   expire_on_commit=False,
                                   class_=AsyncSession)


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as err:
            logger.error(f"Error at database: {err}")
            await session.rollback()
            raise
        finally:
            await session.close()
