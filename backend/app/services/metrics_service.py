from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal

import numpy as np
import pandas as pd
from openoa.plant import PlantData

TimeRange = Literal["24h", "7d", "30d"]


@dataclass(frozen=True)
class MetricsSummary:
    timestamp: datetime
    power_output_mw: float
    avg_wind_speed_ms: float
    efficiency_pct: float
    active_turbines: int
    total_turbines: int


def _parse_range(range_str: TimeRange) -> timedelta:
    if range_str == "24h":
        return timedelta(hours=24)
    if range_str == "7d":
        return timedelta(days=7)
    if range_str == "30d":
        return timedelta(days=30)
    raise ValueError(f"Unsupported range: {range_str}")


def _latest_timestamp(scada: pd.DataFrame) -> datetime:
    # PlantData SCADA is usually indexed; tolerate either case.
    if "time" in scada.columns:
        ts = pd.to_datetime(scada["time"]).max()
    else:
        idx = scada.index
        if isinstance(idx, pd.MultiIndex) and "time" in idx.names:
            ts = pd.to_datetime(idx.get_level_values("time")).max()
        else:
            ts = pd.to_datetime(idx).max()
    return ts.to_pydatetime()


def _filter_scada_by_window(scada: pd.DataFrame, end: datetime, window: timedelta) -> pd.DataFrame:
    start = end - window
    if "time" in scada.columns:
        t = pd.to_datetime(scada["time"])
        return scada.loc[(t >= start) & (t <= end)]

    idx = scada.index
    if isinstance(idx, pd.MultiIndex) and "time" in idx.names:
        t = pd.to_datetime(idx.get_level_values("time"))
        return scada.loc[(t >= start) & (t <= end)]

    t = pd.to_datetime(idx)
    return scada.loc[(t >= start) & (t <= end)]


def compute_metrics_summary(plant: PlantData, range_str: TimeRange = "24h") -> MetricsSummary:
    scada = plant.scada.copy()
    end = _latest_timestamp(scada)
    window = _parse_range(range_str)
    scada_w = _filter_scada_by_window(scada, end=end, window=window)

    # Power output (instantaneous): mean of latest timestamp across turbines, MW
    power_kw_col = "WTUR_W"
    wind_ms_col = "WMET_HorWdSpd"
    temp_c_col = "WMET_EnvTmp"

    # Use most recent 10-min interval in window
    if isinstance(scada_w.index, pd.MultiIndex) and "time" in scada_w.index.names:
        times = pd.to_datetime(scada_w.index.get_level_values("time"))
        latest_t = times.max()
        latest = scada_w.loc[times == latest_t]
    else:
        # fallback: try time column or index equality
        if "time" in scada_w.columns:
            times = pd.to_datetime(scada_w["time"])
            latest_t = times.max()
            latest = scada_w.loc[times == latest_t]
        else:
            times = pd.to_datetime(scada_w.index)
            latest_t = times.max()
            latest = scada_w.loc[times == latest_t]

    power_output_mw = float(np.nanmean(latest[power_kw_col].to_numpy()) / 1000.0) if power_kw_col in latest.columns else 0.0

    # Average wind speed over window
    avg_wind_speed_ms = float(np.nanmean(scada_w[wind_ms_col].to_numpy())) if wind_ms_col in scada_w.columns else 0.0

    # Efficiency (simple proxy): actual power / (rated_power * active_turbines) at latest timestamp
    total_turbines = int(getattr(plant, "n_turbines", 0) or len(getattr(plant, "turbine_ids", [])))
    rated_power_mw = None
    try:
        if hasattr(plant, "asset") and plant.asset is not None and "rated_power" in plant.asset.columns:
            rated_power_mw = float(pd.to_numeric(plant.asset["rated_power"], errors="coerce").dropna().median())
    except Exception:
        rated_power_mw = None
    if rated_power_mw is None:
        rated_power_mw = 2.05  # fallback for La Haute Borne

    # Active turbines heuristic: turbines with non-null wind speed and power at latest timestamp
    if power_kw_col in latest.columns:
        active_turbines = int(np.sum(~np.isnan(pd.to_numeric(latest[power_kw_col], errors="coerce").to_numpy())))
    else:
        active_turbines = total_turbines

    denom = max(active_turbines, 1) * rated_power_mw
    efficiency_pct = float(np.clip((power_output_mw / denom) * 100.0, 0.0, 100.0)) if denom > 0 else 0.0

    return MetricsSummary(
        timestamp=end,
        power_output_mw=round(power_output_mw, 3),
        avg_wind_speed_ms=round(avg_wind_speed_ms, 3),
        efficiency_pct=round(efficiency_pct, 2),
        active_turbines=active_turbines,
        total_turbines=total_turbines,
    )

