from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from ..dependencies import get_plantdata
from ..models.turbines import TurbineHealthRow, TurbineStatusResponse
from ..services.turbine_service import compute_turbine_health


router = APIRouter(prefix="/turbines", tags=["turbines"])


@router.get("/status", response_model=TurbineStatusResponse)
def turbines_status(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    plant=Depends(get_plantdata),
):
    rows, total = compute_turbine_health(plant=plant, limit=limit, offset=offset)
    return TurbineStatusResponse(
        rows=[
            TurbineHealthRow(
                turbineId=r.turbine_id,
                status=r.status,  # type: ignore[arg-type]
                generationKW=r.generation_kw,
                temperatureC=r.temperature_c,
                lastUpdate=r.last_update,
            )
            for r in rows
        ],
        total=total,
    )

