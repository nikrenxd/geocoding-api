import logging

from sqlalchemy import Date, cast, delete, func, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.geodata import Geodata

logger = logging.getLogger("repositories.geodata")


class GeodataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_data(self, data: dict) -> Geodata | None:
        try:
            stmt = insert(Geodata).values(**data).returning(Geodata)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar()
        except SQLAlchemyError:
            logger.error("Failed to save data")

    async def delete_current_date_data(self) -> None:
        try:
            stmt = delete(Geodata).where(
                cast(Geodata.created_at, Date) == func.current_date()
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError:
            logger.error("Failed to delete data")

    async def get_data_by_current_date(self) -> list[Geodata | None]:
        try:
            stmt = select(Geodata).where(
                cast(Geodata.created_at, Date) == func.current_date()
            )
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError:
            logger.error("Failed to get filtered data")
