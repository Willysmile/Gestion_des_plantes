import { useParams, Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import DiseaseHistory from '../components/DiseaseHistory'

export default function DiseaseHistoryPage() {
  const { id: plantId } = useParams()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <Link
            to={`/plants/${plantId}`}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition"
          >
            <ArrowLeft className="w-5 h-5" />
            Retour à la plante
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Historique des maladies</h1>
            <p className="text-gray-600">Plante #{plantId}</p>
          </div>
        </div>

        {/* Historique des maladies */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <DiseaseHistory plantId={parseInt(plantId)} />
        </div>
      </div>
    </div>
  )
}
