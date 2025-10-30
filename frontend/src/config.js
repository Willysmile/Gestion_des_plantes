/**
 * Configuration centralisée de l'application
 * Point unique de vérité pour toutes les URLs et configurations
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  TIMEOUT: 30000, // 30 secondes
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 seconde
}

// Application Configuration
export const APP_CONFIG = {
  APP_NAME: 'Gestion des Plantes',
  VERSION: '2.0',
  ENVIRONMENT: import.meta.env.VITE_ENV || 'development',
  DEBUG: import.meta.env.VITE_DEBUG_API === 'true',
}

// Feature Flags
export const FEATURES = {
  PHOTOS_ENABLED: true,
  HISTORY_ENABLED: true,
  SETTINGS_ENABLED: true,
  EXPORT_ENABLED: true,
}

// Constants
export const LIMITS = {
  PHOTO_MAX_SIZE: 5 * 1024 * 1024, // 5MB
  PLANT_NAME_MAX_LENGTH: 100,
  DESCRIPTION_MAX_LENGTH: 1000,
  PAGINATION_SIZE: 10,
}

// Routes API
export const API_ENDPOINTS = {
  PLANTS: {
    LIST: '/plants',
    CREATE: '/plants',
    GET: (id) => `/plants/${id}`,
    UPDATE: (id) => `/plants/${id}`,
    DELETE: (id) => `/plants/${id}`,
    ARCHIVE: (id) => `/plants/${id}/archive`,
    RESTORE: (id) => `/plants/${id}/restore`,
    REGENERATE_REFERENCE: (id) => `/plants/${id}/regenerate-reference`,
    SEARCH: '/plants/search',
  },
  PHOTOS: {
    LIST: (plantId) => `/plants/${plantId}/photos`,
    UPLOAD: (plantId) => `/plants/${plantId}/photos`,
    DELETE: (plantId, photoId) => `/plants/${plantId}/photos/${photoId}`,
    SET_PRIMARY: (plantId, photoId) => `/plants/${plantId}/photos/${photoId}/set-primary`,
    SERVE: (photoId) => `/plants/photos/${photoId}`,
  },
  HISTORY: {
    WATERING: (plantId) => `/plants/${plantId}/watering-history`,
    FERTILIZING: (plantId) => `/plants/${plantId}/fertilizing-history`,
    REPOTTING: (plantId) => `/plants/${plantId}/repotting-history`,
    DISEASE: (plantId) => `/plants/${plantId}/disease-history`,
    NOTES: (plantId) => `/plants/${plantId}/notes-history`,
  },
  LOOKUPS: {
    LOCATIONS: '/lookups/locations',
    PURCHASE_PLACES: '/lookups/purchase-places',
    WATERING_FREQUENCIES: '/lookups/watering-frequencies',
    LIGHT_REQUIREMENTS: '/lookups/light-requirements',
    FERTILIZER_TYPES: '/lookups/fertilizer-types',
    DISEASE_TYPES: '/lookups/disease-types',
    TREATMENT_TYPES: '/lookups/treatment-types',
    PLANT_HEALTH_STATUSES: '/lookups/plant-health-statuses',
    WATERING_METHODS: '/lookups/watering-methods',
    WATER_TYPES: '/lookups/water-types',
    SEASONS: '/lookups/seasons',
  },
  SETTINGS: {
    TAGS: '/settings/tags',
    TAG_CATEGORIES: '/settings/tag-categories',
    DISEASES: '/settings/diseases',
    TREATMENTS: '/settings/treatments',
  },
}

// Helper functions for common endpoint patterns
export const getHistoryEndpoint = (type, plantId) => {
  const endpoints = {
    watering: API_ENDPOINTS.HISTORY.WATERING(plantId),
    fertilizing: API_ENDPOINTS.HISTORY.FERTILIZING(plantId),
    repotting: API_ENDPOINTS.HISTORY.REPOTTING(plantId),
    disease: API_ENDPOINTS.HISTORY.DISEASE(plantId),
    notes: API_ENDPOINTS.HISTORY.NOTES(plantId),
  }
  return endpoints[type]
}

// Add shortcut aliases to API_ENDPOINTS for backward compatibility
API_ENDPOINTS.wateringHistory = (plantId) => API_ENDPOINTS.HISTORY.WATERING(plantId)
API_ENDPOINTS.fertilizingHistory = (plantId) => API_ENDPOINTS.HISTORY.FERTILIZING(plantId)
API_ENDPOINTS.repottingHistory = (plantId) => API_ENDPOINTS.HISTORY.REPOTTING(plantId)
API_ENDPOINTS.diseaseHistory = (plantId) => API_ENDPOINTS.HISTORY.DISEASE(plantId)
API_ENDPOINTS.notesHistory = (plantId) => API_ENDPOINTS.HISTORY.NOTES(plantId)

// Add shortcut aliases for lookups
API_ENDPOINTS.diseaseTypes = API_ENDPOINTS.LOOKUPS.DISEASE_TYPES
API_ENDPOINTS.treatmentTypes = API_ENDPOINTS.LOOKUPS.TREATMENT_TYPES
API_ENDPOINTS.plantHealthStatuses = API_ENDPOINTS.LOOKUPS.PLANT_HEALTH_STATUSES

// Log configuration on load (debug mode)
if (APP_CONFIG.DEBUG) {
  console.log('🔧 APP Configuration:', APP_CONFIG)
  console.log('📡 API Configuration:', API_CONFIG)
}

export default {
  API_CONFIG,
  APP_CONFIG,
  FEATURES,
  LIMITS,
  API_ENDPOINTS,
}
