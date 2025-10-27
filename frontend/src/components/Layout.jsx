import { Outlet, Link, useLocation } from 'react-router-dom'
import { Leaf, Plus, Save, X } from 'lucide-react'
import { ModalProvider, useModal } from '../contexts/ModalContext'
import PlantDetailModal from './PlantDetailModal'

function LayoutContent() {
  const location = useLocation()
  const isEditPage = location.pathname.includes('/edit')
  const { modalState, closeModal } = useModal()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
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
            <Link 
              to="/plants/new"
              className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
            >
              <Plus className="w-5 h-5" />
              Nouvelle Plante
            </Link>
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
    <ModalProvider>
      <LayoutContent />
    </ModalProvider>
  )
}
