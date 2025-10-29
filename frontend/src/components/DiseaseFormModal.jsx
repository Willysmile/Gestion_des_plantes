import { useState } from 'react'
import { X } from 'lucide-react'
import { useDiseaseHistory } from '../hooks/useDiseaseHistory'

export function DiseaseFormModal({ plantId, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    disease_name: '',
    treatment: '',
    treated_date: '',
    recovered: false,
    notes: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { addDisease } = useDiseaseHistory(plantId)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      await addDisease({
        date: formData.date,
        disease_name: formData.disease_name,
        treatment: formData.treatment,
        treated_date: formData.treated_date,
        recovered: formData.recovered,
        notes: formData.notes
      })

      onSuccess?.()
      onClose()
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la maladie:', error)
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
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date <span className="text-red-500">*</span>
            </label>
            <input
              type="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nom de la maladie <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              name="disease_name"
              placeholder="Ex: Mildiou, Rouille..."
              value={formData.disease_name}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Traitement appliqué
            </label>
            <input
              type="text"
              name="treatment"
              placeholder="Ex: Fongicide sulfate de cuivre"
              value={formData.treatment}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
            />
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
