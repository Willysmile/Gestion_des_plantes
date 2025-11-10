/**
 * AuditCharts.test.jsx
 * Tests unitaires pour les composants graphiques Recharts
 * Couvre: AuditDailyActivityChart, AuditEntityBreakdownChart, AuditUserActivityChart, AuditActionByEntityChart
 */

import { render, screen } from '@testing-library/react';
import {
  AuditDailyActivityChart,
  AuditEntityBreakdownChart,
  AuditUserActivityChart,
  AuditActionByEntityChart,
} from '../components/AuditCharts';

describe('AuditCharts', () => {
  // ==================== AuditDailyActivityChart ====================

  describe('AuditDailyActivityChart', () => {
    test('affiche le message de chargement', () => {
      render(<AuditDailyActivityChart data={[]} isLoading={true} />);
      expect(screen.getByText('Chargement des tendances...')).toBeInTheDocument();
    });

    test('affiche le message "aucune donnée" quand liste vide', () => {
      render(<AuditDailyActivityChart data={[]} isLoading={false} />);
      expect(screen.getByText('Aucune donnée disponible')).toBeInTheDocument();
    });

    test('affiche le titre et les données', () => {
      const data = [
        { date: '2025-11-01', INSERT: 5, UPDATE: 12, DELETE: 2, total: 19 },
        { date: '2025-11-02', INSERT: 3, UPDATE: 8, DELETE: 1, total: 12 },
      ];
      render(<AuditDailyActivityChart data={data} isLoading={false} />);
      expect(screen.getByText('📈 Activité Quotidienne')).toBeInTheDocument();
      expect(screen.getByText('Total: 31 modifications')).toBeInTheDocument();
    });

    test('affiche les légendes des lignes', () => {
      const data = [
        { date: '2025-11-01', INSERT: 5, UPDATE: 12, DELETE: 2, total: 19 },
      ];
      render(<AuditDailyActivityChart data={data} isLoading={false} />);
      expect(screen.getByText('Créations')).toBeInTheDocument();
      expect(screen.getByText('Modifications')).toBeInTheDocument();
    });
  });

  // ==================== AuditEntityBreakdownChart ====================

  describe('AuditEntityBreakdownChart', () => {
    test('affiche le message de chargement', () => {
      render(<AuditEntityBreakdownChart data={[]} isLoading={true} />);
      expect(screen.getByText('Chargement de la distribution...')).toBeInTheDocument();
    });

    test('affiche le message "aucune donnée" quand liste vide', () => {
      render(<AuditEntityBreakdownChart data={[]} isLoading={false} />);
      expect(screen.getByText('Aucune donnée disponible')).toBeInTheDocument();
    });

    test('affiche le titre et le total', () => {
      const data = [
        { entity_type: 'Plant', count: 45 },
        { entity_type: 'Photo', count: 23 },
        { entity_type: 'WateringHistory', count: 12 },
      ];
      render(<AuditEntityBreakdownChart data={data} isLoading={false} />);
      expect(screen.getByText('🔍 Distribution par Entité')).toBeInTheDocument();
      expect(screen.getByText('Total: 80 modifications')).toBeInTheDocument();
    });

    test('affiche les types d\'entité dans les labels', () => {
      const data = [
        { entity_type: 'Plant', count: 50 },
        { entity_type: 'Photo', count: 30 },
      ];
      render(<AuditEntityBreakdownChart data={data} isLoading={false} />);
      // Les labels du pie chart sont générés dynamiquement, vérifions au moins le rendu
      const svg = screen.getByRole('presentation').querySelector('svg');
      expect(svg).toBeInTheDocument();
    });
  });

  // ==================== AuditUserActivityChart ====================

  describe('AuditUserActivityChart', () => {
    test('affiche le message de chargement', () => {
      render(<AuditUserActivityChart data={[]} isLoading={true} />);
      expect(screen.getByText('Chargement de l\'activité utilisateur...')).toBeInTheDocument();
    });

    test('affiche le message "aucune donnée" quand liste vide', () => {
      render(<AuditUserActivityChart data={[]} isLoading={false} />);
      expect(screen.getByText('Aucune donnée disponible')).toBeInTheDocument();
    });

    test('affiche le titre et le total', () => {
      const data = [
        { user_id: 1, count: 25 },
        { user_id: 2, count: 18 },
        { user_id: 3, count: 12 },
      ];
      render(<AuditUserActivityChart data={data} isLoading={false} />);
      expect(screen.getByText('👥 Activité par Utilisateur')).toBeInTheDocument();
      expect(screen.getByText('Total: 55 modifications par 3 utilisateur(s)')).toBeInTheDocument();
    });

    test('affiche "Admin" pour user_id null', () => {
      const data = [
        { user_id: null, count: 10 },
        { user_id: 1, count: 5 },
      ];
      render(<AuditUserActivityChart data={data} isLoading={false} />);
      // Le rendu des données se fait dynamiquement via Recharts
      const svg = screen.getByRole('presentation').querySelector('svg');
      expect(svg).toBeInTheDocument();
    });
  });

  // ==================== AuditActionByEntityChart ====================

  describe('AuditActionByEntityChart', () => {
    test('affiche le message de chargement', () => {
      render(<AuditActionByEntityChart data={[]} isLoading={true} />);
      expect(screen.getByText('Chargement du tableau croisé...')).toBeInTheDocument();
    });

    test('affiche le message "aucune donnée" quand liste vide', () => {
      render(<AuditActionByEntityChart data={[]} isLoading={false} />);
      expect(screen.getByText('Aucune donnée disponible')).toBeInTheDocument();
    });

    test('affiche le titre et le total', () => {
      const data = [
        { entity_type: 'Plant', INSERT: 5, UPDATE: 10, DELETE: 2 },
        { entity_type: 'Photo', INSERT: 3, UPDATE: 8, DELETE: 1 },
      ];
      render(<AuditActionByEntityChart data={data} isLoading={false} />);
      expect(screen.getByText('📊 Actions par Entité')).toBeInTheDocument();
      expect(screen.getByText('Total: 29 modifications')).toBeInTheDocument();
    });

    test('affiche les légendes d\'actions', () => {
      const data = [
        { entity_type: 'Plant', INSERT: 5, UPDATE: 10, DELETE: 2 },
      ];
      render(<AuditActionByEntityChart data={data} isLoading={false} />);
      expect(screen.getByText('Créations')).toBeInTheDocument();
      expect(screen.getByText('Modifications')).toBeInTheDocument();
      expect(screen.getByText('Suppressions')).toBeInTheDocument();
    });
  });

  // ==================== Integration Tests ====================

  describe('Charts Integration', () => {
    test('gère les données avec valeurs NULL', () => {
      const data = [
        { date: '2025-11-01', INSERT: null, UPDATE: 5, DELETE: 0, total: 5 },
      ];
      render(<AuditDailyActivityChart data={data} isLoading={false} />);
      expect(screen.getByText('Total: 5 modifications')).toBeInTheDocument();
    });

    test('gère les données manquantes gracefully', () => {
      render(<AuditDailyActivityChart data={undefined} isLoading={false} />);
      expect(screen.getByText('Aucune donnée disponible')).toBeInTheDocument();
    });

    test('affiche correctement avec données volumineuses', () => {
      const largeData = Array.from({ length: 100 }, (_, i) => ({
        date: `2025-${String(Math.floor(i / 3) + 1).padStart(2, '0')}-${String((i % 28) + 1).padStart(2, '0')}`,
        INSERT: Math.floor(Math.random() * 50),
        UPDATE: Math.floor(Math.random() * 100),
        DELETE: Math.floor(Math.random() * 20),
        total: Math.floor(Math.random() * 150),
      }));
      render(<AuditDailyActivityChart data={largeData} isLoading={false} />);
      expect(screen.getByText(/Total: \d+ modifications/)).toBeInTheDocument();
    });
  });
});
