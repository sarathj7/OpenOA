"use client";

import { QueryClientProvider } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { makeQueryClient } from "@/lib/query-client";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopBar } from "@/components/layout/TopBar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => makeQueryClient());
  const router = useRouter();

  // Simple client-side auth gate (backend enforces auth per-route)
  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) router.replace("/login");
  }, [router]);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="flex min-w-0 flex-1 flex-col">
          <TopBar />
          <main className="flex-1 p-6">{children}</main>
        </div>
      </div>
    </QueryClientProvider>
  );
}

