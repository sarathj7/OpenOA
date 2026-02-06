from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from openoa.plant import PlantData


@dataclass(frozen=True)
class TurbineGeo:
    turbine_id: str
    lat: float
    lon: float
    status: str
    current_power_kw: float


def _latest_scada_snapshot(plant: PlantData) -> pd.DataFrame:
    scada = plant.scada.copy()
    if "time" in scada.columns:
        t = pd.to_datetime(scada["time"])
        latest = t.max()
        return scada.loc[t == latest]
    if isinstance(scada.index, pd.MultiIndex) and "time" in scada.index.names:
        t = pd.to_datetime(scada.index.get_level_values("time"))
        latest = t.max()
        return scada.loc[t == latest]
    t = pd.to_datetime(scada.index)
    latest = t.max()
    return scada.loc[t == latest]


def get_turbine_geospatial_points(plant: PlantData) -> list[TurbineGeo]:
    asset = plant.asset.copy()
    # Standardized via metadata mapping
    id_col = "asset_id" if "asset_id" in asset.columns else None
    lat_col = "latitude" if "latitude" in asset.columns else None
    lon_col = "longitude" if "longitude" in asset.columns else None
    if not (id_col and lat_col and lon_col):
        return []

    # Join latest SCADA power on turbineId
    scada_latest = _latest_scada_snapshot(plant)
    if "asset_id" in scada_latest.columns:
        scada_latest = scada_latest.copy()
        scada_latest["asset_id"] = scada_latest["asset_id"].astype(str)
        power_by_id = (
            pd.to_numeric(scada_latest.get("WTUR_W"), errors="coerce")
            .groupby(scada_latest["asset_id"])
            .mean()
        )
    elif isinstance(scada_latest.index, pd.MultiIndex) and "asset_id" in scada_latest.index.names:
        asset_ids = scada_latest.index.get_level_values("asset_id").astype(str)
        power_by_id = pd.to_numeric(scada_latest.get("WTUR_W"), errors="coerce").groupby(asset_ids).mean()
    else:
        power_by_id = pd.Series(dtype=float)

    points: list[TurbineGeo] = []
    for _, row in asset.iterrows():
        tid = str(row[id_col])
        lat = float(row[lat_col])
        lon = float(row[lon_col])
        p = float(power_by_id.get(tid, np.nan))
        if np.isnan(p):
            p = 0.0
        status = "online" if p > 0 else "maintenance"
        points.append(TurbineGeo(turbine_id=tid, lat=lat, lon=lon, status=status, current_power_kw=p))

    return points

