import { useState } from 'react'
import { X } from 'lucide-react'
import { useRepottingHistory } from '../hooks/useRepottingHistory'
import { getTodayDateString } from '../utils/dateUtils'

export function RepottingFormModal({ plantId, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    soil_type: '',
    pot_size_before: '',
    pot_size_after: '',
    notes: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const { addRepotting } = useRepottingHistory(plantId)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)

    try {
      await addRepotting({
        date: formData.date,
        soil_type: formData.soil_type,
        pot_size_before: formData.pot_size_before,
        pot_size_after: formData.pot_size_after,
        notes: formData.notes
      })

      onSuccess?.()
      onClose()
    } catch (error) {
      console.error('Erreur lors de l\'ajout du rempotage:', error)
      if (error.response?.data?.detail) {
        setError(error.response.data.detail)
      } else if (error.response?.data) {
        const firstError = Array.isArray(error.response.data) 
          ? error.response.data[0]?.msg 
          : error.response.data.detail
        setError(firstError || 'Erreur lors de l\'ajout du rempotage')
      } else {
        setError('Erreur lors de l\'ajout du rempotage')
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
          <h2 className="text-lg font-semibold text-gray-800">Ajouter un rempotage</h2>
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
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type de terreau
            </label>
            <input
              type="text"
              name="soil_type"
              placeholder="Ex: Terreau universel"
              value={formData.soil_type}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Taille du pot avant rempotage
            </label>
            <input
              type="text"
              name="pot_size_before"
              placeholder="Ex: 20cm"
              value={formData.pot_size_before}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Taille du pot après rempotage
            </label>
            <input
              type="text"
              name="pot_size_after"
              placeholder="Ex: 25cm"
              value={formData.pot_size_after}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
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
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
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
              className="flex-1 px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg transition disabled:opacity-50"
            >
              {isSubmitting ? 'Ajout...' : 'Ajouter'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
