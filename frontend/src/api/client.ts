import axios from "axios";
import { useAuthStore } from "../store/authStore";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  withCredentials: false,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token || localStorage.getItem("token");
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  r => r,
  err => {
    const status = err.response?.status;
    const url = err.config?.url ?? "";
    if (status === 401 && url.includes("/auth/me")) {
      // aquí sí puedes desloguear
      const { logout } = useAuthStore.getState();
      logout();
    }
    return Promise.reject(err);
  }
);

export default api;
