from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


TurbineStatus = Literal["online", "warning", "maintenance"]


class TurbineMapPoint(BaseModel):
    turbineId: str
    lat: float
    lon: float
    status: TurbineStatus
    currentPowerKW: float


class TurbineMapResponse(BaseModel):
    turbines: list[TurbineMapPoint]

