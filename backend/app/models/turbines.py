from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


TurbineStatus = Literal["online", "warning", "maintenance"]


class TurbineHealthRow(BaseModel):
    turbineId: str
    status: TurbineStatus
    generationKW: float
    temperatureC: float | None
    lastUpdate: datetime


class TurbineStatusResponse(BaseModel):
    rows: list[TurbineHealthRow]
    total: int

