import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Wind Farm Performance Dashboard",
  description: "OpenOA-powered wind farm analytics dashboard"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">{children}</body>
    </html>
  );
}

