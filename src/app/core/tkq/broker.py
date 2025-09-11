from dishka import make_container
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from src.app.core.config import Settings
from src.app.core.di.providers import ConfigProvider


def create_rmq_broker() -> AioPikaBroker:
    container = make_container(ConfigProvider())
    config = container.get(Settings)
    broker = AioPikaBroker(url=config.RMQ_URL).with_result_backend(
        RedisAsyncResultBackend(redis_url=config.REDIS_URL)
    )
    container.close()

    return broker


pika_broker = create_rmq_broker()
