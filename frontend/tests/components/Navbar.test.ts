import Navbar from '../../src/components/Navbar';
import { renderWithProviders } from '../utils/renderWithProviders';
import { screen } from '@testing-library/react';

test('muestra "Crear evento" si hay token', () => {
  renderWithProviders(<Navbar />, { token: 'AAA' });
  expect(screen.getByText(/Crear evento/i)).toBeInTheDocument();
});

test('no muestra "Crear evento" si no hay token', () => {
  renderWithProviders(<Navbar />);
  expect(screen.queryByText(/Crear evento/i)).not.toBeInTheDocument();
});
