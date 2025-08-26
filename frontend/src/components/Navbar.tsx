import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export default function Navbar() {
  const { token, email, logout } = useAuthStore();
  const nav = useNavigate();

  return (
    <header className="bg-white border-b border-gray-200">
      <nav className="container-page flex items-center gap-4">
        <Link to="/" className="text-lg font-semibold text-indigo-700">Mis Eventos</Link>
        <Link to="/" className="btn btn-ghost">Eventos</Link>
        {token && <Link to="/me" className="btn btn-ghost">Mis registros</Link>}
        <div className="ml-auto" />
        {!token ? (
          <>
            <Link to="/login" className="btn btn-ghost">Login</Link>
            <Link to="/register" className="btn btn-primary">Registro</Link>
          </>
        ) : (
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-600">{email}</span>
            <button
              className="btn btn-ghost"
              onClick={() => { logout(); nav("/"); }}
            >
              Salir
            </button>
          </div>
        )}
      </nav>
    </header>
  );
}
