from datetime import datetime

from pydantic import BaseModel


class GeodataCreatedAt(BaseModel):
    created_at: datetime


class GeodataLocationResponse(GeodataCreatedAt):
    display_name: str


class GeodataResponse(GeodataCreatedAt):
    display_name: str
    lat: float
    lon: float
