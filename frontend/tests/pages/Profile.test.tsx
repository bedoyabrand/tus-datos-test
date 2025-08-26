import Profile from '../../src/pages/Profile';
import { renderWithProviders } from '../utils/renderWithProviders';
import { screen, waitFor } from '@testing-library/react';

test('renderiza registros y link "ver"', async () => {
  renderWithProviders(<Profile />, { token: 'AAA' });
  await waitFor(() => {
    expect(screen.getByText(/#1 — Evento 101/i)).toBeInTheDocument();
  });
  expect(screen.getByRole('link', { name: /ver/i })).toHaveAttribute('href', '/events/101');
});
