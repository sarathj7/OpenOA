"use client";

export function MetricCard({
  title,
  value,
  sub,
  loading
}: {
  title: string;
  value: string;
  sub: string;
  loading?: boolean;
}) {
  return (
    <div className="rounded-2xl border border-dashboard-border bg-dashboard-panel p-5 shadow-soft">
      <div className="text-xs font-medium text-dashboard-muted">{title}</div>
      <div className="mt-2 text-2xl font-semibold tracking-tight">{loading ? "Loading..." : value}</div>
      <div className="mt-2 text-xs text-dashboard-muted">{sub}</div>
    </div>
  );
}

