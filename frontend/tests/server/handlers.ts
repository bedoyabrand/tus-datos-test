import { http, HttpResponse } from 'msw';

const API = 'http://localhost:8000';

export const handlers = [
  http.get(`${API}/events`, () =>
    HttpResponse.json({
      items: [{ id: 101, name: 'TechConf 2025' }],
      page: 1, pages: 1
    })
  ),
  http.get(`${API}/events/:id`, ({ params }) =>
    HttpResponse.json({ id: Number(params.id), name: 'TechConf 2025' })
  ),
  http.get(`${API}/me/registrations`, () =>
    HttpResponse.json([{ id: 1, event_id: 101, session_id: null, status: 'confirmed' }])
  ),
  http.post(`${API}/auth/login`, async () =>
    HttpResponse.json({ access_token: 'AAA.BBB', email: 'user@mail.com' })
  ),
  http.post(`${API}/events`, async ({ request }) => {
    const auth = (request.headers as any).get('authorization');
    if (!auth) return new HttpResponse('Unauthorized', { status: 401 });
    return HttpResponse.json({ id: 999, name: 'Nuevo' }, { status: 201 });
  }),
];
