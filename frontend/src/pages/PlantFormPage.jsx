import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { plantsAPI, lookupsAPI } from '../lib/api'
import { usePlant } from '../hooks/usePlants'
import { ArrowLeft } from 'lucide-react'

export default function PlantFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { plant: existingPlant } = usePlant(id)

  const [formData, setFormData] = useState({
    name: '',
    family: '',
    genus: '',
    species: '',
    description: '',
    temperature_min: 15,
    temperature_max: 25,
    humidity_level: 60,
    soil_type: '',
    health_status: 'healthy',
    is_favorite: false,
    is_indoor: false,
    is_outdoor: false,
    is_toxic: false,
    watering_frequency_id: null,
    light_requirement_id: null,
    location_id: null,
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [lookups, setLookups] = useState({
    locations: [],
    wateringFrequencies: [],
    lightRequirements: [],
  })

  // Load existing plant data
  useEffect(() => {
    if (id && existingPlant) {
      setFormData(existingPlant)
    }
  }, [id, existingPlant])

  // Load lookups
  useEffect(() => {
    const loadLookups = async () => {
      try {
        const [locations, frequencies, lights] = await Promise.all([
          lookupsAPI.getLocations(),
          lookupsAPI.getWateringFrequencies(),
          lookupsAPI.getLightRequirements(),
        ])
        setLookups({
          locations: locations.data || [],
          wateringFrequencies: frequencies.data || [],
          lightRequirements: lights.data || [],
        })
      } catch (err) {
        console.error('Erreur lors du chargement des données:', err)
      }
    }
    loadLookups()
  }, [])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value === '' ? null : (type === 'number' ? Number(value) : value)
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      if (id) {
        await plantsAPI.update(id, formData)
        alert('Plante mise à jour avec succès!')
      } else {
        await plantsAPI.create(formData)
        alert('Plante créée avec succès!')
      }
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Erreur lors de la sauvegarde')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Link to="/" className="flex items-center gap-2 text-blue-600 hover:underline mb-6">
        <ArrowLeft className="w-5 h-5" />
        Retour
      </Link>

      <div className="bg-white rounded-lg shadow p-8 max-w-2xl">
        <h1 className="text-3xl font-bold mb-6">
          {id ? 'Éditer' : 'Nouvelle'} Plante
        </h1>

        {error && <div className="bg-red-100 text-red-700 p-4 rounded mb-6">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Informations de Base */}
          <fieldset>
            <legend className="text-xl font-bold mb-4">Informations de base</legend>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block font-semibold mb-2">Nom *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div>
                <label className="block font-semibold mb-2">Famille *</label>
                <input
                  type="text"
                  name="family"
                  value={formData.family}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div>
                <label className="block font-semibold mb-2">Genre</label>
                <input
                  type="text"
                  name="genus"
                  value={formData.genus}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div>
                <label className="block font-semibold mb-2">Espèce</label>
                <input
                  type="text"
                  name="species"
                  value={formData.species}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
            </div>
          </fieldset>

          {/* Environnement */}
          <fieldset>
            <legend className="text-xl font-bold mb-4">Environnement</legend>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block font-semibold mb-2">Temp Min (°C)</label>
                <input
                  type="number"
                  name="temperature_min"
                  value={formData.temperature_min}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div>
                <label className="block font-semibold mb-2">Temp Max (°C)</label>
                <input
                  type="number"
                  name="temperature_max"
                  value={formData.temperature_max}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div>
                <label className="block font-semibold mb-2">Humidité (%)</label>
                <input
                  type="number"
                  name="humidity_level"
                  value={formData.humidity_level}
                  onChange={handleChange}
                  min="0"
                  max="100"
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div>
                <label className="block font-semibold mb-2">Type de sol</label>
                <input
                  type="text"
                  name="soil_type"
                  value={formData.soil_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
              <div>
                <label className="block font-semibold mb-2">Fréquence d'arrosage</label>
                <select
                  name="watering_frequency_id"
                  value={formData.watering_frequency_id || ''}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                >
                  <option value="">Sélectionner...</option>
                  {lookups.wateringFrequencies.map(freq => (
                    <option key={freq.id} value={freq.id}>{freq.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block font-semibold mb-2">Luminosité</label>
                <select
                  name="light_requirement_id"
                  value={formData.light_requirement_id || ''}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                >
                  <option value="">Sélectionner...</option>
                  {lookups.lightRequirements.map(light => (
                    <option key={light.id} value={light.id}>{light.name}</option>
                  ))}
                </select>
              </div>
            </div>
          </fieldset>

          {/* Description */}
          <div>
            <label className="block font-semibold mb-2">Description</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              className="w-full px-3 py-2 border border-gray-300 rounded"
            />
          </div>

          {/* Flags */}
          <fieldset>
            <legend className="text-xl font-bold mb-4">Propriétés</legend>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="is_favorite"
                  checked={formData.is_favorite}
                  onChange={handleChange}
                  className="mr-2"
                />
                Favorite
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="is_indoor"
                  checked={formData.is_indoor}
                  onChange={handleChange}
                  className="mr-2"
                />
                Intérieur
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="is_outdoor"
                  checked={formData.is_outdoor}
                  onChange={handleChange}
                  className="mr-2"
                />
                Extérieur
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="is_toxic"
                  checked={formData.is_toxic}
                  onChange={handleChange}
                  className="mr-2"
                />
                Toxique
              </label>
            </div>
          </fieldset>

          {/* Santé */}
          <div>
            <label className="block font-semibold mb-2">État de santé</label>
            <select
              name="health_status"
              value={formData.health_status}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded"
            >
              <option value="healthy">En bonne santé</option>
              <option value="sick">Malade</option>
              <option value="recovering">En récupération</option>
              <option value="dead">Morte</option>
            </select>
          </div>

          {/* Actions */}
          <div className="flex gap-4 pt-6 border-t">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Enregistrement...' : id ? 'Mettre à jour' : 'Créer'}
            </button>
            <Link to="/" className="flex-1 bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 text-center">
              Annuler
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
