import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import api from '../lib/api'
import {
  AuditDailyActivityChart,
  AuditEntityBreakdownChart,
  AuditUserActivityChart,
  AuditActionByEntityChart,
} from '../components/AuditCharts'

export default function AuditDashboardPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  // Stats
  const [statsLoading, setStatsLoading] = useState(false)
  const [statsError, setStatsError] = useState(null)
  const [dailyActivity, setDailyActivity] = useState([])
  const [entityBreakdown, setEntityBreakdown] = useState([])
  const [userActivity, setUserActivity] = useState([])
  const [actionByEntity, setActionByEntity] = useState([])
  const [showStats, setShowStats] = useState(false)
  
  // Filtres
  const [filterType, setFilterType] = useState(searchParams.get('type') || 'all')
  const [filterAction, setFilterAction] = useState(searchParams.get('action') || 'all')
  const [filterDays, setFilterDays] = useState(searchParams.get('days') || '7')
  const [searchEntity, setSearchEntity] = useState(searchParams.get('entity') || '')
  
  // Pagination
  const [limit, setLimit] = useState(50)
  const [selectedLog, setSelectedLog] = useState(null)

  // Charger les logs
  useEffect(() => {
    console.log('📋 AuditDashboardPage mounted, loading logs...')
    loadLogs()
  }, [filterType, filterAction, filterDays, searchEntity])

  // Charger les stats
  useEffect(() => {
    if (showStats) {
      loadStats()
    }
  }, [showStats, filterDays])

  const loadStats = async () => {
    setStatsLoading(true)
    setStatsError(null)
    try {
      const days = filterDays === 'all' ? 365 : parseInt(filterDays)
      
      // Charger les 4 stats en parallèle
      const [dailyRes, entityRes, userRes, actionRes] = await Promise.all([
        api.get(`/audit/stats/daily-activity?days=${days}`),
        api.get(`/audit/stats/entity-breakdown?days=${days}`),
        api.get(`/audit/stats/user-activity?limit=10&days=${days}`),
        api.get(`/audit/stats/action-by-entity?days=${days}`),
      ])

      setDailyActivity(dailyRes.data || [])
      setEntityBreakdown(entityRes.data || [])
      setUserActivity(userRes.data || [])
      setActionByEntity(actionRes.data || [])
    } catch (err) {
      let errorMsg = 'Erreur lors du chargement des statistiques'
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string' ? err.response.data.detail : JSON.stringify(err.response.data.detail)
      } else if (err.message) {
        errorMsg = err.message
      }
      setStatsError(errorMsg)
    } finally {
      setStatsLoading(false)
    }
  }

  const loadLogs = async () => {
    console.log('🔍 loadLogs called')
    setLoading(true)
    setError(null)
    try {
      let url = '/audit/logs'
      const params = new URLSearchParams()
      params.append('limit', limit)

      // Déterminer l'endpoint basé sur les filtres
      if (filterDays !== 'all' && filterDays !== 'custom') {
        url = `/audit/logs/recent?days=${filterDays}`
      } else if (filterAction !== 'all') {
        url = `/audit/logs/action/${filterAction}`
      } else if (filterType !== 'all' && searchEntity) {
        url = `/audit/logs/entity/${filterType}/${searchEntity}`
      }

      console.log('📡 Fetching from:', url)
      const response = await api.get(url, { params })
      console.log('✅ Got response:', response.data)
      setLogs(response.data)
    } catch (err) {
      console.error('❌ Error loading logs:', err)
      let errorMsg = 'Erreur de chargement'
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string' ? err.response.data.detail : JSON.stringify(err.response.data.detail)
      } else if (err.message) {
        errorMsg = err.message
      }
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = () => {
    setSearchParams({
      type: filterType,
      action: filterAction,
      days: filterDays,
      entity: searchEntity,
    })
  }

  const handleCleanup = async () => {
    if (!window.confirm('Supprimer tous les logs?')) return
    
    try {
      setLoading(true)
      const res = await api.delete('/audit/logs/cleanup')
      let successMsg = 'Logs supprimés avec succès'
      if (res.data?.message) {
        successMsg = res.data.message
      }
      setError(successMsg)
      loadLogs()
    } catch (err) {
      let errorMsg = 'Erreur de suppression'
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string' ? err.response.data.detail : JSON.stringify(err.response.data.detail)
      } else if (err.message) {
        errorMsg = err.message
      }
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleString('fr-FR')
  }

  const getActionBadgeColor = (action) => {
    switch (action) {
      case 'INSERT':
        return 'bg-green-100 text-green-800'
      case 'UPDATE':
        return 'bg-blue-100 text-blue-800'
      case 'DELETE':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getActionLabel = (action) => {
    const labels = {
      'INSERT': '✨ Création',
      'UPDATE': '📝 Modification',
      'DELETE': '🗑️ Suppression'
    }
    return labels[action] || action
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4 sm:p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
                📋 Historique d'Audit
              </h1>
              <p className="text-slate-600 mt-2">Suivi complet de tous les changements</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => setShowStats(!showStats)}
                className={`px-4 py-2 rounded-lg transition font-medium ${
                  showStats
                    ? 'bg-purple-600 text-white hover:bg-purple-700'
                    : 'bg-purple-100 text-purple-800 hover:bg-purple-200'
                }`}
              >
                📊 {showStats ? 'Masquer' : 'Afficher'} Stats
              </button>
              <button
                onClick={handleCleanup}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition font-medium"
                disabled={loading}
              >
                🗑️ Nettoyer logs
              </button>
            </div>
          </div>

          {/* Filtres */}
          <div className="bg-slate-50 rounded-lg p-4 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Action Filter */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Action
                </label>
                <select
                  value={filterAction}
                  onChange={(e) => setFilterAction(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Toutes les actions</option>
                  <option value="INSERT">✨ Création</option>
                  <option value="UPDATE">📝 Modification</option>
                  <option value="DELETE">🗑️ Suppression</option>
                </select>
              </div>

              {/* Type Filter */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Type d'entité
                </label>
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Tous les types</option>
                  <option value="Plant">🌱 Plantes</option>
                  <option value="Photo">📸 Photos</option>
                  <option value="WateringHistory">💧 Arrosage</option>
                  <option value="FertilizingHistory">🌿 Fertilisation</option>
                </select>
              </div>

              {/* Period Filter */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Période
                </label>
                <select
                  value={filterDays}
                  onChange={(e) => setFilterDays(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="1">Dernier jour</option>
                  <option value="7">Dernière semaine</option>
                  <option value="30">Dernier mois</option>
                  <option value="90">Dernier trimestre</option>
                  <option value="all">Tous les logs</option>
                </select>
              </div>

              {/* Search Entity */}
              {filterType !== 'all' && (
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    ID Entité (optionnel)
                  </label>
                  <input
                    type="number"
                    value={searchEntity}
                    onChange={(e) => setSearchEntity(e.target.value)}
                    placeholder="Ex: 1, 2, 3..."
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              )}
            </div>

            <button
              onClick={handleFilterChange}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
              disabled={loading}
            >
              {loading ? '⏳ Chargement...' : '🔍 Appliquer filtres'}
            </button>
          </div>
        </div>

        {/* Messages */}
        {error && (
          <div className={`rounded-lg p-4 mb-6 ${error.includes('succès') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
            {error}
          </div>
        )}

        {statsError && (
          <div className="rounded-lg p-4 mb-6 bg-red-100 text-red-800">
            Erreur statistiques temporairement désactivées
          </div>
        )}

        {/* Stats Section - TEMPORAIREMENT DÉSACTIVÉ */}
        {false && showStats && (
          <div className="mb-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              {/* Daily Activity Chart */}
              <AuditDailyActivityChart 
                data={dailyActivity} 
                isLoading={statsLoading}
              />

              {/* Entity Breakdown Chart */}
              <AuditEntityBreakdownChart 
                data={entityBreakdown} 
                isLoading={statsLoading}
              />

              {/* User Activity Chart */}
              <AuditUserActivityChart 
                data={userActivity} 
                isLoading={statsLoading}
              />

              {/* Action by Entity Chart */}
              <AuditActionByEntityChart 
                data={actionByEntity} 
                isLoading={statsLoading}
              />
            </div>
          </div>
        )}

        {/* Timeline */}
        <div className="space-y-4">
          {loading && !logs.length ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-slate-600">Chargement des logs...</p>
            </div>
          ) : logs.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-slate-600">Aucun log d'audit trouvé</p>
            </div>
          ) : (
            <>
              <div className="text-sm text-slate-600 mb-4">
                📊 {logs.length} logs affichés
              </div>
              {logs.map((log, idx) => (
                <div
                  key={log.id || idx}
                  className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer"
                  onClick={() => setSelectedLog(selectedLog?.id === log.id ? null : log)}
                >
                  {/* Log Header */}
                  <div className="p-4 sm:p-6 flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getActionBadgeColor(log.action)}`}>
                          {getActionLabel(log.action)}
                        </span>
                        <span className="px-3 py-1 bg-slate-200 text-slate-800 rounded-full text-sm font-medium">
                          {log.entity_type}
                        </span>
                        <span className="text-slate-500 text-sm">
                          ID: {log.entity_id}
                        </span>
                      </div>

                      <p className="text-slate-900 font-medium mb-2">
                        {log.description}
                      </p>

                      <div className="flex flex-wrap gap-3 text-sm text-slate-500">
                        <span>📅 {formatDate(log.created_at)}</span>
                        {log.user_id && <span>👤 User #{log.user_id}</span>}
                        {log.ip_address && <span>🌐 {log.ip_address}</span>}
                      </div>
                    </div>

                    <div className="text-slate-400 ml-4">
                      {selectedLog?.id === log.id ? '▼' : '▶'}
                    </div>
                  </div>

                  {/* Log Details - Expanded */}
                  {selectedLog?.id === log.id && (
                    <div className="border-t border-slate-200 p-4 sm:p-6 bg-slate-50 space-y-4">
                      {/* Field Change (UPDATE) */}
                      {log.field_name && (
                        <div className="bg-white rounded p-4 border-l-4 border-blue-500">
                          <h4 className="font-semibold text-slate-900 mb-3">
                            Champ modifié: <span className="text-blue-600">{log.field_name}</span>
                          </h4>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                              <p className="text-sm text-slate-600 mb-1">❌ Ancienne valeur</p>
                              <pre className="bg-red-50 text-red-800 p-3 rounded text-xs overflow-x-auto">
                                {typeof log.old_value === 'string' 
                                  ? log.old_value 
                                  : JSON.stringify(log.old_value, null, 2)}
                              </pre>
                            </div>
                            <div>
                              <p className="text-sm text-slate-600 mb-1">✅ Nouvelle valeur</p>
                              <pre className="bg-green-50 text-green-800 p-3 rounded text-xs overflow-x-auto">
                                {typeof log.new_value === 'string'
                                  ? log.new_value
                                  : JSON.stringify(log.new_value, null, 2)}
                              </pre>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* All Changes (INSERT/DELETE) */}
                      {log.raw_changes && Object.keys(log.raw_changes).length > 0 && (
                        <div className="bg-white rounded p-4 border-l-4 border-slate-500">
                          <h4 className="font-semibold text-slate-900 mb-3">
                            📦 Tous les changements
                          </h4>
                          <pre className="bg-slate-100 text-slate-800 p-3 rounded text-xs overflow-x-auto max-h-64">
                            {JSON.stringify(log.raw_changes, null, 2)}
                          </pre>
                        </div>
                      )}

                      {/* Metadata */}
                      <div className="bg-white rounded p-4 border-l-4 border-slate-400">
                        <h4 className="font-semibold text-slate-900 mb-3">
                          📌 Métadonnées
                        </h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
                          <div>
                            <p className="text-slate-600">ID Log: <span className="font-mono text-slate-900">{log.id}</span></p>
                            <p className="text-slate-600 mt-1">Action: <span className="font-mono text-slate-900">{log.action}</span></p>
                          </div>
                          <div>
                            <p className="text-slate-600">Entity: <span className="font-mono text-slate-900">{log.entity_type} #{log.entity_id}</span></p>
                            {log.user_agent && (
                              <p className="text-slate-600 mt-1">User Agent: <span className="font-mono text-xs text-slate-900">{log.user_agent}</span></p>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  )
}
