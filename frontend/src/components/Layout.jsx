import { Outlet, Link, useLocation } from 'react-router-dom'
import { Leaf, Plus, Save, X, Settings } from 'lucide-react'
import { ModalProvider, useModal } from '../contexts/ModalContext'
import { RefreshProvider, useRefresh } from '../contexts/RefreshContext'
import PlantDetailModal from './PlantDetailModal'
import { useWateringStats } from '../hooks/useWateringNotifications'
import { useEffect } from 'react'

function LayoutContent() {
  const location = useLocation()
  const isEditPage = location.pathname.includes('/edit')
  const { modalState, closeModal } = useModal()
  const { toWater, toFertilize, inCareCount, refresh } = useWateringStats()
  const { refreshTrigger } = useRefresh()

  // Auto-refresh toutes les 30 secondes
  useEffect(() => {
    const interval = setInterval(() => {
      refresh()
    }, 30 * 1000)
    return () => clearInterval(interval)
  }, [refresh])

  // Refresh quand le trigger change
  useEffect(() => {
    if (refreshTrigger > 0) {
      refresh()
    }
  }, [refreshTrigger, refresh])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-8 flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2">
            <Leaf className="w-8 h-8 text-green-600" />
            <span className="text-2xl font-bold">Gestion des Plantes</span>
          </Link>
          
          {isEditPage ? (
            <div className="flex gap-2">
              <button
                type="submit"
                form="plant-form"
                className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
              >
                <Save className="w-5 h-5" />
                Mettre à jour
              </button>
              <Link
                to="/"
                className="flex items-center gap-2 bg-gray-300 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-400"
              >
                <X className="w-5 h-5" />
                Annuler
              </Link>
            </div>
          ) : (
            <div className="flex gap-2 items-center">
              <Link 
                to="/dashboard"
                className="relative flex items-center bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-all"
              >
                Tableau de Bord
                <div className="absolute -top-2.5 -right-2.5 flex gap-1">
                  <div className="w-5 h-5 bg-blue-400 text-white rounded-full flex items-center justify-center text-xs font-extrabold shadow-lg drop-shadow-lg" style={{textShadow: '0 1px 2px rgba(0,0,0,0.5), 0 2px 4px rgba(0,0,0,0.3)'}}>{toWater}</div>
                  <div className="w-5 h-5 bg-amber-400 text-white rounded-full flex items-center justify-center text-xs font-extrabold shadow-lg drop-shadow-lg" style={{textShadow: '0 1px 2px rgba(0,0,0,0.5), 0 2px 4px rgba(0,0,0,0.3)'}}>{toFertilize}</div>
                  <div className="w-5 h-5 bg-red-500 text-white rounded-full flex items-center justify-center text-xs font-extrabold shadow-lg drop-shadow-lg" style={{textShadow: '0 1px 2px rgba(0,0,0,0.5), 0 2px 4px rgba(0,0,0,0.3)'}}>{inCareCount}</div>
                </div>
              </Link>
              <div className="flex gap-1 bg-blue-50 rounded-lg p-1">
                <Link 
                  to="/propagations"
                  className="flex items-center gap-2 bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-700 transition text-sm font-medium"
                >
                  Tableau
                </Link>
                <Link 
                  to="/propagations/calendar"
                  className="flex items-center gap-2 bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600 transition text-sm font-medium"
                >
                  Calendrier
                </Link>
                <Link 
                  to="/propagations/genealogy"
                  className="flex items-center gap-2 bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600 transition text-sm font-medium"
                >
                  Généalogie
                </Link>
                <Link 
                  to="/propagations/statistics"
                  className="flex items-center gap-2 bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600 transition text-sm font-medium"
                >
                  Stats
                </Link>
              </div>
              <Link 
                to="/plants/new"
                className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
              >
                <Plus className="w-5 h-5" />
                Nouvelle Plante
              </Link>
              <Link
                to="/settings"
                className="flex items-center gap-2 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
              >
                <Settings className="w-5 h-5" />
                Paramètres
              </Link>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl 2xl:max-w-[70vw] mx-auto px-4 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-100 mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-600">
          <p>&copy; 2025 Gestion des Plantes - Phase 2 MVP</p>
        </div>
      </footer>

      {/* Global Modal */}
      {modalState.isOpen && modalState.plant && (
        <PlantDetailModal
          plant={modalState.plant}
          onClose={closeModal}
        />
      )}
    </div>
  )
}

export default function Layout() {
  return (
    <RefreshProvider>
      <ModalProvider>
        <LayoutContent />
      </ModalProvider>
    </RefreshProvider>
  )
}
