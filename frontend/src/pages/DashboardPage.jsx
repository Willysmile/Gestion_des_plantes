import { useState, useMemo, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { usePlants } from '../hooks/usePlants'
import { Trash2, Archive, Edit, Eye, Heart } from 'lucide-react'
import { plantsAPI } from '../lib/api'

export default function DashboardPage() {
  const { plants, loading, error, refetch } = usePlants()
  const [filter, setFilter] = useState('')
  const [deletingId, setDeletingId] = useState(null)

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

  if (loading) return <div className="text-center py-12">Chargement...</div>
  if (error) return <div className="text-center py-12 text-red-600">{error}</div>

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Mes Plantes</h1>

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

      {/* Plants Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredPlants.map(plant => (
          <div key={plant.id} className="bg-white rounded-lg shadow hover:shadow-lg transition p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-bold">{plant.name}</h3>
                <p className="text-gray-600">{plant.scientific_name || plant.family}</p>
              </div>
              {plant.is_favorite && <Heart className="w-5 h-5 text-red-500 fill-current" />}
            </div>

            <div className="text-sm text-gray-600 mb-4">
              <p>Ref: <span className="font-mono">{plant.reference}</span></p>
              <p>Santé: {plant.health_status || 'Non spécifiée'}</p>
            </div>

            <div className="flex gap-2">
              <Link
                to={`/plants/${plant.id}`}
                className="flex-1 flex items-center justify-center gap-2 bg-blue-100 text-blue-700 px-3 py-2 rounded hover:bg-blue-200"
              >
                <Eye className="w-4 h-4" />
                Voir
              </Link>
              <Link
                to={`/plants/${plant.id}/edit`}
                className="flex items-center justify-center gap-2 bg-yellow-100 text-yellow-700 px-3 py-2 rounded hover:bg-yellow-200"
              >
                <Edit className="w-4 h-4" />
              </Link>
              <button
                onClick={() => handleArchive(plant.id)}
                className="flex items-center justify-center gap-2 bg-purple-100 text-purple-700 px-3 py-2 rounded hover:bg-purple-200"
              >
                <Archive className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleDelete(plant.id)}
                className="flex items-center justify-center gap-2 bg-red-100 text-red-700 px-3 py-2 rounded hover:bg-red-200"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
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
