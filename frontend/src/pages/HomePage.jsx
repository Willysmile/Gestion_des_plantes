import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { usePlants } from '../hooks/usePlants'
import { Plus, Search } from 'lucide-react'
import PlantCard from '../components/PlantCard'

export default function HomePage() {
  const { plants, loading, error } = usePlants()
  const [filter, setFilter] = useState('')

  // Filtrer les plantes par nom ou famille
  const filteredPlants = useMemo(() =>
    plants.filter(plant =>
      plant.name?.toLowerCase().includes(filter.toLowerCase()) ||
      plant.scientific_name?.toLowerCase().includes(filter.toLowerCase()) ||
      plant.family?.toLowerCase().includes(filter.toLowerCase())
    ),
    [plants, filter]
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des plantes...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-800 font-semibold">❌ Erreur</p>
        <p className="text-red-600 text-sm mt-2">{error}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-gray-900">🌿 Mes Plantes</h1>
          <p className="text-gray-600 mt-1">{filteredPlants.length} plante{filteredPlants.length !== 1 ? 's' : ''}</p>
        </div>
        <Link
          to="/plants/new"
          className="flex items-center gap-2 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-semibold transition"
        >
          <Plus className="w-5 h-5" />
          Nouvelle Plante
        </Link>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder="Rechercher par nom, espèce ou famille..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
        />
      </div>

      {/* Plants Grid */}
      {filteredPlants.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          {filteredPlants.map(plant => (
            <PlantCard key={plant.id} plant={plant} />
          ))}
        </div>
      ) : (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-12 text-center">
          <div className="text-5xl mb-4">🌱</div>
          {plants.length === 0 ? (
            <>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Aucune plante</h3>
              <p className="text-gray-600 mb-4">Commence par créer ta première plante !</p>
              <Link
                to="/plants/new"
                className="inline-flex items-center gap-2 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-semibold transition"
              >
                <Plus className="w-5 h-5" />
                Créer la première plante
              </Link>
            </>
          ) : (
            <>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Aucune plante trouvée</h3>
              <p className="text-gray-600">Essaie avec d'autres mots-clés</p>
            </>
          )}
        </div>
      )}
    </div>
  )
}
