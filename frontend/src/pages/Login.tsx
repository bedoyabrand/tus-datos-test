import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";
import { useAuthStore } from "../store/authStore";

export default function Login() {
  const [email, setEmail] = useState("user@mail.com");
  const [password, setPassword] = useState("secret123");
  const [error, setError] = useState("");
  const nav = useNavigate();
  const { login: setAuth } = useAuthStore();

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      const data = await login({ email, password });
      setAuth({ access_token: data.access_token, email });
      nav("/");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Error de login");
    }
  }

  return (
    <div className="container-page">
      <form onSubmit={onSubmit} className="card p-6 max-w-md mx-auto grid gap-3">
        <h2 className="text-xl font-semibold">Login</h2>
        <label className="label">Email</label>
        <input className="input" value={email} onChange={(e)=>setEmail(e.target.value)} />
        <label className="label">Password</label>
        <input className="input" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
        <button type="submit" className="btn btn-primary mt-2">Entrar</button>
        {error && <div className="text-red-600 text-sm">{error}</div>}
      </form>
    </div>
  );
}
