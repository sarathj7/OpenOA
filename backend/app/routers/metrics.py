from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Query

from ..dependencies import get_plantdata
from ..models.metrics import MetricValueResponse, MetricsSummaryResponse
from ..services.metrics_service import compute_metrics_summary


router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/summary", response_model=MetricsSummaryResponse)
def get_metrics_summary(
    range: Literal["24h", "7d", "30d"] = Query("24h"),
    plant=Depends(get_plantdata),
):
    summary = compute_metrics_summary(plant=plant, range_str=range)
    return MetricsSummaryResponse(
        timestamp=summary.timestamp,
        powerOutputMW=summary.power_output_mw,
        averageWindSpeedMS=summary.avg_wind_speed_ms,
        efficiencyPct=summary.efficiency_pct,
        activeTurbines=summary.active_turbines,
        totalTurbines=summary.total_turbines,
    )


@router.get("/power-output", response_model=MetricValueResponse)
def power_output(
    range: Literal["24h", "7d", "30d"] = Query("24h"),
    plant=Depends(get_plantdata),
):
    s = compute_metrics_summary(plant=plant, range_str=range)
    return MetricValueResponse(timestamp=s.timestamp, value=s.power_output_mw)


@router.get("/wind-speed", response_model=MetricValueResponse)
def wind_speed(
    range: Literal["24h", "7d", "30d"] = Query("24h"),
    plant=Depends(get_plantdata),
):
    s = compute_metrics_summary(plant=plant, range_str=range)
    return MetricValueResponse(timestamp=s.timestamp, value=s.avg_wind_speed_ms)


@router.get("/efficiency", response_model=MetricValueResponse)
def efficiency(
    range: Literal["24h", "7d", "30d"] = Query("24h"),
    plant=Depends(get_plantdata),
):
    s = compute_metrics_summary(plant=plant, range_str=range)
    return MetricValueResponse(timestamp=s.timestamp, value=s.efficiency_pct)


@router.get("/active-turbines", response_model=MetricValueResponse)
def active_turbines(
    range: Literal["24h", "7d", "30d"] = Query("24h"),
    plant=Depends(get_plantdata),
):
    s = compute_metrics_summary(plant=plant, range_str=range)
    return MetricValueResponse(timestamp=s.timestamp, value=float(s.active_turbines))

