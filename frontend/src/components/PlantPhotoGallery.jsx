import { useState } from 'react'
import { Trash2, Star } from 'lucide-react'
import PhotoCarousel from './PhotoCarousel'
import { photosAPI } from '../lib/api'

export default function PlantPhotoGallery({ photos = [], plantId, onPhotoDeleted, onPhotoPrimaryChanged }) {
  const [selectedPhotoIndex, setSelectedPhotoIndex] = useState(null)
  const [isCarouselOpen, setIsCarouselOpen] = useState(false)
  const [isDeleting, setIsDeleting] = useState(null)

  const handlePhotoClick = (index) => {
    setSelectedPhotoIndex(index)
    setIsCarouselOpen(true)
  }

  const handleDeletePhoto = async (photoId, e) => {
    e.stopPropagation()

    if (!window.confirm('Supprimer cette photo?')) {
      return
    }

    setIsDeleting(photoId)
    try {
      await photosAPI.deletePhoto(plantId, photoId)
      if (onPhotoDeleted) {
        onPhotoDeleted(photoId)
      }
    } catch (err) {
      console.error('Error deleting photo:', err)
      alert('Erreur lors de la suppression')
    } finally {
      setIsDeleting(null)
    }
  }

  const handleSetPrimary = async (photoId, e) => {
    e.stopPropagation()

    try {
      await photosAPI.setPrimaryPhoto(plantId, photoId)
      if (onPhotoPrimaryChanged) {
        onPhotoPrimaryChanged(photoId)
      }
    } catch (err) {
      console.error('Error setting primary photo:', err)
      alert('Erreur lors de la modification')
    }
  }

  if (!photos || photos.length === 0) {
    return (
      <div className="text-center py-8 bg-gray-50 rounded-lg border border-gray-200">
        <p className="text-gray-500">Aucune photo pour cette plante</p>
      </div>
    )
  }

  return (
    <>
      {/* Grille de photos */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        {photos && photos.filter(p => p?.filename).map((photo, index) => (
          <div
            key={photo.id}
            onClick={() => handlePhotoClick(index)}
            className="relative group cursor-pointer overflow-hidden rounded-lg bg-gray-100 aspect-square"
          >
            {/* Image */}
            <img
              src={photosAPI.getPhotoUrl(plantId, photo.filename, 'thumbnail')}
              alt={`Photo ${index + 1}`}
              className="w-full h-full object-cover transition-transform duration-200 group-hover:scale-110"
            />

            {/* Overlay au survol */}
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors duration-200"></div>

            {/* Badge principale */}
            {photo.is_primary && (
              <div className="absolute top-1 left-1 bg-yellow-400 text-gray-900 px-2 py-1 rounded text-xs font-semibold flex items-center gap-1">
                <Star size={12} fill="currentColor" />
                Principale
              </div>
            )}

            {/* Boutons au survol */}
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center gap-2">
              {/* Bouton supprimer */}
              <button
                onClick={(e) => handleDeletePhoto(photo.id, e)}
                disabled={isDeleting === photo.id}
                className="bg-red-500 hover:bg-red-600 text-white p-2 rounded transition-colors disabled:opacity-50"
              >
                <Trash2 size={16} />
              </button>

              {/* Bouton définir principale */}
              {!photo.is_primary && (
                <button
                  onClick={(e) => handleSetPrimary(photo.id, e)}
                  className="bg-yellow-500 hover:bg-yellow-600 text-white p-2 rounded transition-colors"
                >
                  <Star size={16} />
                </button>
              )}
            </div>

            {/* Indicateur suppression */}
            {isDeleting === photo.id && (
              <div className="absolute inset-0 bg-red-500/20 flex items-center justify-center">
                <p className="text-white text-sm font-semibold">Suppression...</p>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Carousel */}
      {isCarouselOpen && selectedPhotoIndex !== null && (
        <PhotoCarousel
          photos={photos}
          initialIndex={selectedPhotoIndex}
          plantId={plantId}
          onClose={() => setIsCarouselOpen(false)}
          onPhotoDeleted={onPhotoDeleted}
        />
      )}
    </>
  )
}
