import { useState } from 'react'
import axios from 'axios'

import { API_CONFIG, API_ENDPOINTS } from '../config'

const api = axios.create({ baseURL: API_CONFIG.BASE_URL })

export const useRepottingHistory = (plantId) => {
  const [repottingHistory, setRepottingHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Récupérer tous les rempotages
  const getAllRepotting = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(API_ENDPOINTS.repottingHistory(plantId))
      setRepottingHistory(response.data || [])
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Ajouter un rempotage
  const addRepotting = async (repottingData) => {
    setLoading(true)
    setError(null)
    try {
      // Convertir les chaînes vides en null pour les champs optionnels
      const cleanData = {
        date: repottingData.date,
        soil_type: repottingData.soil_type && repottingData.soil_type.trim() ? repottingData.soil_type : null,
        pot_size: repottingData.pot_size && repottingData.pot_size.trim() ? repottingData.pot_size : null,
        notes: repottingData.notes && repottingData.notes.trim() ? repottingData.notes : null
      }
      const response = await api.post(API_ENDPOINTS.repottingHistory(plantId), cleanData)
      setRepottingHistory(prev => [response.data, ...prev])
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Modifier un rempotage
  const updateRepotting = async (historyId, repottingData) => {
    setLoading(true)
    setError(null)
    try {
      const cleanData = {
        soil_type: repottingData.soil_type && repottingData.soil_type.trim() ? repottingData.soil_type : null,
        pot_size: repottingData.pot_size && repottingData.pot_size.trim() ? repottingData.pot_size : null,
        notes: repottingData.notes && repottingData.notes.trim() ? repottingData.notes : null
      }
      const response = await api.put(
        `${API_ENDPOINTS.repottingHistory(plantId)}/${historyId}`,
        cleanData
      )
      setRepottingHistory(prev =>
        prev.map(item => item.id === historyId ? response.data : item)
      )
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Supprimer un rempotage
  const deleteRepotting = async (historyId) => {
    setLoading(true)
    setError(null)
    try {
      await api.delete(`${API_ENDPOINTS.repottingHistory(plantId)}/${historyId}`)
      setRepottingHistory(prev => prev.filter(item => item.id !== historyId))
      return true
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    repottingHistory,
    loading,
    error,
    getAllRepotting,
    addRepotting,
    updateRepotting,
    deleteRepotting
  }
}
