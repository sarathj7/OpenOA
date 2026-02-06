"use client";

import dynamic from "next/dynamic";

const TurbineMap = dynamic(() => import("@/components/widgets/TurbineMap"), { ssr: false });

export default function GeospatialViewPage() {
  return <TurbineMap />;
}

