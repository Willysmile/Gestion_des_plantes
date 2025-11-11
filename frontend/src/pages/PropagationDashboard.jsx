import { useEffect, useState } from 'react';
import { useGetPropagations, useGetPropagationStats } from '../hooks/usePropagations';
import { useGetPlants } from '../hooks/usePlants';
import PropagationCard from '../components/propagation/PropagationCard';
import PropagationForm from '../components/propagation/PropagationForm';

const PropagationDashboard = () => {
  const { propagations, loading: loadingProps, fetch: fetchProps } = useGetPropagations();
  const { stats, fetch: fetchStats } = useGetPropagationStats();
  const { plants } = useGetPlants();
  
  const [showForm, setShowForm] = useState(false);
  const [filterStatus, setFilterStatus] = useState('');
  const [filterSource, setFilterSource] = useState('');

  useEffect(() => {
    fetchProps();
    fetchStats();
  }, []);

  const filteredProps = propagations.filter(p => {
    if (filterStatus && p.status !== filterStatus) return false;
    if (filterSource && p.source_type !== filterSource) return false;
    return true;
  });

  const statuses = [
    'pending', 'rooting', 'rooted', 'growing', 
    'ready-to-pot', 'potted', 'transplanted', 'established', 
    'failed', 'abandoned'
  ];

  const sources = ['cutting', 'seeds', 'division', 'offset'];

  const getStatusColor = (status) => {
    const colors = {
      'pending': 'bg-gray-100 text-gray-700',
      'rooting': 'bg-blue-100 text-blue-700',
      'rooted': 'bg-blue-200 text-blue-800',
      'growing': 'bg-green-100 text-green-700',
      'ready-to-pot': 'bg-yellow-100 text-yellow-700',
      'potted': 'bg-orange-100 text-orange-700',
      'transplanted': 'bg-purple-100 text-purple-700',
      'established': 'bg-green-200 text-green-800',
      'failed': 'bg-red-100 text-red-700',
      'abandoned': 'bg-gray-400 text-gray-700',
    };
    return colors[status] || 'bg-gray-100 text-gray-700';
  };

  const getParentPlantName = (parentId) => {
    return plants.find(p => p.id === parentId)?.name || `Plant #${parentId}`;
  };

  if (loadingProps && !propagations.length) {
    return <div className="p-6 text-center">Chargement...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Gestion des Boutures</h1>
          <p className="text-gray-600">Suivi des propagations de plantes</p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-gray-500 text-sm font-medium">Total</div>
              <div className="text-3xl font-bold text-gray-900">{stats.total}</div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-gray-500 text-sm font-medium">Taux de Succès</div>
              <div className="text-3xl font-bold text-green-600">{(stats.success_rate * 100).toFixed(0)}%</div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-gray-500 text-sm font-medium">Durée Moyenne</div>
              <div className="text-3xl font-bold text-blue-600">{stats.average_duration_days.toFixed(0)}j</div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-gray-500 text-sm font-medium">Par Statut</div>
              <div className="mt-2 space-y-1 text-sm">
                {Object.entries(stats.by_status).slice(0, 3).map(([status, count]) => (
                  <div key={status} className="flex justify-between">
                    <span className="text-gray-600">{status}:</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Filters & Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Statut</label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Tous les statuts</option>
                {statuses.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Source</label>
              <select
                value={filterSource}
                onChange={(e) => setFilterSource(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Toutes les sources</option>
                {sources.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={() => fetchProps()}
                className="w-full px-4 py-2 bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300 transition font-medium"
              >
                ↻ Rafraîchir
              </button>
            </div>

            <div className="flex items-end">
              <button
                onClick={() => setShowForm(true)}
                className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium"
              >
                ➕ Nouvelle Bouture
              </button>
            </div>
          </div>
        </div>

        {/* Form Modal */}
        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="sticky top-0 bg-white border-b p-6 flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900">Nouvelle Propagation</h2>
                <button
                  onClick={() => setShowForm(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              <div className="p-6">
                <PropagationForm
                  plants={plants}
                  onSuccess={() => {
                    setShowForm(false);
                    fetchProps();
                    fetchStats();
                  }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Propagations Grid */}
        {filteredProps.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProps.map(prop => (
              <PropagationCard
                key={prop.id}
                propagation={prop}
                parentPlantName={getParentPlantName(prop.parent_plant_id)}
                statusColor={getStatusColor(prop.status)}
              />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <div className="text-gray-400 text-lg mb-2">Aucune propagation trouvée</div>
            <p className="text-gray-500 mb-6">Commencez par créer une nouvelle bouture</p>
            <button
              onClick={() => setShowForm(true)}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
            >
              ➕ Créer une Bouture
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PropagationDashboard;
