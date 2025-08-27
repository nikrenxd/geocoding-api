from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.database import Base


class Geodata(Base):
    __tablename__ = "geodata"

    id: Mapped[int] = mapped_column(primary_key=True)

    display_name: Mapped[str]
    lat: Mapped[float]
    lon: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
