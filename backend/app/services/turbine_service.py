from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd
from openoa.plant import PlantData


@dataclass(frozen=True)
class TurbineHealth:
    turbine_id: str
    status: str
    generation_kw: float
    temperature_c: float | None
    last_update: datetime


def _get_asset_id_series(df: pd.DataFrame) -> pd.Series | None:
    if "asset_id" in df.columns:
        return df["asset_id"]
    if isinstance(df.index, pd.MultiIndex) and "asset_id" in df.index.names:
        return pd.Series(df.index.get_level_values("asset_id"), index=df.index)
    return None


def _get_time_series(df: pd.DataFrame) -> pd.Series:
    if "time" in df.columns:
        return pd.to_datetime(df["time"])
    if isinstance(df.index, pd.MultiIndex) and "time" in df.index.names:
        return pd.to_datetime(df.index.get_level_values("time"))
    return pd.to_datetime(df.index)


def compute_turbine_health(plant: PlantData, limit: int = 50, offset: int = 0) -> tuple[list[TurbineHealth], int]:
    scada = plant.scada.copy()
    t = _get_time_series(scada)
    latest_t = t.max()
    scada_latest = scada.loc[t == latest_t]

    asset_ids = _get_asset_id_series(scada_latest)
    if asset_ids is None:
        # fallback to PlantData turbine IDs
        turbine_ids = list(getattr(plant, "turbine_ids", []))
    else:
        turbine_ids = list(pd.unique(asset_ids.astype(str)))

    power_col = "WTUR_W"
    temp_col = "WMET_EnvTmp"

    rows: list[TurbineHealth] = []
    for tid in turbine_ids:
        if asset_ids is not None:
            mask = asset_ids.astype(str) == str(tid)
            df_t = scada_latest.loc[mask]
        else:
            df_t = scada_latest

        power_kw = float(np.nanmean(pd.to_numeric(df_t.get(power_col, pd.Series(dtype=float)), errors="coerce")))
        temp_c = None
        if temp_col in df_t.columns:
            v = float(np.nanmean(pd.to_numeric(df_t[temp_col], errors="coerce")))
            temp_c = None if np.isnan(v) else v

        # simple status rules
        status = "online"
        if np.isnan(power_kw) or power_kw <= 0:
            status = "maintenance"
        elif temp_c is not None and temp_c >= 35:
            status = "warning"

        rows.append(
            TurbineHealth(
                turbine_id=str(tid),
                status=status,
                generation_kw=0.0 if np.isnan(power_kw) else power_kw,
                temperature_c=temp_c,
                last_update=pd.to_datetime(latest_t).to_pydatetime(),
            )
        )

    total = len(rows)
    rows = sorted(rows, key=lambda r: r.turbine_id)
    return rows[offset : offset + limit], total

