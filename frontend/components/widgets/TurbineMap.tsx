"use client";

import "leaflet/dist/leaflet.css";

import { Icon } from "leaflet";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

type Turbine = {
  turbineId: string;
  lat: number;
  lon: number;
  status: "online" | "warning" | "maintenance";
  currentPowerKW: number;
};

type TurbineMapResponse = { turbines: Turbine[] };

const markerIcon = new Icon({
  iconUrl:
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2322c55e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 2c3.3 0 6 2.7 6 6 0 4.5-6 14-6 14S6 12.5 6 8c0-3.3 2.7-6 6-6Z'/%3E%3Cpath d='M12 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z'/%3E%3C/svg%3E",
  iconSize: [24, 24],
  iconAnchor: [12, 22],
  popupAnchor: [0, -18]
});

export default function TurbineMap() {
  const q = useQuery({
    queryKey: ["turbineMap"],
    queryFn: async () => {
      const res = await api.get<TurbineMapResponse>("/api/geospatial/turbines");
      return res.data;
    },
    refetchInterval: 60_000
  });

  const turbines = q.data?.turbines ?? [];
  const center: [number, number] = turbines.length
    ? [turbines.reduce((a, t) => a + t.lat, 0) / turbines.length, turbines.reduce((a, t) => a + t.lon, 0) / turbines.length]
    : [48.4497, 5.5896];

  return (
    <div className="rounded-2xl border border-dashboard-border bg-dashboard-panel p-5 shadow-soft">
      <div className="text-sm font-semibold">Geospatial View</div>
      <div className="mt-1 text-xs text-dashboard-muted">Turbine locations and live status</div>

      <div className="mt-4 h-[520px] overflow-hidden rounded-2xl border border-dashboard-border">
        <MapContainer center={center} zoom={13} style={{ height: "100%", width: "100%" }}>
          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {turbines.map((t) => (
            <Marker key={t.turbineId} position={[t.lat, t.lon]} icon={markerIcon}>
              <Popup>
                <div className="text-sm font-semibold">{t.turbineId}</div>
                <div className="text-xs">Status: {t.status}</div>
                <div className="text-xs">Power: {t.currentPowerKW.toFixed(0)} kW</div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}

