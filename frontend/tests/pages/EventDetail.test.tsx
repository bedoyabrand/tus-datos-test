import EventDetail from '../../src/pages/EventDetail';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { renderWithProviders } from '../utils/renderWithProviders';
import { screen, waitFor } from '@testing-library/react';

test('renderiza el nombre del evento', async () => {
  renderWithProviders(
    <MemoryRouter initialEntries={['/events/101']}>
      <Routes><Route path="/events/:id" element={<EventDetail />} /></Routes>
    </MemoryRouter>
  );
  await waitFor(() => {
    expect(screen.getByText(/TechConf 2025/i)).toBeInTheDocument();
  });
});
