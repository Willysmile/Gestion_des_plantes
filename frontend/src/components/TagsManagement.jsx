import { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, X } from 'lucide-react';
import useTags from '../hooks/useTags';
import API from '../config';

export default function TagsManagement() {
  const { categories, fetchCategories } = useTags();
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [formData, setFormData] = useState({ name: '' });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Catégories auto (non éditables)
  const autoCategories = ['Emplacement', 'État de la plante', 'Luminosité'];
  const manualCategories = categories.filter(cat => !autoCategories.includes(cat.name));

  const resetForm = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData({ name: '' });
    setError(null);
  };

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setEditingId(null);
    setFormData({ name: '' });
  };

  const handleAddTag = async () => {
    if (!formData.name.trim() || !selectedCategory) {
      setError('Le nom du tag est requis');
      return;
    }

    try {
      setLoading(true);
      await API.post('/api/tags', {
        name: formData.name,
        tag_category_id: selectedCategory.id
      });
      await fetchCategories();
      resetForm();
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de l\'ajout');
    } finally {
      setLoading(false);
    }
  };

  const handleEditTag = (tag) => {
    setEditingId(tag.id);
    setFormData({ name: tag.name });
  };

  const handleUpdateTag = async () => {
    if (!formData.name.trim()) {
      setError('Le nom du tag est requis');
      return;
    }

    try {
      setLoading(true);
      await API.put(`/api/tags/${editingId}`, {
        name: formData.name
      });
      await fetchCategories();
      resetForm();
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la mise à jour');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTag = async (tagId) => {
    if (!confirm('Êtes-vous sûr ?')) return;

    try {
      setLoading(true);
      await API.delete(`/api/tags/${tagId}`);
      await fetchCategories();
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la suppression');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Catégories Auto (Read-only) */}
      <div>
        <h3 className="text-lg font-semibold text-indigo-700 mb-3">Tags Automatiques (en lecture seule)</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {categories
            .filter(cat => autoCategories.includes(cat.name))
            .map(category => (
              <div key={category.id} className="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                <h4 className="font-semibold text-indigo-900 mb-2">{category.name}</h4>
                <div className="flex flex-wrap gap-2">
                  {category.tags?.map(tag => (
                    <span key={tag.id} className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-indigo-200 text-indigo-800">
                      {tag.name}
                    </span>
                  ))}
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Catégories Manuelles */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Tags Personnalisés</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {manualCategories.map(category => (
            <button
              key={category.id}
              onClick={() => handleCategorySelect(category)}
              className={`p-4 rounded-lg border-2 transition text-left ${
                selectedCategory?.id === category.id
                  ? 'border-indigo-500 bg-indigo-50'
                  : 'border-gray-200 bg-white hover:border-indigo-300'
              }`}
            >
              <h4 className="font-semibold text-gray-900 mb-2">{category.name}</h4>
              <div className="flex flex-wrap gap-2">
                {category.tags?.map(tag => (
                  <span key={tag.id} className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                    {tag.name}
                  </span>
                ))}
              </div>
              <p className="text-xs text-gray-500 mt-2">{category.tags?.length || 0} tag(s)</p>
            </button>
          ))}
        </div>
      </div>

      {/* Formulaire d'ajout/édition de tags */}
      {selectedCategory && (
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">{selectedCategory.name}</h3>
            <button
              onClick={() => setSelectedCategory(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded border border-red-200">
              {error}
            </div>
          )}

          {/* Liste des tags actuels */}
          <div className="mb-6">
            <h4 className="font-medium text-gray-700 mb-2">Tags actuels</h4>
            <div className="space-y-2">
              {selectedCategory.tags && selectedCategory.tags.length > 0 ? (
                selectedCategory.tags.map(tag => (
                  <div key={tag.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                    <span className="text-sm">{tag.name}</span>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleEditTag(tag)}
                        className="p-1 text-blue-600 hover:bg-blue-50 rounded transition"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteTag(tag.id)}
                        className="p-1 text-red-600 hover:bg-red-50 rounded transition"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500">Aucun tag dans cette catégorie</p>
              )}
            </div>
          </div>

          {/* Formulaire */}
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {editingId ? 'Modifier le tag' : 'Ajouter un nouveau tag'}
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ name: e.target.value })}
                placeholder="Entrer le nom du tag"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={editingId ? handleUpdateTag : handleAddTag}
                disabled={loading}
                className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
              >
                {editingId ? 'Mettre à jour' : 'Ajouter'}
              </button>
              {editingId && (
                <button
                  onClick={resetForm}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition"
                >
                  Annuler
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
