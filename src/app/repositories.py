from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import Geodata


class GeodataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_data(self, data: dict) -> Geodata | None:
        stmt = insert(Geodata).values(**data).returning(Geodata)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()
