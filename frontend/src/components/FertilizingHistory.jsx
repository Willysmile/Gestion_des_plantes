import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, Leaf } from 'lucide-react'
import { useFertilizingHistory } from '../hooks/useFertilizingHistory'
import { lookupsAPI } from '../lib/api'
import { getTodayDateString } from '../utils/dateUtils'

export default function FertilizingHistory({ plantId }) {
  const { fertilizingHistory, loading, error, addFertilizing, updateFertilizing, deleteFertilizing, getAllFertilizing } = useFertilizingHistory(plantId)
  const [showForm, setShowForm] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [fertilizerTypes, setFertilizerTypes] = useState([])
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    fertilizer_type_id: '',
    amount: '',
    notes: ''
  })

  // Charger les types d'engrais et l'historique au montage
  useEffect(() => {
    const loadTypes = async () => {
      try {
        const response = await lookupsAPI.getFertilizerTypes()
        setFertilizerTypes(response.data || [])
      } catch (err) {
        console.error('Erreur lors du chargement des types d\'engrais:', err)
      }
    }
    loadTypes()
    getAllFertilizing()
  }, [plantId])

  const getFertilizerTypeName = (fertilizerTypeId) => {
    if (!fertilizerTypeId) return 'N/A'
    const fert = fertilizerTypes.find(f => f.id === fertilizerTypeId)
    return fert ? fert.name : 'Type inconnu'
  }

  const getFertilizerUnit = (fertilizerTypeId) => {
    if (!fertilizerTypeId) return 'ml'
    const fert = fertilizerTypes.find(f => f.id === fertilizerTypeId)
    return fert ? fert.unit : 'ml'
  }

  // Pluraliser une unité (ex: "1 ml" vs "2 ml")
  const pluralizeUnit = (unit, amount) => {
    // Remplacer "unité" par "bâton d'engrais"
    let displayUnit = unit === 'unité' ? 'bâton d\'engrais' : unit
    
    if (!amount || amount === 1) return displayUnit
    // Certaines unités ont des formes plurielles en français
    const plurals = {
      'bâton d\'engrais': 'bâtons d\'engrais',
      'bâton': 'bâtons',
      'pastille': 'pastilles',
      'cuillère': 'cuillères',
      'dose': 'doses',
      'unité': 'unités'
    }
    return plurals[displayUnit] || displayUnit
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingItem) {
        await updateFertilizing(editingItem.id, formData)
      } else {
        await addFertilizing(formData)
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
      fertilizer_type_id: item.fertilizer_type_id || '',
      amount: item.amount || '',
      notes: item.notes || ''
    })
    setShowForm(true)
  }

  const handleDelete = async (fertilizingId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette fertilisation ?')) {
      try {
        await deleteFertilizing(fertilizingId)
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
      fertilizer_type_id: '',
      amount: '',
      notes: ''
    })
  }

  if (loading && fertilizingHistory.length === 0) {
    return (
      <div className="text-center py-4">
        <p className="text-gray-500">Chargement des fertilisations...</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {/* En-tête avec bouton ajouter */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Leaf className="w-4 h-4 text-green-500" />
          <h3 className="text-sm font-semibold text-gray-700">Historique de fertilisation</h3>
          <span className="inline-block bg-green-100 text-green-800 text-xs font-bold px-2 py-0.5 rounded-full">
            {fertilizingHistory.length}
          </span>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-1 bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded text-xs transition"
        >
          <Plus className="w-3 h-3" />
          Ajouter
        </button>
      </div>

      {/* Formulaire */}
      {showForm && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 space-y-3">
          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Date *</label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => setFormData({...formData, date: e.target.value})}
                max={getTodayDateString()}
                required
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Type d'engrais</label>
              <select
                value={formData.fertilizer_type_id}
                onChange={(e) => setFormData({...formData, fertilizer_type_id: e.target.value})}
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">Sélectionner un engrais</option>
                {fertilizerTypes.map(fert => (
                  <option key={fert.id} value={fert.id}>
                    {fert.name} ({fert.unit})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Quantité</label>
              <input
                type="number"
                value={formData.amount}
                onChange={(e) => setFormData({...formData, amount: e.target.value})}
                step="0.1"
                min="0"
                placeholder="Ex: 50"
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Notes</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
                rows="2"
                placeholder="Notes additionnelles..."
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                className="flex-1 bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded text-xs transition"
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
      {fertilizingHistory.length === 0 ? (
        <div className="text-center py-4 bg-gray-50 rounded border border-gray-200">
          <p className="text-xs text-gray-500">Aucune fertilisation enregistrée</p>
        </div>
      ) : (
        <div className="space-y-2">
          {fertilizingHistory.map(item => (
            <div key={item.id} className="bg-green-50 border border-green-200 rounded-lg p-3 flex items-start justify-between">
              <div className="flex-1">
                <p className="text-xs font-semibold text-gray-900">{getFertilizerTypeName(item.fertilizer_type_id)}</p>
                <p className="text-xs text-gray-600 mt-1">{new Date(item.date).toLocaleDateString('fr-FR')}</p>
                {item.amount && (
                  <p className="text-xs text-gray-600">{item.amount} {pluralizeUnit(getFertilizerUnit(item.fertilizer_type_id), parseFloat(item.amount))}</p>
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
