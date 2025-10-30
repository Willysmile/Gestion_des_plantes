import { useState } from 'react'
import axios from 'axios'

import { API_CONFIG, API_ENDPOINTS } from '../config'

const api = axios.create({ baseURL: API_CONFIG.BASE_URL })

export const useDiseaseHistory = (plantId) => {
  const [diseaseHistory, setDiseaseHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Récupérer toutes les maladies
  const getAllDiseases = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.get(API_ENDPOINTS.diseaseHistory(plantId))
      setDiseaseHistory(response.data || [])
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Ajouter une maladie
  const addDisease = async (diseaseData) => {
    setLoading(true)
    setError(null)
    try {
      // Convertir les chaînes vides en null pour les champs optionnels
      const cleanData = {
        date: diseaseData.date,
        disease_type_id: diseaseData.disease_type_id || null,
        treatment_type_id: diseaseData.treatment_type_id || null,
        health_status_id: diseaseData.health_status_id || null,
        treated_date: diseaseData.treated_date || null,
        recovered: diseaseData.recovered === true || diseaseData.recovered === 'true',
        notes: diseaseData.notes && diseaseData.notes.trim() ? diseaseData.notes : null
      }
      const response = await api.post(API_ENDPOINTS.diseaseHistory(plantId), cleanData)
      setDiseaseHistory(prev => [response.data, ...prev])
      return response.data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Modifier une maladie
  const updateDisease = async (historyId, diseaseData) => {
    setLoading(true)
    setError(null)
    try {
      const cleanData = {
        disease_type_id: diseaseData.disease_type_id || null,
        treatment_type_id: diseaseData.treatment_type_id || null,
        health_status_id: diseaseData.health_status_id || null,
        treated_date: diseaseData.treated_date || null,
        recovered: diseaseData.recovered === true || diseaseData.recovered === 'true',
        notes: diseaseData.notes && diseaseData.notes.trim() ? diseaseData.notes : null
      }
      const response = await api.put(
        `${API_ENDPOINTS.diseaseHistory(plantId)}/${historyId}`,
        cleanData
      )
      setDiseaseHistory(prev =>
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

  // Supprimer une maladie
  const deleteDisease = async (historyId) => {
    setLoading(true)
    setError(null)
    try {
      await api.delete(`${API_ENDPOINTS.diseaseHistory(plantId)}/${historyId}`)
      setDiseaseHistory(prev => prev.filter(item => item.id !== historyId))
      return true
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    diseaseHistory,
    loading,
    error,
    getAllDiseases,
    addDisease,
    updateDisease,
    deleteDisease
  }
}
