from collections.abc import AsyncIterable

import pytest
from dishka import AsyncContainer
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.app.core.config import Settings
from src.app.core.database import Base
from src.app.core.di.setup import setup_container
from src.app.repositories import GeodataRepository


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
async def container() -> AsyncIterable[AsyncContainer]:
    container = setup_container()
    yield container
    await container.close()


@pytest.fixture()
async def config(container) -> Settings:
    return await container.get(Settings)


@pytest.fixture()
async def request_container(container: AsyncContainer):
    async with container() as request_container:
        yield request_container


@pytest.fixture()
async def async_session(request_container: AsyncContainer):
    return await request_container.get(AsyncSession)


@pytest.fixture()
def geodata_repository(async_session: AsyncSession):
    return GeodataRepository(session=async_session)


@pytest.fixture(autouse=True)
async def setup_test_db(container: AsyncContainer):
    config = await container.get(Settings)
    async_engine = await container.get(AsyncEngine)

    if config.ENV == "TEST":
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    else:
        raise RuntimeError(f"Tests should run in TEST environment not in {config.ENV}")
