"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { api } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("viewer");
  const [password, setPassword] = useState("viewer123");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await api.post("/api/auth/login", { username, password });
      localStorage.setItem("accessToken", res.data.accessToken);
      router.push("/live-dashboard");
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid min-h-screen place-items-center p-6">
      <div className="w-full max-w-md rounded-2xl border border-dashboard-border bg-dashboard-panel p-6 shadow-soft">
        <div className="text-lg font-semibold">Sign in</div>
        <div className="mt-1 text-sm text-dashboard-muted">
          Demo users: <span className="font-mono">admin/admin123</span>,{" "}
          <span className="font-mono">engineer/engineer123</span>,{" "}
          <span className="font-mono">viewer/viewer123</span>
        </div>

        <form onSubmit={onSubmit} className="mt-6 space-y-4">
          <div>
            <label className="text-xs text-dashboard-muted">Username</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 w-full rounded-xl border border-dashboard-border bg-dashboard-bg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-dashboard-accent/40"
            />
          </div>
          <div>
            <label className="text-xs text-dashboard-muted">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full rounded-xl border border-dashboard-border bg-dashboard-bg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-dashboard-accent/40"
            />
          </div>

          {error ? <div className="text-sm text-rose-300">{error}</div> : null}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-dashboard-accent px-4 py-2 text-sm font-semibold text-slate-950 transition hover:opacity-90 disabled:opacity-60"
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}

