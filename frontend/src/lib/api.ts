import axios, { type AxiosRequestConfig } from "axios";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// ── Request interceptor — attach access token ──────────────────────────────
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    try {
      const raw = localStorage.getItem("plux-auth");
      if (raw) {
        const { state } = JSON.parse(raw) as { state: { accessToken: string } };
        if (state?.accessToken) {
          config.headers.Authorization = `Bearer ${state.accessToken}`;
        }
      }
    } catch {
      // localStorage may be unavailable in SSR
    }
  }
  return config;
});

// ── Response interceptor — handle 401, refresh token ──────────────────────
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original: AxiosRequestConfig & { _retry?: boolean } = error.config;

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const raw = localStorage.getItem("plux-auth");
        if (raw) {
          const { state } = JSON.parse(raw) as {
            state: { refreshToken: string };
          };
          if (state?.refreshToken) {
            const { data } = await axios.post(`${BASE_URL}/auth/refresh/`, {
              refresh: state.refreshToken,
            });
            // Update store
            const { useAuthStore } = await import("@/store/auth");
            useAuthStore
              .getState()
              .setTokens(data.access, state.refreshToken);
            original.headers = {
              ...original.headers,
              Authorization: `Bearer ${data.access}`,
            };
            return api(original);
          }
        }
      } catch {
        // Refresh failed — logout
        const { useAuthStore } = await import("@/store/auth");
        useAuthStore.getState().logout();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);
