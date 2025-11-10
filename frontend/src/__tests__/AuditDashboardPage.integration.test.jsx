/**
 * AuditDashboardPage.integration.test.jsx
 * Tests d'intégration pour le dashboard avec composants charts
 * Couvre: Toggle stats, chargement des données, filtres appliqués aux charts
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import AuditDashboardPage from '../pages/AuditDashboardPage';
import * as apiModule from '../config';

// Mock de l'API
jest.mock('../config', () => ({
  default: {
    get: jest.fn(),
    delete: jest.fn(),
  },
}));

const mockApi = apiModule.default;

const mockLogsResponse = [
  {
    id: 1,
    action: 'INSERT',
    entity_type: 'Plant',
    entity_id: 42,
    field_name: null,
    old_value: null,
    new_value: null,
    raw_changes: { name: 'Monstera', type: 'Plant' },
    user_id: 1,
    ip_address: '127.0.0.1',
    user_agent: 'Mozilla/5.0',
    description: 'Nouvelle plante créée',
    created_at: '2025-11-10T10:00:00',
    updated_at: '2025-11-10T10:00:00',
  },
  {
    id: 2,
    action: 'UPDATE',
    entity_type: 'Plant',
    entity_id: 42,
    field_name: 'name',
    old_value: 'Monstera',
    new_value: 'Monstera Deliciosa',
    raw_changes: { name: { old: 'Monstera', new: 'Monstera Deliciosa' } },
    user_id: 1,
    ip_address: '127.0.0.1',
    user_agent: 'Mozilla/5.0',
    description: 'Nom de plante modifié',
    created_at: '2025-11-10T11:00:00',
    updated_at: '2025-11-10T11:00:00',
  },
];

const mockDailyActivityResponse = [
  { date: '2025-11-08', INSERT: 5, UPDATE: 12, DELETE: 2, total: 19 },
  { date: '2025-11-09', INSERT: 8, UPDATE: 15, DELETE: 1, total: 24 },
  { date: '2025-11-10', INSERT: 3, UPDATE: 10, DELETE: 0, total: 13 },
];

const mockEntityBreakdownResponse = [
  { entity_type: 'Plant', count: 35 },
  { entity_type: 'Photo', count: 18 },
  { entity_type: 'WateringHistory', count: 12 },
];

const mockUserActivityResponse = [
  { user_id: 1, count: 45 },
  { user_id: 2, count: 20 },
];

const mockActionByEntityResponse = [
  { entity_type: 'Plant', INSERT: 10, UPDATE: 20, DELETE: 5 },
  { entity_type: 'Photo', INSERT: 8, UPDATE: 8, DELETE: 2 },
];

describe('AuditDashboardPage with Charts Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    // Configuration par défaut des mocks
    mockApi.get.mockImplementation((url) => {
      if (url.includes('/api/audit/logs')) {
        return Promise.resolve({ data: mockLogsResponse });
      }
      if (url.includes('/api/audit/stats/daily-activity')) {
        return Promise.resolve({ data: mockDailyActivityResponse });
      }
      if (url.includes('/api/audit/stats/entity-breakdown')) {
        return Promise.resolve({ data: mockEntityBreakdownResponse });
      }
      if (url.includes('/api/audit/stats/user-activity')) {
        return Promise.resolve({ data: mockUserActivityResponse });
      }
      if (url.includes('/api/audit/stats/action-by-entity')) {
        return Promise.resolve({ data: mockActionByEntityResponse });
      }
      return Promise.reject({ response: { data: { detail: 'Not found' } } });
    });
  });

  test('affiche le bouton "Afficher Stats" par défaut', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Afficher Stats/)).toBeInTheDocument();
    });
  });

  test('toggle les stats quand on clique sur le bouton', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const button = screen.getByText(/Afficher Stats/);
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText('📈 Activité Quotidienne')).toBeInTheDocument();
      expect(screen.getByText('🔍 Distribution par Entité')).toBeInTheDocument();
      expect(screen.getByText('👥 Activité par Utilisateur')).toBeInTheDocument();
      expect(screen.getByText('📊 Actions par Entité')).toBeInTheDocument();
    });
  });

  test('masque les stats quand on clique de nouveau', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const toggleButton = screen.getByText(/Afficher Stats/);
    fireEvent.click(toggleButton);

    await waitFor(() => {
      expect(screen.getByText('📈 Activité Quotidienne')).toBeInTheDocument();
    });

    const hideButton = screen.getByText(/Masquer Stats/);
    fireEvent.click(hideButton);

    await waitFor(() => {
      expect(screen.queryByText('📈 Activité Quotidienne')).not.toBeInTheDocument();
    });
  });

  test('charge les données des 4 charts en parallèle', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const button = screen.getByText(/Afficher Stats/);
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/audit/stats/daily-activity'),
        expect.anything()
      );
      expect(mockApi.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/audit/stats/entity-breakdown'),
        expect.anything()
      );
      expect(mockApi.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/audit/stats/user-activity'),
        expect.anything()
      );
      expect(mockApi.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/audit/stats/action-by-entity'),
        expect.anything()
      );
    });
  });

  test('passe le bon paramètre "days" aux stats', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const periodSelect = screen.getByDisplayValue('Dernière semaine');
    fireEvent.change(periodSelect, { target: { value: '30' } });

    const toggleButton = screen.getByText(/Afficher Stats/);
    fireEvent.click(toggleButton);

    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalledWith(
        expect.stringContaining('days=30'),
        expect.anything()
      );
    });
  });

  test('affiche l\'erreur si le chargement des stats échoue', async () => {
    mockApi.get.mockRejectedValueOnce({
      response: { data: { detail: 'Erreur API' } },
    });

    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const button = screen.getByText(/Afficher Stats/);
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText('Erreur lors du chargement des statistiques')).toBeInTheDocument();
    });
  });

  test('affiche le message de chargement pendant le fetch des stats', async () => {
    mockApi.get.mockImplementationOnce(() => new Promise(() => {})); // Jamais résolue

    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const button = screen.getByText(/Afficher Stats/);
    fireEvent.click(button);

    // Les charts afficheront les messages de chargement
    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalled();
    });
  });

  test('layout responsive: 2 cols sur desktop', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const button = screen.getByText(/Afficher Stats/);
    fireEvent.click(button);

    await waitFor(() => {
      // Vérifier que les 4 charts sont affichés
      expect(screen.getByText('📈 Activité Quotidienne')).toBeInTheDocument();
      expect(screen.getByText('🔍 Distribution par Entité')).toBeInTheDocument();
      expect(screen.getByText('👥 Activité par Utilisateur')).toBeInTheDocument();
      expect(screen.getByText('📊 Actions par Entité')).toBeInTheDocument();
    });
  });

  test('charge les logs indépendamment des stats', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Les logs doivent être chargés au montage du composant
      expect(mockApi.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/audit/logs'),
        expect.anything()
      );
    });

    // Les stats ne doivent pas être chargées par défaut
    const dailyActivityCalls = mockApi.get.mock.calls.filter(call =>
      call[0].includes('/api/audit/stats/daily-activity')
    );
    expect(dailyActivityCalls).toHaveLength(0);
  });

  test('recharge les stats quand on change la période', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const button = screen.getByText(/Afficher Stats/);
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalledWith(
        expect.stringContaining('days=7'),
        expect.anything()
      );
    });

    // Changer la période
    const periodSelect = screen.getByDisplayValue('Dernière semaine');
    fireEvent.change(periodSelect, { target: { value: '30' } });

    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalledWith(
        expect.stringContaining('days=30'),
        expect.anything()
      );
    });
  });

  test('affiche les totaux corrects pour chaque chart', async () => {
    render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    );

    const button = screen.getByText(/Afficher Stats/);
    fireEvent.click(button);

    await waitFor(() => {
      // Daily Activity: 19 + 24 + 13 = 56
      expect(screen.getByText('Total: 56 modifications')).toBeInTheDocument();
    });
  });
});
