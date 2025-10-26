/**
 * API client for photo operations
 * Handles upload, delete, list, and set-primary operations
 */

import axios from 'axios'

const API_BASE_URL = 'http://localhost:8001/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for file uploads
})

/**
 * Upload a photo for a plant
 * @param {number} plantId - Plant ID
 * @param {File} file - Image file
 * @param {function} onProgress - Progress callback (0-100)
 * @returns {Promise<{id, plant_id, filename, file_size, width, height, is_primary, urls}>}
 */
export const uploadPhoto = async (plantId, file, onProgress = null) => {
  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await api.post(
      `/plants/${plantId}/photos`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const percentComplete = Math.round(
              (progressEvent.loaded / progressEvent.total) * 100
            )
            onProgress(percentComplete)
          }
        },
      }
    )

    return {
      success: true,
      data: response.data,
      error: null,
    }
  } catch (error) {
    console.error('Error uploading photo:', error)
    return {
      success: false,
      data: null,
      error: error.response?.data?.detail || error.message,
    }
  }
}

/**
 * Get all photos for a plant
 * @param {number} plantId - Plant ID
 * @returns {Promise<Array>}
 */
export const getPhotos = async (plantId) => {
  try {
    const response = await api.get(`/plants/${plantId}/photos`)

    return {
      success: true,
      data: response.data || [],
      error: null,
    }
  } catch (error) {
    console.error('Error fetching photos:', error)
    return {
      success: false,
      data: [],
      error: error.response?.data?.detail || error.message,
    }
  }
}

/**
 * Delete a photo
 * @param {number} plantId - Plant ID
 * @param {number} photoId - Photo ID
 * @returns {Promise<boolean>}
 */
export const deletePhoto = async (plantId, photoId) => {
  try {
    await api.delete(`/plants/${plantId}/photos/${photoId}`)

    return {
      success: true,
      error: null,
    }
  } catch (error) {
    console.error('Error deleting photo:', error)
    return {
      success: false,
      error: error.response?.data?.detail || error.message,
    }
  }
}

/**
 * Set a photo as primary
 * @param {number} plantId - Plant ID
 * @param {number} photoId - Photo ID
 * @returns {Promise<Object>}
 */
export const setPrimaryPhoto = async (plantId, photoId) => {
  try {
    const response = await api.put(
      `/plants/${plantId}/photos/${photoId}/set-primary`
    )

    return {
      success: true,
      data: response.data,
      error: null,
    }
  } catch (error) {
    console.error('Error setting primary photo:', error)
    return {
      success: false,
      data: null,
      error: error.response?.data?.detail || error.message,
    }
  }
}

/**
 * Get photo file URL for different versions
 * @param {number} plantId - Plant ID
 * @param {string} filename - Filename (e.g., 'photo_1.webp' or 'photo_1_medium.webp')
 * @returns {string} URL to photo
 */
export const getPhotoUrl = (plantId, filename) => {
  return `${API_BASE_URL}/photos/${plantId}/${filename}`
}

/**
 * Validate image before upload
 * @param {File} file - Image file
 * @returns {{valid: boolean, error: string|null}}
 */
export const validateImageFile = (file) => {
  const MAX_SIZE = 5 * 1024 * 1024 // 5MB

  // Check file size
  if (file.size > MAX_SIZE) {
    return {
      valid: false,
      error: `La taille du fichier dépasse 5 MB (${(file.size / 1024 / 1024).toFixed(2)} MB)`,
    }
  }

  // Check file type
  const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!validTypes.includes(file.type)) {
    return {
      valid: false,
      error: `Format non supporté. Formats acceptés: JPG, PNG, GIF, WebP`,
    }
  }

  return {
    valid: true,
    error: null,
  }
}

export default {
  uploadPhoto,
  getPhotos,
  deletePhoto,
  setPrimaryPhoto,
  getPhotoUrl,
  validateImageFile,
}
