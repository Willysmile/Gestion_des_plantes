import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { plantsAPI, lookupsAPI, photosAPI } from '../lib/api'
import api from '../lib/api'
import { usePlant } from '../hooks/usePlants'
import useTags from '../hooks/useTags'
import { validatePlant } from '../lib/schemas'
import { ArrowLeft } from 'lucide-react'
import PlantPhotoUpload from '../components/PlantPhotoUpload'
import PlantPhotoGallery from '../components/PlantPhotoGallery'
import TagsSelector from '../components/TagsSelector'

export default function PlantFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { plant: existingPlant } = usePlant(id)
  const { categories, getManualTagCategories, getAutoTagCategories } = useTags()

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
    temperature_min: '',
    temperature_max: '',
    humidity_level: '',
    soil_type: '',
    health_status: 'healthy',
    is_favorite: false,
    is_indoor: false,
    is_outdoor: false,
    watering_frequency_id: null,
    light_requirement_id: null,
    preferred_watering_method_id: null,
    preferred_water_type_id: null,
    location_id: null,
    tags: [],
  })

  const [fieldErrors, setFieldErrors] = useState({})
  const [globalError, setGlobalError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [photos, setPhotos] = useState([])
  const [photosLoading, setPhotosLoading] = useState(false)
  const [lookups, setLookups] = useState({
    locations: [],
    wateringFrequencies: [],
    lightRequirements: [],
    wateringMethods: [],
    waterTypes: [],
    seasons: [],
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
        temperature_min: existingPlant.temperature_min || '',
        temperature_max: existingPlant.temperature_max || '',
        humidity_level: existingPlant.humidity_level || '',
        soil_type: existingPlant.soil_type || '',
        health_status: existingPlant.health_status || 'healthy',
        is_favorite: existingPlant.is_favorite || false,
        is_indoor: existingPlant.is_indoor || false,
        is_outdoor: existingPlant.is_outdoor || false,
        watering_frequency_id: existingPlant.watering_frequency_id || null,
        light_requirement_id: existingPlant.light_requirement_id || null,
        preferred_watering_method_id: existingPlant.preferred_watering_method_id || null,
        preferred_water_type_id: existingPlant.preferred_water_type_id || null,
        location_id: existingPlant.location_id || null,
        // Garder seulement les tags manuels (pas les auto tags qui sont recalculés)
        tags: existingPlant.tags?.filter(tag => {
          const catName = tag.tag_category?.name || tag.category?.name;
          // Exclure les catégories auto (Emplacement, État de la plante, Luminosité)
          return !['Emplacement', 'État de la plante', 'Luminosité'].includes(catName);
        }).map(tag => tag.id) || [],
      })
    }
  }, [id, existingPlant])

  // Load lookups
  useEffect(() => {
    const loadLookups = async () => {
      try {
        const [locations, frequencies, lights, methods, types, seasons, tags, fertilizerFreq] = await Promise.all([
          lookupsAPI.getLocations(),
          lookupsAPI.getWateringFrequencies(),
          lookupsAPI.getLightRequirements(),
          lookupsAPI.getWateringMethods(),
          lookupsAPI.getWaterTypes(),
          lookupsAPI.getSeasons(),
          lookupsAPI.getTags(),
          lookupsAPI.getFertilizerFrequencies(),
        ])
        setLookups({
          locations: locations.data || [],
          wateringFrequencies: frequencies.data || [],
          lightRequirements: lights.data || [],
          wateringMethods: methods.data || [],
          waterTypes: types.data || [],
          seasons: seasons.data || [],
          tags: tags.data || [],
          fertilizerFrequencies: fertilizerFreq.data || [],
        })
      } catch (err) {
        console.error('Erreur lors du chargement des données:', err)
      }
    }
    loadLookups()
  }, [])

  // Charger les fréquences saisonnières après les lookups
  useEffect(() => {
    if (id && lookups.seasons && lookups.seasons.length > 0) {
      loadSeasonalWatering()
      loadSeasonalFertilizing()
    }
  }, [id, lookups.seasons.length])

  const loadSeasonalWatering = async () => {
    try {
      for (const season of lookups.seasons) {
        try {
          const response = await api.get(`/plants/${id}/seasonal-watering/${season.id}`)
          if (response.data) {
            setFormData(prev => ({
              ...prev,
              [`seasonal_watering_${season.id}`]: response.data.id
            }))
          }
        } catch (err) {
          // Pas de fréquence définie pour cette saison, c'est OK
        }
      }
    } catch (err) {
      console.error('Error loading seasonal watering:', err)
    }
  }

  const loadSeasonalFertilizing = async () => {
    try {
      for (const season of lookups.seasons) {
        try {
          const response = await api.get(`/plants/${id}/seasonal-fertilizing/${season.id}`)
          if (response.data) {
            setFormData(prev => ({
              ...prev,
              [`seasonal_fertilizing_${season.id}`]: response.data.id
            }))
          }
        } catch (err) {
          // Pas de fréquence définie pour cette saison, c'est OK
        }
      }
    } catch (err) {
      console.error('Error loading seasonal fertilizing:', err)
    }
  }

  // Load photos when plant ID changes
  useEffect(() => {
    if (id && existingPlant) {
      const loadPhotos = async () => {
        setPhotosLoading(true)
        try {
          const response = await photosAPI.getPhotos(id)
          setPhotos(response.data || [])
        } catch (err) {
          console.error('Erreur lors du chargement des photos:', err)
        } finally {
          setPhotosLoading(false)
        }
      }
      loadPhotos()
    } else {
      setPhotos([])
    }
  }, [id, existingPlant])

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
    corrected.temperature_min = corrected.temperature_min === '' ? null : Number(corrected.temperature_min)
    corrected.temperature_max = corrected.temperature_max === '' ? null : Number(corrected.temperature_max)
    corrected.humidity_level = corrected.humidity_level === '' ? null : Number(corrected.humidity_level)

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

  const handleSubmit = async (e) => {
    e.preventDefault()
    setGlobalError(null)
    setFieldErrors({})

    setLoading(true)
    try {
      // Log les données saisonnières avant correction
      console.log('📋 Form data avant correction:')
      for (const [key, value] of Object.entries(formData)) {
        if (key.startsWith('seasonal_watering_')) {
          console.log(`  ${key}: ${value}`)
        }
      }

      // Auto-corriger les données selon les règles métier
      let correctedData = autoCorrectData(formData)
      console.log('Corrected data:', {
        temp_min: correctedData.temperature_min,
        temp_max: correctedData.temperature_max,
        humidity: correctedData.humidity_level
      })

      // Valider avec Zod (validation légère: obligatoire/optionnel seulement)
      const validation = validatePlant(correctedData, !!id)
      if (!validation.success) {
        // Ensure all errors are strings (not objects)
        const cleanErrors = {}
        Object.keys(validation.errors).forEach(key => {
          const val = validation.errors[key]
          cleanErrors[key] = typeof val === 'string' ? val : String(val)
        })
        console.log('Validation errors:', cleanErrors)
        setFieldErrors(cleanErrors)
        setGlobalError('Veuillez corriger les erreurs ci-dessous')
        setLoading(false)
        return
      }

      // Préparer les données en excluant les champs auto-générés en création
      let dataToSend = { ...correctedData }
      
      // Convertir tags en tag_ids pour le backend
      if (dataToSend.tags) {
        dataToSend.tag_ids = dataToSend.tags
        delete dataToSend.tags
      }
      
      // Exclure les champs non supportés par le backend
      delete dataToSend.care_instructions  // Not in backend schema
      delete dataToSend.reference  // Auto-generated, cannot be modified
      delete dataToSend.scientific_name  // Auto-generated, cannot be modified
      
      if (!id) {
        // These are only excluded in creation (already deleted above, but explicit)
        // reference and scientific_name are auto-generated by backend
      }

      if (id) {
        await plantsAPI.update(id, dataToSend)
        alert('Plante mise à jour avec succès!')
        
        // Sauvegarder aussi les fréquences saisonnières pour l'update
        for (const [key, value] of Object.entries(formData)) {
          if (key.startsWith('seasonal_watering_') && value) {
            const seasonId = parseInt(key.replace('seasonal_watering_', ''), 10)
            try {
              await api.put(`/plants/${id}/seasonal-watering/${seasonId}`, {
                watering_frequency_id: parseInt(value, 10)
              })
            } catch (err) {
              console.error(`Error saving seasonal watering for season ${seasonId}:`, err)
            }
          }
          if (key.startsWith('seasonal_fertilizing_') && value) {
            const seasonId = parseInt(key.replace('seasonal_fertilizing_', ''), 10)
            try {
              await api.put(`/plants/${id}/seasonal-fertilizing/${seasonId}`, {
                fertilizer_frequency_id: parseInt(value, 10)
              })
            } catch (err) {
              console.error(`Error saving seasonal fertilizing for season ${seasonId}:`, err)
            }
          }
        }
      } else {
        const response = await plantsAPI.create(dataToSend)
        // Récupérer l'ID de la plante créée
        const newPlantId = response.data.id || id
        
        // Sauvegarder les fréquences saisonnières
        if (newPlantId) {
          console.log('📌 Saving seasonal watering and fertilizing for plant', newPlantId)
          for (const [key, value] of Object.entries(formData)) {
            if (key.startsWith('seasonal_watering_') && value) {
              const seasonId = parseInt(key.replace('seasonal_watering_', ''), 10)
              console.log(`  Arrosage - Saison ${seasonId}: Fréquence ${value}`)
              try {
                const resp = await api.put(`/plants/${newPlantId}/seasonal-watering/${seasonId}`, {
                  watering_frequency_id: parseInt(value, 10)
                })
                console.log(`  ✅ Arrosage - Saison ${seasonId} sauvegardée`)
              } catch (err) {
                console.error(`Error saving seasonal watering for season ${seasonId}:`, err)
              }
            }
            if (key.startsWith('seasonal_fertilizing_') && value) {
              const seasonId = parseInt(key.replace('seasonal_fertilizing_', ''), 10)
              console.log(`  Fertilisation - Saison ${seasonId}: Fréquence ${value}`)
              try {
                const resp = await api.put(`/plants/${newPlantId}/seasonal-fertilizing/${seasonId}`, {
                  fertilizer_frequency_id: parseInt(value, 10)
                })
                console.log(`  ✅ Fertilisation - Saison ${seasonId} sauvegardée`)
              } catch (err) {
                console.error(`Error saving seasonal fertilizing for season ${seasonId}:`, err)
              }
            }
          }
        }
        alert('Plante créée avec succès!')
      }
      navigate('/')
    } catch (err) {
      // Log error details for debugging
      console.error('Full error:', err)
      if (err.response?.data) {
        console.error('Error response data:', err.response.data)
        console.error('Error detail:', JSON.stringify(err.response.data.detail, null, 2))
      }
      
      // Extract error message safely
      let errorMessage = 'Erreur lors de la sauvegarde'
      
      if (err.response?.data?.detail) {
        // Handle Pydantic validation errors or FastAPI errors
        const detail = err.response.data.detail
        if (Array.isArray(detail)) {
          // Pydantic validation error array
          errorMessage = detail.map(e => {
            if (typeof e === 'string') return e
            if (e.msg) return e.msg
            if (e.message) return e.message
            return JSON.stringify(e)
          }).join(', ')
        } else if (typeof detail === 'string') {
          errorMessage = detail
        } else if (typeof detail === 'object' && detail.msg) {
          errorMessage = detail.msg
        } else {
          errorMessage = JSON.stringify(detail)
        }
      } else if (err.message) {
        errorMessage = err.message
      }
      
      setGlobalError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  // Handler pour quand une photo est ajoutée
  const handlePhotoAdded = async (result) => {
    const newPhoto = result.data
    setPhotos((prev) => [newPhoto, ...prev])
  }

  // Handler pour quand une photo est supprimée
  const handlePhotoDeleted = (photoId) => {
    setPhotos((prev) => prev.filter((p) => p.id !== photoId))
  }

  // Handler pour quand la photo principale change
  const handlePhotoPrimaryChanged = (photoId) => {
    setPhotos((prev) =>
      prev.map((p) => ({
        ...p,
        is_primary: p.id === photoId,
      }))
    )
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

      <div className="bg-white rounded-lg shadow p-8 max-w-[70vw]">
        <h1 className="text-3xl font-bold mb-6">
          {id ? 'Éditer' : 'Nouvelle'} Plante
        </h1>

        {globalError && (
          <div className="bg-red-100 text-red-700 p-4 rounded mb-6 border border-red-300">
            {globalError}
          </div>
        )}

        <form onSubmit={handleSubmit} id="plant-form" className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Colonne gauche - Formulaire */}
          <div className="space-y-8">
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
                    <div className="flex gap-2 items-center">
                      <div className="flex-1 px-3 py-2 border border-gray-300 rounded bg-gray-100">
                        <p className="text-gray-700 font-mono">{formData.reference || 'À générer...'}</p>
                      </div>
                      {id && (
                        <button
                          type="button"
                          onClick={async () => {
                            try {
                              const response = await plantsAPI.regenerateReference(id)
                              setFormData(prev => ({ ...prev, reference: response.data.reference }))
                              alert('✅ Référence régénérée!')
                            } catch (err) {
                              alert('❌ Erreur: ' + err.message)
                            }
                          }}
                          className="px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded font-semibold text-sm whitespace-nowrap"
                        >
                          🔄 Régénérer
                        </button>
                      )}
                    </div>
                  </div>
                </>
              )}
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
            </div>
          </fieldset>

          {/* Santé */}
          <fieldset>
            <legend className="text-xl font-bold mb-4 pb-2 border-b">Santé</legend>
            <div>
              <label className="block font-semibold mb-2">
                État de santé
              </label>
              <div className="bg-gray-100 p-3 rounded border border-gray-300 text-gray-700">
                {formData.health_status === 'healthy' && '✅ Sain'}
                {formData.health_status === 'sick' && '⚠️ Malade'}
                {formData.health_status === 'recovering' && '🔄 Rétablie'}
                {formData.health_status === 'dead' && '❌ Morte'}
                {formData.health_status === 'critical' && '🚨 Critique'}
                {formData.health_status === 'treating' && '💊 En traitement'}
                {formData.health_status === 'convalescent' && '🏥 En convalescence'}
              </div>
              <p className="text-xs text-gray-500 mt-2">
                L'état de santé est automatiquement mis à jour en fonction des historiques de maladies enregistrées. Utilisez la section "Maladies" pour signaler une nouvelle maladie.
              </p>
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
                  name="temperature_min"
                  value={formData.temperature_min}
                  onChange={handleChange}
                  className={getFieldClass('temperature_min')}
                  placeholder="Ex: 15"
                />
                {fieldErrors.temperature_min && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.temperature_min}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Temp. max (°C)</label>
                <input
                  type="number"
                  name="temperature_max"
                  value={formData.temperature_max}
                  onChange={handleChange}
                  className={getFieldClass('temperature_max')}
                  placeholder="Ex: 25"
                />
                {fieldErrors.temperature_max && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.temperature_max}</p>
                )}
              </div>

              <div>
                <label className="block font-semibold mb-2">Humidité (%)</label>
                <input
                  type="number"
                  name="humidity_level"
                  value={formData.humidity_level}
                  onChange={handleChange}
                  className={getFieldClass('humidity_level')}
                  placeholder="Ex: 60"
                  min="0"
                  max="100"
                />
                {fieldErrors.humidity_level && (
                  <p className="text-red-600 text-sm mt-1">{fieldErrors.humidity_level}</p>
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
          </div>

          {/* Colonne droite - Photos */}
          <div className="space-y-8">
            {/* Photos */}
            {id && (
              <fieldset>
                <legend className="text-xl font-bold mb-4 pb-2 border-b">Photos 📷</legend>
                
                {/* Upload section */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-3">Ajouter une photo</h3>
                  <PlantPhotoUpload plantId={id} onPhotoAdded={handlePhotoAdded} />
                </div>

              {/* Gallery section */}
              {photosLoading ? (
                <div className="text-center py-8">
                  <p className="text-gray-500">Chargement des photos...</p>
                </div>
              ) : (
                <>
                  <h3 className="text-lg font-semibold mb-3">Galerie</h3>
                  <PlantPhotoGallery
                    photos={photos}
                    plantId={id}
                    onPhotoDeleted={handlePhotoDeleted}
                    onPhotoPrimaryChanged={handlePhotoPrimaryChanged}
                  />
                </>
              )}
            </fieldset>
          )}

            {/* Préférences d'Arrosage */}
            <fieldset>
              <legend className="text-xl font-bold mb-4 pb-2 border-b">💧 Préférences d'Arrosage</legend>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block font-semibold mb-2">Méthode d'arrosage préférée</label>
                  <select
                    name="preferred_watering_method_id"
                    value={formData.preferred_watering_method_id || ''}
                    onChange={handleChange}
                    className={getFieldClass('preferred_watering_method_id')}
                  >
                    <option value="">Sélectionner...</option>
                    {lookups.wateringMethods.map(method => (
                      <option key={method.id} value={method.id}>
                        {method.name}
                      </option>
                    ))}
                  </select>
                  <p className="text-gray-600 text-xs mt-1">
                    💡 {lookups.wateringMethods.find(m => m.id == formData.preferred_watering_method_id)?.description || ''}
                  </p>
                </div>

                <div>
                  <label className="block font-semibold mb-2">Type d'eau préféré</label>
                  <select
                    name="preferred_water_type_id"
                    value={formData.preferred_water_type_id || ''}
                    onChange={handleChange}
                    className={getFieldClass('preferred_water_type_id')}
                  >
                    <option value="">Sélectionner...</option>
                    {lookups.waterTypes.map(type => (
                      <option key={type.id} value={type.id}>
                        {type.name}
                      </option>
                    ))}
                  </select>
                  <p className="text-gray-600 text-xs mt-1">
                    💡 {lookups.waterTypes.find(t => t.id == formData.preferred_water_type_id)?.description || ''}
                  </p>
                </div>

                <div className="md:col-span-2">
                  <label className="block font-semibold mb-2">Fréquence d'arrosage et fertilisation par saison</label>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Bloc Arrosage (bleu) */}
                    <div>
                      <h3 className="text-center font-semibold text-blue-900 mb-3">Arrosage</h3>
                      <div className="grid grid-cols-2 gap-3">
                        {lookups.seasons.map(season => (
                          <div key={season.id} className="bg-blue-50 p-3 rounded border border-blue-200">
                            <p className="font-semibold text-blue-900 text-sm">{season.name}</p>
                            <p className="text-xs text-blue-700">
                              {`Mois ${season.start_month}-${season.end_month}`}
                            </p>
                            <select
                              name={`seasonal_watering_${season.id}`}
                              value={formData[`seasonal_watering_${season.id}`] || ''}
                              onChange={handleChange}
                              className="w-full mt-2 px-2 py-1 text-xs border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                              <option value="">Choisir...</option>
                              {lookups.wateringFrequencies.map(freq => (
                                <option key={freq.id} value={freq.id}>
                                  {freq.name}
                                </option>
                              ))}
                            </select>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Bloc Fertilisation (jaune) */}
                    <div>
                      <h3 className="text-center font-semibold text-yellow-900 mb-3">Fertilisation</h3>
                      <div className="grid grid-cols-2 gap-3">
                        {lookups.seasons.map(season => (
                          <div key={season.id} className="bg-yellow-50 p-3 rounded border border-yellow-200">
                            <p className="font-semibold text-yellow-900 text-sm">{season.name}</p>
                            <p className="text-xs text-yellow-700">
                              {`Mois ${season.start_month}-${season.end_month}`}
                            </p>
                            <select
                              name={`seasonal_fertilizing_${season.id}`}
                              value={formData[`seasonal_fertilizing_${season.id}`] || ''}
                              onChange={handleChange}
                              className="w-full mt-2 px-2 py-1 text-xs border border-yellow-300 rounded focus:outline-none focus:ring-2 focus:ring-yellow-500"
                            >
                              <option value="">Choisir...</option>
                              {lookups.fertilizerFrequencies?.map(freq => (
                                <option key={freq.id} value={freq.id}>
                                  {freq.name}
                                </option>
                              ))}
                            </select>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </fieldset>
          </div>

          {/* Tags - Pleine largeur */}
          <fieldset className="lg:col-span-2">
            <legend className="text-xl font-bold mb-4 pb-2 border-b">Tags 🏷️</legend>
            <TagsSelector 
              formData={formData}
              lookups={lookups}
              selectedTagIds={formData.tags}
              plantId={id}
              onChange={(tagIds) => setFormData({ ...formData, tags: tagIds })}
            />
          </fieldset>
        </form>
      </div>
    </div>
  )
}
