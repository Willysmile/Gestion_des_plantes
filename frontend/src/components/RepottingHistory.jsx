import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, Flower2 } from 'lucide-react'
import { useRepottingHistory } from '../hooks/useRepottingHistory'

export default function RepottingHistory({ plantId }) {
  const { repottingHistory, loading, error, addRepotting, updateRepotting, deleteRepotting, getAllRepotting } = useRepottingHistory(plantId)
  const [showForm, setShowForm] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    soil_type: '',
    pot_size: '',
    notes: ''
  })

  useEffect(() => {
    getAllRepotting()
  }, [plantId])

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingItem) {
        await updateRepotting(editingItem.id, formData)
      } else {
        await addRepotting(formData)
      }
      resetForm()
    } catch (err) {
      console.error('Erreur lors de la sauvegarde:', err)
    }
  }

  const handleEdit = (item) => {
    setEditingItem(item)
    setFormData({
      date: item.date,
      soil_type: item.soil_type || '',
      pot_size: item.pot_size || '',
      notes: item.notes || ''
    })
    setShowForm(true)
  }

  const handleDelete = async (repottingId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce rempotage ?')) {
      try {
        await deleteRepotting(repottingId)
      } catch (err) {
        console.error('Erreur lors de la suppression:', err)
      }
    }
  }

  const resetForm = () => {
    setShowForm(false)
    setEditingItem(null)
    setFormData({
      date: new Date().toISOString().split('T')[0],
      soil_type: '',
      pot_size: '',
      notes: ''
    })
  }

  if (loading && repottingHistory.length === 0) {
    return (
      <div className="text-center py-4">
        <p className="text-gray-500">Chargement des rempotages...</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {/* En-tête avec bouton ajouter */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Flower2 className="w-4 h-4 text-yellow-500" />
          <h3 className="text-sm font-semibold text-gray-700">Historique de rempotage</h3>
          <span className="inline-block bg-yellow-100 text-yellow-800 text-xs font-bold px-2 py-0.5 rounded-full">
            {repottingHistory.length}
          </span>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-1 bg-yellow-500 hover:bg-yellow-600 text-white px-2 py-1 rounded text-xs transition"
        >
          <Plus className="w-3 h-3" />
          Ajouter
        </button>
      </div>

      {/* Formulaire */}
      {showForm && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 space-y-3">
          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Date *</label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => setFormData({...formData, date: e.target.value})}
                required
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Type de terre</label>
              <input
                type="text"
                value={formData.soil_type}
                onChange={(e) => setFormData({...formData, soil_type: e.target.value})}
                placeholder="Ex: Terreau drainant"
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Taille du pot</label>
              <input
                type="text"
                value={formData.pot_size}
                onChange={(e) => setFormData({...formData, pot_size: e.target.value})}
                placeholder="Ex: 20cm"
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Notes</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
                rows="2"
                placeholder="Notes additionnelles..."
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-yellow-500 resize-none"
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                className="flex-1 bg-yellow-500 hover:bg-yellow-600 text-white px-2 py-1 rounded text-xs transition"
              >
                {editingItem ? 'Modifier' : 'Ajouter'}
              </button>
              <button
                type="button"
                onClick={resetForm}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-2 py-1 rounded text-xs transition"
              >
                Annuler
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Liste */}
      {repottingHistory.length === 0 ? (
        <div className="text-center py-4 bg-gray-50 rounded border border-gray-200">
          <p className="text-xs text-gray-500">Aucun rempotage enregistré</p>
        </div>
      ) : (
        <div className="space-y-2">
          {repottingHistory.map(item => (
            <div key={item.id} className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 flex items-start justify-between">
              <div className="flex-1">
                <p className="text-xs font-semibold text-gray-900">{new Date(item.date).toLocaleDateString('fr-FR')}</p>
                {item.soil_type && (
                  <p className="text-xs text-gray-600 mt-1">Terre: {item.soil_type}</p>
                )}
                {item.pot_size && (
                  <p className="text-xs text-gray-600">Pot: {item.pot_size}</p>
                )}
                {item.notes && (
                  <p className="text-xs text-gray-500 italic mt-1">{item.notes}</p>
                )}
              </div>
              <div className="flex gap-1 ml-2">
                <button
                  onClick={() => handleEdit(item)}
                  className="text-blue-500 hover:text-blue-700 transition"
                  title="Modifier"
                >
                  <Edit className="w-3 h-3" />
                </button>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="text-red-500 hover:text-red-700 transition"
                  title="Supprimer"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
