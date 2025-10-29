import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, AlertCircle } from 'lucide-react'
import { useDiseaseHistory } from '../hooks/useDiseaseHistory'

const API_BASE = 'http://127.0.0.1:8002/api'

export default function DiseaseHistory({ plantId }) {
  const { diseaseHistory, loading, error, addDisease, updateDisease, deleteDisease, getAllDiseases } = useDiseaseHistory(plantId)
  const [showForm, setShowForm] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    disease_type_id: '',
    treatment_type_id: '',
    health_status_id: '',
    treated_date: '',
    recovered: false,
    notes: ''
  })
  const [lookups, setLookups] = useState({
    diseaseTypes: [],
    treatmentTypes: [],
    healthStatuses: []
  })
  const [lookupsLoading, setLookupsLoading] = useState(true)

  // Charger les lookups
  useEffect(() => {
    const loadLookups = async () => {
      try {
        const [diseaseRes, treatmentRes, healthRes] = await Promise.all([
          fetch(`${API_BASE}/lookups/disease-types`),
          fetch(`${API_BASE}/lookups/treatment-types`),
          fetch(`${API_BASE}/lookups/plant-health-statuses`)
        ])
        const diseaseData = diseaseRes.ok ? await diseaseRes.json() : []
        const treatmentData = treatmentRes.ok ? await treatmentRes.json() : []
        const healthData = healthRes.ok ? await healthRes.json() : []
        setLookups({ diseaseTypes: diseaseData, treatmentTypes: treatmentData, healthStatuses: healthData })
      } catch (error) {
        console.error('Erreur lookups:', error)
      } finally {
        setLookupsLoading(false)
      }
    }
    loadLookups()
  }, [])

  useEffect(() => {
    getAllDiseases()
  }, [plantId])

  const getNameFromId = (id, type) => {
    let data = []
    if (type === 'disease') data = lookups.diseaseTypes
    else if (type === 'treatment') data = lookups.treatmentTypes
    else if (type === 'health') data = lookups.healthStatuses
    const item = data.find(d => d.id === id)
    return item ? item.name : `ID: ${id}`
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingItem) {
        await updateDisease(editingItem.id, formData)
      } else {
        await addDisease(formData)
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
      disease_type_id: item.disease_type_id || '',
      treatment_type_id: item.treatment_type_id || '',
      health_status_id: item.health_status_id || '',
      treated_date: item.treated_date || '',
      recovered: item.recovered || false,
      notes: item.notes || ''
    })
    setShowForm(true)
  }

  const handleDelete = async (diseaseId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette maladie ?')) {
      try {
        await deleteDisease(diseaseId)
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
      disease_type_id: '',
      treatment_type_id: '',
      health_status_id: '',
      treated_date: '',
      recovered: false,
      notes: ''
    })
  }

  const getStatusBadge = (recovered) => {
    return recovered 
      ? { label: 'Rétablie', color: 'bg-green-100 text-green-800' }
      : { label: 'En cours', color: 'bg-red-100 text-red-800' }
  }

  if (loading && diseaseHistory.length === 0) {
    return (
      <div className="text-center py-4">
        <p className="text-gray-500">Chargement des maladies...</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {/* En-tête avec bouton ajouter */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <h3 className="text-sm font-semibold text-gray-700">Historique des maladies</h3>
          <span className="inline-block bg-red-100 text-red-800 text-xs font-bold px-2 py-0.5 rounded-full">
            {diseaseHistory.length}
          </span>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-1 bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-xs transition"
        >
          <Plus className="w-3 h-3" />
          Ajouter
        </button>
      </div>

      {/* Formulaire */}
      {showForm && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 space-y-3">
          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Date *</label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => setFormData({...formData, date: e.target.value})}
                required
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Type de maladie *</label>
              <select
                value={formData.disease_type_id}
                onChange={(e) => setFormData({...formData, disease_type_id: e.target.value})}
                required
                disabled={lookupsLoading}
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="">-- Sélectionner --</option>
                {lookups.diseaseTypes.map(dt => (
                  <option key={dt.id} value={dt.id}>{dt.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Type de traitement</label>
              <select
                value={formData.treatment_type_id}
                onChange={(e) => setFormData({...formData, treatment_type_id: e.target.value})}
                disabled={lookupsLoading}
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="">-- Sélectionner (optionnel) --</option>
                {lookups.treatmentTypes.map(tt => (
                  <option key={tt.id} value={tt.id}>{tt.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">État de santé</label>
              <select
                value={formData.health_status_id}
                onChange={(e) => setFormData({...formData, health_status_id: e.target.value})}
                disabled={lookupsLoading}
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="">-- Sélectionner (optionnel) --</option>
                {lookups.healthStatuses.map(hs => (
                  <option key={hs.id} value={hs.id}>{hs.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Date du traitement</label>
              <input
                type="date"
                value={formData.treated_date}
                onChange={(e) => setFormData({...formData, treated_date: e.target.value})}
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div>
              <label className="flex items-center gap-2 text-xs font-medium text-gray-700">
                <input
                  type="checkbox"
                  checked={formData.recovered}
                  onChange={(e) => setFormData({...formData, recovered: e.target.checked})}
                  className="w-4 h-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
                />
                Rétablie
              </label>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Notes</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
                rows="2"
                placeholder="Notes additionnelles..."
                className="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500 resize-none"
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                className="flex-1 bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-xs transition"
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
      {diseaseHistory.length === 0 ? (
        <div className="text-center py-4 bg-gray-50 rounded border border-gray-200">
          <p className="text-xs text-gray-500">Aucune maladie enregistrée</p>
        </div>
      ) : (
        <div className="space-y-2">
          {diseaseHistory.map(item => {
            const badge = getStatusBadge(item.recovered)
            return (
              <div key={item.id} className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p className="text-xs font-semibold text-gray-900">
                      {getNameFromId(item.disease_type_id, 'disease')}
                    </p>
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded ${badge.color}`}>
                      {badge.label}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">{new Date(item.date).toLocaleDateString('fr-FR')}</p>
                  {item.treatment_type_id && (
                    <p className="text-xs text-gray-600">Traitement: {getNameFromId(item.treatment_type_id, 'treatment')}</p>
                  )}
                  {item.treated_date && (
                    <p className="text-xs text-gray-600">Traité le: {new Date(item.treated_date).toLocaleDateString('fr-FR')}</p>
                  )}
                  {item.health_status_id && (
                    <p className="text-xs text-gray-600">État: {getNameFromId(item.health_status_id, 'health')}</p>
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
            )
          })}
        </div>
      )}
    </div>
  )
}
