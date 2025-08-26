import api from "./client";

export type Event = {
  id: number;
  organizer_id: number;
  name: string;
  description?: string;
  start_at: string;
  end_at: string;
  venue?: string;
  status: "draft" | "published" | "cancelled";
  capacity_total?: number | null;
};

export type Session = {
  id: number;
  event_id: number;
  title: string;
  description?: string | null;
  start_at: string;
  end_at: string;
  room?: string | null;
  capacity?: number | null;
  speaker_name?: string | null;
  speaker_bio?: string | null;
};

export type PageMeta = { page: number; page_size: number; total: number };
export type EventsPage = { items: Event[]; meta: PageMeta };

export type Registration = {
  id: number;
  user_id: number;
  event_id: number;
  session_id?: number | null;
  status: "pending" | "confirmed" | "cancelled";
  created_at: string;
};

export async function listEvents(params: {
  q?: string;
  page?: number;
  page_size?: number;
  status?: string;
}): Promise<EventsPage> {
  const { data } = await api.get<EventsPage>("/events", { params });
  return data;
}

export async function getEvent(id: string | number): Promise<Event> {
  const { data } = await api.get<Event>(`/events/${id}`);
  return data;
}

export async function listSessions(eventId: string | number): Promise<Session[]> {
  const { data } = await api.get<Session[]>(`/events/${eventId}/sessions`);
  return data;
}

export async function registerToEvent(eventId: string | number, sessionId?: number | null) {
  const body = sessionId ? { session_id: sessionId } : {};
  const { data } = await api.post<Registration>(`/events/${eventId}/register`, body);
  return data;
}

export async function myRegistrations(): Promise<Registration[]> {
  const { data } = await api.get<Registration[]>("/events/me/registrations");
  return data;
}
