import Login from '../../src/pages/Login';
import { renderWithProviders } from '../utils/renderWithProviders';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('guarda token y email al loguear', async () => {
  renderWithProviders(<Login />);
  await userEvent.type(screen.getByLabelText(/email/i), 'user@mail.com');
  await userEvent.type(screen.getByLabelText(/contraseña|password/i), '123456');
  await userEvent.click(screen.getByRole('button', { name: /ingresar|login/i }));

  await waitFor(() => {
    expect(localStorage.getItem('token')).toBeTruthy();
    expect(localStorage.getItem('email')).toBe('user@mail.com');
  });
});
