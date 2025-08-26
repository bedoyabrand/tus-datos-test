import EventCreate from '../../src/pages/EventCreate';
import { renderWithProviders } from '../utils/renderWithProviders';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('envía formulario con token y crea evento', async () => {
  renderWithProviders(<EventCreate />, { token: 'AAA' });
  await userEvent.type(screen.getByLabelText(/nombre/i), 'Mi evento');
  await userEvent.type(screen.getByLabelText(/fecha/i), '2025-12-01T09:00');
  await userEvent.click(screen.getByRole('button', { name: /crear/i }));

  await waitFor(() => {
    expect(screen.getByText(/creado|éxito/i)).toBeInTheDocument(); // ajusta al mensaje real
  });
});
