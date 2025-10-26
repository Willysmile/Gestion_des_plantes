import { useParams } from 'react-router-dom'
import { usePlant } from '../hooks/usePlants'
import { ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function PlantDetailPage() {
  const { id } = useParams()
  const { plant, loading, error } = usePlant(id)

  if (loading) return <div className="text-center py-12">Chargement...</div>
  if (error) return <div className="text-center py-12 text-red-600">{error}</div>
  if (!plant) return <div className="text-center py-12">Plante non trouvée</div>

  return (
    <div>
      <Link to="/" className="flex items-center gap-2 text-blue-600 hover:underline mb-6">
        <ArrowLeft className="w-5 h-5" />
        Retour
      </Link>

      <div className="bg-white rounded-lg shadow p-8 max-w-2xl">
        <h1 className="text-3xl font-bold mb-2">{plant.name}</h1>
        <p className="text-gray-600 text-lg mb-6">{plant.scientific_name || plant.family}</p>

        <div className="grid grid-cols-2 gap-6">
          {/* Left Column */}
          <div>
            <h3 className="font-bold text-lg mb-4 border-b pb-2">Informations Générales</h3>
            <dl className="space-y-3 text-sm">
              <div>
                <dt className="font-semibold text-gray-700">Référence</dt>
                <dd className="text-gray-600 font-mono">{plant.reference}</dd>
              </div>
              <div>
                <dt className="font-semibold text-gray-700">Famille</dt>
                <dd className="text-gray-600">{plant.family}</dd>
              </div>
              <div>
                <dt className="font-semibold text-gray-700">Genre</dt>
                <dd className="text-gray-600">{plant.genus || 'Non spécifié'}</dd>
              </div>
              <div>
                <dt className="font-semibold text-gray-700">Espèce</dt>
                <dd className="text-gray-600">{plant.species || 'Non spécifiée'}</dd>
              </div>
              <div>
                <dt className="font-semibold text-gray-700">Santé</dt>
                <dd className="text-gray-600">{plant.health_status || 'Non spécifiée'}</dd>
              </div>
            </dl>
          </div>

          {/* Right Column */}
          <div>
            <h3 className="font-bold text-lg mb-4 border-b pb-2">Environnement</h3>
            <dl className="space-y-3 text-sm">
              <div>
                <dt className="font-semibold text-gray-700">Température</dt>
                <dd className="text-gray-600">
                  {plant.temperature_min}°C - {plant.temperature_max}°C
                </dd>
              </div>
              <div>
                <dt className="font-semibold text-gray-700">Humidité</dt>
                <dd className="text-gray-600">{plant.humidity_level}%</dd>
              </div>
              <div>
                <dt className="font-semibold text-gray-700">Type de sol</dt>
                <dd className="text-gray-600">{plant.soil_type || 'Non spécifié'}</dd>
              </div>
              <div>
                <dt className="font-semibold text-gray-700">Lumière</dt>
                <dd className="text-gray-600">{plant.light_requirement_id ? 'Configurée' : 'Non spécifiée'}</dd>
              </div>
              <div>
                <dt className="font-semibold text-gray-700">Taille du pot</dt>
                <dd className="text-gray-600">{plant.pot_size || 'Non spécifiée'}</dd>
              </div>
            </dl>
          </div>
        </div>

        {/* Description */}
        {plant.description && (
          <div className="mt-6 pt-6 border-t">
            <h3 className="font-bold text-lg mb-2">Description</h3>
            <p className="text-gray-600">{plant.description}</p>
          </div>
        )}

        {/* Flags */}
        <div className="mt-6 pt-6 border-t flex gap-4">
          {plant.is_favorite && <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm">❤️ Favorite</span>}
          {plant.is_indoor && <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">Intérieur</span>}
          {plant.is_outdoor && <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm">Extérieur</span>}
          {plant.is_toxic && <span className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm">⚠️ Toxique</span>}
          {plant.is_archived && <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">Archivée</span>}
        </div>

        {/* Actions */}
        <div className="mt-6 pt-6 border-t flex gap-4">
          <Link
            to={`/plants/${plant.id}/edit`}
            className="bg-yellow-600 text-white px-6 py-2 rounded-lg hover:bg-yellow-700"
          >
            Éditer
          </Link>
          <Link to="/" className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700">
            Retour
          </Link>
        </div>
      </div>
    </div>
  )
}
