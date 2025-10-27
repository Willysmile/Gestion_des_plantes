import { useState, useEffect, useCallback } from 'react'
import { X, ChevronLeft, ChevronRight } from 'lucide-react'
import { photosAPI } from '../lib/api'

export default function PhotoCarousel({ photos, initialIndex = 0, plantId, onClose, onPhotoDeleted }) {
  const [currentIndex, setCurrentIndex] = useState(initialIndex)

  const currentPhoto = photos[currentIndex]

  const goToNext = useCallback((e) => {
    e?.stopPropagation()
    setCurrentIndex((prev) => (prev + 1) % photos.length)
  }, [photos.length])

  const goToPrevious = useCallback((e) => {
    e?.stopPropagation()
    setCurrentIndex((prev) => (prev - 1 + photos.length) % photos.length)
  }, [photos.length])

  // Navigation au clavier
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose()
      else if (e.key === 'ArrowLeft') goToPrevious()
      else if (e.key === 'ArrowRight') goToNext()
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onClose, goToPrevious, goToNext])

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
        <div className="flex-1 flex items-center justify-center min-h-0" onClick={(e) => e.stopPropagation()}>
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
              onClick={(e) => {
                e.stopPropagation()
                e.preventDefault()
                goToPrevious(e)
              }}
              disabled={photos.length <= 1}
              className="text-white hover:text-gray-300 disabled:opacity-30 transition-colors"
            >
              <ChevronLeft size={32} />
            </button>

            {/* Bouton suivant */}
            <button
              onClick={(e) => {
                e.stopPropagation()
                e.preventDefault()
                goToNext(e)
              }}
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
