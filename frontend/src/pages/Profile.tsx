import { useQuery } from "@tanstack/react-query";
import { myRegistrations, type Registration } from "../api/events";

export default function Profile() {
  const { data, isLoading } = useQuery<Registration[]>({
    queryKey: ["myregs"],
    queryFn: myRegistrations,
  });

  return (
    <div className="container-page">
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-3">Mis registros</h2>
        {isLoading && <p>Cargando…</p>}
        <ul className="space-y-2">
          {data?.map((r) => (
            <li key={r.id} className="flex items-center justify-between border-b border-gray-100 pb-2">
              <span>
                #{r.id} — Evento {r.event_id} {r.session_id ? `(sesión ${r.session_id})` : ""} — {r.status}
              </span>
              <a className="text-indigo-600 hover:underline" href={`/events/${r.event_id}`}>ver</a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
