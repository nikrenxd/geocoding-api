from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.app.config import Settings


def create_engine(config: Settings) -> AsyncEngine:
    engine = create_async_engine(config.DB_URL)

    return engine


def create_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase): ...
