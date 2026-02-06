"use client";

import {
  CartesianGrid,
  Legend,
  Line,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

type Point = { windSpeed: number; powerKW: number };

export function PowerCurveChart({
  title,
  range,
  loading,
  scatter,
  curve
}: {
  title: string;
  range: string;
  loading?: boolean;
  scatter: Point[];
  curve: Point[];
}) {
  return (
    <div className="rounded-2xl border border-dashboard-border bg-dashboard-panel p-5 shadow-soft">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm font-semibold">{title}</div>
          <div className="text-xs text-dashboard-muted">SCADA scatter with IEC theoretical overlay ({range})</div>
        </div>
      </div>

      <div className="mt-4 h-[360px]">
        {loading ? (
          <div className="grid h-full place-items-center text-sm text-dashboard-muted">Loading chart...</div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 0 }}>
              <CartesianGrid stroke="rgba(148,163,184,0.15)" strokeDasharray="4 4" />
              <XAxis
                type="number"
                dataKey="windSpeed"
                unit=" m/s"
                tick={{ fill: "rgba(226,232,240,0.8)", fontSize: 12 }}
                axisLine={{ stroke: "rgba(148,163,184,0.2)" }}
                tickLine={{ stroke: "rgba(148,163,184,0.2)" }}
              />
              <YAxis
                type="number"
                dataKey="powerKW"
                unit=" kW"
                tick={{ fill: "rgba(226,232,240,0.8)", fontSize: 12 }}
                axisLine={{ stroke: "rgba(148,163,184,0.2)" }}
                tickLine={{ stroke: "rgba(148,163,184,0.2)" }}
              />
              <Tooltip
                contentStyle={{
                  background: "rgba(2,6,23,0.9)",
                  border: "1px solid rgba(148,163,184,0.2)",
                  borderRadius: 12
                }}
                labelStyle={{ color: "rgba(226,232,240,0.8)" }}
              />
              <Legend />

              <Scatter name="SCADA (Actual)" data={scatter} fill="rgba(34,197,94,0.65)" />
              <Line
                name="Power Curve (IEC)"
                type="monotone"
                dataKey="powerKW"
                data={curve}
                dot={false}
                stroke="rgba(56,189,248,0.9)"
                strokeWidth={2}
              />
            </ScatterChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

