import { useState, useMemo, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { usePlants } from '../hooks/usePlants'
import { Trash2, Archive, Edit, Eye, Heart } from 'lucide-react'
import { plantsAPI } from '../lib/api'
import PlantCard from '../components/PlantCard'

export default function DashboardPage() {
  const { plants, loading, error, refetch } = usePlants()
  const [filter, setFilter] = useState('')
  const [deletingId, setDeletingId] = useState(null)

  // Debug logs
  console.log('DashboardPage render:', { loading, error, plantsCount: plants.length })

  const handleDelete = useCallback(async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette plante ?')) {
      try {
        await plantsAPI.delete(id)
        await refetch()
      } catch (err) {
        alert('Erreur: ' + err.message)
      }
    }
    setDeletingId(null)
  }, [refetch])

  const handleArchive = useCallback(async (id, reason = 'Archivée') => {
    try {
      await plantsAPI.archive(id, reason)
      await refetch()
    } catch (err) {
      alert('Erreur: ' + err.message)
    }
  }, [refetch])

  // Mémoriser le filtrage pour éviter les re-rendus inutiles
  const filteredPlants = useMemo(() =>
    plants.filter(plant =>
      plant.name?.toLowerCase().includes(filter.toLowerCase()) ||
      plant.family?.toLowerCase().includes(filter.toLowerCase())
    ),
    [plants, filter]
  )

  if (loading) return (
    <div className="text-center py-12 space-y-4">
      <p className="text-lg">⏳ Chargement...</p>
      <p className="text-sm text-gray-500">Fetching plants from API...</p>
    </div>
  )
  if (error) return (
    <div className="text-center py-12 text-red-600 space-y-2">
      <p className="text-lg">❌ Erreur</p>
      <p>{error}</p>
    </div>
  )

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Mes Plantes ({plants.length})</h1>

      {/* Search & Filter */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Rechercher par nom ou famille..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
        />
      </div>

      {/* Plants Grid: 5 cards par ligne, 3 lignes maxi */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 max-h-[calc(100vh-300px)] overflow-y-auto">
        {filteredPlants.map(plant => (
          <PlantCard
            key={plant.id}
            plant={plant}
          />
        ))}
      </div>

      {filteredPlants.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">Aucune plante trouvée.</p>
          <Link to="/plants/new" className="text-green-600 hover:underline">
            Créer la première plante
          </Link>
        </div>
      )}
    </div>
  )
}
