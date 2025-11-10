/**
 * Composant pour afficher les changements d'audit avec diff visuel
 */

export function AuditDiffViewer({ oldValue, newValue, fieldName }) {
  const formatValue = (value) => {
    if (typeof value === 'string') {
      try {
        return JSON.stringify(JSON.parse(value), null, 2)
      } catch {
        return value
      }
    }
    return JSON.stringify(value, null, 2)
  }

  const oldStr = formatValue(oldValue)
  const newStr = formatValue(newValue)

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Old Value */}
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="inline-block w-3 h-3 bg-red-500 rounded-full"></span>
            <span className="font-semibold text-red-700">Ancienne valeur</span>
          </div>
          <pre className="bg-red-50 border-l-4 border-red-500 text-red-900 p-3 rounded text-xs overflow-x-auto max-h-48">
            {oldStr || 'null'}
          </pre>
        </div>

        {/* New Value */}
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="inline-block w-3 h-3 bg-green-500 rounded-full"></span>
            <span className="font-semibold text-green-700">Nouvelle valeur</span>
          </div>
          <pre className="bg-green-50 border-l-4 border-green-500 text-green-900 p-3 rounded text-xs overflow-x-auto max-h-48">
            {newStr || 'null'}
          </pre>
        </div>
      </div>
    </div>
  )
}

/**
 * Composant pour afficher les logs d'audit en format timeline
 */
export function AuditTimeline({ logs }) {
  const getActionColor = (action) => {
    switch (action) {
      case 'INSERT':
        return 'border-green-500 bg-green-50'
      case 'UPDATE':
        return 'border-blue-500 bg-blue-50'
      case 'DELETE':
        return 'border-red-500 bg-red-50'
      default:
        return 'border-gray-500 bg-gray-50'
    }
  }

  const getActionIcon = (action) => {
    switch (action) {
      case 'INSERT':
        return '✨'
      case 'UPDATE':
        return '📝'
      case 'DELETE':
        return '🗑️'
      default:
        return '📋'
    }
  }

  return (
    <div className="space-y-4">
      {logs.map((log, idx) => (
        <div
          key={log.id || idx}
          className={`border-l-4 p-4 rounded-r-lg ${getActionColor(log.action)}`}
        >
          <div className="flex items-start gap-3">
            <span className="text-2xl mt-1">{getActionIcon(log.action)}</span>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="font-semibold text-slate-900">{log.description}</h3>
                <span className="text-xs text-slate-600">
                  {log.entity_type} #{log.entity_id}
                </span>
              </div>
              <p className="text-xs text-slate-600">
                {new Date(log.created_at).toLocaleString('fr-FR')}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

/**
 * Composant pour afficher les statistiques d'audit
 */
export function AuditStats({ logs }) {
  const stats = {
    insert: logs.filter(l => l.action === 'INSERT').length,
    update: logs.filter(l => l.action === 'UPDATE').length,
    delete: logs.filter(l => l.action === 'DELETE').length,
  }

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
        <p className="text-sm text-green-700 font-semibold">✨ Créations</p>
        <p className="text-2xl font-bold text-green-900">{stats.insert}</p>
      </div>
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
        <p className="text-sm text-blue-700 font-semibold">📝 Modifications</p>
        <p className="text-2xl font-bold text-blue-900">{stats.update}</p>
      </div>
      <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
        <p className="text-sm text-red-700 font-semibold">🗑️ Suppressions</p>
        <p className="text-2xl font-bold text-red-900">{stats.delete}</p>
      </div>
    </div>
  )
}
