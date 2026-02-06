from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal

import numpy as np
import pandas as pd
from openoa.plant import PlantData
from openoa.utils.power_curve.functions import IEC

TimeRange = Literal["24h", "7d", "30d"]


@dataclass(frozen=True)
class PowerCurveData:
    scatter: list[tuple[float, float]]
    curve: list[tuple[float, float]]


def _parse_range(range_str: TimeRange) -> timedelta:
    if range_str == "24h":
        return timedelta(hours=24)
    if range_str == "7d":
        return timedelta(days=7)
    if range_str == "30d":
        return timedelta(days=30)
    raise ValueError(f"Unsupported range: {range_str}")


def _get_time_series(df: pd.DataFrame) -> pd.Series:
    if "time" in df.columns:
        return pd.to_datetime(df["time"])
    if isinstance(df.index, pd.MultiIndex) and "time" in df.index.names:
        return pd.to_datetime(df.index.get_level_values("time"))
    return pd.to_datetime(df.index)


def build_power_curve(
    plant: PlantData,
    range_str: TimeRange = "30d",
    max_scatter_points: int = 2500,
    curve_step_ms: float = 0.25,
) -> PowerCurveData:
    scada = plant.scada.copy()
    t = _get_time_series(scada)
    end = t.max().to_pydatetime()
    window = _parse_range(range_str)
    start = end - window
    mask = (t >= start) & (t <= end)
    df = scada.loc[mask]

    ws = pd.to_numeric(df.get("WMET_HorWdSpd"), errors="coerce")
    p = pd.to_numeric(df.get("WTUR_W"), errors="coerce")
    valid = (~ws.isna()) & (~p.isna()) & (ws >= 0) & (ws <= 35) & (p >= 0)
    ws = ws.loc[valid]
    p = p.loc[valid]

    if len(ws) == 0:
        return PowerCurveData(scatter=[], curve=[])

    # Downsample scatter points deterministically
    if len(ws) > max_scatter_points:
        idx = np.linspace(0, len(ws) - 1, max_scatter_points).astype(int)
        ws_s = ws.to_numpy()[idx]
        p_s = p.to_numpy()[idx]
    else:
        ws_s = ws.to_numpy()
        p_s = p.to_numpy()

    scatter = list(zip(ws_s.astype(float).tolist(), p_s.astype(float).tolist()))

    # Fit IEC binned power curve and evaluate on a dense windspeed grid
    df_fit = pd.DataFrame({"ws": ws.to_numpy(), "p": p.to_numpy()})
    pc = IEC("ws", "p", data=df_fit, bin_width=0.5, windspeed_start=0, windspeed_end=30.0, interpolate=True)

    ws_grid = np.arange(0.0, 30.0 + curve_step_ms, curve_step_ms)
    curve_p = pc(ws_grid)
    curve = list(zip(ws_grid.astype(float).tolist(), np.asarray(curve_p, dtype=float).tolist()))
    return PowerCurveData(scatter=scatter, curve=curve)

