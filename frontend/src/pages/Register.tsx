import { useState } from "react";
import { registerUser } from "../api/auth";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("attendee");
  const [msg, setMsg] = useState("");

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMsg("");
    try {
      await registerUser({ email, password, role });
      setMsg("Usuario registrado. Ya puedes iniciar sesión.");
    } catch (err: any) {
      setMsg(err?.response?.data?.detail || "Error en registro");
    }
  }

  return (
    <div className="container-page">
      <form onSubmit={onSubmit} className="card p-6 max-w-md mx-auto grid gap-3">
        <h2 className="text-xl font-semibold">Registro</h2>
        <label className="label">Email</label>
        <input className="input" value={email} onChange={(e)=>setEmail(e.target.value)} />
        <label className="label">Password</label>
        <input className="input" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
        <label className="label">Rol</label>
        <select className="select" value={role} onChange={(e)=>setRole(e.target.value)}>
          <option value="attendee">Asistente</option>
          <option value="organizer">Organizador</option>
          <option value="admin">Admin</option>
        </select>
        <button className="btn btn-primary mt-2">Crear cuenta</button>
        {msg && <div className="text-sm">{msg}</div>}
      </form>
    </div>
  );
}
