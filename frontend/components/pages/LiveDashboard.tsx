"use client";

import { useEffect, useMemo, useState } from "react";

import { MetricCard } from "@/components/widgets/MetricCard";
import { PowerCurveChart } from "@/components/widgets/PowerCurveChart";
import { TurbineHealthTable } from "@/components/widgets/TurbineHealthTable";
import { useMetricsSummary, usePowerCurve, useTurbineStatus } from "@/lib/hooks/dashboard";

type RangeKey = "24h" | "7d" | "30d";

export function LiveDashboard() {
  const [range, setRange] = useState<RangeKey>("24h");

  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent).detail as RangeKey;
      setRange(detail);
    };
    window.addEventListener("dashboard:range", handler);
    return () => window.removeEventListener("dashboard:range", handler);
  }, []);

  const metrics = useMetricsSummary(range);
  const powerCurve = usePowerCurve(range);
  const turbineStatus = useTurbineStatus();

  const cards = useMemo(
    () => [
      {
        title: "Power Output",
        value: metrics.data ? `${metrics.data.powerOutputMW.toFixed(2)} MW` : "--",
        sub: "Latest aggregate output"
      },
      {
        title: "Average Wind Speed",
        value: metrics.data ? `${metrics.data.averageWindSpeedMS.toFixed(2)} m/s` : "--",
        sub: `Avg over ${range}`
      },
      {
        title: "Efficiency",
        value: metrics.data ? `${metrics.data.efficiencyPct.toFixed(1)}%` : "--",
        sub: "Proxy vs rated output"
      },
      {
        title: "Active Turbines",
        value: metrics.data ? `${metrics.data.activeTurbines}/${metrics.data.totalTurbines}` : "--",
        sub: "Online now"
      }
    ],
    [metrics.data, range]
  );

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map((c) => (
          <MetricCard key={c.title} title={c.title} value={c.value} sub={c.sub} loading={metrics.isLoading} />
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <PowerCurveChart
            title="Power Curve Analysis"
            range={range}
            loading={powerCurve.isLoading}
            scatter={powerCurve.data?.scatter ?? []}
            curve={powerCurve.data?.curve ?? []}
          />
        </div>
        <div className="xl:col-span-1">
          <TurbineHealthTable loading={turbineStatus.isLoading} rows={turbineStatus.data?.rows ?? []} />
        </div>
      </div>
    </div>
  );
}

