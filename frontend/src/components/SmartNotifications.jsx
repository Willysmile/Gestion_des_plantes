import { useEffect, useState } from 'react'
import { Droplet, Leaf, AlertCircle, Loader } from 'lucide-react'
import api from '../lib/api'

export default function SmartNotifications({ days = 7 }) {
  const [notifications, setNotifications] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadNotifications()
    const interval = setInterval(loadNotifications, 5 * 60 * 1000) // Refresh every 5 min
    return () => clearInterval(interval)
  }, [days])

  const loadNotifications = async () => {
    setLoading(true)
    try {
      const response = await api.get(`/statistics/notifications?days=${days}`)
      setNotifications(response.data)
      setError(null)
    } catch (err) {
      console.error('Erreur chargement notifications:', err)
      setError('Impossible de charger les notifications')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-48">
        <div className="text-center">
          <Loader className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-2" />
          <p className="text-gray-600 text-sm">Chargement des prédictions...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
        <AlertCircle className="w-5 h-5 text-red-600" />
        <div>
          <p className="font-semibold text-red-800 text-sm">{error}</p>
        </div>
      </div>
    )
  }

  if (!notifications) {
    return null
  }

  const { waterings = [], fertilizings = [], summary = {} } = notifications

  return (
    <div className="space-y-4">
      {/* Summary Alert */}
      {summary.most_urgent && (
        <div className="bg-gradient-to-r from-orange-50 to-red-50 border-l-4 border-orange-500 p-4 rounded-lg">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-6 h-6 text-orange-600 flex-shrink-0" />
            <div>
              <p className="text-sm font-semibold text-gray-900">Tâche la plus urgente</p>
              <p className="text-lg font-bold text-orange-700 mt-1">{summary.most_urgent}</p>
            </div>
          </div>
        </div>
      )}

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-blue-50 p-3 rounded-lg text-center border border-blue-200">
          <p className="text-2xl font-bold text-blue-700">{summary.count_watering || 0}</p>
          <p className="text-xs text-blue-600 mt-1">Arrosages</p>
        </div>
        <div className="bg-green-50 p-3 rounded-lg text-center border border-green-200">
          <p className="text-2xl font-bold text-green-700">{summary.count_fertilizing || 0}</p>
          <p className="text-xs text-green-600 mt-1">Fertilisations</p>
        </div>
        <div className="bg-purple-50 p-3 rounded-lg text-center border border-purple-200">
          <p className="text-2xl font-bold text-purple-700">{summary.total_count || 0}</p>
          <p className="text-xs text-purple-600 mt-1">Total ({days}j)</p>
        </div>
      </div>

      {/* Watering Tasks */}
      {waterings.length > 0 && (
        <div className="bg-white rounded-lg shadow border border-blue-100">
          <div className="bg-blue-600 text-white px-4 py-3 rounded-t-lg flex items-center gap-2">
            <Droplet className="w-5 h-5" />
            <h3 className="font-semibold">Arrosages prédits ({waterings.length})</h3>
          </div>
          <div className="space-y-2 p-4">
            {waterings.map((task, idx) => (
              <div key={idx} className="flex items-start justify-between bg-blue-50 p-3 rounded border border-blue-200">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{task.plant_name}</p>
                  <div className="flex items-center gap-3 mt-1 text-xs text-gray-600">
                    <span>📅 {new Date(task.predicted_date).toLocaleDateString('fr-FR')}</span>
                    <span>⏱️ dans {task.days_until} j{task.days_until > 1 ? 's' : ''}</span>
                  </div>
                </div>
                <span className={`text-xs font-bold px-2 py-1 rounded whitespace-nowrap ml-2 ${
                  task.days_until === 0 ? 'bg-red-500 text-white' :
                  task.days_until === 1 ? 'bg-orange-500 text-white' :
                  task.days_until <= 3 ? 'bg-yellow-500 text-white' :
                  'bg-blue-500 text-white'
                }`}>
                  {task.days_until === 0 ? '🔴 URGENT' : `+${task.days_until}j`}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Fertilizing Tasks */}
      {fertilizings.length > 0 && (
        <div className="bg-white rounded-lg shadow border border-green-100">
          <div className="bg-green-600 text-white px-4 py-3 rounded-t-lg flex items-center gap-2">
            <Leaf className="w-5 h-5" />
            <h3 className="font-semibold">Fertilisations prédites ({fertilizings.length})</h3>
          </div>
          <div className="space-y-2 p-4">
            {fertilizings.map((task, idx) => (
              <div key={idx} className="flex items-start justify-between bg-green-50 p-3 rounded border border-green-200">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{task.plant_name}</p>
                  <div className="flex items-center gap-3 mt-1 text-xs text-gray-600">
                    <span>📅 {new Date(task.predicted_date).toLocaleDateString('fr-FR')}</span>
                    <span>⏱️ dans {task.days_until} j{task.days_until > 1 ? 's' : ''}</span>
                  </div>
                </div>
                <span className={`text-xs font-bold px-2 py-1 rounded whitespace-nowrap ml-2 ${
                  task.days_until === 0 ? 'bg-red-500 text-white' :
                  task.days_until === 1 ? 'bg-orange-500 text-white' :
                  task.days_until <= 3 ? 'bg-yellow-500 text-white' :
                  'bg-green-500 text-white'
                }`}>
                  {task.days_until === 0 ? '🔴 URGENT' : `+${task.days_until}j`}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {waterings.length === 0 && fertilizings.length === 0 && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
          <Leaf className="w-12 h-12 text-green-600 mx-auto mb-3 opacity-50" />
          <p className="text-green-700 font-semibold">Aucune tâche prévue</p>
          <p className="text-green-600 text-sm mt-1">Excellente nouvelle ! Pas de tâches programmées pour les {days} prochains jours.</p>
        </div>
      )}
    </div>
  )
}
