import { useState } from "react";
import { useQuery, keepPreviousData } from "@tanstack/react-query";
import { listEvents, type EventsPage } from "../api/events";
import { Link } from "react-router-dom";
import Pagination from "../components/Pagination";

export default function EventsList() {
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);

  const { data, isLoading, error, refetch } = useQuery<EventsPage>({
    queryKey: ["events", q, page],
    queryFn: () => listEvents({ q, page, page_size: 10 }),
    placeholderData: keepPreviousData,
  });

  return (
    <div className="container-page">
      <h2 className="text-2xl font-semibold mb-4">Eventos</h2>

      <div className="flex gap-2 mb-4">
        <input
          className="input w-full max-w-md"
          placeholder="Buscar por nombre..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <button
          className="btn btn-primary"
          onClick={() => { setPage(1); refetch(); }}
        >
          Buscar
        </button>
      </div>

      {isLoading && <p>Cargando…</p>}
      {error && <p className="text-red-600">Error al cargar</p>}

      <ul className="space-y-3">
        {data?.items?.map((evt) => (
          <li key={evt.id} className="card p-4">
            <Link to={`/events/${evt.id}`} className="text-indigo-700 font-medium hover:underline">
              {evt.name}
            </Link>
            {evt.description && <div className="text-sm text-gray-700 mt-1">{evt.description}</div>}
            <small className="text-gray-500">
              {evt.status} — {new Date(evt.start_at).toLocaleString()}
            </small>
          </li>
        ))}
      </ul>

      <Pagination meta={data?.meta} onPage={setPage} />
    </div>
  );
}
