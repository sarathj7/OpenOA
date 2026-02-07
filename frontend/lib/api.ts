import axios from "axios";

// Ensure the API URL is correctly set at build time
const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL;

if (!apiBaseUrl) {
  throw new Error(
    "NEXT_PUBLIC_API_URL environment variable is not defined. " +
    "Frontend cannot connect to backend."
  );
}

export const api = axios.create({
  baseURL: apiBaseUrl,   // <-- THIS ENSURES REQUESTS GO TO BACKEND
  timeout: 30000,
  headers: {
    "Content-Type": "application/json"
  }
});

// Attach JWT token if present
api.interceptors.request.use((config) => {
  if (typeof window === "undefined") return config;

  const token = localStorage.getItem("accessToken");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Handle auth failures globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("accessToken");
      }
    }
    return Promise.reject(error);
  }
);
