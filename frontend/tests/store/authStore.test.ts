import { useAuthStore } from '../../src/store/authStore';

beforeEach(() => localStorage.clear());

test('login guarda estado y localStorage', () => {
  const { login } = useAuthStore.getState();
  login({ access_token: 'AAA', email: 'u@mail.com', role: 'admin' });
  const { token, email, role } = useAuthStore.getState();
  expect(token).toBe('AAA');
  expect(email).toBe('u@mail.com');
  expect(role).toBe('admin');
  expect(localStorage.getItem('token')).toBe('AAA');
});

test('logout limpia todo', () => {
  const { login, logout } = useAuthStore.getState();
  login({ access_token: 'AAA', email: 'u@mail.com', role: 'admin' });
  logout();
  const s = useAuthStore.getState();
  expect(s.token).toBe('');
  expect(s.email).toBe('');
  expect(s.role).toBe('');
  expect(localStorage.getItem('token')).toBeNull();
});
