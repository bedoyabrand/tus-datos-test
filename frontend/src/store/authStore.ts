import { create } from "zustand";

type AuthState = {
  token: string;
  email: string;
  role: string;
  login: (p: { access_token: string; email: string; role?: string }) => void;
  logout: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem("token") || "",
  email: localStorage.getItem("email") || "",
  role: localStorage.getItem("role") || "",
  login: ({ access_token, email, role }) => {
    localStorage.setItem("token", access_token);
    localStorage.setItem("email", email);
    localStorage.setItem("role", role ?? "");
    set({ token: access_token, email, role: role ?? "" });
  },
  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    localStorage.removeItem("role");
    set({ token: "", email: "", role: "" });
  },
}));
