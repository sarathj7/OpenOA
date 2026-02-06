from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class MetricsSummaryResponse(BaseModel):
    timestamp: datetime
    powerOutputMW: float = Field(..., description="Aggregate latest power output (MW)")
    averageWindSpeedMS: float = Field(..., description="Average wind speed over window (m/s)")
    efficiencyPct: float = Field(..., description="Efficiency proxy (%)")
    activeTurbines: int
    totalTurbines: int


class MetricValueResponse(BaseModel):
    timestamp: datetime
    value: float

