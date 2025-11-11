import { useNavigate } from 'react-router-dom';
import { useUpdatePropagation } from '../../hooks/usePropagations';

const PropagationCard = ({ propagation, parentPlantName, statusColor }) => {
  const navigate = useNavigate();
  const { update } = useUpdatePropagation();

  const handleStatusChange = async (newStatus) => {
    try {
      await update(propagation.id, { status: newStatus });
      // Trigger parent refresh
      window.location.reload();
    } catch (error) {
      console.error('Erreur mise à jour statut:', error);
      alert('Erreur lors de la mise à jour du statut');
    }
  };

  const progressPercent = Math.min(
    ((propagation.days_since_propagation || 0) / (propagation.expected_duration_days || 1)) * 100,
    100
  );

  const daysRemaining = Math.max(
    (propagation.expected_duration_days || 0) - (propagation.days_since_propagation || 0),
    0
  );

  // Déterminer les transitions valides selon l'état actuel
  const getNextValidStatus = () => {
    const statusFlow = {
      'pending': 'rooting',
      'rooting': 'rooted',
      'rooted': 'growing',
      'growing': 'ready-to-pot',
      'ready-to-pot': 'potted',
      'potted': 'transplanted',
      'transplanted': 'established',
      'established': null,
      'failed': null,
      'abandoned': null,
    };
    return statusFlow[propagation.status] || null;
  };

  const nextStatus = getNextValidStatus();

  return (
    <div className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer" onClick={() => navigate(`/propagations/${propagation.id}`)}>
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-t-lg">
        <div className="flex justify-between items-start mb-2">
          <div>
            <div className="font-semibold">{parentPlantName}</div>
            <div className="text-sm opacity-90">{propagation.source_type} · {propagation.method}</div>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColor}`}>
            {propagation.status}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Progression</span>
            <span className="text-sm text-gray-500">{progressPercent.toFixed(0)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <div className="text-xs text-gray-500 mb-1">Jours écoulés</div>
            <div className="text-lg font-bold text-gray-900">{propagation.days_since_propagation}</div>
          </div>
          <div>
            <div className="text-xs text-gray-500 mb-1">Jours restants</div>
            <div className="text-lg font-bold text-gray-900">{daysRemaining}</div>
          </div>
          <div>
            <div className="text-xs text-gray-500 mb-1">Durée estimée</div>
            <div className="text-lg font-bold text-gray-900">{propagation.expected_duration_days}j</div>
          </div>
          <div>
            <div className="text-xs text-gray-500 mb-1">Succès estimé</div>
            <div className="text-lg font-bold text-green-600">{Math.round((propagation.success_rate_estimate || 0) * 100)}%</div>
          </div>
        </div>

        {/* Dates */}
        <div className="bg-gray-50 rounded p-3 mb-4 text-sm">
          <div className="flex justify-between mb-2">
            <span className="text-gray-600">Démarrage:</span>
            <span className="font-medium">{new Date(propagation.propagation_date).toLocaleDateString('fr-FR')}</span>
          </div>
          {propagation.expected_ready && (
            <div className="flex justify-between mb-2">
              <span className="text-gray-600">Prévu:</span>
              <span className={`font-medium ${propagation.is_overdue ? 'text-red-600' : 'text-gray-900'}`}>
                {new Date(propagation.expected_ready).toLocaleDateString('fr-FR')}
                {propagation.is_overdue && ' ⚠️'}
              </span>
            </div>
          )}
          {propagation.success_date && (
            <div className="flex justify-between">
              <span className="text-gray-600">Succès:</span>
              <span className="font-medium text-green-600">{new Date(propagation.success_date).toLocaleDateString('fr-FR')}</span>
            </div>
          )}
        </div>

        {/* Notes */}
        {propagation.notes && (
          <div className="mb-4 p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded">
            <div className="text-sm text-yellow-700">{propagation.notes}</div>
          </div>
        )}

        {/* Quick Status Change */}
        {nextStatus && (
          <div className="flex gap-2">
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleStatusChange(nextStatus);
              }}
              className="flex-1 px-3 py-2 bg-blue-100 text-blue-700 text-sm font-medium rounded hover:bg-blue-200 transition"
            >
              → {nextStatus}
            </button>
            {!['established', 'failed', 'abandoned'].includes(propagation.status) && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleStatusChange('failed');
                }}
                className="flex-1 px-3 py-2 bg-red-100 text-red-700 text-sm font-medium rounded hover:bg-red-200 transition"
              >
                Échoué
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default PropagationCard;
