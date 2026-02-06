"use client";

import { useEffect, useState } from "react";
import { CalendarDays, User } from "lucide-react";

import { cn } from "@/lib/cn";
import { useMe } from "@/lib/hooks/auth";

const ranges = [
  { key: "24h", label: "24h" },
  { key: "7d", label: "7 days" },
  { key: "30d", label: "30 days" }
] as const;

export type TimeRangeKey = (typeof ranges)[number]["key"];

export function TopBar() {
  const [range, setRange] = useState<TimeRangeKey>("24h");
  const me = useMe();

  useEffect(() => {
    window.dispatchEvent(new CustomEvent("dashboard:range", { detail: range }));
  }, [range]);

  return (
    <header className="sticky top-0 z-20 border-b border-dashboard-border bg-dashboard-bg/80 backdrop-blur">
      <div className="flex items-center justify-between gap-4 px-6 py-4">
        <div className="min-w-0">
          <div className="truncate text-sm font-semibold">Live Dashboard</div>
          <div className="truncate text-xs text-dashboard-muted">
            Real-time performance, diagnostics, and insights
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden items-center gap-2 rounded-xl border border-dashboard-border bg-dashboard-panel px-2 py-1 md:flex">
            <CalendarDays className="h-4 w-4 text-dashboard-muted" />
            {ranges.map((r) => (
              <button
                key={r.key}
                onClick={() => setRange(r.key)}
                className={cn(
                  "rounded-lg px-2 py-1 text-xs transition",
                  range === r.key
                    ? "bg-dashboard-panel2 text-dashboard-text"
                    : "text-dashboard-muted hover:text-dashboard-text"
                )}
              >
                {r.label}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2 rounded-xl border border-dashboard-border bg-dashboard-panel px-3 py-2">
            <User className="h-4 w-4 text-dashboard-muted" />
            <span className="text-xs text-dashboard-muted">
              {me.data ? `${me.data.username} (${me.data.role})` : "Role-based access"}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}

