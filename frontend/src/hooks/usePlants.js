import { useState, useEffect, useCallback } from 'react'
import { plantsAPI } from '../lib/api'

export function usePlants() {
  const [plants, setPlants] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetch = useCallback(async (params = {}) => {
    try {
      console.log('🌱 usePlants.fetch() starting...', params)
      setLoading(true)
      const response = await plantsAPI.getAll(params)
      console.log('🌱 API response received:', response)
      setPlants(response.data || [])
      setError(null)
      console.log('🌱 State updated, plants:', (response.data || []).length)
    } catch (err) {
      console.error('🌱 Error in usePlants.fetch():', err)
      setError(err.message || 'Erreur lors du chargement des plantes')
      setPlants([])
    } finally {
      setLoading(false)
      console.log('🌱 usePlants.fetch() completed')
    }
  }, [])

  useEffect(() => {
    let isMounted = true

    const loadData = async () => {
      console.log('🌱 useEffect: loadData() called')
      if (isMounted) await fetch()
    }

    loadData()

    return () => {
      console.log('🌱 useEffect cleanup')
      isMounted = false
    }
  }, [fetch])

  return { plants, loading, error, refetch: fetch }
}

export function usePlant(id) {
  const [plant, setPlant] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!id) {
      setPlant(null)
      setLoading(false)
      return
    }

    let isMounted = true

    const loadPlant = async () => {
      try {
        setLoading(true)
        const response = await plantsAPI.getById(id)
        if (isMounted) {
          setPlant(response.data || null)
          setError(null)
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || 'Erreur lors du chargement de la plante')
          setPlant(null)
        }
      } finally {
        if (isMounted) setLoading(false)
      }
    }

    loadPlant()

    return () => {
      isMounted = false
    }
  }, [id])

  return { plant, loading, error }
}
