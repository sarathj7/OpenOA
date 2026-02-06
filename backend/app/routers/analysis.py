from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Query

from ..dependencies import get_plantdata, require_role
from ..models.analysis import PowerCurvePoint, PowerCurveResponse
from ..services.power_curve_service import build_power_curve


router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/power-curve", response_model=PowerCurveResponse)
def power_curve(
    range: Literal["24h", "7d", "30d"] = Query("30d"),
    plant=Depends(get_plantdata),
):
    data = build_power_curve(plant=plant, range_str=range)
    return PowerCurveResponse(
        scatter=[PowerCurvePoint(windSpeed=x, powerKW=y) for x, y in data.scatter],
        curve=[PowerCurvePoint(windSpeed=x, powerKW=y) for x, y in data.curve],
    )


@router.get("/aep")
def aep_placeholder(_user=Depends(require_role("engineer"))):
    # Advanced OpenOA AEP analyses can be exposed here later.
    return {"message": "AEP endpoint reserved for engineer/admin roles."}

