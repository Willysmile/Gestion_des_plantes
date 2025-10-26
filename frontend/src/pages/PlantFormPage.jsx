import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { plantsAPI, lookupsAPI } from '../lib/api'
import { usePlant } from '../hooks/usePlants'
import { validatePlant } from '../lib/schemas'
import { ArrowLeft } from 'lucide-react'

export default function PlantFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { plant: existingPlant } = usePlant(id)

  const [formData, setFormData] = useState({
    name: '',
    family: '',
    subfamily: '',
    genus: '',
    species: '',
    subspecies: '',
    variety: '',
    cultivar: '',
    scientific_name: '',
    reference: '',
    description: '',
    care_instructions: '',
    difficulty_level: '',
    growth_speed: '',
    flowering_season: '',
    temp_min: '',
    temp_max: '',
    humidity: '',
    soil_type: '',
    health_status: 'healthy',
    is_favorite: false,
    is_indoor: false,
    is_outdoor: false,
    is_toxic: false,
    watering_frequency_id: null,
    light_requirement_id: null,
    location_id: null,
    tags: [],
  })

  const [fieldErrors, setFieldErrors] = useState({})
  const [globalError, setGlobalError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [lookups, setLookups] = useState({
    locations: [],
    wateringFrequencies: [],
    lightRequirements: [],
    tags: [],
  })

  // Load existing plant data
  useEffect(() => {
    if (id && existingPlant) {
      setFormData({
        name: existingPlant.name || '',
        family: existingPlant.family || '',
        subfamily: existingPlant.subfamily || '',
        genus: existingPlant.genus || '',
        species: existingPlant.species || '',
        subspecies: existingPlant.subspecies || '',
        variety: existingPlant.variety || '',
        cultivar: existingPlant.cultivar || '',
        scientific_name: existingPlant.scientific_name || '',
        reference: existingPlant.reference || '',
        description: existingPlant.description || '',
        care_instructions: existingPlant.care_instructions || '',
        difficulty_level: existingPlant.difficulty_level || '',
        growth_speed: existingPlant.growth_speed || '',
        flowering_season: existingPlant.flowering_season || '',
        temp_min: existingPlant.temp_min || '',
        temp_max: existingPlant.temp_max || '',
        humidity: existingPlant.humidity || '',
        soil_type: existingPlant.soil_type || '',
        health_status: existingPlant.health_status || 'healthy',
        is_favorite: existingPlant.is_favorite || false,
        is_indoor: existingPlant.is_indoor || false,
        is_outdoor: existingPlant.is_outdoor || false,
        is_toxic: existingPlant.is_toxic || false,
        watering_frequency_id: existingPlant.watering_frequency_id || null,
        light_requirement_id: existingPlant.light_requirement_id || null,
        location_id: existingPlant.location_id || null,
        tags: existingPlant.tags?.map(tag => tag.id) || [],
      })
    }
  }, [id, existingPlant])

  // Load lookups
  useEffect(() => {
    const loadLookups = async () => {
      try {
        const [locations, frequencies, lights, tags] = await Promise.all([
          lookupsAPI.getLocations(),
          lookupsAPI.getWateringFrequencies(),
          lookupsAPI.getLightRequirements(),
          lookupsAPI.getTags(),
        ])
        setLookups({
          locations: locations.data || [],
          wateringFrequencies: frequencies.data || [],
          lightRequirements: lights.data || [],
          tags: tags.data || [],
        })
      } catch (err) {
        console.error('Erreur lors du chargement des données:', err)
      }
    }
    loadLookups()
  }, [])

  /**
   * Auto-correction des données selon les règles métier
   * Applique les transformations taxonomiques automatiquement
   */
  const autoCorrectData = (data) => {
    const corrected = { ...data }

    // Genus: 1ère lettre majuscule, reste minuscule
    if (corrected.genus && corrected.genus.trim()) {
      corrected.genus = corrected.genus.trim().charAt(0).toUpperCase() + corrected.genus.trim().slice(1).toLowerCase()
    }

    // Species: tout en minuscule
    if (corrected.species && corrected.species.trim()) {
      corrected.species = corrected.species.trim().toLowerCase()
    }

    // Subspecies: minuscule + préfixe "subsp." si absent
    if (corrected.subspecies && corrected.subspecies.trim()) {
      let subsp = corrected.subspecies.trim().toLowerCase()
      if (!subsp.startsWith('subsp.')) {
        corrected.subspecies = 'subsp. ' + subsp
      } else {
        corrected.subspecies = subsp
      }
    }

    // Variety: minuscule + préfixe "var." si absent
    if (corrected.variety && corrected.variety.trim()) {
      let var_value = corrected.variety.trim().toLowerCase()
      if (!var_value.startsWith('var.')) {
        corrected.variety = 'var. ' + var_value
      } else {
        corrected.variety = var_value
      }
    }

    // Cultivar: entre guillemets simples si absent
    if (corrected.cultivar && corrected.cultivar.trim()) {
      let cult = corrected.cultivar.trim()
      if (!cult.startsWith("'") || !cult.endsWith("'")) {
        corrected.cultivar = "'" + cult + "'"
      }
    }

    // Convert numeric fields from string to number (or null if empty)
    corrected.temp_min = corrected.temp_min === '' ? null : Number(corrected.temp_min)
    corrected.temp_max = corrected.temp_max === '' ? null : Number(corrected.temp_max)
    corrected.humidity = corrected.humidity === '' ? null : Number(corrected.humidity)

    // Map frontend field names to backend field names
    corrected.temperature_min = corrected.temp_min
    corrected.temperature_max = corrected.temp_max
    corrected.humidity_level = corrected.humidity
    
    // Remove old frontend field names
    delete corrected.temp_min
    delete corrected.temp_max
    delete corrected.humidity

    return corrected
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
    // Clear error for this field when user starts typing
    if (fieldErrors[name]) {
      setFieldErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[name]
        return newErrors
      })
    }
  }

  const handleTagChange = (tagId) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.includes(tagId)
        ? prev.tags.filter(id => id !== tagId)
        : [...prev.tags, tagId]
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setGlobalError(null)
    setFieldErrors({})

    setLoading(true)
    try {
      // Auto-corriger les données selon les règles métier
      let correctedData = autoCorrectData(formData)

      // Valider avec Zod (validation légère: obligatoire/optionnel seulement)
      const validation = validatePlant(correctedData, !!id)
      if (!validation.success) {
        // Ensure all errors are strings (not objects)
        const cleanErrors = {}
        Object.keys(validation.errors).forEach(key => {
          const val = validation.errors[key]
          cleanErrors[key] = typeof val === 'string' ? val : String(val)
        })
        setFieldErrors(cleanErrors)
        setGlobalError('Veuillez corriger les erreurs ci-dessous')
        setLoading(false)
        return
      }

      // Préparer les données en excluant les champs auto-générés en création
      let dataToSend = { ...correctedData }
      
      // Exclure les champs non supportés par le backend
      delete dataToSend.care_instructions  // Not in backend schema
      
      if (!id) {
        // En création, exclure reference et scientific_name (auto-générés par backend)
        delete dataToSend.reference
        delete dataToSend.scientific_name
      }

      if (id) {
        await plantsAPI.update(id, dataToSend)
        alert('Plante mise à jour avec succès!')
      } else {
        await plantsAPI.create(dataToSend)
        alert('Plante créée avec succès!')
      }
      navigate('/')
    } catch (err) {
      setGlobalError(err.response?.data?.detail || err.message || 'Erreur lors de la sauvegarde')
    } finally {
      setLoading(false)
    }
  }

  const getFieldClass = (fieldName) => {
    const baseClass = "w-full px-3 py-2 border rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
    return fieldErrors[fieldName]
      ? baseClass + " border-red-500 bg-red-50"
      : baseClass + " border-gray-300"
  }

  return (
    <div>
      <Link to="/" className="flex items-center gap-2 text-blue-600 hover:underline mb-6">
        <ArrowLeft className="w-5 h-5" />
        Retour
      </Link>

      <div className="bg-white rounded-lg shadow p-8 max-w-4xl">
        <h1 className="text-3xl font-bold mb-6">
          {id ? 'Éditer' : 'Nouvelle'} Plante
        </h1>

        {globalError && (
          <div className="bg-red-100 text-red-700 p-4 rounded mb-6 border border-red-300">
            {globalError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Informations de Base */}
          <fieldset>
            <legend className="text-xl font-bold mb-4 pb-2 border-b">Informations de base</legend>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block font-semibold mb-2">
                  Nom <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className={getFieldClass('name')}
                  placeholder="Ex: Monstera"
                />
                {fieldErrors.name && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.name}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">
                  Famille <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="family"
                  value={formData.family}
                  onChange={handleChange}
                  className={getFieldClass('family')}
                  placeholder="Ex: Araceae"
                />
                {fieldErrors.family && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.family}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Sous-famille</label>
                <input
                  type="text"
                  name="subfamily"
                  value={formData.subfamily}
                  onChange={handleChange}
                  className={getFieldClass('subfamily')}
                  placeholder="Ex: Pothoideae"
                />
                {fieldErrors.subfamily && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.subfamily}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Genre</label>
                <input
                  type="text"
                  name="genus"
                  value={formData.genus}
                  onChange={handleChange}
                  className={getFieldClass('genus')}
                  placeholder="Ex: Monstera"
                />
                <p className="text-gray-600 text-sm mt-1">💡 Format: première lettre majuscule, reste minuscule</p>
                {fieldErrors.genus && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.genus}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Espèce</label>
                <input
                  type="text"
                  name="species"
                  value={formData.species}
                  onChange={handleChange}
                  className={getFieldClass('species')}
                  placeholder="Ex: deliciosa"
                />
                <p className="text-gray-600 text-sm mt-1">💡 Format: tout en minuscule</p>
                {fieldErrors.species && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.species}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Sous-espèce</label>
                <input
                  type="text"
                  name="subspecies"
                  value={formData.subspecies}
                  onChange={handleChange}
                  className={getFieldClass('subspecies')}
                  placeholder="Ex: borsigiana"
                />
                <p className="text-gray-600 text-sm mt-1">💡 Format: préfixé par "subsp. " et minuscule</p>
                {fieldErrors.subspecies && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.subspecies}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Variété</label>
                <input
                  type="text"
                  name="variety"
                  value={formData.variety}
                  onChange={handleChange}
                  className={getFieldClass('variety')}
                  placeholder="Ex: variegata"
                />
                <p className="text-gray-600 text-sm mt-1">💡 Format: préfixé par "var. " et minuscule</p>
                {fieldErrors.variety && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.variety}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Cultivar</label>
                <input
                  type="text"
                  name="cultivar"
                  value={formData.cultivar}
                  onChange={handleChange}
                  className={getFieldClass('cultivar')}
                  placeholder="Ex: Thai Constellation"
                />
                <p className="text-gray-600 text-sm mt-1">💡 Format: entouré de guillemets simples</p>
                {fieldErrors.cultivar && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.cultivar}</p>
                )}
              </div>

              {id && (
                <>
                  <div>
                    <label className="block font-semibold mb-2">Nom scientifique (auto-généré)</label>
                    <div className="w-full px-3 py-2 border border-gray-300 rounded bg-gray-100">
                      <p className="text-gray-700">{formData.scientific_name || 'À générer...'}</p>
                    </div>
                  </div>

                  <div>
                    <label className="block font-semibold mb-2">Référence (auto-générée)</label>
                    <div className="w-full px-3 py-2 border border-gray-300 rounded bg-gray-100">
                      <p className="text-gray-700">{formData.reference || 'À générer...'}</p>
                    </div>
                  </div>
                </>
              )}
            </div>
          </fieldset>

          {/* Environnement */}
          <fieldset>
            <legend className="text-xl font-bold mb-4 pb-2 border-b">Environnement</legend>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block font-semibold mb-2">Temp. min (°C)</label>
                <input
                  type="number"
                  name="temp_min"
                  value={formData.temp_min}
                  onChange={handleChange}
                  className={getFieldClass('temp_min')}
                  placeholder="Ex: 15"
                />
                {fieldErrors.temp_min && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.temp_min}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Temp. max (°C)</label>
                <input
                  type="number"
                  name="temp_max"
                  value={formData.temp_max}
                  onChange={handleChange}
                  className={getFieldClass('temp_max')}
                  placeholder="Ex: 25"
                />
                {fieldErrors.temp_max && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.temp_max}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Humidité (%)</label>
                <input
                  type="number"
                  name="humidity"
                  value={formData.humidity}
                  onChange={handleChange}
                  className={getFieldClass('humidity')}
                  placeholder="Ex: 60"
                  min="0"
                  max="100"
                />
                {fieldErrors.humidity && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.humidity}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Type de sol</label>
                <input
                  type="text"
                  name="soil_type"
                  value={formData.soil_type}
                  onChange={handleChange}
                  className={getFieldClass('soil_type')}
                  placeholder="Ex: terreau"
                />
              </div>

              <div>
                <label className="block font-semibold mb-2">Fréquence d'arrosage</label>
                <select
                  name="watering_frequency_id"
                  value={formData.watering_frequency_id || ''}
                  onChange={handleChange}
                  className={getFieldClass('watering_frequency_id')}
                >
                  <option value="">Sélectionner...</option>
                  {lookups.wateringFrequencies.map(freq => (
                    <option key={freq.id} value={freq.id}>
                      {freq.name} ({freq.days} jours)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold mb-2">Besoin en lumière</label>
                <select
                  name="light_requirement_id"
                  value={formData.light_requirement_id || ''}
                  onChange={handleChange}
                  className={getFieldClass('light_requirement_id')}
                >
                  <option value="">Sélectionner...</option>
                  {lookups.lightRequirements.map(light => (
                    <option key={light.id} value={light.id}>
                      {light.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold mb-2">Emplacement actuel</label>
                <select
                  name="location_id"
                  value={formData.location_id || ''}
                  onChange={handleChange}
                  className={getFieldClass('location_id')}
                >
                  <option value="">Sélectionner...</option>
                  {lookups.locations.map(loc => (
                    <option key={loc.id} value={loc.id}>
                      {loc.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </fieldset>

          {/* Description */}
          <fieldset>
            <legend className="text-xl font-bold mb-4 pb-2 border-b">Description</legend>
            <div className="space-y-4">
              <div>
                <label className="block font-semibold mb-2">Description générale</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  className={getFieldClass('description')}
                  placeholder="Décrivez votre plante..."
                  rows="3"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block font-semibold mb-2">Niveau de difficulté</label>
                  <select
                    name="difficulty_level"
                    value={formData.difficulty_level || ''}
                    onChange={handleChange}
                    className={getFieldClass('difficulty_level')}
                  >
                    <option value="">Sélectionner...</option>
                    <option value="easy">Facile 😊</option>
                    <option value="medium">Moyen 🤔</option>
                    <option value="hard">Difficile 😅</option>
                  </select>
                  {fieldErrors.difficulty_level && (
                    <p className="text-red-600 text-sm mt-1">{fieldErrors.difficulty_level}</p>
                  )}
                </div>

                <div>
                  <label className="block font-semibold mb-2">Vitesse de croissance</label>
                  <select
                    name="growth_speed"
                    value={formData.growth_speed || ''}
                    onChange={handleChange}
                    className={getFieldClass('growth_speed')}
                  >
                    <option value="">Sélectionner...</option>
                    <option value="slow">Lente 🐢</option>
                    <option value="medium">Normale 🚶</option>
                    <option value="fast">Rapide 🚀</option>
                  </select>
                  {fieldErrors.growth_speed && (
                    <p className="text-red-600 text-sm mt-1">{fieldErrors.growth_speed}</p>
                  )}
                </div>

                <div>
                  <label className="block font-semibold mb-2">Saison de floraison</label>
                  <input
                    type="text"
                    name="flowering_season"
                    value={formData.flowering_season}
                    onChange={handleChange}
                    className={getFieldClass('flowering_season')}
                    placeholder="Ex: Printemps-Été"
                  />
                  {fieldErrors.flowering_season && (
                    <p className="text-red-600 text-sm mt-1">{fieldErrors.flowering_season}</p>
                  )}
                </div>
              </div>
            </div>
          </fieldset>

          {/* Tags */}
          <fieldset>
            <legend className="text-xl font-bold mb-4 pb-2 border-b">Tags</legend>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {lookups.tags && lookups.tags.length > 0 ? (
                lookups.tags.map(tag => (
                  <label key={tag.id} className="flex items-center gap-2 cursor-pointer p-2 border rounded hover:bg-gray-50">
                    <input
                      type="checkbox"
                      checked={formData.tags.includes(tag.id)}
                      onChange={() => handleTagChange(tag.id)}
                      className="w-4 h-4"
                    />
                    <span className="text-sm">{tag.name}</span>
                  </label>
                ))
              ) : (
                <p className="text-gray-500 text-sm col-span-full">Aucun tag disponible</p>
              )}
            </div>
          </fieldset>

          {/* Propriétés */}
          <fieldset>
            <legend className="text-xl font-bold mb-4 pb-2 border-b">Propriétés</legend>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="is_favorite"
                  checked={formData.is_favorite}
                  onChange={handleChange}
                  className="w-4 h-4"
                />
                <span>Favorite ❤️</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="is_indoor"
                  checked={formData.is_indoor}
                  onChange={handleChange}
                  className="w-4 h-4"
                />
                <span>Intérieur 🏠</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="is_outdoor"
                  checked={formData.is_outdoor}
                  onChange={handleChange}
                  className="w-4 h-4"
                />
                <span>Extérieur 🌱</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="is_toxic"
                  checked={formData.is_toxic}
                  onChange={handleChange}
                  className="w-4 h-4"
                />
                <span>Toxique ⚠️</span>
              </label>
            </div>
          </fieldset>

          {/* Santé */}
          <fieldset>
            <legend className="text-xl font-bold mb-4 pb-2 border-b">Santé</legend>
            <div>
              <label className="block font-semibold mb-2">État de santé</label>
              <select
                name="health_status"
                value={formData.health_status}
                onChange={handleChange}
                className={getFieldClass('health_status')}
              >
                <option value="healthy">En bonne santé</option>
                <option value="sick">Malade</option>
                <option value="recovering">En rétablissement</option>
                <option value="dead">Morte</option>
              </select>
            </div>
          </fieldset>

          {/* Buttons */}
          <div className="flex gap-4 pt-6 border-t">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-green-600 text-white font-bold py-3 rounded hover:bg-green-700 disabled:bg-gray-400 transition"
            >
              {loading ? 'Sauvegarde...' : (id ? 'Mettre à jour' : 'Créer')}
            </button>
            <Link
              to="/"
              className="flex-1 bg-gray-300 text-gray-800 font-bold py-3 rounded hover:bg-gray-400 transition text-center"
            >
              Annuler
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
