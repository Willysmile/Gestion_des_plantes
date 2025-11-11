import { useState } from 'react';
import { useCreatePropagation } from '../../hooks/usePropagations';

const PropagationForm = ({ plants = [], onSuccess }) => {
  const { create, loading, error } = useCreatePropagation();
  
  const [formData, setFormData] = useState({
    parent_plant_id: '',
    child_plant_id: '',
    source_type: 'cutting',
    method: 'water',
    propagation_date: new Date().toISOString().split('T')[0],
    date_harvested: new Date().toISOString().split('T')[0],
    expected_ready: '',
    notes: '',
  });

  const [errors, setErrors] = useState({});

  const sourceOptions = {
    'cutting': ['water', 'soil', 'air-layer', 'substrate'],
    'seeds': ['water', 'soil', 'substrate'],
    'division': ['soil', 'substrate'],
    'offset': ['water', 'soil'],
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newFormData = { ...formData, [name]: value };
    
    // Si on change la source_type, réinitialiser la méthode
    if (name === 'source_type') {
      const validMethods = sourceOptions[value];
      newFormData.method = validMethods?.[0] || 'soil';
    }
    
    setFormData(newFormData);
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const calculateExpectedReady = () => {
    const estimates = {
      'cutting-water': 14,
      'cutting-soil': 21,
      'cutting-air-layer': 30,
      'cutting-substrate': 21,
      'seeds-water': 21,
      'seeds-soil': 28,
      'seeds-substrate': 28,
      'division-soil': 14,
      'division-substrate': 14,
      'offset-water': 10,
      'offset-soil': 14,
    };

    const key = `${formData.source_type}-${formData.method}`;
    const days = estimates[key] || 21;
    const harvestDate = new Date(formData.date_harvested);
    harvestDate.setDate(harvestDate.getDate() + days);
    return harvestDate.toISOString().split('T')[0];
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    // Validation
    const newErrors = {};
    if (!formData.parent_plant_id) newErrors.parent_plant_id = 'Parent requis';
    if (!formData.source_type) newErrors.source_type = 'Source requise';
    if (!formData.method) newErrors.method = 'Méthode requise';
    if (!formData.propagation_date) newErrors.propagation_date = 'Date de démarrage requise';
    if (!formData.date_harvested) newErrors.date_harvested = 'Date de récolte requise';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      const submitData = {
        ...formData,
        parent_plant_id: parseInt(formData.parent_plant_id),
        child_plant_id: formData.child_plant_id ? parseInt(formData.child_plant_id) : null,
        expected_ready: formData.expected_ready || calculateExpectedReady(),
      };

      await create(submitData);
      onSuccess?.();
    } catch (err) {
      console.error('Erreur création:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Parent Plant */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Plante Mère *
          </label>
          <select
            name="parent_plant_id"
            value={formData.parent_plant_id}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.parent_plant_id ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            <option value="">Sélectionner une plante</option>
            {plants.map(plant => (
              <option key={plant.id} value={plant.id}>
                {plant.name}
              </option>
            ))}
          </select>
          {errors.parent_plant_id && (
            <p className="text-red-500 text-sm mt-1">{errors.parent_plant_id}</p>
          )}
        </div>

        {/* Child Plant (optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Plante Enfant (optionnel)
          </label>
          <select
            name="child_plant_id"
            value={formData.child_plant_id}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Aucune</option>
            {plants.map(plant => (
              <option key={plant.id} value={plant.id}>
                {plant.name}
              </option>
            ))}
          </select>
        </div>

        {/* Source Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Type de Propagation *
          </label>
          <select
            name="source_type"
            value={formData.source_type}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.source_type ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            <option value="cutting">Bouture</option>
            <option value="seeds">Graines</option>
            <option value="division">Division</option>
            <option value="offset">Rejet</option>
          </select>
          {errors.source_type && (
            <p className="text-red-500 text-sm mt-1">{errors.source_type}</p>
          )}
        </div>

        {/* Method */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Méthode *
          </label>
          <select
            name="method"
            value={formData.method}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.method ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            {sourceOptions[formData.source_type]?.map(method => (
              <option key={method} value={method}>
                {method === 'water' ? 'Eau'
                  : method === 'soil' ? 'Terre'
                  : method === 'air-layer' ? 'Marcottage'
                  : 'Substrat'}
              </option>
            )) || <option>Sélectionner une source</option>}
          </select>
          {errors.method && (
            <p className="text-red-500 text-sm mt-1">{errors.method}</p>
          )}
        </div>

        {/* Propagation Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Date de Démarrage *
          </label>
          <input
            type="date"
            name="propagation_date"
            value={formData.propagation_date}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.propagation_date ? 'border-red-500' : 'border-gray-300'
            }`}
          />
          {errors.propagation_date && (
            <p className="text-red-500 text-sm mt-1">{errors.propagation_date}</p>
          )}
        </div>

        {/* Harvest Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Date de Récolte *
          </label>
          <input
            type="date"
            name="date_harvested"
            value={formData.date_harvested}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.date_harvested ? 'border-red-500' : 'border-gray-300'
            }`}
          />
          {errors.date_harvested && (
            <p className="text-red-500 text-sm mt-1">{errors.date_harvested}</p>
          )}
        </div>

        {/* Expected Ready Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Date Prévue (auto-calculée)
          </label>
          <input
            type="date"
            name="expected_ready"
            value={formData.expected_ready || calculateExpectedReady()}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Notes */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Notes
        </label>
        <textarea
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          rows="3"
          placeholder="Observations, conditions particulières..."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Submit */}
      <div className="flex gap-4 justify-end">
        <button
          type="button"
          onClick={() => onSuccess?.()}
          className="px-6 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition font-medium"
        >
          Annuler
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium disabled:opacity-50"
        >
          {loading ? 'Création...' : 'Créer Propagation'}
        </button>
      </div>
    </form>
  );
};

export default PropagationForm;
