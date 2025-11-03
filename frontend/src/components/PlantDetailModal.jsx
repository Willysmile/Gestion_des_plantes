import { useState, useEffect, useMemo } from 'react'
import { X, Edit, Droplet, Sun, Eye, Leaf, Flower2, AlertCircle, Thermometer, Droplets, RefreshCw } from 'lucide-react'
import { Link } from 'react-router-dom'
import { photosAPI, lookupsAPI, plantsAPI } from '../lib/api'
import api from '../lib/api'
import PhotoCarousel from './PhotoCarousel'
import WateringHistory from './WateringHistory'
import NotesHistory from './NotesHistory'
import { WateringFormModal } from './WateringFormModal'
import { FertilizingFormModal } from './FertilizingFormModal'
import { RepottingFormModal } from './RepottingFormModal'
import { DiseaseFormModal } from './DiseaseFormModal'
import { useModal } from '../contexts/ModalContext'
import useTags from '../hooks/useTags'

export default function PlantDetailModal({ plant: initialPlant, onClose }) {
  const [plant, setPlant] = useState(initialPlant)
  const [photos, setPhotos] = useState([])
  const [primaryPhoto, setPrimaryPhoto] = useState(null)
  const [photosLoading, setPhotosLoading] = useState(false)
  const [isCarouselOpen, setIsCarouselOpen] = useState(false)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [lastWatering, setLastWatering] = useState(null)
  const [showWateringForm, setShowWateringForm] = useState(false)
  const [lastFertilizing, setLastFertilizing] = useState(null)
  const [showFertilizingForm, setShowFertilizingForm] = useState(false)
  const [lastRepotting, setLastRepotting] = useState(null)
  const [showRepottingForm, setShowRepottingForm] = useState(false)
  const [lastDisease, setLastDisease] = useState(null)
  const [showDiseaseForm, setShowDiseaseForm] = useState(false)
  const [seasonalWatering, setSeasonalWatering] = useState(null)
  const [nextSeasonalWatering, setNextSeasonalWatering] = useState(null)
  const [seasonalFertilizing, setSeasonalFertilizing] = useState(null)
  const [currentSeasonWateringTag, setCurrentSeasonWateringTag] = useState(null)
  const [lookups, setLookups] = useState({
    wateringFrequencies: [],
    lightRequirements: [],
    fertilizerTypes: [],
    diseaseTypes: [],
    healthStatuses: [],
    seasons: [],
    wateringMethods: [],
    waterTypes: [],
  })

  // Charger la plante complète depuis l'API
  // Charger la plante complète depuis l'API
  const loadFullPlant = async () => {
    try {
      const response = await plantsAPI.getById(initialPlant.id)
      setPlant(response.data)
      console.log('✅ Full plant loaded from API:', response.data)
    } catch (err) {
      console.error('Error loading full plant:', err)
      setPlant(initialPlant)
    }
  }

  // Fonction pour rafraîchir la modale
  const handleRefresh = async () => {
    setIsRefreshing(true)
    try {
      const response = await plantsAPI.getById(initialPlant.id)
      setPlant(response.data)
      console.log('✅ Plant refreshed:', {
        id: response.data.id,
        health_status: response.data.health_status
      })
      await loadLastWatering()
      await loadLastFertilizing()
      await loadLastRepotting()
      await loadLastDisease()
    } catch (err) {
      console.error('Error refreshing modal:', err)
    } finally {
      setIsRefreshing(false)
    }
  }

  useEffect(() => {
    loadFullPlant()
  }, [initialPlant.id])

  useEffect(() => {
    loadPhotos()
  }, [plant.id])

  useEffect(() => {
    if (plant.id) {
      loadLastWatering()
    }
  }, [plant.id])

  useEffect(() => {
    if (plant.id) {
      loadLastFertilizing()
      loadLastRepotting()
      loadLastDisease()
    }
  }, [plant.id])

  useEffect(() => {
    loadLookups()
  }, [])

  // Hook pour accéder aux tags
  const { categories, getAutoTagCategories } = useTags()

  // Calculer les auto tags basés sur les données actuelles de la plante
  const autoTagIds = useMemo(() => {
    if (!plant || categories.length === 0) return [];

    const locationId = plant.location_id;
    const healthStatus = plant.health_status;
    const lightRequirementId = plant.light_requirement_id;
    const allTags = categories.flatMap(cat => cat.tags || []);
    const autoCategories = getAutoTagCategories();

    console.log('🏷️ Recalculating autoTagIds for plant:', {
      plantId: plant.id,
      healthStatus: healthStatus,
      locationId: locationId,
      lightRequirementId: lightRequirementId,
      categoriesCount: categories.length,
      tagsCount: allTags.length
    });

    const autoTags = [];

    // Tag Emplacement
    if (locationId) {
      // Trouver le nom de la location correspondante
      const location = lookups.locations?.find(loc => loc.id === locationId);
      if (location) {
        const locationTag = allTags.find(t => {
          const catName = t.tag_category?.name || t.category?.name;
          return catName === 'Emplacement' && t.name === location.name;
        });
        if (locationTag) autoTags.push(locationTag);
      }
    }

    // Tag État de la plante
    if (healthStatus) {
      const healthMap = {
        healthy: 'Sain',
        sick: 'Malade',
        recovering: 'Rétablie',
        dead: 'Morte',  // Note: pas de "Morte" en base, mais on le garde au cas où
        critical: 'Critique',
        treating: 'En traitement',
        convalescent: 'En convalescence'
      };
      const healthTagName = healthMap[healthStatus];
      console.log('🏥 Looking for health tag:', { healthStatus, healthTagName });
      const healthTag = allTags.find(t => {
        const catName = t.tag_category?.name || t.category?.name;
        return catName === 'État de la plante' && t.name === healthTagName;
      });
      console.log('🏥 Health tag found:', healthTag?.name);
      if (healthTag) autoTags.push(healthTag);
    }

    // Tag Luminosité
    if (lightRequirementId) {
      // Trouver le nom du light requirement correspondant
      const lightReq = lookups.lightRequirements?.find(lr => lr.id === lightRequirementId);
      if (lightReq) {
        const lightTag = allTags.find(t => {
          const catName = t.tag_category?.name || t.category?.name;
          return catName === 'Luminosité' && t.name === lightReq.name;
        });
        if (lightTag) autoTags.push(lightTag);
      }
    }

    console.log('🏷️ Final autoTags:', autoTags.map(t => t.name));
    return autoTags;
  }, [plant?.location_id, plant?.health_status, plant?.light_requirement_id, categories, lookups?.locations, lookups?.lightRequirements])

  // Combine auto tags + manual tags + watering tag
  const allDisplayTags = useMemo(() => {
    const tagIds = new Set(autoTagIds.map(t => t.id));
    // Noms des catégories auto
    const autoCategoryNames = new Set(['Emplacement', 'État de la plante', 'Luminosité']);
    
    const manualTags = (plant.tags || []).filter(t => {
      // Exclure si déjà dans les autoTags
      if (tagIds.has(t.id)) return false;
      // Exclure si c'est un tag de catégorie auto
      const catName = t.tag_category?.name || t.category?.name;
      if (autoCategoryNames.has(catName)) return false;
      return true;
    });
    
    // Ajouter le tag "Besoins en eau" saisonnier si disponible
    const displayTags = [...autoTagIds, ...manualTags];
    if (currentSeasonWateringTag) {
      // Créer un objet tag fictif avec l'icône goutte d'eau
      const wateringTag = {
        id: 'seasonal-watering',
        name: `💧 ${currentSeasonWateringTag.name}`,
        category: { name: 'Besoins en eau' },
        isSeasonalWatering: true
      };
      displayTags.push(wateringTag);
    }
    
    return displayTags;
  }, [autoTagIds, plant?.tags, currentSeasonWateringTag])

  // Charger la fréquence saisonnière une seule fois quand les lookups sont chargés
  useEffect(() => {
    if (plant.id && lookups.seasons?.length > 0) {
      const month = new Date().getMonth() + 1 // 1-12
      const currentSeason = lookups.seasons.find(s => {
        if (s.start_month <= s.end_month) {
          return month >= s.start_month && month <= s.end_month
        } else {
          // Pour l'hiver (12->2)
          return month >= s.start_month || month <= s.end_month
        }
      })
      
      if (currentSeason) {
        console.log(`🔍 Current season: ${currentSeason.name} (month ${month})`)
        loadSeasonalWatering(currentSeason.id)
        loadSeasonalFertilizing(currentSeason.id)
        
        // Charger aussi la prochaine saison
        const nextIndex = (lookups.seasons.findIndex(s => s.id === currentSeason.id) + 1) % lookups.seasons.length
        const nextSeason = lookups.seasons[nextIndex]
        if (nextSeason) {
          loadNextSeasonalWatering(nextSeason.id)
        }
      }
    }
  }, [plant.id, lookups.seasons?.length])

  // Charger la fréquence d'arrosage actuelle pour le tag "Besoins en eau"
  useEffect(() => {
    if (plant.id) {
      const loadCurrentSeasonWatering = async () => {
        try {
          const response = await plantsAPI.getCurrentSeasonWatering(plant.id)
          if (response.data?.frequency_name) {
            setCurrentSeasonWateringTag({
              name: response.data.frequency_name,
              fullName: response.data.full_frequency_name,
              season: response.data.season
            })
            console.log('💧 Current season watering tag loaded:', response.data)
          }
        } catch (err) {
          console.error('Error loading current season watering tag:', err)
          setCurrentSeasonWateringTag(null)
        }
      }
      loadCurrentSeasonWatering()
    }
  }, [plant.id])

  const loadSeasonalWatering = async (seasonId) => {
    try {
      const response = await api.get(`/plants/${plant.id}/seasonal-watering/${seasonId}`)
      setSeasonalWatering(response.data)
      console.log('✅ Seasonal watering loaded:', response.data)
    } catch (err) {
      console.error('Error loading seasonal watering:', err)
      setSeasonalWatering(null)
    }
  }

  const loadNextSeasonalWatering = async (seasonId) => {
    try {
      const response = await api.get(`/plants/${plant.id}/seasonal-watering/${seasonId}`)
      setNextSeasonalWatering(response.data)
      console.log('✅ Next seasonal watering loaded:', response.data)
    } catch (err) {
      console.error('Error loading next seasonal watering:', err)
      setNextSeasonalWatering(null)
    }
  }

  const loadSeasonalFertilizing = async (seasonId) => {
    try {
      const response = await api.get(`/plants/${plant.id}/seasonal-fertilizing/${seasonId}`)
      setSeasonalFertilizing(response.data)
      console.log('✅ Seasonal fertilizing loaded:', response.data)
    } catch (err) {
      console.error('Error loading seasonal fertilizing:', err)
      setSeasonalFertilizing(null)
    }
  }

  const loadLookups = async () => {
    try {
      const [freqRes, lightRes, fertRes, diseaseRes, healthRes, seasonsRes, methodsRes, typesRes] = await Promise.all([
        lookupsAPI.getWateringFrequencies(),
        lookupsAPI.getLightRequirements(),
        lookupsAPI.getFertilizerTypes(),
        lookupsAPI.getDiseaseTypes(),
        api.get('/lookups/plant-health-statuses'),
        api.get('/lookups/seasons'),
        api.get('/lookups/watering-methods'),
        api.get('/lookups/water-types'),
      ])
      setLookups({
        wateringFrequencies: freqRes.data || [],
        lightRequirements: lightRes.data || [],
        fertilizerTypes: fertRes.data || [],
        diseaseTypes: diseaseRes.data || [],
        healthStatuses: healthRes.data || [],
        seasons: seasonsRes.data || [],
        wateringMethods: methodsRes.data || [],
        waterTypes: typesRes.data || [],
      })
    } catch (err) {
      console.error('Error loading lookups:', err)
    }
  }

  const loadPhotos = async () => {
    setPhotosLoading(true)
    try {
      const response = await photosAPI.getPhotos(plant.id)
      const photoList = response.data || []
      setPhotos(photoList)
      const primary = photoList.find(p => p.is_primary)
      setPrimaryPhoto(primary)
    } catch (err) {
      console.error('Error loading photos:', err)
    } finally {
      setPhotosLoading(false)
    }
  }

  const loadLastWatering = async () => {
    try {
      console.log(`🔄 Loading watering history for plant ${plant.id}...`)
      const response = await api.get(`/plants/${plant.id}/watering-history`)
      console.log('📊 API Response:', response.data)
      if (response.data && response.data.length > 0) {
        // Trier par date décroissante et prendre le premier
        const sorted = response.data.sort((a, b) => new Date(b.date) - new Date(a.date))
        console.log('✅ Last watering after sort:', sorted[0])
        setLastWatering(sorted[0])
      } else {
        console.log('⚠️  No watering history found')
        setLastWatering(null)
      }
    } catch (err) {
      console.error('❌ Error loading last watering:', err)
    }
  }

  const loadLastFertilizing = async () => {
    try {
      const response = await api.get(`/plants/${plant.id}/fertilizing-history`)
      if (response.data && response.data.length > 0) {
        const sorted = response.data.sort((a, b) => new Date(b.date) - new Date(a.date))
        setLastFertilizing(sorted[0])
      } else {
        setLastFertilizing(null)
      }
    } catch (err) {
      console.error('Error loading last fertilizing:', err)
    }
  }

  const loadLastRepotting = async () => {
    try {
      const response = await api.get(`/plants/${plant.id}/repotting-history`)
      if (response.data && response.data.length > 0) {
        const sorted = response.data.sort((a, b) => new Date(b.date) - new Date(a.date))
        setLastRepotting(sorted[0])
      } else {
        setLastRepotting(null)
      }
    } catch (err) {
      console.error('Error loading last repotting:', err)
    }
  }

  const loadLastDisease = async () => {
    try {
      const response = await api.get(`/plants/${plant.id}/disease-history`)
      if (response.data && response.data.length > 0) {
        const sorted = response.data.sort((a, b) => {
          const dateCompare = new Date(b.date) - new Date(a.date)
          if (dateCompare !== 0) return dateCompare
          // Si dates égales, trier par ID décroissant
          return b.id - a.id
        })
        setLastDisease(sorted[0])
      } else {
        setLastDisease(null)
      }
    } catch (err) {
      console.error('Error loading last disease:', err)
    }
  }

  const handleGalleryPhotoClick = async (photoId) => {
    try {
      await photosAPI.setPrimaryPhoto(plant.id, photoId)
      // Recharger les photos pour mettre à jour l'affichage
      await loadPhotos()
    } catch (err) {
      console.error('Error setting primary photo:', err)
      alert('Erreur lors de la modification')
    }
  }

  // Obtenir le nom du type d'engrais par ID
  const getFertilizerTypeName = (fertilizerTypeId) => {
    if (!fertilizerTypeId) return 'N/A'
    const fert = lookups.fertilizerTypes.find(f => f.id === fertilizerTypeId)
    return fert ? fert.name : 'Type inconnu'
  }

  // Obtenir l'unité du type d'engrais par ID
  const getFertilizerUnit = (fertilizerTypeId) => {
    if (!fertilizerTypeId) return 'ml'
    const fert = lookups.fertilizerTypes.find(f => f.id === fertilizerTypeId)
    return fert ? fert.unit : 'ml'
  }

  // Pluraliser une unité (ex: "1 ml" vs "2 ml")
  const pluralizeUnit = (unit, amount) => {
    // Remplacer "unité" par "bâton d'engrais"
    let displayUnit = unit === 'unité' ? 'bâton d\'engrais' : unit
    
    if (!amount || amount === 1) return displayUnit
    // Certaines unités ont des formes plurielles en français
    const plurals = {
      'bâton d\'engrais': 'bâtons d\'engrais',
      'bâton': 'bâtons',
      'pastille': 'pastilles',
      'cuillère': 'cuillères',
      'dose': 'doses',
      'unité': 'unités'
    }
    return plurals[displayUnit] || displayUnit
  }

  // Pluraliser "cm" dans les tailles de pots
  const pluralizeCm = (count) => {
    return count === 1 ? 'cm' : 'cm'
  }

  const handleOpenCarousel = () => {
    if (photos.length > 0) {
      setIsCarouselOpen(true)
    }
  }

  const getWateringFrequencyName = () => {
    if (!plant.watering_frequency_id) return '[Placeholder]'
    const freq = lookups.wateringFrequencies.find(f => f.id === plant.watering_frequency_id)
    return freq?.name || '[Placeholder]'
  }

  const getLightRequirementName = () => {
    if (!plant.light_requirement_id) return '[Placeholder]'
    const light = lookups.lightRequirements.find(l => l.id === plant.light_requirement_id)
    return light?.name || '[Placeholder]'
  }

  // Obtenir le nom du type de maladie par ID
  const getDiseaseName = (diseaseTypeId) => {
    if (!diseaseTypeId) return 'N/A'
    const disease = lookups.diseaseTypes?.find(d => d.id === diseaseTypeId)
    return disease ? disease.name : 'Type inconnu'
  }

  // Obtenir la traduction de l'état de santé
  const getHealthStatusName = (healthStatusId) => {
    if (!healthStatusId) return 'N/A'
    const status = lookups.healthStatuses?.find(s => s.id === healthStatusId)
    return status ? status.name : 'État inconnu'
  }

  // Obtenir la saison actuelle
  const getCurrentSeason = () => {
    const month = new Date().getMonth() + 1 // 1-12
    return lookups.seasons?.find(s => {
      if (s.start_month <= s.end_month) {
        return month >= s.start_month && month <= s.end_month
      } else {
        // Pour l'hiver (12->2)
        return month >= s.start_month || month <= s.end_month
      }
    })
  }

  // Obtenir la prochaine saison
  const getNextSeason = () => {
    const currentSeason = getCurrentSeason()
    if (!currentSeason) return null
    
    const seasons = lookups.seasons || []
    const currentIndex = seasons.findIndex(s => s.id === currentSeason.id)
    if (currentIndex === -1) return null
    
    // La prochaine saison est la suivante dans la liste
    return seasons[(currentIndex + 1) % seasons.length]
  }

  // Obtenir la fréquence de la prochaine saison
  const getNextSeasonalWatering = async () => {
    const nextSeason = getNextSeason()
    if (!nextSeason || !plant.id) return null
    
    try {
      const response = await api.get(`/plants/${plant.id}/seasonal-watering/${nextSeason.id}`)
      return response.data
    } catch (err) {
      return null
    }
  }

  // Obtenir le nom de la méthode d'arrosage
  const getWateringMethodName = () => {
    if (!plant.preferred_watering_method_id) return '—'
    const method = lookups.wateringMethods?.find(m => m.id === plant.preferred_watering_method_id)
    return method?.name || '—'
  }

  // Obtenir le nom du type d'eau
  const getWaterTypeName = () => {
    if (!plant.preferred_water_type_id) return '—'
    const type = lookups.waterTypes?.find(t => t.id === plant.preferred_water_type_id)
    return type?.name || '—'
  }

  // Galerie: max 2 photos, excluant la photo principale
  const galleryPhotos = photos.filter(p => !p.is_primary).slice(0, 2)
  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-1"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg shadow-lg overflow-hidden"
        style={{ maxWidth: '90vw', width: '80vw', height: '90vh' }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="h-full flex flex-col">
          {/* En-tête */}
          <div className="flex items-center justify-between p-3 border-b">
            <div className="flex items-center gap-3 flex-1">
              <div>
                {plant.scientific_name && (
                  <h2 className="text-lg font-semibold italic text-green-700">{plant.scientific_name}</h2>
                )}
                <div className="flex gap-2 mt-1 items-center">
                  {plant.family && (
                    <>
                      <span className="text-xs uppercase font-bold text-gray-400 tracking-wide">{plant.family}</span>
                      {plant.subfamily && (
                        <span className="text-xs font-medium text-gray-500">{plant.subfamily}</span>
                      )}
                    </>
                  )}
                </div>
                {plant.name && (
                  <p className="text-sm text-gray-700 mt-1">{plant.name}</p>
                )}
              </div>
            </div>

            {/* Référence et Emplacement badges */}
            <div className="flex items-center gap-3">
              {/* Référence badge */}
              {plant.reference && (
                <div className="bg-purple-50 px-4 py-2 rounded border border-purple-200 text-xs text-center">
                  <p className="text-gray-600 font-medium">Référence</p>
                  <p className="text-purple-700 font-mono font-semibold mt-1">{plant.reference}</p>
                </div>
              )}

              {/* Emplacement badge */}
              {plant.location_name && (
                <div className="bg-green-50 px-4 py-2 rounded border border-green-200 text-xs text-center">
                  <p className="text-gray-600 font-medium">📍 Emplacement</p>
                  <p className="text-green-700 font-semibold mt-1">{plant.location_name}</p>
                </div>
              )}
            </div>

            {/* Boutons */}
            <div className="flex items-center gap-2 ml-4">
              <button
                onClick={handleRefresh}
                disabled={isRefreshing}
                className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600 transition flex items-center gap-1 disabled:opacity-50"
                title="Rafraîchir la modale"
              >
                <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                {isRefreshing ? 'Chargement...' : 'Rafraîchir'}
              </button>
              <Link
                to={`/plants/${plant.id}/edit`}
                className="px-3 py-1 bg-yellow-500 text-white rounded text-sm hover:bg-yellow-600 transition flex items-center gap-1"
                onClick={onClose}
              >
                <Edit className="w-4 h-4" />
                Éditer
              </Link>
              <button
                onClick={onClose}
                className="px-2 py-1 bg-gray-200 rounded text-sm hover:bg-gray-300 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Contenu principal */}
          <div className="flex-1 overflow-hidden flex flex-col xl:flex-row p-3 gap-4">
            {/* Colonne gauche (1/2) */}
            <div className="w-full xl:w-1/2 flex flex-col gap-4 overflow-y-auto pr-3">
              {/* Photo principale */}
              <button
                onClick={handleOpenCarousel}
                disabled={!primaryPhoto}
                className="bg-gray-100 rounded-lg border border-gray-200 flex items-center justify-center overflow-hidden hover:shadow-lg transition disabled:cursor-not-allowed"
                style={{ height: '380px' }}
              >
                {photosLoading ? (
                  <p className="text-gray-400 text-sm">Chargement...</p>
                ) : primaryPhoto ? (
                  <img
                    src={photosAPI.getPhotoUrl(plant.id, primaryPhoto.filename)}
                    alt={plant.name}
                    style={{ height: '100%', width: '100%', objectFit: 'contain', cursor: 'pointer' }}
                  />
                ) : (
                  <p className="text-gray-400 text-sm">Pas de photo</p>
                )}
              </button>

              {/* Description */}
              {plant.description && (
                <div className="bg-gray-50 p-3 rounded-lg border-l-4 border-green-500 text-sm">
                  <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide text-center">Description</h3>
                  <p className="mt-2 text-gray-700 leading-relaxed text-xs">{plant.description}</p>
                </div>
              )}

              {/* Historiques (4 cartes) */}
              <div className="grid grid-cols-4 gap-2">
                <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 relative min-h-32 flex flex-col items-center justify-center">
                  <Link
                    to={`/plants/${plant.id}/watering-history`}
                    onClick={onClose}
                    className="text-xs font-semibold text-gray-700 hover:text-blue-600 transition text-center"
                  >
                    Dernier arrosage
                  </Link>
                  <div className="text-center flex-1 mt-2">
                    <p className="text-xs text-gray-600 font-medium">
                      {lastWatering ? (
                        new Date(lastWatering.date).toLocaleDateString('fr-FR')
                      ) : (
                        'Aucun arrosage'
                      )}
                    </p>
                  </div>
                  <Droplet className="absolute bottom-2 left-2 w-5 h-5 text-blue-500" />
                  <button
                    onClick={() => setShowWateringForm(true)}
                    className="absolute bottom-2 right-2 px-2 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded text-xs transition"
                  >
                    Créer
                  </button>
                </div>
                <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500 relative min-h-32">
                  <Link
                    to={`/plants/${plant.id}/fertilizing-history`}
                    onClick={onClose}
                    className="text-xs font-semibold text-gray-700 hover:text-green-600 transition block text-center"
                  >
                    Dernière fertilisation
                  </Link>
                  {lastFertilizing && (
                    <p className="text-xs text-gray-500 text-center mt-0.5">
                      {new Date(lastFertilizing.date).toLocaleDateString('fr-FR')}
                    </p>
                  )}
                  <div className="text-center flex-1 mt-2">
                    {lastFertilizing ? (
                      <>
                        <p className="text-xs text-gray-600 font-medium">
                          {getFertilizerTypeName(lastFertilizing.fertilizer_type_id)}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {lastFertilizing.amount} {lastFertilizing.amount ? pluralizeUnit(getFertilizerUnit(lastFertilizing.fertilizer_type_id), parseFloat(lastFertilizing.amount)) : ''}
                        </p>
                      </>
                    ) : (
                      <p className="text-xs text-gray-600">Aucune fertilisation</p>
                    )}
                  </div>
                  <Leaf className="absolute bottom-2 left-2 w-5 h-5 text-green-500" />
                  <button
                    onClick={() => setShowFertilizingForm(true)}
                    className="absolute bottom-2 right-2 px-2 py-1 bg-green-500 hover:bg-green-600 text-white rounded text-xs transition"
                  >
                    Créer
                  </button>
                </div>
                <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500 relative min-h-32">
                  <Link
                    to={`/plants/${plant.id}/repotting-history`}
                    onClick={onClose}
                    className="text-xs font-semibold text-gray-700 hover:text-yellow-600 transition block text-center"
                  >
                    Dernier rempotage
                  </Link>
                  <div className="text-center flex-1 mt-2">
                    <p className="text-xs text-gray-600 font-medium">
                      {lastRepotting ? (
                        new Date(lastRepotting.date).toLocaleDateString('fr-FR')
                      ) : (
                        'Aucun rempotage'
                      )}
                    </p>
                    {lastRepotting && (
                      <>
                        <p className="text-xs text-gray-500 mt-1">
                          Pot: {lastRepotting.pot_size_before || '?'}{pluralizeCm(lastRepotting.pot_size_before)} → {lastRepotting.pot_size_after || '?'}{pluralizeCm(lastRepotting.pot_size_after)}
                        </p>
                      </>
                    )}
                  </div>
                  <Flower2 className="absolute bottom-2 left-2 w-5 h-5 text-yellow-500" />
                  <button
                    onClick={() => setShowRepottingForm(true)}
                    className="absolute bottom-2 right-2 px-2 py-1 bg-yellow-500 hover:bg-yellow-600 text-white rounded text-xs transition"
                  >
                    Créer
                  </button>
                </div>
                <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500 relative min-h-32">
                  <Link
                    to={`/plants/${plant.id}/disease-history`}
                    onClick={onClose}
                    className="text-xs font-semibold text-gray-700 hover:text-red-600 transition block text-center"
                  >
                    Maladie
                  </Link>
                  {lastDisease && (
                    <p className="text-xs text-gray-500 text-center mt-0.5">
                      {new Date(lastDisease.date).toLocaleDateString('fr-FR')}
                    </p>
                  )}
                  <div className="text-center flex-1 mt-2">
                    {lastDisease ? (
                      <>
                        <p className="text-xs text-gray-600 font-medium">
                          {getDiseaseName(lastDisease.disease_type_id)}
                        </p>
                        {lastDisease.health_status_id && (
                          <p className="text-xs text-gray-500 mt-1">
                            État: {getHealthStatusName(lastDisease.health_status_id)}
                          </p>
                        )}
                      </>
                    ) : (
                      <p className="text-xs text-gray-600">Aucune maladie</p>
                    )}
                  </div>
                  <AlertCircle className="absolute bottom-2 left-2 w-5 h-5 text-red-500" />
                  <button
                    onClick={() => setShowDiseaseForm(true)}
                    className="absolute bottom-2 right-2 px-2 py-1 bg-red-500 hover:bg-red-600 text-white rounded text-xs transition"
                  >
                    Créer
                  </button>
                </div>
                </div>



              {/* Notes Générales */}
              <div className="p-2 bg-indigo-50 rounded border border-indigo-200">
                <NotesHistory plantId={plant.id} hideHeader={true} onClose={onClose} />
              </div>
            </div>

            {/* Colonne droite (1/2) */}
            <div className="w-full xl:w-1/2 flex flex-col">
              {/* Cartes scrollables */}
              <div className="overflow-y-auto pr-2 flex-1">
                <div className="grid grid-cols-2 gap-3">
                  {/* Carte Arrosage - Grande carte contenant 4 petites cartes */}
                  <div className="col-span-2 bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide mb-3 text-center">
                      💧 Arrosage
                    </h3>
                    <div className="grid grid-cols-4 gap-2">
                      {/* Saison actuelle */}
                      <div className="bg-white p-2 rounded border border-green-200 text-center">
                        <p className="text-xs font-medium text-gray-600 mb-1">Saison actuelle</p>
                        {getCurrentSeason() && (
                          <p className="text-xs text-gray-500 mb-1">{getCurrentSeason().name}</p>
                        )}
                        {seasonalWatering ? (
                          <p className="text-xs text-green-700 font-semibold">{seasonalWatering.name}</p>
                        ) : (
                          <p className="text-xs text-gray-500">—</p>
                        )}
                      </div>

                      {/* Saison future */}
                      <div className="bg-white p-2 rounded border border-yellow-200 text-center">
                        <p className="text-xs font-medium text-gray-600 mb-1">Saison future</p>
                        {getNextSeason() && (
                          <p className="text-xs text-gray-500 mb-1">{getNextSeason().name}</p>
                        )}
                        {nextSeasonalWatering ? (
                          <p className="text-xs text-yellow-700 font-semibold">{nextSeasonalWatering.name}</p>
                        ) : (
                          <p className="text-xs text-gray-500">—</p>
                        )}
                      </div>

                      {/* Méthode & Type d'eau */}
                      <div className="bg-white p-2 rounded border border-purple-200 text-center">
                        <p className="text-xs font-medium text-gray-600 mb-1">Type d'eau</p>
                        <p className="text-xs text-indigo-700 font-semibold mb-2">{getWaterTypeName()}</p>
                        <p className="text-xs text-cyan-700 font-semibold">{getWateringMethodName()}</p>
                      </div>

                      {/* Fertilisation */}
                      <div className="bg-white p-2 rounded border border-green-200 text-center">
                        <p className="text-xs font-medium text-gray-600 mb-1">Fertilisation</p>
                        {seasonalFertilizing ? (
                          <p className="text-xs text-green-700 font-semibold">{seasonalFertilizing.name}</p>
                        ) : (
                          <p className="text-xs text-gray-500">—</p>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Besoins - 3 colonnes: Lumière, Température, Humidité */}
                  <div className="bg-gradient-to-r from-yellow-50 via-red-50 to-cyan-50 p-3 rounded-lg border-l-4 border-yellow-500 col-span-2">
                    <div className="text-center mb-3">
                      <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">Besoins</h3>
                    </div>
                    <div className="grid grid-cols-3 gap-3">
                      {/* Colonne 1: Lumière */}
                      <div className="flex flex-col items-center gap-1 pb-3 border-r border-gray-200">
                        <Sun className="w-5 h-5 text-yellow-500" />
                        <span className="text-xs text-gray-600 font-semibold">Lumière</span>
                        <span className="text-xs text-gray-700 font-medium text-center">{getLightRequirementName()}</span>
                      </div>
                      
                      {/* Colonne 2: Température */}
                      <div className="flex flex-col items-center gap-1 pb-3 border-r border-gray-200">
                        <Thermometer className="w-5 h-5 text-red-500" />
                        <span className="text-xs text-gray-600 font-semibold">Température</span>
                        <div className="text-gray-800 text-xs font-medium">
                          {(plant.temperature_min || plant.temperature_max) 
                            ? `${plant.temperature_min || '?'}°C-${plant.temperature_max || '?'}°C`
                            : '—'}
                        </div>
                      </div>
                      
                      {/* Colonne 3: Humidité */}
                      <div className="flex flex-col items-center gap-1">
                        <Droplets className="w-5 h-5 text-cyan-500" />
                        <span className="text-xs text-gray-600 font-semibold">Humidité</span>
                        <div className="text-gray-800 text-xs font-medium">{plant.humidity_level || '—'}%</div>
                      </div>
                    </div>
                  </div>

                  {/* Tags */}
                  <div className="bg-indigo-50 p-3 rounded-lg border border-indigo-200">
                    <h3 className="text-xs font-semibold text-indigo-700 mb-2 uppercase tracking-wide text-center">🏷️ Tags</h3>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {allDisplayTags?.length > 0 ? (
                        allDisplayTags.map(tag => (
                          <span
                            key={tag.id}
                            className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-200 text-indigo-800"
                          >
                            {tag.name}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-gray-500">—</span>
                      )}
                    </div>
                  </div>

                  {/* Notes */}
                  {plant.notes && (
                    <div className="bg-indigo-50 p-2 rounded-lg border-l-4 border-indigo-500 col-span-2">
                      <div className="text-center">
                        <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">Notes</h3>
                      </div>
                      <p className="mt-2 text-gray-700 leading-relaxed text-xs">{plant.notes}</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Localisation */}
              <div className="grid gap-2 text-xs mt-2" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(0, 1fr))' }}>
                {plant.purchase_date && (
                  <div className="bg-blue-50 p-2 rounded border border-blue-200">
                    <p className="text-gray-600 font-medium text-xs">📅 Date d'achat</p>
                    <p className="text-blue-700 font-semibold">{plant.purchase_date}</p>
                  </div>
                )}
                {plant.purchase_place && (
                  <div className="bg-orange-50 p-2 rounded border border-orange-200">
                    <p className="text-gray-600 font-medium text-xs">🛒 Lieu d'achat</p>
                    <p className="text-orange-700 font-semibold">{plant.purchase_place}</p>
                  </div>
                )}
              </div>

              {/* Galerie */}
              <div className="border-t pt-2 mt-2">
                <h3 className="font-medium text-xs mb-2 text-center uppercase">Galerie</h3>
                <div className="flex justify-center gap-2">
                  {/* Max 2 photos */}
                  {galleryPhotos.map((photo, idx) => (
                    <button
                      key={photo.id}
                      onClick={() => handleGalleryPhotoClick(photo.id)}
                      className="w-16 h-16 bg-gray-100 rounded border border-gray-200 overflow-hidden flex items-center justify-center hover:border-blue-400 hover:shadow-md transition cursor-pointer"
                    >
                      <img
                        src={photosAPI.getPhotoUrl(plant.id, photo.filename, 'thumbnail')}
                        alt={`Photo ${idx + 1}`}
                        style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain' }}
                      />
                    </button>
                  ))}
                  
                  {/* Bouton voir plus (3 points) */}
                  <Link
                    to={`/plants/${plant.id}`}
                    onClick={onClose}
                    className="w-16 h-16 border-0 bg-transparent flex items-center justify-center text-2xl text-gray-400 hover:text-gray-600 transition rounded hover:bg-gray-100"
                  >
                    ⋯
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Carousel */}
      {isCarouselOpen && photos.length > 0 && (
        <PhotoCarousel
          photos={photos}
          initialIndex={photos.findIndex(p => p.id === primaryPhoto?.id) || 0}
          plantId={plant.id}
          onClose={() => setIsCarouselOpen(false)}
          onPhotoDeleted={() => loadPhotos()}
        />
      )}

      {/* Modal formulaire arrosage */}
      {showWateringForm && (
        <WateringFormModal
          plantId={plant.id}
          onClose={() => setShowWateringForm(false)}
          onSuccess={() => {
            loadLastWatering()
            setShowWateringForm(false)
          }}
        />
      )}

      {/* Modal formulaire fertilisation */}
      {showFertilizingForm && (
        <FertilizingFormModal
          plantId={plant.id}
          onClose={() => setShowFertilizingForm(false)}
          onSuccess={() => {
            loadLastFertilizing()
            setShowFertilizingForm(false)
          }}
        />
      )}

      {/* Modal formulaire rempotage */}
      {showRepottingForm && (
        <RepottingFormModal
          plantId={plant.id}
          onClose={() => setShowRepottingForm(false)}
          onSuccess={() => {
            loadLastRepotting()
            setShowRepottingForm(false)
          }}
        />
      )}

      {/* Modal formulaire maladie */}
      {showDiseaseForm && (
        <DiseaseFormModal
          plantId={plant.id}
          onClose={() => setShowDiseaseForm(false)
          }
          onSuccess={() => {
            loadLastDisease()
            loadFullPlant()
            setShowDiseaseForm(false)
          }}
        />
      )}
    </div>
  )
}

