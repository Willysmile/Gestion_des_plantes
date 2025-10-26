import { useState, useRef } from 'react'
import { Upload, X } from 'lucide-react'
import { photosAPI } from '../lib/api'

export default function PlantPhotoUpload({ plantId, onPhotoAdded }) {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState(null)
  const [preview, setPreview] = useState(null)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFileInput = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFile = async (file) => {
    setError(null)
    setPreview(null)

    // Valider le fichier côté client
    const validation = photosAPI.validateImageFile(file)
    if (!validation.valid) {
      setError(validation.error)
      return
    }

    // Afficher preview
    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target.result)
    }
    reader.readAsDataURL(file)

    // Uploader
    await uploadPhoto(file)
  }

  const uploadPhoto = async (file) => {
    setIsUploading(true)
    setUploadProgress(0)

    try {
      const onProgress = (progressEvent) => {
        if (progressEvent.total) {
          const percentComplete = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          setUploadProgress(percentComplete)
        }
      }

      const result = await photosAPI.uploadPhoto(plantId, file, onProgress)

      setUploadProgress(100)
      // Attendre 500ms avant de réinitialiser
      setTimeout(() => {
        setPreview(null)
        setUploadProgress(0)
        setIsUploading(false)
        if (onPhotoAdded) {
          onPhotoAdded(result)
        }
      }, 500)
    } catch (err) {
      console.error('Upload error:', err)
      setError(err.message || 'Erreur lors de l\'upload')
      setIsUploading(false)
      setUploadProgress(0)
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  const clearPreview = () => {
    setPreview(null)
    setError(null)
    setUploadProgress(0)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="space-y-3">
      <h3 className="font-semibold text-lg">Ajouter une photo</h3>

      {/* Zone de drop */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
        className={`
          border-2 border-dashed rounded-lg p-6 text-center cursor-pointer
          transition-all duration-200
          ${isDragging 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400 bg-gray-50'
          }
          ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        {!preview ? (
          <div className="space-y-2">
            <Upload className="mx-auto text-gray-400" size={32} />
            <div>
              <p className="text-gray-700 font-medium">Glissez une image ici</p>
              <p className="text-gray-500 text-sm">ou cliquez pour parcourir</p>
              <p className="text-gray-400 text-xs mt-1">JPG, PNG, GIF (max 5MB)</p>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <img
              src={preview}
              alt="Preview"
              className="mx-auto max-h-32 rounded"
            />
            <p className="text-sm text-gray-600">Uploading...</p>
          </div>
        )}
      </div>

      {/* Barre de progression */}
      {isUploading && (
        <div className="space-y-2">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 text-center">{uploadProgress}%</p>
        </div>
      )}

      {/* Erreur */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-red-700 text-sm flex items-center gap-2">
            <X size={16} />
            {error}
          </p>
        </div>
      )}

      {/* Input caché */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileInput}
        disabled={isUploading}
        className="hidden"
      />

      {/* Bouton annuler si preview */}
      {preview && (
        <button
          onClick={clearPreview}
          disabled={isUploading}
          className="w-full px-3 py-2 text-gray-700 hover:bg-gray-100 rounded transition-colors disabled:opacity-50"
        >
          Annuler
        </button>
      )}
    </div>
  )
}
