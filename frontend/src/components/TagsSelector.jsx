import React, { useState } from 'react';
import useTags from '../hooks/useTags';

/**
 * Composant pour sélectionner les tags d'une plante en édition
 * Affiche tous les tags (auto + manuels) en chips cliquables sur 2 colonnes
 * Tags auto = couleur bleue, Tags manuels = couleur indigo
 * Confirmation nécessaire pour désélectionner les tags auto
 */
export default function TagsSelector({ plant, selectedTagIds = [], onChange }) {
  const { categories, getAutoTagCategories, getManualTagCategories } = useTags();
  const [showConfirm, setShowConfirm] = useState(null); // null ou tagId à désélectionner

  const autoCategories = getAutoTagCategories();
  const manualCategories = getManualTagCategories();

  // Tous les tags disponibles
  const allTags = categories.flatMap(cat => cat.tags || []);
  
  // Déterminer si un tag est auto
  const isAutoTag = (tagId) => {
    const tag = allTags.find(t => t.id === tagId);
    if (!tag) return false;
    const catName = tag.tag_category?.name || tag.category?.name;
    return autoCategories.includes(catName);
  };

  // Toggle la sélection d'un tag
  const toggleTag = (tagId) => {
    if (selectedTagIds.includes(tagId)) {
      // Demande confirmation si c'est un tag auto
      if (isAutoTag(tagId)) {
        setShowConfirm(tagId);
      } else {
        deselectTag(tagId);
      }
    } else {
      selectTag(tagId);
    }
  };

  const selectTag = (tagId) => {
    onChange([...selectedTagIds, tagId]);
  };

  const deselectTag = (tagId) => {
    onChange(selectedTagIds.filter(id => id !== tagId));
    setShowConfirm(null);
  };

  if (categories.length === 0) {
    return <div className="text-gray-500 text-sm">Chargement des tags...</div>;
  }

  return (
    <div className="space-y-4">
      {/* Grille 2 colonnes de catégories */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {categories.map(category => {
          const isAutoCategory = autoCategories.includes(category.name);
          
          return (
            <div key={category.id} className="space-y-2">
              <h4 className="text-sm font-semibold text-gray-700">
                {category.name}
                {isAutoCategory && <span className="text-blue-600 ml-1">(Auto)</span>}
              </h4>
              
              <div className="flex flex-wrap gap-2">
                {category.tags?.length > 0 ? (
                  category.tags.map(tag => {
                    const isSelected = selectedTagIds.includes(tag.id);
                    const isAuto = autoCategories.includes(category.name);
                    
                    return (
                      <div key={tag.id} className="relative">
                        <button
                          type="button"
                          onClick={() => toggleTag(tag.id)}
                          className={`px-3 py-1 rounded-full text-xs font-medium transition-all cursor-pointer ${
                            isSelected
                              ? isAuto
                                ? 'bg-blue-500 text-white'
                                : 'bg-indigo-500 text-white'
                              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                          }`}
                        >
                          {tag.name}
                        </button>

                        {/* Modal de confirmation pour tags auto */}
                        {showConfirm === tag.id && (
                          <div className="absolute inset-0 z-50 flex items-center justify-center">
                            <div className="bg-white border border-gray-300 rounded shadow-lg p-3 text-center">
                              <p className="text-xs font-semibold mb-2">
                                Désélectionner ce tag ?
                              </p>
                              <div className="flex gap-2 justify-center">
                                <button
                                  type="button"
                                  onClick={() => deselectTag(tag.id)}
                                  className="px-2 py-1 bg-red-500 text-white text-xs rounded hover:bg-red-600"
                                >
                                  Oui
                                </button>
                                <button
                                  type="button"
                                  onClick={() => setShowConfirm(null)}
                                  className="px-2 py-1 bg-gray-400 text-white text-xs rounded hover:bg-gray-500"
                                >
                                  Non
                                </button>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })
                ) : (
                  <p className="text-xs text-gray-500">Aucun tag</p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
