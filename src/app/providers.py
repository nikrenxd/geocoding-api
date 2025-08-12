from dishka import Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.app.config import Settings, create_config
from src.app.database import create_engine, create_session


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


container = make_async_container(
    DatabaseProvider(),
    ConfigProvider(),
)
