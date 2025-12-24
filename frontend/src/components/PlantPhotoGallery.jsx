import { useState } from 'react'
import { Trash2, Star, GripVertical } from 'lucide-react'
import { DndContext, closestCenter, PointerSensor, useSensor, useSensors } from '@dnd-kit/core'
import { arrayMove, SortableContext, useSortable, rectSortingStrategy } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import PhotoCarousel from './PhotoCarousel'
import { photosAPI } from '../lib/api'

function SortablePhoto({ photo, index, plantId, isDeleting, onPhotoClick, onDelete, onSetPrimary }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging
  } = useSortable({ id: photo.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="relative group cursor-pointer overflow-hidden rounded-lg bg-gray-100 aspect-square"
    >
      {/* Drag handle */}
      <div
        {...attributes}
        {...listeners}
        className="absolute top-1 right-1 z-10 bg-white/80 p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity cursor-grab active:cursor-grabbing"
      >
        <GripVertical size={16} className="text-gray-600" />
      </div>

      {/* Image */}
      <img
        src={photosAPI.getPhotoUrl(plantId, photo.filename, 'thumbnail')}
        alt={`Photo ${index + 1}`}
        className="w-full h-full object-contain transition-transform duration-200 group-hover:scale-110"
        onClick={() => onPhotoClick(index)}
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
        <button
          onClick={(e) => onDelete(photo.id, e)}
          disabled={isDeleting === photo.id}
          className="bg-red-500 hover:bg-red-600 text-white p-2 rounded transition-colors disabled:opacity-50"
        >
          <Trash2 size={16} />
        </button>

        {!photo.is_primary && (
          <button
            onClick={(e) => onSetPrimary(photo.id, e)}
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
  )
}

export default function PlantPhotoGallery({ photos = [], plantId, onPhotoDeleted, onPhotoPrimaryChanged }) {
  const [localPhotos, setLocalPhotos] = useState(photos)
  const [selectedPhotoIndex, setSelectedPhotoIndex] = useState(null)
  const [isCarouselOpen, setIsCarouselOpen] = useState(false)
  const [isDeleting, setIsDeleting] = useState(null)

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // Drag after 8px movement
      },
    })
  )

  // Update local state when photos prop changes
  useState(() => {
    setLocalPhotos(photos)
  }, [photos])

  const handleDragEnd = async (event) => {
    const { active, over } = event

    if (!over || active.id === over.id) {
      return
    }

    const oldIndex = localPhotos.findIndex((p) => p.id === active.id)
    const newIndex = localPhotos.findIndex((p) => p.id === over.id)

    // Optimistic UI update
    const reordered = arrayMove(localPhotos, oldIndex, newIndex)
    setLocalPhotos(reordered)

    // Update backend
    const photoOrders = reordered.map((photo, index) => ({
      id: photo.id,
      order: index
    }))

    try {
      await photosAPI.reorderPhotos(plantId, photoOrders)
    } catch (err) {
      console.error('Error reordering photos:', err)
      // Revert on error
      setLocalPhotos(photos)
      alert('Erreur lors du réordonnancement')
    }
  }

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

  if (!localPhotos || localPhotos.length === 0) {
    return (
      <div className="text-center py-8 bg-gray-50 rounded-lg border border-gray-200">
        <p className="text-gray-500">Aucune photo pour cette plante</p>
      </div>
    )
  }

  return (
    <>
      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={localPhotos.map((p) => p.id)}
          strategy={rectSortingStrategy}
        >
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {localPhotos.filter(p => p?.filename).map((photo, index) => (
              <SortablePhoto
                key={photo.id}
                photo={photo}
                index={index}
                plantId={plantId}
                isDeleting={isDeleting}
                onPhotoClick={handlePhotoClick}
                onDelete={handleDeletePhoto}
                onSetPrimary={handleSetPrimary}
              />
            ))}
          </div>
        </SortableContext>
      </DndContext>

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
