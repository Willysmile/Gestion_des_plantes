import React, { useState, useEffect } from 'react';
import { AlertTriangle, AlertCircle, AlertOctagon, CheckCircle, RefreshCw, X, Clock } from 'lucide-react';
import { getAdvancedAlerts } from '../utils/api';

export default function AlertsPanel() {
  const [alerts, setAlerts] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expandedSeverity, setExpandedSeverity] = useState('critical');
  const [dismissedAlerts, setDismissedAlerts] = useState(new Set());
  const [snoozedAlerts, setSnoozedAlerts] = useState(new Map());

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const data = await getAdvancedAlerts();
      setAlerts(data.alerts || []);
      setSummary(data.summary || {});
    } catch (error) {
      console.error('Erreur chargement alertes:', error);
      setAlerts([]);
      setSummary({});
    } finally {
      setLoading(false);
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return <AlertOctagon size={20} className="text-red-600" />;
      case 'high':
        return <AlertTriangle size={20} className="text-orange-600" />;
      case 'medium':
        return <AlertCircle size={20} className="text-yellow-600" />;
      case 'low':
        return <CheckCircle size={20} className="text-green-600" />;
      default:
        return null;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 border-red-200 hover:bg-red-100';
      case 'high':
        return 'bg-orange-50 border-orange-200 hover:bg-orange-100';
      case 'medium':
        return 'bg-yellow-50 border-yellow-200 hover:bg-yellow-100';
      case 'low':
        return 'bg-green-50 border-green-200 hover:bg-green-100';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  const getSeverityLabel = (severity) => {
    switch (severity) {
      case 'critical':
        return 'CRITIQUE';
      case 'high':
        return 'Élevé';
      case 'medium':
        return 'Moyen';
      case 'low':
        return 'Faible';
      default:
        return severity;
    }
  };

  const severityOrder = ['critical', 'high', 'medium', 'low'];

  const groupedAlerts = {
    critical: alerts.filter(a => a.severity === 'critical'),
    high: alerts.filter(a => a.severity === 'high'),
    medium: alerts.filter(a => a.severity === 'medium'),
    low: alerts.filter(a => a.severity === 'low')
  };

  // Filtrer les alertes snooze et dismiss
  const filteredAlerts = alerts.filter(alert => {
    if (dismissedAlerts.has(alert.id)) return false;
    
    const snoozedUntil = snoozedAlerts.get(alert.id);
    if (snoozedUntil && new Date() < snoozedUntil) return false;
    
    return true;
  });

  const filteredGroupedAlerts = {
    critical: filteredAlerts.filter(a => a.severity === 'critical'),
    high: filteredAlerts.filter(a => a.severity === 'high'),
    medium: filteredAlerts.filter(a => a.severity === 'medium'),
    low: filteredAlerts.filter(a => a.severity === 'low')
  };

  const handleMarkAsRead = (alertId) => {
    setDismissedAlerts(new Set([...dismissedAlerts, alertId]));
  };

  const handleSnooze = (alertId, minutes = 60) => {
    const snoozeUntil = new Date(Date.now() + minutes * 60000);
    setSnoozedAlerts(new Map(snoozedAlerts).set(alertId, snoozeUntil));
  };

  const handleTakeAction = (alert) => {
    // TODO: Implémenter action (arroser, fertiliser, etc.)
    console.log('Action:', alert.action, 'pour plante:', alert.plant_id);
    // Après l'action, marquer comme lu
    handleMarkAsRead(alert.id);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">🔔 Alertes Avancées</h2>
        <button
          onClick={fetchAlerts}
          disabled={loading}
          className="p-2 hover:bg-gray-200 rounded-lg transition-colors disabled:opacity-50"
          title="Actualiser"
        >
          <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      {/* Résumé des alertes */}
      {summary && (
        <div className="grid grid-cols-4 gap-4 mb-6 bg-gray-50 p-4 rounded-lg">
          <div
            className="cursor-pointer hover:bg-white rounded transition-colors p-2"
            onClick={() => setExpandedSeverity('critical')}
          >
            <p className="text-sm text-gray-600">🔴 Critique</p>
            <p className="text-2xl font-bold text-red-600">{filteredGroupedAlerts.critical.length}</p>
          </div>
          <div
            className="cursor-pointer hover:bg-white rounded transition-colors p-2"
            onClick={() => setExpandedSeverity('high')}
          >
            <p className="text-sm text-gray-600">🟠 Élevé</p>
            <p className="text-2xl font-bold text-orange-600">{filteredGroupedAlerts.high.length}</p>
          </div>
          <div
            className="cursor-pointer hover:bg-white rounded transition-colors p-2"
            onClick={() => setExpandedSeverity('medium')}
          >
            <p className="text-sm text-gray-600">🟡 Moyen</p>
            <p className="text-2xl font-bold text-yellow-600">{filteredGroupedAlerts.medium.length}</p>
          </div>
          <div
            className="cursor-pointer hover:bg-white rounded transition-colors p-2"
            onClick={() => setExpandedSeverity('low')}
          >
            <p className="text-sm text-gray-600">🟢 Faible</p>
            <p className="text-2xl font-bold text-green-600">{filteredGroupedAlerts.low.length}</p>
          </div>
        </div>
      )}

      {/* Alertes groupées par sévérité */}
      {loading ? (
        <div className="text-center py-8">
          <p className="text-gray-500">Chargement des alertes...</p>
        </div>
      ) : filteredAlerts.length === 0 ? (
        <div className="text-center py-8 bg-green-50 rounded-lg">
          <CheckCircle size={48} className="mx-auto text-green-600 mb-2" />
          <p className="text-green-700 font-semibold">Aucune alerte ! 🎉</p>
          <p className="text-green-600 text-sm">Toutes vos plantes vont bien</p>
        </div>
      ) : (
        <div className="space-y-6">
          {severityOrder.map(severity => {
            const severityAlerts = filteredGroupedAlerts[severity];
            if (severityAlerts.length === 0) return null;

            const isExpanded = expandedSeverity === severity;

            return (
              <div key={severity} className="border rounded-lg overflow-hidden">
                {/* Header de la section */}
                <button
                  onClick={() => setExpandedSeverity(isExpanded ? null : severity)}
                  className={`w-full p-4 flex items-center justify-between ${
                    getSeverityColor(severity)
                  } border transition-all`}
                >
                  <div className="flex items-center gap-3">
                    {getSeverityIcon(severity)}
                    <div className="text-left">
                      <p className="font-semibold">{getSeverityLabel(severity)}</p>
                      <p className="text-sm opacity-75">
                        {severityAlerts.length} alerte{severityAlerts.length > 1 ? 's' : ''}
                      </p>
                    </div>
                  </div>
                  <span className="text-lg font-bold">
                    {isExpanded ? '−' : '+'}
                  </span>
                </button>

                {/* Contenu de la section */}
                {isExpanded && (
                  <div className="bg-gray-50 p-4 space-y-3">
                    {severityAlerts.map(alert => {
                      const isSnoozed = snoozedAlerts.has(alert.id) && new Date() < snoozedAlerts.get(alert.id);
                      const isDismissed = dismissedAlerts.has(alert.id);
                      
                      if (isDismissed) return null;
                      
                      return (
                      <div
                        key={alert.id}
                        className={`p-4 rounded-lg border-l-4 flex items-start justify-between ${
                          isSnoozed ? 'opacity-60 bg-gray-100' : getSeverityColor(severity)
                        }`}
                      >
                        <div className="flex-1">
                          <div className="flex items-start gap-2">
                            <p className="font-semibold text-gray-900 flex-1">
                              {alert.plant_name}
                            </p>
                            <button
                              onClick={() => handleMarkAsRead(alert.id)}
                              className="text-gray-400 hover:text-gray-600 transition-colors"
                              title="Fermer"
                            >
                              <X size={16} />
                            </button>
                          </div>
                          <p className="text-sm text-gray-700 mt-1">
                            {alert.message}
                          </p>
                          {alert.date && (
                            <p className="text-xs text-gray-500 mt-2">
                              Depuis: {new Date(alert.date).toLocaleDateString('fr-FR')}
                            </p>
                          )}
                          {isSnoozed && (
                            <p className="text-xs text-blue-600 mt-2 flex items-center gap-1">
                              <Clock size={12} />
                              Masquée temporairement
                            </p>
                          )}
                        </div>

                        {/* Actions */}
                        <div className="ml-4 flex gap-2 flex-shrink-0">
                          {!isSnoozed && alert.action !== 'none' && (
                            <button
                              onClick={() => handleTakeAction(alert)}
                              className={`px-3 py-2 rounded font-medium text-sm whitespace-nowrap transition-all ${
                                severity === 'critical'
                                  ? 'bg-red-600 text-white hover:bg-red-700'
                                  : severity === 'high'
                                  ? 'bg-orange-600 text-white hover:bg-orange-700'
                                  : severity === 'medium'
                                  ? 'bg-yellow-600 text-white hover:bg-yellow-700'
                                  : 'bg-gray-400 text-white hover:bg-gray-500'
                              }`}
                            >
                              {alert.action === 'water' && '💧'}
                              {alert.action === 'fertilize' && '🥗'}
                              {alert.action === 'check' && '👀'}
                            </button>
                          )}
                          {!isSnoozed && (
                            <button
                              onClick={() => handleSnooze(alert.id, 60)}
                              className="px-3 py-2 rounded font-medium text-sm bg-gray-300 text-gray-800 hover:bg-gray-400 transition-all"
                              title="Masquer pendant 1h"
                            >
                              <Clock size={16} />
                            </button>
                          )}
                        </div>
                      </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Footer */}
      <div className="mt-6 pt-6 border-t text-xs text-gray-500">
        <p>
          🔄 Les alertes sont calculées en temps réel basé sur l'historique des soins
        </p>
      </div>
    </div>
  );
}
