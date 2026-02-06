from __future__ import annotations

from pydantic import BaseModel


class PowerCurvePoint(BaseModel):
    windSpeed: float
    powerKW: float


class PowerCurveResponse(BaseModel):
    scatter: list[PowerCurvePoint]
    curve: list[PowerCurvePoint]
