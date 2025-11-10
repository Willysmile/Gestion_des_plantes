import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, BookOpen, ChevronDown } from 'lucide-react'
import { Link } from 'react-router-dom'
import api from '../lib/api'
import { getTodayDateString } from '../utils/dateUtils'

export default function NotesHistory({ plantId, hideHeader = false, onClose = () => {} }) {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [showList, setShowList] = useState(!hideHeader)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({
    date: getTodayDateString(),
    title: '',
    note: '',
    category: ''
  })

  // Charger les notes au montage
  useEffect(() => {
    loadNotes()
  }, [plantId])

  const loadNotes = async () => {
    setLoading(true)
    try {
      const response = await api.get(`/plants/${plantId}/plant-history`)
      setNotes(response.data || [])
      setError(null)
    } catch (err) {
      console.error('Erreur chargement notes:', err)
      setError('Impossible de charger les notes')
      setNotes([])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.note.trim()) {
      alert('Veuillez entrer une note')
      return
    }

    try {
      if (editingItem) {
        // Pour la modification, on envoie seulement note, title, category (pas date)
        const updateData = {
          title: formData.title || null,
          note: formData.note,
          category: formData.category || null
        }
        await api.put(`/plants/${plantId}/plant-history/${editingItem.id}`, updateData)
      } else {
        // Pour la création, on envoie tous les champs
        await api.post(`/plants/${plantId}/plant-history`, formData)
      }
      await loadNotes()
      resetForm()
    } catch (err) {
      console.error('Erreur lors de la sauvegarde:', err)
      console.error('Détail erreur complet:', JSON.stringify(err.response?.data, null, 2))
      console.error('Message:', err.response?.data?.detail)
      setError('Erreur lors de la sauvegarde de la note')
    }
  }

  const handleEdit = (item) => {
    setEditingItem(item)
    setFormData({
      date: item.date || getTodayDateString(),
      title: item.title || '',
      note: item.note || '',
      category: item.category || ''
    })
    setShowForm(true)
  }

  const handleDelete = async (noteId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette note ?')) {
      try {
        await api.delete(`/plants/${plantId}/plant-history/${noteId}`)
        await loadNotes()
      } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        setError('Erreur lors de la suppression')
      }
    }
  }

  const resetForm = () => {
    setFormData({
      date: getTodayDateString(),
      title: '',
      note: '',
      category: ''
    })
    setEditingItem(null)
    setShowForm(false)
  }

  return (
    <div className="space-y-3">
      {/* En-tête avec bouton ajouter */}
      <div className="flex items-center justify-between">
        <Link
          to={`/plants/${plantId}/notes`}
          onClick={hideHeader ? onClose : undefined}
          className="flex items-center gap-2 hover:opacity-75 transition flex-1"
        >
          <BookOpen className="w-4 h-4 text-indigo-500" />
          <h3 className="text-sm font-semibold text-gray-700 cursor-pointer">Notes Générales</h3>
          <span className="inline-block bg-indigo-100 text-indigo-800 text-xs font-bold px-2 py-0.5 rounded-full">
            {notes.length}
          </span>
        </Link>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              setShowForm(true)
              setShowList(true)
            }}
            className="flex items-center gap-1 bg-indigo-500 hover:bg-indigo-600 text-white px-2 py-1 rounded text-xs transition"
          >
            <Plus className="w-3 h-3" />
            Ajouter
          </button>
          {hideHeader && (
            <button
              onClick={() => setShowList(!showList)}
              className="p-1 hover:bg-indigo-100 rounded transition"
              title="Dérouler/Replier"
            >
              <ChevronDown className={`w-5 h-5 text-indigo-500 transition-transform ${showList ? 'rotate-0' : '-rotate-90'}`} />
            </button>
          )}
        </div>
      </div>      {/* Formulaire */}
      {showList && showForm && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 space-y-3">
          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Date</label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                className="w-full p-2 border border-gray-300 rounded text-xs focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Titre (optionnel)</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                placeholder="Titre de la note"
                className="w-full p-2 border border-gray-300 rounded text-xs focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Note *</label>
              <textarea
                value={formData.note}
                onChange={(e) => setFormData({ ...formData, note: e.target.value })}
                placeholder="Écrivez votre note..."
                className="w-full p-2 border border-gray-300 rounded text-xs focus:outline-none focus:border-indigo-500 resize-none h-20"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Catégorie (optionnel)</label>
              <input
                type="text"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                placeholder="ex: Observation, Conseil, Problème..."
                className="w-full p-2 border border-gray-300 rounded text-xs focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                className="flex-1 bg-indigo-500 hover:bg-indigo-600 text-white px-3 py-1.5 rounded text-xs font-medium transition"
              >
                {editingItem ? 'Modifier' : 'Ajouter'}
              </button>
              <button
                type="button"
                onClick={resetForm}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-3 py-1.5 rounded text-xs font-medium transition"
              >
                Annuler
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Liste */}
      {showList && (
        <>
          {notes.length === 0 ? (
            <div className="text-center py-4 bg-gray-50 rounded border border-gray-200">
              <p className="text-xs text-gray-500">Aucune note enregistrée</p>
            </div>
          ) : (
            <div className="space-y-2">
          {notes.map(note => {
            return (
              <div key={note.id} className="bg-indigo-50 border border-indigo-200 rounded-lg p-3 flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p className="text-xs font-semibold text-gray-900">
                      {note.title || 'Note sans titre'}
                    </p>
                    {note.category && (
                      <span className="inline-block bg-indigo-200 text-indigo-800 text-xs px-2 py-0.5 rounded-full">
                        {note.category}
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-gray-600 mt-1">{note.note}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(note.date).toLocaleDateString('fr-FR')}
                  </p>
                </div>
                <div className="flex gap-1 ml-2">
                  <button
                    onClick={() => handleEdit(note)}
                    className="text-blue-500 hover:text-blue-700 transition"
                    title="Modifier"
                  >
                    <Edit className="w-3 h-3" />
                  </button>
                  <button
                    onClick={() => handleDelete(note.id)}
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
        </>
      )}
    </div>
  )
}