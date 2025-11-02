import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, Settings as SettingsIcon } from 'lucide-react'
import { lookupsAPI } from '../lib/api'
import TagsManagement from '../components/TagsManagement'

// Helper function to pluralize "unité"
const pluralizeUnit = (count) => count > 1 ? 'unités' : 'unité'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('units')
  
  // Units state
  const [units, setUnits] = useState([])
  const [fertilizerTypes, setFertilizerTypes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  
  // Form data
  const [formData, setFormData] = useState({
    name: '',
    symbol: '',
    description: ''
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)
      const [unitsRes, fertRes] = await Promise.all([
        lookupsAPI.getUnits(),
        lookupsAPI.getFertilizerTypes()
      ])
      setUnits(unitsRes.data || [])
      setFertilizerTypes(fertRes.data || [])
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err)
      setError('Impossible de charger les données')
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setShowForm(false)
    setEditingId(null)
    setFormData({
      name: '',
      symbol: '',
      description: ''
    })
    setError(null)
  }

  const handleSubmitUnit = async (e) => {
    e.preventDefault()
    if (!formData.name.trim()) {
      setError('Le nom de l\'unité est requis')
      return
    }
    if (!formData.symbol.trim()) {
      setError('Le symbole de l\'unité est requis')
      return
    }

    try {
      setError(null)
      const data = {
        name: formData.name,
        symbol: formData.symbol,
        description: formData.description
      }
      if (editingId) {
        await lookupsAPI.updateUnit(editingId, data)
      } else {
        await lookupsAPI.createUnit(data)
      }
      resetForm()
      await loadData()
    } catch (err) {
      console.error('Erreur lors de la sauvegarde:', err)
      setError(err.response?.data?.detail || 'Erreur lors de la sauvegarde')
    }
  }

  const handleDeleteUnit = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette unité ?')) {
      try {
        await lookupsAPI.deleteUnit(id)
        await loadData()
      } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        setError('Impossible de supprimer cette unité')
      }
    }
  }

  const handleEditUnit = (unit) => {
    setEditingId(unit.id)
    setFormData({
      name: unit.name,
      symbol: unit.symbol,
      description: unit.description || ''
    })
    setShowForm(true)
  }

  const handleSubmitFertilizer = async (e) => {
    e.preventDefault()
    if (!formData.name.trim()) {
      setError('Le nom de l\'engrais est requis')
      return
    }

    try {
      setError(null)
      const data = {
        name: formData.name,
        unit: formData.symbol,
        description: formData.description
      }
      if (editingId) {
        await lookupsAPI.updateFertilizerType(editingId, data)
      } else {
        await lookupsAPI.createFertilizerType(data)
      }
      resetForm()
      await loadData()
    } catch (err) {
      console.error('Erreur lors de la sauvegarde:', err)
      setError(err.response?.data?.detail || 'Erreur lors de la sauvegarde')
    }
  }

  const handleDeleteFertilizer = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce type d\'engrais ?')) {
      try {
        await lookupsAPI.deleteFertilizerType(id)
        await loadData()
      } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        setError('Impossible de supprimer ce type d\'engrais')
      }
    }
  }

  const handleEditFertilizer = (fertilizer) => {
    setEditingId(fertilizer.id)
    setFormData({
      name: fertilizer.name,
      symbol: fertilizer.unit || 'ml',
      description: fertilizer.description || ''
    })
    setShowForm(true)
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex items-center gap-3 mb-6">
        <SettingsIcon className="w-6 h-6 text-gray-700" />
        <h1 className="text-3xl font-bold text-gray-900">Paramètres</h1>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-gray-200">
        <button
          onClick={() => {
            setActiveTab('units')
            resetForm()
          }}
          className={`px-4 py-2 font-medium transition ${
            activeTab === 'units'
              ? 'border-b-2 border-green-500 text-green-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          {pluralizeUnit(units.length).charAt(0).toUpperCase() + pluralizeUnit(units.length).slice(1)}
        </button>
        <button
          onClick={() => {
            setActiveTab('fertilizers')
            resetForm()
          }}
          className={`px-4 py-2 font-medium transition ${
            activeTab === 'fertilizers'
              ? 'border-b-2 border-green-500 text-green-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Types d'engrais
        </button>
        <button
          onClick={() => {
            setActiveTab('tags')
            resetForm()
          }}
          className={`px-4 py-2 font-medium transition ${
            activeTab === 'tags'
              ? 'border-b-2 border-indigo-500 text-indigo-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Tags 🏷️
        </button>
      </div>

      {/* Units Tab */}
      {activeTab === 'units' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-800">
              Gérer les {pluralizeUnit(units.length)}
            </h2>
            <button
              onClick={() => {
                resetForm()
                setShowForm(true)
              }}
              className="flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition"
            >
              <Plus className="w-4 h-4" />
              Ajouter une {pluralizeUnit(1)}
            </button>
          </div>

          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 rounded-md p-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {/* Form */}
          {showForm && (
            <div className="mb-6 bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-4">
              <h3 className="font-semibold text-gray-800">
                {editingId ? 'Modifier l\'unité' : 'Ajouter une nouvelle unité'}
              </h3>
              <form onSubmit={handleSubmitUnit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nom *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    placeholder="Ex: millilitre, gramme..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Symbole *
                  </label>
                  <input
                    type="text"
                    value={formData.symbol}
                    onChange={(e) => setFormData({...formData, symbol: e.target.value})}
                    placeholder="Ex: ml, g, L..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description (optionnel)
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    placeholder="Ex: Unité de volume..."
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

          {/* List */}
          {loading ? (
            <div className="text-center py-8">
              <p className="text-gray-500">Chargement...</p>
            </div>
          ) : units.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500">Aucune unité</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Nom</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Symbole</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Description</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {units.map((unit) => (
                    <tr key={unit.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-gray-900 font-medium">{unit.name}</td>
                      <td className="py-3 px-4 text-gray-600">
                        <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">
                          {unit.symbol}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 text-sm">
                        {unit.description || '-'}
                      </td>
                      <td className="py-3 px-4 text-center">
                        <div className="flex gap-2 justify-center">
                          <button
                            onClick={() => handleEditUnit(unit)}
                            className="text-blue-500 hover:text-blue-700 transition"
                            title="Modifier"
                          >
                            <Edit className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDeleteUnit(unit.id)}
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
      )}

      {/* Fertilizer Types Tab */}
      {activeTab === 'fertilizers' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-800">Types d'engrais</h2>
            <button
              onClick={() => {
                resetForm()
                setShowForm(true)
              }}
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

          {/* Form */}
          {showForm && (
            <div className="mb-6 bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-4">
              <h3 className="font-semibold text-gray-800">
                {editingId ? 'Modifier l\'engrais' : 'Ajouter un nouvel engrais'}
              </h3>
              <form onSubmit={handleSubmitFertilizer} className="space-y-4">
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

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Unité *
                  </label>
                  <select
                    value={formData.symbol}
                    onChange={(e) => setFormData({...formData, symbol: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    <option value="">Sélectionner une unité</option>
                    <option value="ml">ml (millilitre)</option>
                    <option value="g">g (gramme)</option>
                    <option value="cuillère">cuillère</option>
                    <option value="bâton">bâton</option>
                    <option value="pastille">pastille</option>
                    <option value="dose">dose</option>
                  </select>
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

          {/* List */}
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
                            onClick={() => handleEditFertilizer(fert)}
                            className="text-blue-500 hover:text-blue-700 transition"
                            title="Modifier"
                          >
                            <Edit className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDeleteFertilizer(fert.id)}
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
      )}

      {/* Tags Tab */}
      {activeTab === 'tags' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <TagsManagement />
        </div>
      )}
    </div>
  )
}
