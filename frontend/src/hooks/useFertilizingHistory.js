import { useState } from 'react'
import axios from 'axios'
import { API_CONFIG, API_ENDPOINTS } from '../config'

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
})

export const useFertilizingHistory = (plantId) => {
  const [fertilizingHistory, setFertilizingHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Récupérer tous les arrosages
  const getAllFertilizing = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(API_ENDPOINTS.fertilizingHistory(plantId))
      setFertilizingHistory(response.data || [])
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Ajouter une fertilisation
  const addFertilizing = async (fertilizingData) => {
    setLoading(true)
    setError(null)
    try {
      // Convertir les chaînes vides en null pour les champs optionnels
      const cleanData = {
        date: fertilizingData.date,
        fertilizer_type_id: fertilizingData.fertilizer_type_id ? parseInt(fertilizingData.fertilizer_type_id) : null,
        amount: fertilizingData.amount && fertilizingData.amount.trim() ? fertilizingData.amount.trim() : null,
        notes: fertilizingData.notes && fertilizingData.notes.trim() ? fertilizingData.notes.trim() : null
      }
      const response = await api.post(API_ENDPOINTS.fertilizingHistory(plantId), cleanData)
      setFertilizingHistory(prev => [response.data, ...prev])
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Modifier une fertilisation
  const updateFertilizing = async (historyId, fertilizingData) => {
    setLoading(true)
    setError(null)
    try {
      const cleanData = {
        fertilizer_type_id: fertilizingData.fertilizer_type_id ? parseInt(fertilizingData.fertilizer_type_id) : null,
        amount: fertilizingData.amount && fertilizingData.amount.trim() ? fertilizingData.amount.trim() : null,
        notes: fertilizingData.notes && fertilizingData.notes.trim() ? fertilizingData.notes.trim() : null
      }
      console.log('DEBUG updateFertilizing sending:', cleanData)
      const response = await api.put(
        `${API_ENDPOINTS.fertilizingHistory(plantId)}/${historyId}`,
        cleanData
      )
      setFertilizingHistory(prev =>
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

  // Supprimer une fertilisation
  const deleteFertilizing = async (historyId) => {
    setLoading(true)
    setError(null)
    try {
      await api.delete(`${API_ENDPOINTS.fertilizingHistory(plantId)}/${historyId}`)
      setFertilizingHistory(prev => prev.filter(item => item.id !== historyId))
      return true
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    fertilizingHistory,
    loading,
    error,
    getAllFertilizing,
    addFertilizing,
    updateFertilizing,
    deleteFertilizing
  }
}
