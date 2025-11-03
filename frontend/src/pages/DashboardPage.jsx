import { PlantsToWaterList, PlantsToFertilizeList } from '../components/WateringNotifications'
import { useWateringStats } from '../hooks/useWateringNotifications'
import { Droplet, AlertCircle, TrendingUp } from 'lucide-react'

export default function DashboardPage() {
  const { toWater, toFertilize, total, loading, error } = useWateringStats()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du tableau de bord...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Page Title */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 flex items-center gap-3">
          <TrendingUp className="w-10 h-10 text-green-600" />
          Tableau de Bord
        </h1>
        <p className="text-gray-600 mt-2">Résumé des soins à apporter à vos plantes</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Card: À Arroser */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6 border-l-4 border-blue-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-700 font-semibold">À Arroser</p>
              <p className="text-3xl font-bold text-blue-900 mt-2">{toWater}</p>
              <p className="text-xs text-blue-600 mt-1">plantes en attente</p>
            </div>
            <Droplet className="w-12 h-12 text-blue-400 opacity-50" />
          </div>
        </div>

        {/* Card: À Fertiliser */}
        <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-lg p-6 border-l-4 border-amber-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-amber-700 font-semibold">À Fertiliser</p>
              <p className="text-3xl font-bold text-amber-900 mt-2">{toFertilize}</p>
              <p className="text-xs text-amber-600 mt-1">plantes en attente</p>
            </div>
            <AlertCircle className="w-12 h-12 text-amber-400 opacity-50" />
          </div>
        </div>

        {/* Card: Total */}
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6 border-l-4 border-green-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-700 font-semibold">Total Soins</p>
              <p className="text-3xl font-bold text-green-900 mt-2">{total}</p>
              <p className="text-xs text-green-600 mt-1">plantes à soigner</p>
            </div>
            <TrendingUp className="w-12 h-12 text-green-400 opacity-50" />
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600" />
          <div>
            <p className="font-semibold text-red-800">Erreur</p>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Plants Lists */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Plants to Water */}
        <div className="bg-white rounded-lg shadow">
          <div className="bg-blue-600 text-white px-6 py-4 rounded-t-lg flex items-center gap-2">
            <Droplet className="w-5 h-5" />
            <h2 className="text-xl font-semibold">Plantes à Arroser</h2>
          </div>
          <div className="p-6">
            <PlantsToWaterList />
          </div>
        </div>

        {/* Plants to Fertilize */}
        <div className="bg-white rounded-lg shadow">
          <div className="bg-amber-600 text-white px-6 py-4 rounded-t-lg flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            <h2 className="text-xl font-semibold">Plantes à Fertiliser</h2>
          </div>
          <div className="p-6">
            <PlantsToFertilizeList />
          </div>
        </div>
      </div>

      {/* Empty State */}
      {total === 0 && !loading && (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-12 text-center">
          <div className="text-5xl mb-4">🌿</div>
          <h3 className="text-2xl font-bold text-green-800 mb-2">Parfait !</h3>
          <p className="text-green-700">Toutes vos plantes sont bien entretenues.</p>
          <p className="text-green-600 text-sm mt-2">Revenez bientôt pour de nouveaux soins à apporter.</p>
        </div>
      )}
    </div>
  )
}
