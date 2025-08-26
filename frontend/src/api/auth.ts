import api from "./client";

export type LoginResp = { access_token: string; token_type: string };

export async function login(params: { email: string; password: string }): Promise<LoginResp> {
  const form = new URLSearchParams();
  form.append("username", params.email);
  form.append("password", params.password);
  const { data } = await api.post<LoginResp>("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data;
}

export async function registerUser(params: { email: string; password: string; role: string }) {
  const { data } = await api.post("/auth/register", params);
  return data;
}
