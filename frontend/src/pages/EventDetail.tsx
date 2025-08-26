import { useParams } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getEvent, listSessions, registerToEvent, type Session, type Event } from "../api/events";
import { useAuthStore } from "../store/authStore";
import { useState } from "react";

export default function EventDetail() {
  const { id = "" } = useParams();
  const qc = useQueryClient();
  const { token } = useAuthStore();
  const [msg, setMsg] = useState("");

  const eventQ = useQuery<Event>({ queryKey: ["event", id], queryFn: () => getEvent(id) });
  const sessionsQ = useQuery<Session[]>({ queryKey: ["sessions", id], queryFn: () => listSessions(id) });

  const regMutation = useMutation({
    mutationFn: (sessionId: number | null) => registerToEvent(id, sessionId ?? null),
    onSuccess: () => { setMsg("Registro exitoso ✅"); qc.invalidateQueries({ queryKey: ["myregs"] }); },
    onError: (err: any) => setMsg(err?.response?.data?.detail || "Error al registrarte"),
  });

  if (eventQ.isLoading) return <div className="container-page">Cargando…</div>;
  if (eventQ.error) return <div className="container-page text-red-600">Error al cargar el evento</div>;
  const evt = eventQ.data as Event;

  return (
    <div className="container-page space-y-4">
      <div className="card p-6">
        <h2 className="text-2xl font-semibold">{evt.name}</h2>
        {evt.description && <p className="mt-2 text-gray-700">{evt.description}</p>}
        <small className="text-gray-500">
          {evt.status} — {new Date(evt.start_at).toLocaleString()} — {evt.venue}
        </small>
      </div>

      <div className="card p-6 space-y-3">
        <h3 className="text-lg font-semibold">Sesiones</h3>
        {sessionsQ.isLoading ? (
          <p>Cargando sesiones…</p>
        ) : (
          <ul className="space-y-3">
            {sessionsQ.data?.map((s) => (
              <li key={s.id} className="border border-gray-200 rounded-lg p-3">
                <div className="font-medium">{s.title}</div>
                <div className="text-sm text-gray-600">
                  {new Date(s.start_at).toLocaleTimeString()}–{new Date(s.end_at).toLocaleTimeString()}
                  {s.room ? ` · ${s.room}` : ""}
                </div>
                {token && (
                  <button
                    className="btn btn-primary mt-2"
                    onClick={() => regMutation.mutate(s.id)}
                    disabled={regMutation.isPending}
                  >
                    {regMutation.isPending ? "Registrando..." : "Registrarme a esta sesión"}
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}

        {token && (
          <button
            className="btn btn-primary"
            onClick={() => regMutation.mutate(null)}
            disabled={regMutation.isPending}
          >
            {regMutation.isPending ? "Registrando..." : "Registrarme al evento completo"}
          </button>
        )}
        {msg && <div className="text-sm">{msg}</div>}
        {!token && <small className="text-gray-500">Inicia sesión para registrarte.</small>}
      </div>
    </div>
  );
}
