import { useState, useEffect } from 'react'
import { Eye, X } from 'lucide-react'
import { photosAPI } from '../lib/api'
import { useModal } from '../contexts/ModalContext'

export default function PlantCard({ plant }) {
  const [primaryPhoto, setPrimaryPhoto] = useState(null)
  const { openModal } = useModal()

  useEffect(() => {
    loadPrimaryPhoto()
  }, [plant.id])

  const loadPrimaryPhoto = async () => {
    try {
      const response = await photosAPI.getPhotos(plant.id)
      const photoList = response.data || []
      const primary = photoList.find(p => p.is_primary)
      setPrimaryPhoto(primary)
    } catch (err) {
      console.error('Error loading photos:', err)
    }
  }

  return (
    <>
      {/* Card cliquable */}
      <div
        onClick={() => openModal(plant)}
        className="bg-white rounded-lg shadow hover:shadow-xl transition flex flex-col group cursor-pointer h-full"
      >
        {/* Thumbnail - object-contain pour ne pas cropper */}
        <div className="relative bg-gray-200 flex-shrink-0 flex items-center justify-center rounded-t-lg" style={{ minHeight: '220px' }}>
          {primaryPhoto ? (
            <img
              src={photosAPI.getPhotoUrl(plant.id, primaryPhoto.filename, 'thumbnail')}
              alt={plant.name}
              style={{ maxHeight: '220px', width: 'auto', maxWidth: '100%' }}
              className="object-contain group-hover:scale-105 transition"
            />
          ) : (
            <div className="flex items-center justify-center bg-gray-300 w-full" style={{ height: '220px' }}>
              <span className="text-gray-500 text-sm">Pas de photo</span>
            </div>
          )}
        </div>

        {/* Info + bouton */}
        <div className="flex-1 p-3 flex flex-col justify-between">
          {/* Titre + référence */}
          <div className="text-left">
            <h3 className="font-bold text-sm line-clamp-2">{plant.name}</h3>
            <p className="text-xs text-gray-500 font-mono mt-1">
              {plant.reference || '—'}
            </p>
          </div>

          {/* Bouton voir en bas à droite */}
          <div className="flex justify-end">
            <button
              className="flex items-center justify-center gap-1 bg-blue-500 hover:bg-blue-600 text-white px-2 py-1 rounded text-xs font-semibold"
              onClick={(e) => {
                e.stopPropagation()
                openModal(plant)
              }}
            >
              <Eye className="w-3 h-3" />
              Voir
            </button>
          </div>
        </div>
      </div>

    </>
  )
}
