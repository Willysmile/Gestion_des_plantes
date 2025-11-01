import axios from 'axios'
import { API_CONFIG } from '../config'

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: API_CONFIG.TIMEOUT,
})

// Retry logic pour les erreurs réseau
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Ne pas retry sur les erreurs client (4xx)
    if (error.response?.status >= 400 && error.response?.status < 500) {
      return Promise.reject(error)
    }

    // Retry sur les erreurs serveur (5xx) ou réseau
    const config = error.config
    if (!config.retry) config.retry = 0

    config.retry += 1
    if (config.retry > 3) {
      return Promise.reject(error)
    }

    return new Promise((resolve) => {
      setTimeout(() => resolve(api(config)), 1000 * config.retry)
    })
  }
)

// Plants endpoints
export const plantsAPI = {
  getAll: async (params = {}) => {
    try {
      console.log('📡 plantsAPI.getAll() called, params:', params)
      console.log('📡 API_CONFIG.BASE_URL:', API_CONFIG.BASE_URL)
      const response = await api.get('/plants', { params })
      console.log('📡 plantsAPI.getAll() response:', response)
      return response
    } catch (error) {
      console.error('📡 Error fetching plants:', error)
      throw error
    }
  },
  getById: async (id) => {
    try {
      return await api.get(`/plants/${id}`)
    } catch (error) {
      console.error(`Error fetching plant ${id}:`, error)
      throw error
    }
  },
  create: async (data) => {
    try {
      return await api.post('/plants', data)
    } catch (error) {
      console.error('Error creating plant:', error)
      throw error
    }
  },
  update: async (id, data) => {
    try {
      return await api.put(`/plants/${id}`, data)
    } catch (error) {
      console.error(`Error updating plant ${id}:`, error)
      throw error
    }
  },
  delete: async (id) => {
    try {
      return await api.delete(`/plants/${id}`)
    } catch (error) {
      console.error(`Error deleting plant ${id}:`, error)
      throw error
    }
  },
  archive: async (id, reason) => {
    try {
      return await api.patch(`/plants/${id}/archive`, { reason })
    } catch (error) {
      console.error(`Error archiving plant ${id}:`, error)
      throw error
    }
  },
  restore: async (id) => {
    try {
      return await api.patch(`/plants/${id}/restore`)
    } catch (error) {
      console.error(`Error restoring plant ${id}:`, error)
      throw error
    }
  },
  regenerateReference: async (id) => {
    try {
      return await api.post(`/plants/${id}/regenerate-reference`)
    } catch (error) {
      console.error(`Error regenerating reference for plant ${id}:`, error)
      throw error
    }
  },
}

// Lookups endpoints
export const lookupsAPI = {
  getLocations: async () => {
    try {
      return await api.get('/lookups/locations')
    } catch (error) {
      console.error('Error fetching locations:', error)
      throw error
    }
  },
  getWateringFrequencies: async () => {
    try {
      return await api.get('/lookups/watering-frequencies')
    } catch (error) {
      console.error('Error fetching watering frequencies:', error)
      throw error
    }
  },
  getFertilizerFrequencies: async () => {
    try {
      return await api.get('/lookups/fertilizer-frequencies')
    } catch (error) {
      console.error('Error fetching fertilizer frequencies:', error)
      throw error
    }
  },
  getLightRequirements: async () => {
    try {
      return await api.get('/lookups/light-requirements')
    } catch (error) {
      console.error('Error fetching light requirements:', error)
      throw error
    }
  },
  getTags: async () => {
    try {
      return await api.get('/settings/tags')
    } catch (error) {
      console.error('Error fetching tags:', error)
      throw error
    }
  },
  getFertilizerTypes: async () => {
    try {
      return await api.get('/lookups/fertilizer-types')
    } catch (error) {
      console.error('Error fetching fertilizer types:', error)
      throw error
    }
  },
  getDiseaseTypes: async () => {
    try {
      return await api.get('/lookups/disease-types')
    } catch (error) {
      console.error('Error fetching disease types:', error)
      throw error
    }
  },
  createFertilizerType: async (data) => {
    try {
      return await api.post('/lookups/fertilizer-types', data)
    } catch (error) {
      console.error('Error creating fertilizer type:', error)
      throw error
    }
  },
  updateFertilizerType: async (id, data) => {
    try {
      return await api.put(`/lookups/fertilizer-types/${id}`, data)
    } catch (error) {
      console.error('Error updating fertilizer type:', error)
      throw error
    }
  },
  deleteFertilizerType: async (id) => {
    try {
      return await api.delete(`/lookups/fertilizer-types/${id}`)
    } catch (error) {
      console.error('Error deleting fertilizer type:', error)
      throw error
    }
  },
  getUnits: async () => {
    try {
      return await api.get('/lookups/units')
    } catch (error) {
      console.error('Error fetching units:', error)
      throw error
    }
  },
  createUnit: async (data) => {
    try {
      return await api.post('/lookups/units', data)
    } catch (error) {
      console.error('Error creating unit:', error)
      throw error
    }
  },
  updateUnit: async (id, data) => {
    try {
      return await api.put(`/lookups/units/${id}`, data)
    } catch (error) {
      console.error('Error updating unit:', error)
      throw error
    }
  },
  deleteUnit: async (id) => {
    try {
      return await api.delete(`/lookups/units/${id}`)
    } catch (error) {
      console.error('Error deleting unit:', error)
      throw error
    }
  },
  getWateringMethods: async () => {
    try {
      return await api.get('/lookups/watering-methods')
    } catch (error) {
      console.error('Error fetching watering methods:', error)
      throw error
    }
  },
  getWaterTypes: async () => {
    try {
      return await api.get('/lookups/water-types')
    } catch (error) {
      console.error('Error fetching water types:', error)
      throw error
    }
  },
  getSeasons: async () => {
    try {
      return await api.get('/lookups/seasons')
    } catch (error) {
      console.error('Error fetching seasons:', error)
      throw error
    }
  },
}

// Import photo API
import photosAPI from './api/photosAPI'

export { photosAPI }
export default api
