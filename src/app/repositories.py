from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import Geodata


class GeodataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_data(
        self, address: str, lat: float, lon: float
    ) -> str | None:
        try:
            async with self.session() as session:
                stmt = (
                    insert(Geodata)
                    .values(
                        displayed_name=address,
                        lat=lat,
                        lon=lon,
                    )
                    .returning(Geodata.displayed_name)
                )
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar()
        except SQLAlchemyError:
            pass
