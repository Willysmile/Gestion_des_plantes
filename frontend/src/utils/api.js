/**
 * Utilitaires API - Communications avec le backend FastAPI
 */

const API_BASE_URL = 'http://localhost:8000/api';

// Fonctions utilitaires
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Erreur API');
  }
  return response.json();
};

const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  });
  return handleResponse(response);
};

// ============= STATISTICS =============

export const getDashboardStats = () => {
  return apiCall('/statistics/dashboard');
};

export const getUpcomingWaterings = (days = 7) => {
  return apiCall(`/statistics/upcoming-waterings?days=${days}`);
};

export const getUpcomingFertilizing = (days = 7) => {
  return apiCall(`/statistics/upcoming-fertilizing?days=${days}`);
};

export const getActivity = (days = 30) => {
  return apiCall(`/statistics/activity?days=${days}`);
};

export const getCalendarEvents = (year, month) => {
  return apiCall(`/statistics/calendar?year=${year}&month=${month}`);
};

export const getAdvancedAlerts = () => {
  return apiCall('/statistics/alerts');
};

// ============= PLANTS =============

export const getAllPlants = () => {
  return apiCall('/plants');
};

export const getPlantById = (id) => {
  return apiCall(`/plants/${id}`);
};

export const createPlant = (data) => {
  return apiCall('/plants', {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

export const updatePlant = (id, data) => {
  return apiCall(`/plants/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

export const archivePlant = (id) => {
  return apiCall(`/plants/${id}/archive`, {
    method: 'PUT'
  });
};

export const deletePlant = (id) => {
  return apiCall(`/plants/${id}`, {
    method: 'DELETE'
  });
};

// ============= WATERING HISTORY =============

export const getWateringHistory = (plantId) => {
  return apiCall(`/histories/watering/${plantId}`);
};

export const createWateringEntry = (data) => {
  return apiCall('/histories/watering', {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

export const updateWateringEntry = (id, data) => {
  return apiCall(`/histories/watering/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

export const deleteWateringEntry = (id) => {
  return apiCall(`/histories/watering/${id}`, {
    method: 'DELETE'
  });
};

// ============= FERTILIZING HISTORY =============

export const getFertilizingHistory = (plantId) => {
  return apiCall(`/histories/fertilizing/${plantId}`);
};

export const createFertilizingEntry = (data) => {
  return apiCall('/histories/fertilizing', {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

export const updateFertilizingEntry = (id, data) => {
  return apiCall(`/histories/fertilizing/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

export const deleteFertilizingEntry = (id) => {
  return apiCall(`/histories/fertilizing/${id}`, {
    method: 'DELETE'
  });
};

// ============= PHOTOS =============

export const uploadPhoto = (plantId, formData) => {
  const url = `${API_BASE_URL}/photos/plant/${plantId}`;
  const response = fetch(url, {
    method: 'POST',
    body: formData
  });
  return handleResponse(response);
};

export const deletePhoto = (photoId) => {
  return apiCall(`/photos/${photoId}`, {
    method: 'DELETE'
  });
};

// ============= TAGS =============

export const getAllTags = () => {
  return apiCall('/tags');
};

export const createTag = (data) => {
  return apiCall('/tags', {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

export const updateTag = (id, data) => {
  return apiCall(`/tags/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

export const deleteTag = (id) => {
  return apiCall(`/tags/${id}`, {
    method: 'DELETE'
  });
};

export const assignTagToPlant = (plantId, tagId) => {
  return apiCall(`/tags/${tagId}/assign/${plantId}`, {
    method: 'POST'
  });
};

export const removeTagFromPlant = (plantId, tagId) => {
  return apiCall(`/tags/${tagId}/remove/${plantId}`, {
    method: 'POST'
  });
};
