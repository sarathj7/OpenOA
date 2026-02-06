"use client";

import { useMe } from "@/lib/hooks/auth";

export default function ConfigurationPage() {
  const me = useMe();
  const allowed = me.data?.role === "admin";

  return (
    <div className="rounded-2xl border border-dashboard-border bg-dashboard-panel p-6 shadow-soft">
      <div className="text-sm font-semibold">Configuration</div>
      <div className="mt-1 text-sm text-dashboard-muted">
        Admin-only settings (data source, thresholds, alert rules) will live here.
      </div>

      <div className="mt-6 rounded-xl border border-dashboard-border bg-dashboard-bg p-4 text-sm text-dashboard-muted">
        {me.isLoading
          ? "Loading user..."
          : allowed
            ? "You are an admin. Configuration features can be enabled here."
            : "You do not have access to configuration. Sign in as admin to view this section."}
      </div>
    </div>
  );
}

