import { useEffect, useState } from 'react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Droplet, AlertCircle, Heart, Leaf, TrendingUp } from 'lucide-react'
import api from '../lib/api'

export default function AdvancedDashboardPage() {
  const [stats, setStats] = useState(null)
  const [upcoming, setUpcoming] = useState([])
  const [activity, setActivity] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadAllData()
    // Refresh every 5 minutes
    const interval = setInterval(loadAllData, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  const loadAllData = async () => {
    try {
      setLoading(true)
      const [statsRes, upcomingRes, activityRes] = await Promise.all([
        api.get('/statistics/dashboard'),
        api.get('/statistics/upcoming-waterings?days=7'),
        api.get('/statistics/activity?days=30'),
      ])

      setStats(statsRes.data)
      setUpcoming(upcomingRes.data || [])
      setActivity(activityRes.data || [])
      setError(null)
    } catch (err) {
      console.error('Error loading dashboard stats:', err)
      setError('Erreur de chargement des statistiques')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="flex items-center justify-center h-96">Chargement...</div>
  }

  if (error) {
    return <div className="text-center text-red-500 p-4">{error}</div>
  }

  const COLORS = {
    healthy: '#10b981',
    sick: '#f97316',
    critical: '#ef4444',
    excellent: '#06b6d4',
    good: '#84cc16',
    poor: '#f59e0b',
  }

  // Pie chart data
  const healthData = stats
    ? [
        { name: 'Excellente', value: stats.health_excellent || 0, color: COLORS.excellent },
        { name: 'Bonne', value: stats.health_good || 0, color: COLORS.good },
        { name: 'Mauvaise', value: stats.health_poor || 0, color: COLORS.poor },
      ].filter(item => item.value > 0)
    : []

  return (
    <div className="space-y-6 pb-8">
      {/* En-tête */}
      <div>
        <h1 className="text-4xl font-bold text-gray-800">📊 Dashboard Avancé</h1>
        <p className="text-gray-600 mt-2">Vue d'ensemble et prévisions de votre collection</p>
      </div>

      {/* KPI Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Total plantes */}
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Plantes</p>
                <p className="text-3xl font-bold text-gray-800">{stats.total_plants}</p>
              </div>
              <Leaf className="w-12 h-12 text-blue-500 opacity-20" />
            </div>
          </div>

          {/* Santé moyenne */}
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Santé Moyenne</p>
                <p className="text-3xl font-bold text-gray-800">
                  {stats.health_excellent + stats.health_good}/{stats.total_plants}
                </p>
                <p className="text-sm text-green-600 mt-1">✅ Saines</p>
              </div>
              <Heart className="w-12 h-12 text-green-500 opacity-20" />
            </div>
          </div>

          {/* En retard */}
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">À Arroser</p>
                <p className="text-3xl font-bold text-red-600">{upcoming.length}</p>
                <p className="text-sm text-red-600 mt-1">🚨 En retard</p>
              </div>
              <Droplet className="w-12 h-12 text-red-500 opacity-20" />
            </div>
          </div>

          {/* Critiques */}
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Critiques</p>
                <p className="text-3xl font-bold text-orange-600">{stats.health_poor}</p>
                <p className="text-sm text-orange-600 mt-1">⚠️ À surveiller</p>
              </div>
              <AlertCircle className="w-12 h-12 text-orange-500 opacity-20" />
            </div>
          </div>
        </div>
      )}

      {/* Graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Santé globale - Pie Chart */}
        {healthData.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">État de Santé</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={healthData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {healthData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Activité - Bar Chart */}
        {activity.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Activité (30 derniers jours)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={activity.slice(-14)} margin={{ top: 20, right: 30, left: 0, bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="date"
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  interval={1}
                  tick={{ fontSize: 12 }}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="watering_count" fill="#3b82f6" name="Arrosages" />
                <Bar dataKey="fertilizing_count" fill="#10b981" name="Fertilisations" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Prévisions à arroser */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          🌊 À arroser dans les 7 prochains jours ({upcoming.length})
        </h2>
        {upcoming.length > 0 ? (
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {upcoming.map(plant => (
              <div
                key={plant.id}
                className="flex items-center justify-between p-4 bg-blue-50 border-l-4 border-blue-400 rounded"
              >
                <div>
                  <p className="font-semibold text-gray-800">{plant.name}</p>
                  <p className="text-sm text-gray-600">{plant.scientific_name}</p>
                  {plant.last_watered && (
                    <p className="text-xs text-blue-600 mt-1">
                      Dernier arrosage: {new Date(plant.last_watered).toLocaleDateString('fr-FR')}
                    </p>
                  )}
                </div>
                <div className="text-right">
                  {plant.days_since !== null ? (
                    <p className="text-2xl font-bold text-blue-600">{plant.days_since}j</p>
                  ) : (
                    <p className="text-sm text-red-600 font-semibold">Jamais</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">
            ✅ Aucune plante à arroser en retard!
          </div>
        )}
      </div>

      {/* Tendances */}
      <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg shadow p-6 border-l-4 border-green-500">
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="w-6 h-6 text-green-600" />
          <h2 className="text-xl font-semibold text-gray-800">Tendances</h2>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-gray-600">Santé globale</p>
            <p className="text-2xl font-bold text-green-600">
              {stats
                ? Math.round(
                    ((stats.health_excellent + stats.health_good) / stats.total_plants) * 100
                  )
                : 0}
              %
            </p>
          </div>
          <div>
            <p className="text-gray-600">À arroser</p>
            <p className="text-2xl font-bold text-blue-600">{upcoming.length}</p>
          </div>
          <div>
            <p className="text-gray-600">Maladies</p>
            <p className="text-2xl font-bold text-orange-600">{stats?.health_poor || 0}</p>
          </div>
          <div>
            <p className="text-gray-600">Photos</p>
            <p className="text-2xl font-bold text-purple-600">{stats?.total_photos || 0}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
