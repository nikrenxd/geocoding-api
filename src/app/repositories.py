from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import Geodata


class GeodataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Geodata]:
        stmt = select(Geodata).distinct()
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def save_data_list(self, data: list[dict]) -> list[Geodata] | None:
        result = await self.session.execute(
            insert(Geodata).returning(Geodata),
            [*data],
        )
        await self.session.commit()
        return result.scalars().all()

    async def save_data(self, data: dict) -> Geodata | None:
        stmt = insert(Geodata).values(**data).returning(Geodata)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()
