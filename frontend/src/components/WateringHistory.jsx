import { useState } from 'react'
import { Plus, Edit, Trash2, Droplets } from 'lucide-react'
import { useWateringHistory } from '../hooks/useWateringHistory'

export default function WateringHistory({ plantId }) {
  const { wateringHistory, loading, error, addWatering, updateWatering, deleteWatering } = useWateringHistory(plantId)
  const [showForm, setShowForm] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    amount_ml: '',
    notes: ''
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingItem) {
        await updateWatering(editingItem.id, formData)
      } else {
        await addWatering(formData)
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
      amount_ml: item.amount_ml || '',
      notes: item.notes || ''
    })
    setShowForm(true)
  }

  const handleDelete = async (wateringId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet arrosage ?')) {
      try {
        await deleteWatering(wateringId)
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
      amount_ml: '',
      notes: ''
    })
  }

  if (loading && wateringHistory.length === 0) {
    return (
      <div className="text-center py-4">
        <p className="text-gray-500">Chargement des arrosages...</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {/* En-tête avec bouton ajouter */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Droplets className="w-4 h-4 text-blue-500" />
          <h3 className="text-sm font-semibold text-gray-700">Historique d'arrosage</h3>
          <span className="inline-block bg-blue-100 text-blue-800 text-xs font-bold px-2 py-0.5 rounded-full">
            {wateringHistory.length}
          </span>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-1 bg-blue-500 hover:bg-blue-600 text-white px-2 py-1 rounded text-xs transition"
        >
          <Plus className="w-3 h-3" />
          Ajouter
        </button>
      </div>

      {/* Formulaire d'ajout/édition */}
      {showForm && (
        <form onSubmit={handleSubmit} className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mb-2">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Date</label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
                className="w-full px-2 py-1 border rounded text-xs"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Quantité (ml)</label>
              <input
                type="number"
                value={formData.amount_ml}
                onChange={(e) => setFormData(prev => ({ ...prev, amount_ml: e.target.value }))}
                className="w-full px-2 py-1 border rounded text-xs"
                placeholder="Ex: 250"
                min="0"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Notes</label>
              <input
                type="text"
                value={formData.notes}
                onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                className="w-full px-2 py-1 border rounded text-xs"
                placeholder="Notes optionnelles"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-xs transition disabled:opacity-50"
            >
              {loading ? 'Sauvegarde...' : (editingItem ? 'Modifier' : 'Ajouter')}
            </button>
            <button
              type="button"
              onClick={resetForm}
              className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-3 py-1 rounded text-xs transition"
            >
              Annuler
            </button>
          </div>
        </form>
      )}

      {/* Liste des arrosages */}
      <div className="space-y-2 max-h-40 overflow-y-auto">
        {wateringHistory.length === 0 ? (
          <p className="text-gray-500 text-xs text-center py-4">Aucun arrosage enregistré</p>
        ) : (
          wateringHistory.map((watering) => (
            <div key={watering.id} className="bg-blue-50 p-2 rounded border border-blue-100 flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-medium text-gray-700">
                    {new Date(watering.date).toLocaleDateString('fr-FR')}
                  </span>
                  {watering.amount_ml && (
                    <span className="text-xs text-blue-600 font-semibold">
                      {watering.amount_ml}ml
                    </span>
                  )}
                </div>
                {watering.notes && (
                  <p className="text-xs text-gray-600">{watering.notes}</p>
                )}
              </div>
              <div className="flex gap-1 ml-2">
                <button
                  onClick={() => handleEdit(watering)}
                  className="text-blue-600 hover:text-blue-800 p-1 rounded transition"
                  title="Modifier"
                >
                  <Edit className="w-3 h-3" />
                </button>
                <button
                  onClick={() => handleDelete(watering.id)}
                  className="text-red-600 hover:text-red-800 p-1 rounded transition"
                  title="Supprimer"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {error && (
        <p className="text-red-600 text-xs text-center">{error}</p>
      )}
    </div>
  )
}