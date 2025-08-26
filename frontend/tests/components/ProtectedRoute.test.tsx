import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from '../../src/components/ProtectedRoute';
import { render } from '@testing-library/react';

function Page() { return <div>Privado</div>; }
function Login() { return <div>Login</div>; }

test('redirige a /login cuando no hay token', () => {
  const { getByText } = render(
    <MemoryRouter initialEntries={['/priv']}>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/priv" element={<Page />} />
        </Route>
      </Routes>
    </MemoryRouter>
  );
  expect(getByText(/login/i)).toBeInTheDocument();
});
