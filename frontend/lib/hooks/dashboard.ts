"use client";

import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";

export type RangeKey = "24h" | "7d" | "30d";

export type MetricsSummary = {
  timestamp: string;
  powerOutputMW: number;
  averageWindSpeedMS: number;
  efficiencyPct: number;
  activeTurbines: number;
  totalTurbines: number;
};

export type PowerCurveResponse = {
  scatter: { windSpeed: number; powerKW: number }[];
  curve: { windSpeed: number; powerKW: number }[];
};

export type TurbineStatusResponse = {
  rows: {
    turbineId: string;
    status: "online" | "warning" | "maintenance";
    generationKW: number;
    temperatureC: number | null;
    lastUpdate: string;
  }[];
  total: number;
};

export function useMetricsSummary(range: RangeKey) {
  return useQuery({
    queryKey: ["metricsSummary", range],
    queryFn: async () => {
      const res = await api.get<MetricsSummary>("/api/metrics/summary", { params: { range } });
      return res.data;
    },
    refetchInterval: 30_000
  });
}

export function usePowerCurve(range: RangeKey) {
  return useQuery({
    queryKey: ["powerCurve", range],
    queryFn: async () => {
      const res = await api.get<PowerCurveResponse>("/api/analysis/power-curve", { params: { range } });
      return res.data;
    },
    refetchInterval: 60_000
  });
}

export function useTurbineStatus() {
  return useQuery({
    queryKey: ["turbineStatus"],
    queryFn: async () => {
      const res = await api.get<TurbineStatusResponse>("/api/turbines/status", { params: { limit: 50, offset: 0 } });
      return res.data;
    },
    refetchInterval: 30_000
  });
}

