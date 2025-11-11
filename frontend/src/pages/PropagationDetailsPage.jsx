import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  useGetPropagation,
  useUpdatePropagation,
  useDeletePropagation,
  useGetPropagationEvents,
  useAddPropagationEvent,
} from '../hooks/usePropagations';
import PropagationForm from '../components/propagation/PropagationForm';

const PropagationDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { propagation, loading: propLoading, error: propError } = useGetPropagation(id);
  const { data: events, loading: eventsLoading } = useGetPropagationEvents(id);
  const { update, loading: updateLoading } = useUpdatePropagation();
  const { delete: deleteProp, loading: deleteLoading } = useDeletePropagation();
  const { create: addEvent, loading: eventLoading } = useAddPropagationEvent();

  const [editMode, setEditMode] = useState(false);
  const [showEventForm, setShowEventForm] = useState(false);
  const [eventData, setEventData] = useState({
    event_type: 'measurement',
    notes: '',
  });

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

  const statusOptions = [
    'pending', 'rooting', 'rooted', 'growing', 'ready-to-pot',
    'potted', 'transplanted', 'established', 'failed', 'abandoned'
  ];

  const eventTypeOptions = ['measurement', 'milestone', 'photo', 'problem', 'note'];

  if (propLoading) return <div className="p-6">Chargement...</div>;
  if (propError) return <div className="p-6 text-red-600">{propError}</div>;
  if (!propagation) return <div className="p-6">Propagation non trouvée</div>;

  const handleStatusChange = async (newStatus) => {
    try {
      await update(id, { status: newStatus });
    } catch (err) {
      console.error('Erreur mise à jour:', err);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Confirmer la suppression?')) {
      try {
        await deleteProp(id);
        navigate('/propagations');
      } catch (err) {
        console.error('Erreur suppression:', err);
      }
    }
  };

  const handleAddEvent = async (e) => {
    e.preventDefault();
    try {
      await addEvent(id, eventData);
      setEventData({ event_type: 'measurement', notes: '' });
      setShowEventForm(false);
    } catch (err) {
      console.error('Erreur ajout événement:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Propagation: {propagation.parent_plant_name}
            </h1>
            <p className="text-gray-600 mt-2">
              {propagation.source_type} - {propagation.method}
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => navigate('/propagations')}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
            >
              Retour
            </button>
            <button
              onClick={handleDelete}
              disabled={deleteLoading}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition disabled:opacity-50"
            >
              Supprimer
            </button>
          </div>
        </div>

        {/* Status Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center gap-4 mb-4">
            <span className={`px-4 py-2 rounded-full font-semibold ${statusColors[propagation.status] || 'bg-gray-100'}`}>
              {propagation.status}
            </span>
            <select
              value={propagation.status}
              onChange={(e) => handleStatusChange(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg"
            >
              {statusOptions.map(status => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-gray-600 text-sm">Dates écoulées</p>
              <p className="text-2xl font-bold text-gray-900">
                {propagation.days_since_propagation}j
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Estimé</p>
              <p className="text-2xl font-bold text-gray-900">
                {propagation.expected_duration_days}j
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Succès estimé</p>
              <p className="text-2xl font-bold text-green-600">
                {propagation.success_rate_estimate}%
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Surclassement</p>
              <p className={`text-2xl font-bold ${propagation.is_overdue ? 'text-red-600' : 'text-gray-900'}`}>
                {propagation.is_overdue ? '⚠️ OUI' : 'Non'}
              </p>
            </div>
          </div>
        </div>

        {/* Dates Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Dates</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-gray-600 text-sm">Démarrage</p>
              <p className="text-lg font-semibold text-gray-900">
                {new Date(propagation.propagation_date).toLocaleDateString('fr-FR')}
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Récolte</p>
              <p className="text-lg font-semibold text-gray-900">
                {new Date(propagation.date_harvested).toLocaleDateString('fr-FR')}
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Prévue Prête</p>
              <p className="text-lg font-semibold text-gray-900">
                {new Date(propagation.expected_ready).toLocaleDateString('fr-FR')}
              </p>
            </div>
            {propagation.success_date && (
              <div>
                <p className="text-gray-600 text-sm">Succès</p>
                <p className="text-lg font-semibold text-green-600">
                  {new Date(propagation.success_date).toLocaleDateString('fr-FR')}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Notes */}
        {propagation.notes && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-yellow-800 mb-2">Notes</h3>
            <p className="text-yellow-700">{propagation.notes}</p>
          </div>
        )}

        {/* Timeline Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-gray-900">Événements</h2>
            <button
              onClick={() => setShowEventForm(!showEventForm)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              + Ajouter Événement
            </button>
          </div>

          {showEventForm && (
            <form onSubmit={handleAddEvent} className="bg-gray-50 p-4 rounded-lg mb-6 border border-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Type d'événement
                  </label>
                  <select
                    value={eventData.event_type}
                    onChange={(e) => setEventData({...eventData, event_type: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  >
                    {eventTypeOptions.map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notes
                </label>
                <textarea
                  value={eventData.notes}
                  onChange={(e) => setEventData({...eventData, notes: e.target.value})}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={eventLoading}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                >
                  Ajouter
                </button>
                <button
                  type="button"
                  onClick={() => setShowEventForm(false)}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
                >
                  Annuler
                </button>
              </div>
            </form>
          )}

          {eventsLoading ? (
            <p className="text-gray-600">Chargement des événements...</p>
          ) : events && events.length > 0 ? (
            <div className="space-y-4">
              {events.map(event => (
                <div key={event.id} className="border-l-4 border-blue-500 pl-4 py-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold text-gray-900">{event.event_type}</p>
                      <p className="text-gray-600 text-sm">
                        {new Date(event.event_date).toLocaleDateString('fr-FR')}
                      </p>
                    </div>
                  </div>
                  {event.notes && (
                    <p className="text-gray-700 mt-2">{event.notes}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">Aucun événement enregistré</p>
          )}
        </div>

        {/* Edit Section */}
        {editMode && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Modifier</h2>
            <PropagationForm
              onSuccess={() => setEditMode(false)}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default PropagationDetailsPage;
