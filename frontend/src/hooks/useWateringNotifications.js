import { useState, useEffect } from 'react'
import api from '../lib/api'

/**
 * Hook pour charger les plantes à arroser
 * @returns {Object} { plantsToWater, loading, error, refresh }
 */
export function usePlantsToWater() {
  const [plantsToWater, setPlantsToWater] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const loadPlantsToWater = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get('/plants/to-water')
      setPlantsToWater(response.data || [])
    } catch (err) {
      setError(err.message)
      setPlantsToWater([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPlantsToWater()
    // Recharger toutes les 5 minutes
    const interval = setInterval(loadPlantsToWater, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  return {
    plantsToWater,
    loading,
    error,
    refresh: loadPlantsToWater,
    count: plantsToWater.length,
  }
}

/**
 * Hook pour charger les plantes à fertiliser
 */
export function usePlantsToFertilize() {
  const [plantsToFertilize, setPlantsToFertilize] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const loadPlantsToFertilize = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get('/plants/to-fertilize')
      setPlantsToFertilize(response.data || [])
    } catch (err) {
      setError(err.message)
      setPlantsToFertilize([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPlantsToFertilize()
    // Recharger toutes les 5 minutes
    const interval = setInterval(loadPlantsToFertilize, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  return {
    plantsToFertilize,
    loading,
    error,
    refresh: loadPlantsToFertilize,
    count: plantsToFertilize.length,
  }
}

/**
 * Hook pour charger les stats de notifications
 */
export function useWateringStats() {
  const water = usePlantsToWater()
  const fertilize = usePlantsToFertilize()

  return {
    toWater: water.count,
    toFertilize: fertilize.count,
    total: water.count + fertilize.count,
    loading: water.loading || fertilize.loading,
    error: water.error || fertilize.error,
  }
}
