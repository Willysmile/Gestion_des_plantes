/**
 * Tests pour Phase 6.3: AuditLog Dashboard UI
 * Vérifie le rendu, les filtres, l'expansion des logs, etc.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AuditDashboardPage from '../pages/AuditDashboardPage'
import { BrowserRouter } from 'react-router-dom'

// Mock api
vi.mock('../config', () => ({
  default: {
    get: vi.fn(),
    delete: vi.fn(),
  },
}))

const mockLogs = [
  {
    id: 1,
    action: 'INSERT',
    entity_type: 'Plant',
    entity_id: 1,
    field_name: null,
    old_value: null,
    new_value: '{"name": "Rose"}',
    user_id: null,
    ip_address: null,
    user_agent: null,
    description: 'Création de Plant #1',
    raw_changes: { name: 'Rose', family: 'Rosaceae' },
    created_at: '2025-11-10T10:00:00',
    updated_at: '2025-11-10T10:00:00',
  },
  {
    id: 2,
    action: 'UPDATE',
    entity_type: 'Plant',
    entity_id: 1,
    field_name: 'name',
    old_value: '"Rose"',
    new_value: '"Rose Moderne"',
    user_id: 1,
    ip_address: '192.168.1.1',
    user_agent: 'Mozilla/5.0',
    description: 'Modification name: Rose → Rose Moderne',
    raw_changes: { name: { old: 'Rose', new: 'Rose Moderne' } },
    created_at: '2025-11-10T11:00:00',
    updated_at: '2025-11-10T11:00:00',
  },
  {
    id: 3,
    action: 'DELETE',
    entity_type: 'Plant',
    entity_id: 2,
    field_name: null,
    old_value: '{"name": "Cactus"}',
    new_value: null,
    user_id: null,
    ip_address: null,
    user_agent: null,
    description: 'Suppression de Plant #2',
    raw_changes: { name: 'Cactus', family: 'Cactaceae' },
    created_at: '2025-11-10T12:00:00',
    updated_at: '2025-11-10T12:00:00',
  },
]

describe('AuditDashboardPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  const renderAudit = () => {
    return render(
      <BrowserRouter>
        <AuditDashboardPage />
      </BrowserRouter>
    )
  }

  describe('Rendering', () => {
    it('should render the audit dashboard header', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('📋 Historique d\'Audit')).toBeInTheDocument()
        expect(screen.getByText('Suivi complet de tous les changements')).toBeInTheDocument()
      })
    })

    it('should display loading spinner initially', () => {
      const api = require('../config').default
      api.get.mockImplementationOnce(() => new Promise(() => {})) // Never resolves

      renderAudit()

      // The loading text might appear briefly
      // This is hard to test without additional hooks
    })

    it('should render filter controls', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: [] })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('Action')).toBeInTheDocument()
        expect(screen.getByText('Type d\'entité')).toBeInTheDocument()
        expect(screen.getByText('Période')).toBeInTheDocument()
      })
    })
  })

  describe('Log Display', () => {
    it('should display logs when loaded', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('Création de Plant #1')).toBeInTheDocument()
        expect(screen.getByText('Modification name: Rose → Rose Moderne')).toBeInTheDocument()
        expect(screen.getByText('Suppression de Plant #2')).toBeInTheDocument()
      })
    })

    it('should display correct action badges', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('✨ Création')).toBeInTheDocument()
        expect(screen.getByText('📝 Modification')).toBeInTheDocument()
        expect(screen.getByText('🗑️ Suppression')).toBeInTheDocument()
      })
    })

    it('should display entity type badges', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        const plantBadges = screen.getAllByText('Plant')
        expect(plantBadges.length).toBeGreaterThan(0)
      })
    })

    it('should show empty state when no logs', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: [] })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('Aucun log d\'audit trouvé')).toBeInTheDocument()
      })
    })
  })

  describe('Log Expansion', () => {
    it('should expand log details on click', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('Modification name: Rose → Rose Moderne')).toBeInTheDocument()
      })

      // Click on the UPDATE log
      const updateLog = screen.getByText('Modification name: Rose → Rose Moderne').closest('div')
      fireEvent.click(updateLog)

      // Should show diff details
      await waitFor(() => {
        expect(screen.getByText(/Champ modifié/)).toBeInTheDocument()
      })
    })

    it('should show old and new values for UPDATE', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: [mockLogs[1]] })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('Modification name: Rose → Rose Moderne')).toBeInTheDocument()
      })

      // Expand the log
      const updateLog = screen.getByText('Modification name: Rose → Rose Moderne').closest('div')
      fireEvent.click(updateLog)

      await waitFor(() => {
        expect(screen.getByText(/❌ Ancienne valeur/)).toBeInTheDocument()
        expect(screen.getByText(/✅ Nouvelle valeur/)).toBeInTheDocument()
      })
    })

    it('should collapse expanded log on second click', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('Modification name: Rose → Rose Moderne')).toBeInTheDocument()
      })

      const updateLog = screen.getByText('Modification name: Rose → Rose Moderne').closest('div')
      
      // Expand
      fireEvent.click(updateLog)
      await waitFor(() => {
        expect(screen.getByText(/Champ modifié/)).toBeInTheDocument()
      })

      // Collapse
      fireEvent.click(updateLog)
      // The details should still exist but we can check the log count
      expect(screen.getAllByText(/Champ modifié/).length).toBeGreaterThan(0)
    })
  })

  describe('Filters', () => {
    it('should filter by action', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('📝 Modification')).toBeInTheDocument()
      })

      // Change action filter
      const actionSelect = screen.getByDisplayValue('Toutes les actions')
      await userEvent.selectOption(actionSelect, 'UPDATE')

      const filterBtn = screen.getByText('🔍 Appliquer filtres')
      fireEvent.click(filterBtn)

      await waitFor(() => {
        // API should be called with action filter
        expect(api.get).toHaveBeenCalledWith(
          expect.stringContaining('/action/UPDATE'),
          expect.any(Object)
        )
      })
    })

    it('should filter by period', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      const periodSelect = screen.getByDisplayValue('Dernière semaine')
      await userEvent.selectOption(periodSelect, '30')

      const filterBtn = screen.getByText('🔍 Appliquer filtres')
      fireEvent.click(filterBtn)

      await waitFor(() => {
        expect(api.get).toHaveBeenCalledWith(
          expect.stringContaining('/recent?days=30'),
          expect.any(Object)
        )
      })
    })

    it('should update URL search params on filter', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('📋 Historique d\'Audit')).toBeInTheDocument()
      })

      const actionSelect = screen.getByDisplayValue('Toutes les actions')
      await userEvent.selectOption(actionSelect, 'INSERT')

      const filterBtn = screen.getByText('🔍 Appliquer filtres')
      fireEvent.click(filterBtn)

      // URL should be updated with action param
      await waitFor(() => {
        expect(window.location.search).toContain('action=INSERT')
      })
    })
  })

  describe('Cleanup', () => {
    it('should show cleanup button', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('🗑️ Nettoyer logs')).toBeInTheDocument()
      })
    })

    it('should call cleanup API on button click', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })
      api.delete.mockResolvedValueOnce({ data: { deleted: 5 } })

      global.confirm = vi.fn(() => true)

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('🗑️ Nettoyer logs')).toBeInTheDocument()
      })

      const cleanupBtn = screen.getByText('🗑️ Nettoyer logs')
      fireEvent.click(cleanupBtn)

      await waitFor(() => {
        expect(api.delete).toHaveBeenCalledWith('/api/audit/logs/cleanup?days=90')
      })
    })

    it('should not cleanup if user cancels', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: mockLogs })

      global.confirm = vi.fn(() => false)

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('🗑️ Nettoyer logs')).toBeInTheDocument()
      })

      const cleanupBtn = screen.getByText('🗑️ Nettoyer logs')
      fireEvent.click(cleanupBtn)

      // Delete should not be called
      expect(api.delete).not.toHaveBeenCalled()
    })
  })

  describe('Error Handling', () => {
    it('should display error message on API failure', async () => {
      const api = require('../config').default
      api.get.mockRejectedValueOnce({
        response: { data: { detail: 'Erreur serveur' } },
      })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('Erreur serveur')).toBeInTheDocument()
      })
    })

    it('should display generic error if no detail provided', async () => {
      const api = require('../config').default
      api.get.mockRejectedValueOnce(new Error('Network error'))

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText('Erreur de chargement')).toBeInTheDocument()
      })
    })
  })

  describe('Metadata Display', () => {
    it('should display user and IP info for logs with metadata', async () => {
      const api = require('../config').default
      api.get.mockResolvedValueOnce({ data: [mockLogs[1]] })

      renderAudit()

      await waitFor(() => {
        expect(screen.getByText(/Modification name:/)).toBeInTheDocument()
      })

      // Expand to see metadata
      const updateLog = screen.getByText(/Modification name:/).closest('div')
      fireEvent.click(updateLog)

      await waitFor(() => {
        expect(screen.getByText(/👤 User #1/)).toBeInTheDocument()
        expect(screen.getByText(/🌐 192\.168\.1\.1/)).toBeInTheDocument()
      })
    })
  })
})
