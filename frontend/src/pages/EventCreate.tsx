import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { createEvent, type Event } from "../api/events";
import { useNavigate } from "react-router-dom";

export default function EventCreate() {
  const [form, setForm] = useState({
    name: "",
    description: "",
    start_at: "",
    end_at: "",
    venue: "",
    capacity_total: 100,
  });
  const [msg, setMsg] = useState("");
  const nav = useNavigate();

  const createMut = useMutation({
    mutationFn: () => createEvent({
      ...form,
      capacity_total: Number(form.capacity_total) || null,
    }),
    onSuccess: async (evt: Event) => {
      setMsg("Evento creado ✅");
      // Opcional: publicar inmediatamente
      // await publishEvent(evt.id);
      nav(`/events/${evt.id}`);
    },
    onError: (err: any) => setMsg(err?.response?.data?.detail || "Error al crear el evento"),
  });

  function onChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const { name, value } = e.target;
    setForm((s) => ({ ...s, [name]: value }));
  }

  return (
    <div className="container-page">
      <div className="card p-6 max-w-2xl mx-auto grid gap-3">
        <h2 className="text-xl font-semibold">Crear evento</h2>

        <label className="label">Nombre</label>
        <input className="input" name="name" value={form.name} onChange={onChange} />

        <label className="label">Descripción</label>
        <textarea className="input" name="description" value={form.description} onChange={onChange} />

        <label className="label">Inicio (ISO)</label>
        <input className="input" name="start_at" placeholder="2025-12-01T09:00:00Z" value={form.start_at} onChange={onChange} />

        <label className="label">Fin (ISO)</label>
        <input className="input" name="end_at" placeholder="2025-12-01T18:00:00Z" value={form.end_at} onChange={onChange} />

        <label className="label">Lugar</label>
        <input className="input" name="venue" value={form.venue} onChange={onChange} />

        <label className="label">Capacidad total</label>
        <input className="input" name="capacity_total" type="number" value={form.capacity_total} onChange={onChange} />

        <button
          className="btn btn-primary mt-2"
          onClick={() => createMut.mutate()}
          disabled={createMut.isPending}
        >
          {createMut.isPending ? "Creando..." : "Crear evento"}
        </button>

        {msg && <div className="text-sm">{msg}</div>}
        <small className="text-gray-500">* El evento se crea como <b>draft</b>. Desde el detalle podrás publicarlo.</small>
      </div>
    </div>
  );
}
