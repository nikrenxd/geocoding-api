from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.app.api.v1.routes import router
from src.app.core.di.setup import setup_container
from src.app.core.logging import setup_logging
from src.app.core.tkq.broker import pika_broker


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await pika_broker.startup()
    yield
    await pika_broker.shutdown()

    await _app.state.dishka_container.close()


def setup_app(_lifespan) -> FastAPI:
    _app = FastAPI(lifespan=_lifespan)
    _app.include_router(router)
    return _app


def create_app(_lifespan) -> FastAPI:
    container = setup_container()

    _app = setup_app(_lifespan)
    setup_logging()
    setup_dishka(container, _app)
    return _app


app = create_app(lifespan)
