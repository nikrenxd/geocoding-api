from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.app.core.config import Settings, create_config
from src.app.core.database import create_engine, create_session
from src.app.repositories import GeodataRepository
from src.app.services import GeodataService


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Settings:
        return create_config()


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, config: Settings) -> AsyncEngine:
        return create_engine(config)

    @provide(scope=Scope.REQUEST)
    def get_session(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return create_session(engine)


class ServicesProvider(Provider):
    geodata_repository = provide(GeodataRepository)
    geodata_service = provide(GeodataService)
