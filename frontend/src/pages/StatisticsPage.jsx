import { useState } from 'react';
import { useGetPropagationStats, useGetOverduePropagations } from '../hooks/usePropagations';

const StatisticsPage = () => {
  const { data: stats } = useGetPropagationStats();
  const { data: overdue } = useGetOverduePropagations();

  const statusColors = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'rooting': 'bg-blue-100 text-blue-800',
    'rooted': 'bg-green-100 text-green-800',
    'growing': 'bg-green-100 text-green-800',
    'ready-to-pot': 'bg-lime-100 text-lime-800',
    'potted': 'bg-emerald-100 text-emerald-800',
    'transplanted': 'bg-teal-100 text-teal-800',
    'established': 'bg-green-200 text-green-800',
    'failed': 'bg-red-100 text-red-800',
    'abandoned': 'bg-gray-100 text-gray-800',
  };

  if (!stats) {
    return <div className="p-6">Chargement des statistiques...</div>;
  }

  // Calculer les taux
  const successRate = stats.total > 0
    ? Math.round((stats.success_count / stats.total) * 100)
    : 0;

  const failureRate = stats.total > 0
    ? Math.round((stats.failed_count / stats.total) * 100)
    : 0;

  // Données pour les graphiques
  const statusChartData = [
    { name: 'En attente', value: stats.status_distribution?.pending || 0, color: '#fcd34d' },
    { name: 'Enracinement', value: stats.status_distribution?.rooting || 0, color: '#93c5fd' },
    { name: 'Enraciné', value: stats.status_distribution?.rooted || 0, color: '#86efac' },
    { name: 'Croissance', value: stats.status_distribution?.growing || 0, color: '#86efac' },
    { name: 'Prêt à pot', value: stats.status_distribution?.['ready-to-pot'] || 0, color: '#bfef45' },
    { name: 'Empotté', value: stats.status_distribution?.potted || 0, color: '#a3f0b5' },
    { name: 'Repiqué', value: stats.status_distribution?.transplanted || 0, color: '#7dd3fc' },
    { name: 'Établi', value: stats.status_distribution?.established || 0, color: '#4ade80' },
    { name: 'Échoué', value: stats.failed_count || 0, color: '#fca5a5' },
  ];

  const methodStats = Object.entries(stats.method_statistics || {}).map(([method, data]) => ({
    method,
    count: data.count || 0,
    successRate: data.success_rate || 0,
    avgDuration: Math.round(data.avg_duration || 0),
  }));

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Statistiques des Propagations</h1>
          <p className="text-gray-600 mt-2">Analyse complète de votre activité de propagation</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm font-semibold">TOTAL PROPAGATIONS</p>
            <p className="text-4xl font-bold text-gray-900 mt-2">{stats.total}</p>
            <p className="text-gray-500 text-xs mt-2">Toutes les propagations</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm font-semibold">TAUX DE RÉUSSITE</p>
            <p className="text-4xl font-bold text-green-600 mt-2">{successRate}%</p>
            <p className="text-gray-500 text-xs mt-2">{stats.success_count} réussies</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm font-semibold">DURÉE MOYENNE</p>
            <p className="text-4xl font-bold text-blue-600 mt-2">
              {Math.round(stats.avg_propagation_time)}j
            </p>
            <p className="text-gray-500 text-xs mt-2">Pour établissement</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm font-semibold">EN COURS</p>
            <p className="text-4xl font-bold text-yellow-600 mt-2">
              {(stats.total - stats.success_count - stats.failed_count - stats.abandoned_count) || 0}
            </p>
            <p className="text-gray-500 text-xs mt-2">Propagations actives</p>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Status Distribution */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Distribution par Statut</h2>
            <div className="space-y-4">
              {statusChartData.filter(item => item.value > 0).map(item => (
                <div key={item.name}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">{item.name}</span>
                    <span className="text-sm font-bold text-gray-900">{item.value}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all"
                      style={{
                        width: `${(item.value / stats.total) * 100}%`,
                        backgroundColor: item.color,
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Success vs Failure */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Réussite vs Échecs</h2>
            <div className="flex items-center justify-center h-64">
              <div className="relative w-48 h-48 rounded-full border-8" style={{ borderColor: '#e5e7eb' }}>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-3xl font-bold text-green-600">{successRate}%</p>
                    <p className="text-sm text-gray-600">Réussite</p>
                  </div>
                </div>
                <svg className="w-full h-full transform -rotate-90">
                  <circle
                    cx="50%"
                    cy="50%"
                    r="95"
                    fill="none"
                    stroke="#4ade80"
                    strokeWidth="8"
                    strokeDasharray={`${(successRate / 100) * 597} 597`}
                  />
                  <circle
                    cx="50%"
                    cy="50%"
                    r="95"
                    fill="none"
                    stroke="#fca5a5"
                    strokeWidth="8"
                    strokeDasharray={`${(failureRate / 100) * 597} 597`}
                    style={{
                      strokeDashoffset: `-${(successRate / 100) * 597}`,
                    }}
                  />
                </svg>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 mt-6 text-center">
              <div>
                <p className="text-2xl font-bold text-green-600">{stats.success_count}</p>
                <p className="text-sm text-gray-600">Réussies</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-red-600">{stats.failed_count}</p>
                <p className="text-sm text-gray-600">Échouées</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-600">{stats.abandoned_count}</p>
                <p className="text-sm text-gray-600">Abandonnées</p>
              </div>
            </div>
          </div>
        </div>

        {/* Method Statistics */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Statistiques par Méthode</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Méthode</th>
                  <th className="px-6 py-3 text-center text-sm font-semibold text-gray-700">Nombre</th>
                  <th className="px-6 py-3 text-center text-sm font-semibold text-gray-700">Taux Réussite</th>
                  <th className="px-6 py-3 text-center text-sm font-semibold text-gray-700">Durée Moyenne</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {methodStats.length > 0 ? (
                  methodStats.map(method => (
                    <tr key={method.method} className="hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900">
                        {method.method}
                      </td>
                      <td className="px-6 py-4 text-center text-sm text-gray-600">
                        {method.count}
                      </td>
                      <td className="px-6 py-4 text-center text-sm">
                        <span className="font-semibold text-green-600">
                          {Math.round(method.successRate)}%
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center text-sm text-gray-600">
                        {method.avgDuration}j
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="px-6 py-4 text-center text-gray-500">
                      Pas de données disponibles
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Overdue Alerts */}
        {overdue && overdue.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <span className="text-red-600">⚠️</span> Propagations en Retard
            </h2>
            <div className="space-y-4">
              {overdue.map(prop => (
                <div
                  key={prop.id}
                  className="p-4 border border-red-200 bg-red-50 rounded-lg"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold text-gray-900">
                        {prop.parent_plant_name}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {prop.source_type} - {prop.method}
                      </p>
                      <p className="text-sm text-red-600 mt-2">
                        Dépassé de {Math.max(0, Math.ceil((Date.now() - new Date(prop.expected_ready)) / (1000 * 60 * 60 * 24)))}j
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      statusColors[prop.status] || 'bg-gray-100'
                    }`}>
                      {prop.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatisticsPage;
