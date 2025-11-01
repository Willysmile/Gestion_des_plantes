import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import api from '../lib/api'

export function SeasonalWateringFormModal({ plant, seasons, wateringFrequencies, onClose, onSuccess }) {
  const [formData, setFormData] = useState({})
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (seasons && seasons.length > 0) {
      // Initialiser avec les fréquences actuelles
      const initial = {}
      seasons.forEach(season => {
        initial[season.id] = ''
      })
      setFormData(initial)
      loadCurrentFrequencies()
    }
  }, [seasons])

  const loadCurrentFrequencies = async () => {
    try {
      // Charger les fréquences saisonnières actuelles
      const promises = seasons.map(season =>
        api.get(`/plants/${plant.id}/seasonal-watering/${season.id}`).catch(() => null)
      )
      const results = await Promise.all(promises)
      
      const data = {}
      results.forEach((result, idx) => {
        if (result?.data?.id) {
          data[seasons[idx].id] = result.data.id
        }
      })
      setFormData(data)
    } catch (err) {
      console.error('Error loading seasonal watering:', err)
    }
  }

  const handleChange = (seasonId, value) => {
    setFormData(prev => ({
      ...prev,
      [seasonId]: value ? parseInt(value, 10) : ''
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Envoyer les mises à jour pour chaque saison
      for (const [seasonId, frequencyId] of Object.entries(formData)) {
        if (frequencyId) {
          await api.put(`/plants/${plant.id}/seasonal-watering/${seasonId}`, {
            watering_frequency_id: frequencyId
          })
        }
      }
      console.log('✅ Fréquences saisonnières mises à jour')
      onSuccess?.()
      onClose()
    } catch (err) {
      console.error('Error updating seasonal watering:', err)
      alert('Erreur lors de la mise à jour des fréquences saisonnières')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg max-w-md w-full mx-4 p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-bold text-gray-900">Fréquence d'arrosage par saison</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {seasons?.map(season => (
            <div key={season.id}>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {season.name}
              </label>
              <select
                value={formData[season.id] || ''}
                onChange={(e) => handleChange(season.id, e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Choisir une fréquence...</option>
                {wateringFrequencies?.map(freq => (
                  <option key={freq.id} value={freq.id}>
                    {freq.name}
                  </option>
                ))}
              </select>
            </div>
          ))}

          <div className="flex gap-2 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-md text-sm font-medium transition"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white rounded-md text-sm font-medium transition"
            >
              {loading ? '...' : 'Enregistrer'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
