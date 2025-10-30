import { useState, useEffect } from 'react'
import axios from 'axios'

import { API_CONFIG, API_ENDPOINTS } from '../config'

const api = axios.create({ baseURL: API_CONFIG.BASE_URL })

export function useWateringHistory(plantId) {
  const [wateringHistory, setWateringHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Charger l'historique d'arrosage
  const loadWateringHistory = async () => {
    if (!plantId) return

    setLoading(true)
    setError(null)
    try {
      const response = await api.get(API_ENDPOINTS.wateringHistory(plantId))
      setWateringHistory(response.data)
    } catch (err) {
      setError(err.message)
      console.error('Erreur lors du chargement de l\'historique d\'arrosage:', err)
    } finally {
      setLoading(false)
    }
  }

  // Ajouter un arrosage
  const addWatering = async (wateringData) => {
    setLoading(true)
    setError(null)
    try {
      // Convertir les chaînes vides en null pour les champs optionnels
      const cleanData = {
        date: wateringData.date,
        amount_ml: wateringData.amount_ml ? parseInt(wateringData.amount_ml) : null,
        notes: wateringData.notes && wateringData.notes.trim() ? wateringData.notes : null
      }
      const response = await api.post(API_ENDPOINTS.wateringHistory(plantId), cleanData)
      setWateringHistory(prev => [response.data, ...prev])
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Modifier un arrosage
  const updateWatering = async (wateringId, wateringData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.put(`${API_ENDPOINTS.wateringHistory(plantId)}/${wateringId}`, wateringData)
      setWateringHistory(prev =>
        prev.map(item => item.id === wateringId ? response.data : item)
      )
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Supprimer un arrosage
  const deleteWatering = async (wateringId) => {
    setLoading(true)
    setError(null)
    try {
      await api.delete(`${API_ENDPOINTS.wateringHistory(plantId)}/${wateringId}`)
      setWateringHistory(prev => prev.filter(item => item.id !== wateringId))
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Recharger automatiquement quand plantId change
  useEffect(() => {
    loadWateringHistory()
  }, [plantId])

  return {
    wateringHistory,
    loading,
    error,
    addWatering,
    updateWatering,
    deleteWatering,
    reload: loadWateringHistory
  }
}