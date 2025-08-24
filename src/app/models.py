from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.database import Base


class Geodata(Base):
    __tablename__ = "geodata"

    id: Mapped[int] = mapped_column(primary_key=True)

    displayed_name: Mapped[str]
    lat: Mapped[float]
    lon: Mapped[float]
