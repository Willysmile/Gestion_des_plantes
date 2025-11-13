import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  useGetPropagation,
  useUpdatePropagation,
  useDeletePropagation,
  useGetPropagationEvents,
  useAddPropagationEvent,
  useConvertPropagation,
} from '../hooks/usePropagations';
import { usePlant } from '../hooks/usePlants';
import { plantsAPI } from '../lib/api';
import PropagationForm from '../components/propagation/PropagationForm';

const PropagationDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { propagation, loading: propLoading, error: propError, refresh } = useGetPropagation(id);
  const { data: events, loading: eventsLoading } = useGetPropagationEvents(id);
  const { update, loading: updateLoading } = useUpdatePropagation();
  const { delete: deleteProp, loading: deleteLoading } = useDeletePropagation();
  const { create: addEvent, loading: eventLoading } = useAddPropagationEvent();
  const { convert, loading: convertLoading } = useConvertPropagation();
  const { plant: parentPlant, loading: parentPlantLoading } = usePlant(propagation?.parent_plant_id);

  const [editMode, setEditMode] = useState(false);
  const [showEventForm, setShowEventForm] = useState(false);
  const [eventData, setEventData] = useState({
    event_type: 'measurement',
    notes: '',
  });
  const [conversionName, setConversionName] = useState('');
  const [successDate, setSuccessDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [inheritParentSettings, setInheritParentSettings] = useState(true);
  const [overrideChildPlantId, setOverrideChildPlantId] = useState('');
  const [conversionStatusMessage, setConversionStatusMessage] = useState('');
  const [conversionErrorMessage, setConversionErrorMessage] = useState('');
  const [conversionSaving, setConversionSaving] = useState(false);

  useEffect(() => {
    if (!propagation) return;
    setConversionName((current) =>
      current || `${propagation.parent_plant_name || 'Bouture'} · #${propagation.id}`
    );
    setSuccessDate(
      propagation.success_date
        ? new Date(propagation.success_date).toISOString().split('T')[0]
        : new Date().toISOString().split('T')[0]
    );
  }, [propagation]);

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

  const VALID_TRANSITIONS = {
    'pending': ['rooting', 'failed', 'abandoned'],
    'rooting': ['rooted', 'failed', 'abandoned'],
    'rooted': ['growing', 'ready-to-pot', 'failed', 'abandoned'],
    'growing': ['ready-to-pot', 'failed', 'abandoned'],
    'ready-to-pot': ['potted', 'failed', 'abandoned'],
    'potted': ['transplanted', 'established', 'failed', 'abandoned'],
    'transplanted': ['established', 'failed', 'abandoned'],
    'established': ['failed', 'abandoned'],
    'failed': [],
    'abandoned': [],
  };

  const getValidStatusOptions = () => {
    if (!propagation) return [];
    return VALID_TRANSITIONS[propagation.status] || [];
  };

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

  const buildPlantPayload = () => {
    if (!propagation) return { name: conversionName || 'Bouture' };
    const payload = {
      name: conversionName || `Bouture #${propagation.id}`,
      parent_plant_id: propagation.parent_plant_id,
    };

    if (inheritParentSettings && parentPlant) {
      payload.location_id = parentPlant.location_id;
      payload.watering_frequency_id = parentPlant.watering_frequency_id;
      payload.preferred_watering_method_id = parentPlant.preferred_watering_method_id;
      payload.preferred_water_type_id = parentPlant.preferred_water_type_id;
      payload.light_requirement_id = parentPlant.light_requirement_id;
      payload.temperature_min = parentPlant.temperature_min;
      payload.temperature_max = parentPlant.temperature_max;
      payload.humidity_level = parentPlant.humidity_level;
      payload.soil_type = parentPlant.soil_type;
      payload.soil_humidity = parentPlant.soil_humidity;
      payload.difficulty_level = parentPlant.difficulty_level;
      payload.growth_speed = parentPlant.growth_speed;
      payload.flowering_season = parentPlant.flowering_season;
      payload.pot_size = parentPlant.pot_size;
      payload.is_indoor = parentPlant.is_indoor;
      payload.is_outdoor = parentPlant.is_outdoor;
    }

    return Object.fromEntries(
      Object.entries(payload).filter(([, value]) => value !== undefined && value !== null && value !== '')
    );
  };

  const createChildPlant = async () => {
    const payload = buildPlantPayload();
    if (!payload.name) {
      throw new Error('Un nom est requis pour créer la plante');
    }
    const response = await plantsAPI.create(payload);
    return response.data?.id;
  };

  const handleConvert = async () => {
    if (!propagation) return;
    setConversionErrorMessage('');
    setConversionStatusMessage('');
    setConversionSaving(true);
    try {
      let childId = overrideChildPlantId ? Number(overrideChildPlantId) : undefined;
      if (!childId) {
        childId = await createChildPlant();
      }

      if (!childId) {
        throw new Error('Impossible de déterminer la plante enfant à convertir');
      }

      await convert(Number(id), { 
        child_plant_id: childId, 
        success_date: successDate,
        inherit_parent_settings: inheritParentSettings 
      });
      setConversionStatusMessage(`Bouture liée à la plante #${childId}`);
      setOverrideChildPlantId('');
      refresh();
      navigate(`/plants/${childId}`);
    } catch (err) {
      setConversionErrorMessage(err.message || 'Erreur lors de la conversion');
    } finally {
      setConversionSaving(false);
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
            {getValidStatusOptions().length > 0 ? (
              <select
                value={propagation.status}
                onChange={(e) => handleStatusChange(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value={propagation.status}>{propagation.status}</option>
                {getValidStatusOptions().map(status => (
                  <option key={status} value={status}>{status}</option>
                ))}
              </select>
            ) : (
              <span className="text-sm text-gray-500 italic">Pas de transition possible depuis cet état</span>
            )}
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

        {/* Conversion Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Convertir en plante</h2>
              <p className="text-sm text-gray-500">Créer une nouvelle plante fille avec les réglages hérités.</p>
            </div>
            <span className="text-sm text-gray-500">Statut: {propagation.child_plant_id ? 'Convertie' : 'En cours'}</span>
          </div>

          {propagation.child_plant_id ? (
            <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200 space-y-2">
              <p className="text-sm text-emerald-700">
                Cette propagation a déjà été convertie en plante #{propagation.child_plant_id}.
              </p>
              <button
                onClick={() => navigate(`/plants/${propagation.child_plant_id}`)}
                className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition"
              >
                Voir la plante
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Nom de la plante</label>
                  <input
                    value={conversionName}
                    onChange={(e) => setConversionName(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-lg px-3 py-2"
                    placeholder="Nom explicite pour la plante" 
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Date de réussite</label>
                  <input
                    type="date"
                    value={successDate}
                    onChange={(e) => setSuccessDate(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-lg px-3 py-2"
                  />
                </div>
              </div>

              <div className="flex items-center gap-2">
                <input
                  id="inherit-settings"
                  type="checkbox"
                  checked={inheritParentSettings}
                  onChange={(e) => setInheritParentSettings(e.target.checked)}
                  className="h-4 w-4 text-emerald-600 border-gray-300 rounded"
                />
                <label htmlFor="inherit-settings" className="text-sm text-gray-700">
                  Hériter des réglages (localisation, fréquences, lumière, environnement)
                </label>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">ID d'une plante existante (optionnel)</label>
                <input
                  type="number"
                  value={overrideChildPlantId}
                  onChange={(e) => setOverrideChildPlantId(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-lg px-3 py-2"
                  placeholder="Entrez un ID pour lier une plante déjà créée"
                />
              </div>

              <div className="bg-gray-50 border border-dashed rounded-lg p-4 text-sm text-gray-600 space-y-2">
                {parentPlantLoading ? (
                  <p>Chargement des réglages parent...</p>
                ) : parentPlant ? (
                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div>
                      <p className="font-semibold text-gray-900">Parent</p>
                      <p className="text-gray-700">{parentPlant.name}</p>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">Location</p>
                      <p className="text-gray-700">#{parentPlant.location_id || '—'}</p>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">Arrosage</p>
                      <p className="text-gray-700">Freq #{parentPlant.watering_frequency_id || '—'}</p>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">Lumière</p>
                      <p className="text-gray-700">#{parentPlant.light_requirement_id || '—'}</p>
                    </div>
                  </div>
                ) : (
                  <p>Impossible de charger la plante parente pour l'instant.</p>
                )}
              </div>

              {conversionErrorMessage && (
                <p className="text-sm text-red-600">{conversionErrorMessage}</p>
              )}

              {conversionStatusMessage && (
                <p className="text-sm text-emerald-700">{conversionStatusMessage}</p>
              )}

              <button
                onClick={handleConvert}
                disabled={conversionSaving || convertLoading}
                className="w-full px-4 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition disabled:opacity-60"
              >
                {propagation.child_plant_id ? 'Convertie' : 'Convertir et créer la plante'}
              </button>
            </div>
          )}
        </div>

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
