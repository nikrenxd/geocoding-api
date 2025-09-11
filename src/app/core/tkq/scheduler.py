from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from src.app.core.tkq.broker import pika_broker

scheduler = TaskiqScheduler(
    broker=pika_broker,
    sources=[LabelScheduleSource(pika_broker)],
)
