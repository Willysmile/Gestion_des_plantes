import { useParams, useNavigate } from 'react-router-dom'
import { usePlant } from '../hooks/usePlants'
import PlantDetailModal from '../components/PlantDetailModal'

export default function PlantDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { plant, loading, error } = usePlant(id)

  if (loading) return <div className="text-center py-12">Chargement...</div>
  if (error) return <div className="text-center py-12 text-red-600">{error}</div>
  if (!plant) return <div className="text-center py-12">Plante non trouvée</div>

  return (
    <div className="flex items-center justify-center min-h-screen p-1 bg-white" onClick={(e) => e.stopPropagation()}>
      <div
        className="bg-white rounded-lg shadow-lg overflow-hidden"
        style={{ maxWidth: '90vw', width: '80vw', height: '90vh' }}
        onClick={(e) => e.stopPropagation()}
      >
        <PlantDetailModal
          plant={plant}
          onClose={() => navigate('/')}
        />
      </div>
    </div>
  )
}
