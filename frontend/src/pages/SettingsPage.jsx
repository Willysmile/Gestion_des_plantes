import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, Settings as SettingsIcon } from 'lucide-react'
import { lookupsAPI } from '../lib/api'

export default function SettingsPage() {
  const [fertilizerTypes, setFertilizerTypes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    unit: 'ml',
    description: ''
  })

  useEffect(() => {
    loadFertilizerTypes()
  }, [])

  const loadFertilizerTypes = async () => {
    try {
      setLoading(true)
      const response = await lookupsAPI.getFertilizerTypes()
      setFertilizerTypes(response.data || [])
      setError(null)
    } catch (err) {
      console.error('Erreur lors du chargement des engrais:', err)
      setError('Impossible de charger les types d\'engrais')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.name.trim()) {
      setError('Le nom de l\'engrais est requis')
      return
    }

    try {
      setError(null)
      if (editingId) {
        await lookupsAPI.updateFertilizerType(editingId, formData)
      } else {
        await lookupsAPI.createFertilizerType(formData)
      }
      resetForm()
      await loadFertilizerTypes()
    } catch (err) {
      console.error('Erreur lors de la sauvegarde:', err)
      setError(err.response?.data?.detail || 'Erreur lors de la sauvegarde')
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce type d\'engrais ?')) {
      try {
        await lookupsAPI.deleteFertilizerType(id)
        await loadFertilizerTypes()
      } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        setError('Impossible de supprimer ce type d\'engrais')
      }
    }
  }

  const handleEdit = (fertilizer) => {
    setEditingId(fertilizer.id)
    setFormData({
      name: fertilizer.name,
      unit: fertilizer.unit || 'ml',
      description: fertilizer.description || ''
    })
    setShowForm(true)
  }

  const resetForm = () => {
    setShowForm(false)
    setEditingId(null)
    setFormData({
      name: '',
      unit: 'ml',
      description: ''
    })
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex items-center gap-3 mb-6">
        <SettingsIcon className="w-6 h-6 text-gray-700" />
        <h1 className="text-3xl font-bold text-gray-900">Paramètres</h1>
      </div>

      {/* Types d'engrais */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-800">Types d'engrais</h2>
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition"
          >
            <Plus className="w-4 h-4" />
            Ajouter un engrais
          </button>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 rounded-md p-3">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Formulaire */}
        {showForm && (
          <div className="mb-6 bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-4">
            <h3 className="font-semibold text-gray-800">
              {editingId ? 'Modifier l\'engrais' : 'Ajouter un nouvel engrais'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nom *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  placeholder="Ex: Engrais NPK, Bâtons d'engrais..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Unité *
                  </label>
                  <select
                    value={formData.unit}
                    onChange={(e) => setFormData({...formData, unit: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    <option value="ml">ml (millilitre)</option>
                    <option value="g">g (gramme)</option>
                    <option value="cuillère">cuillère</option>
                    <option value="bâton">bâton</option>
                    <option value="pastille">pastille</option>
                    <option value="dose">dose</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description (optionnel)
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  placeholder="Ex: Engrais complet pour tous les types de plantes..."
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  className="flex-1 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition"
                >
                  {editingId ? 'Modifier' : 'Ajouter'}
                </button>
                <button
                  type="button"
                  onClick={resetForm}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-lg transition"
                >
                  Annuler
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Liste */}
        {loading ? (
          <div className="text-center py-8">
            <p className="text-gray-500">Chargement...</p>
          </div>
        ) : fertilizerTypes.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">Aucun type d'engrais</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Nom</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Unité</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Description</th>
                  <th className="text-center py-3 px-4 font-semibold text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                {fertilizerTypes.map((fert) => (
                  <tr key={fert.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-gray-900 font-medium">{fert.name}</td>
                    <td className="py-3 px-4 text-gray-600">
                      <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">
                        {fert.unit}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-600 text-sm">
                      {fert.description || '-'}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <div className="flex gap-2 justify-center">
                        <button
                          onClick={() => handleEdit(fert)}
                          className="text-blue-500 hover:text-blue-700 transition"
                          title="Modifier"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(fert.id)}
                          className="text-red-500 hover:text-red-700 transition"
                          title="Supprimer"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
