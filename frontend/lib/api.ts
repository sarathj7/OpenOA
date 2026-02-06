import axios from "axios";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL;

export const api = axios.create({
  baseURL: apiBaseUrl,
  timeout: 30_000,
  headers: {
    "Content-Type": "application/json"
  }
});

api.interceptors.request.use((config) => {
  if (typeof window === "undefined") return config;
  const token = localStorage.getItem("accessToken");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear invalid token
      if (typeof window !== "undefined") {
        localStorage.removeItem("accessToken");
      }
    }
    return Promise.reject(error);
  }
);

