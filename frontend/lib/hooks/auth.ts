"use client";

import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";

export type Me = {
  username: string;
  role: "admin" | "engineer" | "viewer";
};

export function useMe() {
  return useQuery({
    queryKey: ["me"],
    queryFn: async () => {
      const res = await api.get<Me>("/api/auth/me");
      return res.data;
    },
    staleTime: 60_000
  });
}

