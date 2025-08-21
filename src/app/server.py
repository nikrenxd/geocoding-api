from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.app.api import router
from src.app.core.providers import create_container


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
    container = create_container()
    setup_dishka(container, _app)

    return _app


app = create_app(lifespan)
