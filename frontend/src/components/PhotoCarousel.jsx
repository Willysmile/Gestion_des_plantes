import { useState, useEffect } from 'react'
import { X, ChevronLeft, ChevronRight, Trash2 } from 'lucide-react'
import { photosAPI } from '../lib/api'

export default function PhotoCarousel({ photos, initialIndex = 0, plantId, onClose, onPhotoDeleted }) {
  const [currentIndex, setCurrentIndex] = useState(initialIndex)
  const [isDeleting, setIsDeleting] = useState(false)

  const currentPhoto = photos[currentIndex]

  // Navigation au clavier
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose()
      else if (e.key === 'ArrowLeft') goToPrevious()
      else if (e.key === 'ArrowRight') goToNext()
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [currentIndex])

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % photos.length)
  }

  const goToPrevious = () => {
    setCurrentIndex((prev) => (prev - 1 + photos.length) % photos.length)
  }

  const handleDeletePhoto = async () => {
    if (!window.confirm('Supprimer cette photo?')) {
      return
    }

    setIsDeleting(true)
    try {
      await photosAPI.deletePhoto(plantId, currentPhoto.id)
      if (onPhotoDeleted) {
        onPhotoDeleted(currentPhoto.id)
      }

      // Si c'était la dernière photo, fermer le carousel
      if (photos.length === 1) {
        onClose()
      } else {
        // Ajuster l'index si nécessaire
        const newIndex = currentIndex >= photos.length - 1 ? currentIndex - 1 : currentIndex
        setCurrentIndex(newIndex)
      }
    } catch (err) {
      console.error('Error deleting photo:', err)
      alert('Erreur lors de la suppression')
    } finally {
      setIsDeleting(false)
    }
  }

  // Fermer au clic sur l'arrière-plan
  const handleBackgroundClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  return (
    <div
      onClick={handleBackgroundClick}
      className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4"
    >
      {/* Conteneur principal */}
      <div className="relative flex flex-col items-center justify-center h-full w-full max-w-5xl">
        {/* Bouton fermer */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors"
        >
          <X size={32} />
        </button>

        {/* Image */}
        <div className="flex-1 flex items-center justify-center min-h-0">
          <img
            src={photosAPI.getPhotoUrl(plantId, currentPhoto.filename, 'large')}
            alt={`Photo ${currentIndex + 1}`}
            className="max-w-full max-h-full object-contain"
          />
        </div>

        {/* Contrôles bas */}
        <div className="w-full mt-4 flex flex-col items-center gap-4">
          {/* Compteur */}
          <p className="text-white text-sm">
            {currentIndex + 1} / {photos.length}
          </p>

          {/* Boutons de navigation et suppression */}
          <div className="flex items-center gap-4">
            {/* Bouton précédent */}
            <button
              onClick={goToPrevious}
              disabled={photos.length <= 1}
              className="text-white hover:text-gray-300 disabled:opacity-30 transition-colors"
            >
              <ChevronLeft size={32} />
            </button>

            {/* Bouton supprimer */}
            <button
              onClick={handleDeletePhoto}
              disabled={isDeleting || photos.length === 1}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded flex items-center gap-2 transition-colors disabled:opacity-50"
            >
              <Trash2 size={18} />
              {isDeleting ? 'Suppression...' : 'Supprimer'}
            </button>

            {/* Bouton suivant */}
            <button
              onClick={goToNext}
              disabled={photos.length <= 1}
              className="text-white hover:text-gray-300 disabled:opacity-30 transition-colors"
            >
              <ChevronRight size={32} />
            </button>
          </div>

          {/* Raccourcis clavier */}
          <p className="text-gray-400 text-xs mt-2">
            ← → pour naviguer • ESC pour fermer
          </p>
        </div>
      </div>
    </div>
  )
}
