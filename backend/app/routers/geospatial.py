from __future__ import annotations

from fastapi import APIRouter, Depends

from ..dependencies import get_plantdata
from ..models.geospatial import TurbineMapPoint, TurbineMapResponse
from ..services.geospatial_service import get_turbine_geospatial_points


router = APIRouter(prefix="/geospatial", tags=["geospatial"])


@router.get("/turbines", response_model=TurbineMapResponse)
def geospatial_turbines(plant=Depends(get_plantdata)):
    points = get_turbine_geospatial_points(plant)
    return TurbineMapResponse(
        turbines=[
            TurbineMapPoint(
                turbineId=p.turbine_id,
                lat=p.lat,
                lon=p.lon,
                status=p.status,  # type: ignore[arg-type]
                currentPowerKW=p.current_power_kw,
            )
            for p in points
        ]
    )

