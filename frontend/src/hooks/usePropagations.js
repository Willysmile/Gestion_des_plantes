import { useState, useCallback, useEffect } from 'react';
import axios from 'axios';
import { API_CONFIG } from '../config';

// API instance with proper headers
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Hook for getting all propagations
export const useGetPropagations = (filters = {}) => {
  const [propagations, setPropagations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (filters.parentPlantId) params.append('parent_plant_id', filters.parentPlantId);
      if (filters.status) params.append('status', filters.status);
      if (filters.skip) params.append('skip', filters.skip);
      if (filters.limit) params.append('limit', filters.limit);

      const response = await api.get(`/propagations?${params.toString()}`);
      setPropagations(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  return { propagations, loading, error, fetch, setPropagations };
};

// Hook for getting single propagation
export const useGetPropagation = (propagationId) => {
  const [propagation, setPropagation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    if (!propagationId) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/propagations/${propagationId}`);
      setPropagation(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, [propagationId]);

  // Auto-fetch when propagationId changes
  useEffect(() => {
    if (propagationId) {
      fetch();
    }
  }, [propagationId]);

  const refresh = useCallback(() => {
    fetch();
  }, [fetch]);

  return { propagation, loading, error, fetch, refresh, setPropagation };
};

// Hook for creating propagation
export const useCreatePropagation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const create = useCallback(async (data) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/propagations', data);
      return response.data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  }, []);

  return { create, loading, error };
};

// Hook for updating propagation
export const useUpdatePropagation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const update = useCallback(async (propagationId, data) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.put(`/propagations/${propagationId}`, data);
      return response.data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  }, []);

  return { update, loading, error };
};

// Hook for deleting propagation
export const useDeletePropagation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const delete_ = useCallback(async (propagationId) => {
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/propagations/${propagationId}`);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  }, []);

  return { delete: delete_, loading, error };
};

// Hook for adding event
export const useAddPropagationEvent = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const addEvent = useCallback(async (propagationId, eventData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post(`/propagations/${propagationId}/events`, eventData);
      return response.data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  }, []);

  return { addEvent, loading, error };
};

// Hook for getting events
export const useGetPropagationEvents = (propagationId) => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    if (!propagationId) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/propagations/${propagationId}/events`);
      setEvents(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, [propagationId]);

  return { events, loading, error, fetch, setEvents };
};

// Hook for getting timeline
export const useGetPropagationTimeline = (propagationId) => {
  const [timeline, setTimeline] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    if (!propagationId) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/propagations/${propagationId}/timeline`);
      setTimeline(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, [propagationId]);

  return { timeline, loading, error, fetch };
};

// Hook for getting genealogy
export const useGetGenealogy = (plantId) => {
  const [genealogy, setGenealogy] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    if (!plantId) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/propagations/${plantId}/genealogy`);
      setGenealogy(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, [plantId]);

  return { genealogy, loading, error, fetch };
};

// Hook for getting stats
export const useGetPropagationStats = (parentPlantId = null) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = parentPlantId ? `?parent_plant_id=${parentPlantId}` : '';
      const response = await api.get(`/propagations/stats/overview${params}`);
      setStats(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, [parentPlantId]);

  return { stats, loading, error, fetch };
};

// Hook for getting overdue propagations
export const useGetOverduePropagations = () => {
  const [overdue, setOverdue] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/propagations/alerts/overdue');
      setOverdue(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { overdue, loading, error, fetch };
};

// Hook for converting a propagation to a plant
export const useConvertPropagation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const convert = useCallback(async (propagationId, data) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post(`/propagations/${propagationId}/convert`, data);
      return response.data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  }, []);

  return { convert, loading, error };
};

// Hook for getting calendar events
export const useGetCalendarEvents = (year, month) => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    if (!year || !month) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/propagations/calendar/month?year=${year}&month=${month}`);
      setEvents(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, [year, month]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  const refresh = useCallback(() => {
    fetch();
  }, [fetch]);

  return { events, loading, error, refresh };
};
