import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { useDiseaseHistory } from '../hooks/useDiseaseHistory'
import { getTodayDateString } from '../utils/dateUtils'
import { API_CONFIG, API_ENDPOINTS } from '../config'

import axios from 'axios'

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
})

export function DiseaseFormModal({ plantId, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    disease_type_id: '',
    treatment_type_id: '',
    health_status_id: '',
    treated_date: '',
    recovered: false,
    notes: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [diseaseTypes, setDiseaseTypes] = useState([])
  const [treatmentTypes, setTreatmentTypes] = useState([])
  const [healthStatuses, setHealthStatuses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const { addDisease } = useDiseaseHistory(plantId)

  // Charger les lookups au montage
  useEffect(() => {
    const loadLookups = async () => {
      try {
        const [diseaseRes, treatmentRes, healthRes] = await Promise.all([
          api.get(API_ENDPOINTS.diseaseTypes),
          api.get(API_ENDPOINTS.treatmentTypes),
          api.get(API_ENDPOINTS.plantHealthStatuses)
        ])
        
        setDiseaseTypes(diseaseRes.data || [])
        setTreatmentTypes(treatmentRes.data || [])
        setHealthStatuses(healthRes.data || [])
      } catch (error) {
        console.error('Erreur lors du chargement des lookups:', error)
      } finally {
        setLoading(false)
      }
    }
    loadLookups()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)

    try {
      await addDisease({
        date: formData.date,
        disease_type_id: formData.disease_type_id ? parseInt(formData.disease_type_id) : null,
        treatment_type_id: formData.treatment_type_id ? parseInt(formData.treatment_type_id) : null,
        health_status_id: formData.health_status_id ? parseInt(formData.health_status_id) : null,
        treated_date: formData.treated_date || null,
        recovered: formData.recovered,
        notes: formData.notes || null
      })

      onSuccess?.()
      onClose()
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la maladie:', error)
      if (error.response?.data?.detail) {
        setError(error.response.data.detail)
      } else if (error.response?.data) {
        const firstError = Array.isArray(error.response.data) 
          ? error.response.data[0]?.msg 
          : error.response.data.detail
        setError(firstError || 'Erreur lors de l\'ajout de la maladie')
      } else {
        setError('Erreur lors de l\'ajout de la maladie')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-800">Ajouter une maladie</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date <span className="text-red-500">*</span>
            </label>
            <input
              type="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              max={getTodayDateString()}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type de maladie <span className="text-red-500">*</span>
            </label>
            <select
              name="disease_type_id"
              value={formData.disease_type_id}
              onChange={handleChange}
              required
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="">-- Sélectionner --</option>
              {diseaseTypes.map(dt => (
                <option key={dt.id} value={dt.id}>{dt.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type de traitement
            </label>
            <select
              name="treatment_type_id"
              value={formData.treatment_type_id}
              onChange={handleChange}
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="">-- Sélectionner (optionnel) --</option>
              {treatmentTypes.map(tt => (
                <option key={tt.id} value={tt.id}>{tt.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              État de santé actuel
            </label>
            <select
              name="health_status_id"
              value={formData.health_status_id}
              onChange={handleChange}
              disabled={loading}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="">-- Sélectionner (optionnel) --</option>
              {healthStatuses.map(hs => (
                <option key={hs.id} value={hs.id}>{hs.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date du traitement
            </label>
            <input
              type="date"
              name="treated_date"
              value={formData.treated_date}
              onChange={handleChange}
              max={getTodayDateString()}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>

          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
              <input
                type="checkbox"
                name="recovered"
                checked={formData.recovered}
                onChange={(e) => setFormData(prev => ({ ...prev, recovered: e.target.checked }))}
                className="w-4 h-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
              />
              Rétablie
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notes
            </label>
            <textarea
              name="notes"
              placeholder="Notes additionnelles..."
              value={formData.notes}
              onChange={handleChange}
              rows="3"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>

          <div className="flex gap-2 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg transition"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition disabled:opacity-50"
            >
              {isSubmitting ? 'Ajout...' : 'Ajouter'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
