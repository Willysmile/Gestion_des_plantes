import { useEffect, useState } from 'react'
import { PlantsToWaterList, PlantsToFertilizeList, PlantsInCareList } from '../components/WateringNotifications'
import { useWateringStats } from '../hooks/useWateringNotifications'
import { Droplet, AlertCircle, TrendingUp, Heart, Leaf, BarChart3, Calendar, Bell, Zap } from 'lucide-react'
import axios from 'axios'
import { PieChart, Pie, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'
import CalendarView from '../components/CalendarView'
import AlertsPanel from '../components/AlertsPanel'
import SmartNotifications from '../components/SmartNotifications'

const COLORS = {
  excellent: '#06b6d4',
  good: '#84cc16',
  poor: '#f59e0b',
  watering: '#3b82f6',
  fertilizing: '#22c55e'
}

export default function DashboardPage() {
  const { toWater, toFertilize, total, loading, error } = useWateringStats()
  const [stats, setStats] = useState(null)
  const [activityData, setActivityData] = useState([])
  const [loadingStats, setLoadingStats] = useState(true)
  const [activeTab, setActiveTab] = useState('overview') // 'overview', 'calendar', 'alerts', 'notifications'
  const [notificationsDays, setNotificationsDays] = useState(7)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [dashRes, actRes] = await Promise.all([
          axios.get('http://localhost:8000/api/statistics/dashboard'),
          axios.get('http://localhost:8000/api/statistics/activity?days=30')
        ])
        setStats(dashRes.data)
        setActivityData(actRes.data.daily_activity || [])
      } catch (err) {
        console.error('Erreur chargement stats:', err)
      } finally {
        setLoadingStats(false)
      }
    }

    fetchStats()
    const interval = setInterval(fetchStats, 5 * 60 * 1000) // Rafraîchir toutes les 5 min
    return () => clearInterval(interval)
  }, [])

  const healthData = stats ? [
    { name: 'Excellente', value: stats.health_excellent || 0, color: COLORS.excellent },
    { name: 'Bonne', value: stats.health_good || 0, color: COLORS.good },
    { name: 'Mauvaise', value: stats.health_poor || 0, color: COLORS.poor }
  ] : []

  if (loading || loadingStats) {
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
        <p className="text-gray-600 mt-2">Vue d'ensemble complète de vos plantes</p>
      </div>

      {/* Navigation Tabs */}
      <div className="flex gap-2 bg-gray-50 p-2 rounded-lg w-full">
        <button
          onClick={() => setActiveTab('overview')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all ${
            activeTab === 'overview'
              ? 'bg-white text-green-600 shadow-md'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <BarChart3 size={18} />
          Aperçu
        </button>
        <button
          onClick={() => setActiveTab('calendar')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all ${
            activeTab === 'calendar'
              ? 'bg-white text-green-600 shadow-md'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Calendar size={18} />
          Calendrier
        </button>
        <button
          onClick={() => setActiveTab('alerts')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all ${
            activeTab === 'alerts'
              ? 'bg-white text-green-600 shadow-md'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Bell size={18} />
          Alertes
        </button>
        <button
          onClick={() => setActiveTab('notifications')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all ${
            activeTab === 'notifications'
              ? 'bg-white text-green-600 shadow-md'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Zap size={18} />
          Notifications
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <>

      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <AlertCircle className="w-6 h-6 text-orange-600" />
          Actions Rapides
        </h2>
        
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
                <p className="text-sm text-green-700 font-semibold">Total Plantes</p>
                <p className="text-3xl font-bold text-green-900 mt-2">{stats?.total_plants || 0}</p>
                <p className="text-xs text-green-600 mt-1">dans votre collection</p>
              </div>
              <Leaf className="w-12 h-12 text-green-400 opacity-50" />
            </div>
          </div>
        </div>
      </div>

      {/* Smart Notifications Mini Section */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
            <Zap className="w-5 h-5 text-blue-600" />
            Tâches Prédites (7 prochains jours)
          </h2>
          <button
            onClick={() => setActiveTab('notifications')}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Voir tous →
          </button>
        </div>
        <div className="max-h-48 overflow-y-auto">
          <SmartNotifications days={7} />
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

      {/* SECTION 2: Listes Détaillées */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Droplet className="w-6 h-6 text-blue-600" />
          Détails des Soins
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Plants to Water */}
          <div className="bg-white rounded-lg shadow">
            <div className="bg-blue-600 text-white px-6 py-4 rounded-t-lg flex items-center gap-2">
              <Droplet className="w-5 h-5" />
              <h3 className="text-lg font-semibold">À Arroser</h3>
            </div>
            <div className="p-6">
              <PlantsToWaterList />
            </div>
          </div>

          {/* Plants to Fertilize */}
          <div className="bg-white rounded-lg shadow">
            <div className="bg-amber-600 text-white px-6 py-4 rounded-t-lg flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              <h3 className="text-lg font-semibold">À Fertiliser</h3>
            </div>
            <div className="p-6">
              <PlantsToFertilizeList />
            </div>
          </div>

          {/* Plants In Care */}
          <div className="bg-white rounded-lg shadow">
            <div className="bg-red-600 text-white px-6 py-4 rounded-t-lg flex items-center gap-2">
              <Heart className="w-5 h-5" />
              <h3 className="text-lg font-semibold">En Soin</h3>
            </div>
            <div className="p-6">
              <PlantsInCareList />
            </div>
          </div>
        </div>
      </div>

      {/* SECTION 3: Analytics & Statistiques */}
      {stats && (
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-purple-600" />
            Statistiques & Tendances
          </h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Pie Chart: Health Distribution */}
            {healthData.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">État de Santé Global</h3>
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

            {/* Bar Chart: Activity Last 30 Days */}
            {activityData.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Activité (30 derniers jours)</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={activityData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="watering" fill={COLORS.watering} name="Arrosages" />
                    <Bar dataKey="fertilizing" fill={COLORS.fertilizing} name="Fertilisations" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>

          {/* Health Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
            <div className="bg-white rounded-lg shadow p-6 border-l-4 border-cyan-500">
              <p className="text-gray-600 text-sm">Excellente Santé</p>
              <p className="text-3xl font-bold text-cyan-600 mt-2">{stats.health_excellent}</p>
              <p className="text-xs text-cyan-600 mt-1">✅ Plantes saines</p>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6 border-l-4 border-lime-500">
              <p className="text-gray-600 text-sm">Bonne Santé</p>
              <p className="text-3xl font-bold text-lime-600 mt-2">{stats.health_good}</p>
              <p className="text-xs text-lime-600 mt-1">↗️ En récupération</p>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6 border-l-4 border-amber-500">
              <p className="text-gray-600 text-sm">Mauvaise Santé</p>
              <p className="text-3xl font-bold text-amber-600 mt-2">{stats.health_poor}</p>
              <p className="text-xs text-amber-600 mt-1">🚨 Nécessitent attention</p>
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {total === 0 && !loading && (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-12 text-center">
          <div className="text-5xl mb-4">🌿</div>
          <h3 className="text-2xl font-bold text-green-800 mb-2">Parfait !</h3>
          <p className="text-green-700">Toutes vos plantes sont bien entretenues.</p>
          <p className="text-green-600 text-sm mt-2">Revenez bientôt pour de nouveaux soins à apporter.</p>
        </div>
      )}
      </>
      )}

      {/* Calendar Tab */}
      {activeTab === 'calendar' && (
        <CalendarView />
      )}

      {/* Alerts Tab */}
      {activeTab === 'alerts' && (
        <AlertsPanel />
      )}

      {/* Smart Notifications Tab */}
      {activeTab === 'notifications' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                <Zap className="w-6 h-6 text-blue-600" />
                Notifications Intelligentes
              </h2>
              <p className="text-gray-600 text-sm mt-1">Tâches prédites basées sur les fréquences saisonnières</p>
            </div>
            <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-2">
              <span className="text-sm text-gray-600">Période:</span>
              <select
                value={notificationsDays}
                onChange={(e) => setNotificationsDays(parseInt(e.target.value))}
                className="px-3 py-1 rounded border border-gray-300 focus:outline-none focus:border-blue-500 text-sm"
              >
                <option value={7}>7 jours</option>
                <option value={14}>14 jours</option>
                <option value={30}>30 jours</option>
                <option value={60}>60 jours</option>
              </select>
            </div>
          </div>
          <SmartNotifications days={notificationsDays} />
        </div>
      )}
    </div>
  )
}

