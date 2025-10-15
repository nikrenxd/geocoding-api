from collections.abc import AsyncIterable

from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.app.core.config import Settings, create_config
from src.app.core.database import create_engine, create_session
from src.app.repositories.geodata import GeodataRepository
from src.app.services.geodata.client import GeodataClient
from src.app.services.geodata.service import GeodataService


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Settings:
        return create_config()


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, config: Settings) -> AsyncEngine:
        return create_engine(config)

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return create_session(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    geodata_repository = provide(GeodataRepository)


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    geodata_client = provide(GeodataClient)
    geodata_service = provide(GeodataService)
