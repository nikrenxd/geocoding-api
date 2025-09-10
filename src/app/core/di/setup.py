from dishka import AsyncContainer, make_async_container

from src.app.core.di import providers


def setup_container() -> AsyncContainer:
    return make_async_container(*providers)
