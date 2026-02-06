"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  Map,
  Settings,
  Stethoscope,
  Wind,
  Wrench
} from "lucide-react";

import { cn } from "@/lib/cn";

const navItems = [
  { href: "/live-dashboard", label: "Live Dashboard", icon: Activity },
  { href: "/turbine-analysis", label: "Turbine Analysis", icon: Wind },
  { href: "/geospatial-view", label: "Geospatial View", icon: Map },
  { href: "/maintenance", label: "Maintenance", icon: Wrench },
  { href: "/configuration", label: "Configuration", icon: Settings }
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-72 shrink-0 border-r border-dashboard-border bg-dashboard-panel p-5 md:block">
      <div className="flex items-center gap-3 pb-6">
        <div className="grid h-10 w-10 place-items-center rounded-xl bg-dashboard-panel2 shadow-soft">
          <Stethoscope className="h-5 w-5 text-dashboard-accent" />
        </div>
        <div className="min-w-0">
          <div className="truncate text-sm font-semibold tracking-wide text-dashboard-text">
            Wind Farm Dashboard
          </div>
          <div className="truncate text-xs text-dashboard-muted">OpenOA analytics engine</div>
        </div>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => {
          const active = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition",
                active
                  ? "bg-dashboard-panel2 text-dashboard-text shadow-soft"
                  : "text-dashboard-muted hover:bg-dashboard-panel2 hover:text-dashboard-text"
              )}
            >
              <Icon className={cn("h-4 w-4", active ? "text-dashboard-accent" : "")} />
              <span className="truncate">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}

