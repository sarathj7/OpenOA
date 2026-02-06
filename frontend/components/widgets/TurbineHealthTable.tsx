"use client";

import { MoreHorizontal } from "lucide-react";

type Row = {
  turbineId: string;
  status: "online" | "warning" | "maintenance";
  generationKW: number;
  temperatureC: number | null;
  lastUpdate: string;
};

function badgeClass(status: Row["status"]) {
  switch (status) {
    case "online":
      return "bg-emerald-500/15 text-emerald-300 border-emerald-500/30";
    case "warning":
      return "bg-amber-500/15 text-amber-300 border-amber-500/30";
    case "maintenance":
      return "bg-rose-500/15 text-rose-300 border-rose-500/30";
  }
}

export function TurbineHealthTable({ rows, loading }: { rows: Row[]; loading?: boolean }) {
  return (
    <div className="rounded-2xl border border-dashboard-border bg-dashboard-panel p-5 shadow-soft">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm font-semibold">Turbine Health</div>
          <div className="text-xs text-dashboard-muted">Latest status snapshot</div>
        </div>
      </div>

      <div className="mt-4 overflow-hidden rounded-xl border border-dashboard-border">
        <table className="w-full text-left text-sm">
          <thead className="bg-dashboard-panel2 text-xs text-dashboard-muted">
            <tr>
              <th className="px-3 py-2">Turbine ID</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">Generation</th>
              <th className="px-3 py-2">Temp</th>
              <th className="px-3 py-2"></th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td className="px-3 py-6 text-center text-sm text-dashboard-muted" colSpan={5}>
                  Loading turbines...
                </td>
              </tr>
            ) : rows.length === 0 ? (
              <tr>
                <td className="px-3 py-6 text-center text-sm text-dashboard-muted" colSpan={5}>
                  No data
                </td>
              </tr>
            ) : (
              rows.slice(0, 8).map((r) => (
                <tr key={r.turbineId} className="border-t border-dashboard-border">
                  <td className="px-3 py-3 font-medium">{r.turbineId}</td>
                  <td className="px-3 py-3">
                    <span className={`inline-flex rounded-full border px-2 py-0.5 text-xs ${badgeClass(r.status)}`}>
                      {r.status}
                    </span>
                  </td>
                  <td className="px-3 py-3 text-dashboard-muted">{r.generationKW.toFixed(0)} kW</td>
                  <td className="px-3 py-3 text-dashboard-muted">
                    {r.temperatureC == null ? "--" : `${r.temperatureC.toFixed(1)} °C`}
                  </td>
                  <td className="px-3 py-3 text-right">
                    <button className="rounded-lg p-2 text-dashboard-muted hover:bg-dashboard-panel2 hover:text-dashboard-text">
                      <MoreHorizontal className="h-4 w-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

