import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        dashboard: {
          bg: "#020617",
          panel: "#0b1220",
          panel2: "#0f172a",
          border: "rgba(148,163,184,0.15)",
          text: "#e2e8f0",
          muted: "#94a3b8",
          accent: "#22c55e"
        }
      },
      boxShadow: {
        soft: "0 10px 30px rgba(0,0,0,0.35)"
      }
    }
  },
  plugins: []
} satisfies Config;

