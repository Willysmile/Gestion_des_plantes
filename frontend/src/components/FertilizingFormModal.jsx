import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { useFertilizingHistory } from '../hooks/useFertilizingHistory'
import { lookupsAPI } from '../lib/api'
import { getTodayDateString } from '../utils/dateUtils'

export function FertilizingFormModal({ plantId, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    fertilizer_type_id: '',
    amount: '',
    notes: ''
  })
  const [fertilizerTypes, setFertilizerTypes] = useState([])
  const [selectedFertilizer, setSelectedFertilizer] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const { addFertilizing } = useFertilizingHistory(plantId)

  // Charger les types d'engrais au montage
  useEffect(() => {
    const loadFertilizerTypes = async () => {
      try {
        const response = await lookupsAPI.getFertilizerTypes()
        setFertilizerTypes(response.data)
        setIsLoading(false)
      } catch (error) {
        console.error('Erreur lors du chargement des types d\'engrais:', error)
        setIsLoading(false)
      }
    }
    loadFertilizerTypes()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)

    try {
      await addFertilizing({
        date: formData.date,
        fertilizer_type_id: formData.fertilizer_type_id ? parseInt(formData.fertilizer_type_id) : null,
        amount: formData.amount,
        notes: formData.notes
      })

      onSuccess?.()
      onClose()
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la fertilisation:', error)
      if (error.response?.data?.detail) {
        setError(error.response.data.detail)
      } else if (error.response?.data) {
        const firstError = Array.isArray(error.response.data) 
          ? error.response.data[0]?.msg 
          : error.response.data.detail
        setError(firstError || 'Erreur lors de l\'ajout de la fertilisation')
      } else {
        setError('Erreur lors de l\'ajout de la fertilisation')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    
    // Si on sélectionne un engrais, chercher ses détails
    if (name === 'fertilizer_type_id') {
      const fert = fertilizerTypes.find(f => f.id.toString() === value)
      setSelectedFertilizer(fert || null)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-800">Ajouter une fertilisation</h2>
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
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type d'engrais
            </label>
            {isLoading ? (
              <div className="w-full px-3 py-2 border border-gray-300 rounded-lg text-gray-500">
                Chargement...
              </div>
            ) : (
              <select
                name="fertilizer_type_id"
                value={formData.fertilizer_type_id}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">Sélectionner un engrais</option>
                {fertilizerTypes.map(fert => (
                  <option key={fert.id} value={fert.id}>
                    {fert.name} ({fert.unit})
                  </option>
                ))}
              </select>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Quantité {selectedFertilizer && `(${selectedFertilizer.unit})`}
            </label>
            <input
              type="number"
              name="amount"
              placeholder="Ex: 50"
              value={formData.amount}
              onChange={handleChange}
              step="0.1"
              min="0"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
              className="flex-1 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition disabled:opacity-50"
            >
              {isSubmitting ? 'Ajout...' : 'Ajouter'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
