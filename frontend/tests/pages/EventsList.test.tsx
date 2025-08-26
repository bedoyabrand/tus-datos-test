import EventsList from '../../src/pages/EventsList';
import { renderWithProviders } from '../utils/renderWithProviders';
import { screen, waitFor } from '@testing-library/react';

test('lista eventos desde la API', async () => {
  renderWithProviders(<EventsList />);
  await waitFor(() => {
    expect(screen.getByText(/TechConf 2025/i)).toBeInTheDocument();
  });
});
