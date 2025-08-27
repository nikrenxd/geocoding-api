from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.app.api.v1.routes import router
from src.app.core.providers import (
    ConfigProvider,
    DatabaseProvider,
    RepositoryProvider,
    ServiceProvider,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def setup_app(_lifespan) -> FastAPI:
    _app = FastAPI(lifespan=_lifespan)
    _app.include_router(router)
    return _app


def create_app(_lifespan) -> FastAPI:
    _app = setup_app(_lifespan)
    container = make_async_container(
        DatabaseProvider(),
        ConfigProvider(),
        RepositoryProvider(),
        ServiceProvider(),
    )
    setup_dishka(container, _app)

    return _app


app = create_app(lifespan)
