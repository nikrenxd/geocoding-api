import logging

from dishka.integrations.taskiq import FromDishka, inject, setup_dishka
from taskiq import TaskiqEvents, TaskiqState

from src.app.core.di.setup import setup_container
from src.app.core.tkq.broker import pika_broker
from src.app.services.geodata.service import GeodataService

logger = logging.getLogger("tasks")


@pika_broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState):
    container = setup_container()
    setup_dishka(container, pika_broker)


@pika_broker.task(
    schedule=[
        {
            "cron": "0 */6 * * *",
            # "cron": "*/3 * * * *",
        }
    ]
)
@inject(patch_module=True)
async def task_delete_today_records(service: FromDishka[GeodataService]) -> None:
    data = await service.get_location_data_by_current_date()
    logger.info("Getting locations data")
    if data:
        logger.info("Locations data deleted")
        await service.delete_location_data_by_current_date()
