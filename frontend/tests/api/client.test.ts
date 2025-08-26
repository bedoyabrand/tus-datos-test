import { api } from '../../src/api/client';
import { server } from '../server/server';
import { http, HttpResponse } from 'msw';

test('envía Authorization: Bearer <token>', async () => {
  localStorage.setItem('token', 'AAA.BBB');
  let captured: string | null = null;

  server.use(
    http.get('http://localhost:8000/me/registrations', ({ request }) => {
      captured = request.headers.get('authorization');
      return HttpResponse.json([]);
    })
  );

  await api.get('/me/registrations');
  expect(captured).toBe('Bearer AAA.BBB');
});
