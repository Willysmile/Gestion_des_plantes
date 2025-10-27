import { useState, useEffect } from 'react'
import { X, Edit, Droplet, Sun, Eye } from 'lucide-react'
import { Link } from 'react-router-dom'
import { photosAPI, lookupsAPI, plantsAPI } from '../lib/api'
import api from '../lib/api'
import PhotoCarousel from './PhotoCarousel'
import WateringHistory from './WateringHistory'
import { WateringFormModal } from './WateringFormModal'
import { useModal } from '../contexts/ModalContext'

export default function PlantDetailModal({ plant: initialPlant, onClose }) {
  const [plant, setPlant] = useState(initialPlant)
  const [photos, setPhotos] = useState([])
  const [primaryPhoto, setPrimaryPhoto] = useState(null)
  const [photosLoading, setPhotosLoading] = useState(false)
  const [isCarouselOpen, setIsCarouselOpen] = useState(false)
  const [lastWatering, setLastWatering] = useState(null)
  const [showWateringForm, setShowWateringForm] = useState(false)
  const [lookups, setLookups] = useState({
    wateringFrequencies: [],
    lightRequirements: [],
  })

  // Charger la plante complète depuis l'API
  useEffect(() => {
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
    loadFullPlant()
  }, [initialPlant.id])

  useEffect(() => {
    loadPhotos()
  }, [plant.id])

  useEffect(() => {
    loadLastWatering()
  }, [plant.id])

  useEffect(() => {
    loadLookups()
  }, [])

  const loadLookups = async () => {
    try {
      const [freqRes, lightRes] = await Promise.all([
        lookupsAPI.getWateringFrequencies(),
        lookupsAPI.getLightRequirements(),
      ])
      setLookups({
        wateringFrequencies: freqRes.data || [],
        lightRequirements: lightRes.data || [],
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
      const response = await api.get(`/plants/${plant.id}/watering-history`)
      if (response.data && response.data.length > 0) {
        // Trier par date décroissante et prendre le premier
        const sorted = response.data.sort((a, b) => new Date(b.watering_date) - new Date(a.watering_date))
        setLastWatering(sorted[0])
      }
    } catch (err) {
      console.error('Error loading last watering:', err)
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

  // Galerie: max 2 photos, excluant la photo principale
  const galleryPhotos = photos.filter(p => !p.is_primary).slice(0, 2)
  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-1"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg shadow-lg overflow-hidden"
        style={{ maxWidth: '2000px', minWidth: '45vw', height: '75vh' }}
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

            {/* Référence badge */}
            {plant.reference && (
              <div className="bg-purple-50 px-2 py-1 rounded border border-purple-200 text-xs">
                <p className="text-gray-600 font-medium">Référence</p>
                <p className="text-purple-700 font-mono font-semibold">{plant.reference}</p>
              </div>
            )}

            {/* Boutons */}
            <div className="flex items-center gap-2 ml-4">
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
          <div className="flex-1 overflow-hidden flex p-3 gap-4">
            {/* Colonne gauche (1/2) */}
            <div className="w-1/2 flex flex-col gap-3 overflow-y-auto pr-2">
              {/* Photo principale */}
              <button
                onClick={handleOpenCarousel}
                disabled={!primaryPhoto}
                className="bg-gray-100 rounded-lg border border-gray-200 flex items-center justify-center overflow-hidden hover:shadow-lg transition disabled:cursor-not-allowed"
                style={{ height: '280px' }}
              >
                {photosLoading ? (
                  <p className="text-gray-400 text-sm">Chargement...</p>
                ) : primaryPhoto ? (
                  <img
                    src={photosAPI.getPhotoUrl(plant.id, primaryPhoto.filename)}
                    alt={plant.name}
                    style={{ maxHeight: '280px', maxWidth: '100%', objectFit: 'contain', cursor: 'pointer' }}
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
                <div className="bg-blue-50 p-2 rounded-lg border-l-4 border-blue-500 relative">
                  <Link
                    to={`/plants/${plant.id}/watering-history`}
                    onClick={onClose}
                    className="text-xs font-semibold text-gray-700 hover:text-blue-600 transition block text-center"
                  >
                    Arrosages
                  </Link>
                  <div className="mt-1 text-center">
                    <p className="text-xs text-gray-600">
                      {lastWatering ? (
                        <>
                          Dernier: {new Date(lastWatering.date).toLocaleDateString('fr-FR')}
                          {lastWatering.amount_ml && (
                            <span className="ml-1 text-blue-600">({lastWatering.amount_ml}ml)</span>
                          )}
                        </>
                      ) : (
                        'Aucun arrosage'
                      )}
                    </p>
                  </div>
                  <button
                    onClick={() => setShowWateringForm(true)}
                    className="absolute bottom-1 right-1 px-2 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded text-xs transition"
                  >
                    Créer
                  </button>
                </div>
                <div className="bg-green-50 p-2 rounded-lg border-l-4 border-green-500 text-center">
                  <p className="text-xs font-semibold text-gray-700">Engrais</p>
                  <p className="text-xs text-gray-600 mt-1">[Placeholder]</p>
                </div>
                <div className="bg-yellow-50 p-2 rounded-lg border-l-4 border-yellow-500 text-center">
                  <p className="text-xs font-semibold text-gray-700">Rempotage</p>
                  <p className="text-xs text-gray-600 mt-1">[Placeholder]</p>
                </div>
                <div className="bg-red-50 p-2 rounded-lg border-l-4 border-red-500 text-center">
                  <p className="text-xs font-semibold text-gray-700">Maladies</p>
                  <p className="text-xs text-gray-600 mt-1">[Placeholder]</p>
                </div>
              </div>



              {/* Infos Diverses */}
              <div className="p-2 bg-gray-50 rounded border border-gray-100">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <h4 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">Infos Diverses</h4>
                    <span className="inline-block bg-gray-200 text-gray-700 text-xs font-bold px-2 py-0.5 rounded-full">
                      0
                    </span>
                  </div>
                  <button className="px-2 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded text-xs transition flex items-center gap-1">
                    <Eye className="w-3 h-3" />
                    Voir
                  </button>
                </div>
              </div>
            </div>

            {/* Colonne droite (1/2) */}
            <div className="w-1/2 flex flex-col">
              {/* Cartes scrollables */}
              <div className="overflow-y-auto pr-2 flex-1">
                <div className="grid grid-cols-2 gap-3">
                  {/* Besoins */}
                  <div className="bg-yellow-50 p-2 rounded-lg border-l-4 border-yellow-500">
                    <div className="text-center">
                      <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">Besoins</h3>
                    </div>
                    <div className="mt-2 flex items-center justify-around gap-3">
                      <div className="flex flex-col items-center gap-1">
                        <span className="text-xs text-gray-600">Arrosage</span>
                        <Droplet className="w-5 h-5 text-blue-500" />
                        <span className="text-xs text-gray-600 font-medium">{getWateringFrequencyName()}</span>
                      </div>
                      <div className="flex flex-col items-center gap-1">
                        <span className="text-xs text-gray-600">Lumière</span>
                        <Sun className="w-5 h-5 text-yellow-500" />
                        <span className="text-xs text-gray-600 font-medium">{getLightRequirementName()}</span>
                      </div>
                    </div>
                  </div>

                  {/* Tags */}
                  <div className="bg-purple-50 p-2 rounded-lg border-l-4 border-purple-500">
                    <div className="text-center">
                      <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">Tags</h3>
                    </div>
                    <div className="mt-2 text-center text-xs text-gray-800">
                      {plant.tags?.length > 0 ? plant.tags.map(t => t.name).join(', ') : '—'}
                    </div>
                  </div>

                  {/* Température */}
                  {(plant.temperature_min || plant.temperature_max) && (
                    <div className="bg-red-50 p-2 rounded-lg border-l-4 border-red-500">
                      <div className="text-center">
                        <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">Température</h3>
                      </div>
                      <div className="mt-2 flex flex-col items-center gap-1">
                        <span className="text-xs text-gray-600">Valeurs</span>
                        <div className="text-gray-800 text-xs font-medium">
                          {plant.temperature_min || '?'}°C-{plant.temperature_max || '?'}°C
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Humidité - Toujours visible */}
                  <div className="bg-cyan-50 p-2 rounded-lg border-l-4 border-cyan-500">
                    <div className="text-center">
                      <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">Humidité</h3>
                    </div>
                    <div className="mt-2 flex flex-col items-center gap-1">
                      <span className="text-xs text-gray-600">Taux</span>
                      <div className="text-gray-800 text-xs font-medium">{plant.humidity_level || '—'}%</div>
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
                {plant.location && (
                  <div className="bg-green-50 p-2 rounded border border-green-200">
                    <p className="text-gray-600 font-medium text-xs">📍 Emplacement</p>
                    <p className="text-green-700 font-semibold">{plant.location}</p>
                  </div>
                )}
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
    </div>
  )
}
