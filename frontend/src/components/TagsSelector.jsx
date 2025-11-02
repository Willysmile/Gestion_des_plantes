import React, { useState, useEffect } from 'react';
import useTags from '../hooks/useTags';

/**
 * Composant pour sélectionner les tags manuels d'une plante en édition
 * Affiche les tags auto en read-only et les tags manuels sélectionnés
 */
export default function TagsSelector({ plant, selectedTagIds = [], onChange }) {
  const { categories, getAutoTagCategories, getManualTagCategories } = useTags();
  const [expanded, setExpanded] = useState({});

  // Tags auto générés basés sur les données de la plante
  const autoTags = getAutoTagsForPlant(plant);
  const autoTagIds = autoTags.map(tag => tag.id);

  // Tags manuels disponibles
  const manualCategories = getManualTagCategories();
  const manualTags = categories
    .filter(cat => manualCategories.includes(cat.name))
    .flatMap(cat => cat.tags || []);

  // Tags manuels sélectionnés
  const selectedManualTags = manualTags.filter(tag => selectedTagIds.includes(tag.id));

  // Basculer la sélection d'un tag manuel
  const toggleTag = (tagId) => {
    const newIds = selectedTagIds.includes(tagId)
      ? selectedTagIds.filter(id => id !== tagId)
      : [...selectedTagIds, tagId];
    onChange(newIds);
  };

  // Basculer l'expansion d'une catégorie
  const toggleCategory = (categoryName) => {
    setExpanded(prev => ({
      ...prev,
      [categoryName]: !prev[categoryName]
    }));
  };

  if (categories.length === 0) {
    return <div className="text-gray-500 text-sm">Chargement des tags...</div>;
  }

  return (
    <div className="space-y-4">
      {/* Tags Auto - Read-only */}
      {autoTags.length > 0 && (
        <div className="p-3 bg-indigo-50 rounded border border-indigo-200">
          <h4 className="text-sm font-semibold text-indigo-700 mb-2">Tags Automatiques</h4>
          <div className="flex flex-wrap gap-2">
            {autoTags.map(tag => (
              <span
                key={tag.id}
                className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-200 text-indigo-800"
              >
                {tag.name}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Sélection des Tags Manuels */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-gray-700">Tags Personnalisés</h4>
        
        {/* Affichage des tags manuels sélectionnés */}
        {selectedManualTags.length > 0 && (
          <div className="p-3 bg-indigo-50 rounded border border-indigo-200">
            <h5 className="text-xs font-semibold text-indigo-700 mb-2">Sélection actuelle</h5>
            <div className="flex flex-wrap gap-2">
              {selectedManualTags.map(tag => (
                <span
                  key={tag.id}
                  className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700 border border-indigo-300"
                >
                  {tag.name}
                </span>
              ))}
            </div>
          </div>
        )}
        
        {categories
          .filter(cat => manualCategories.includes(cat.name))
          .map(category => (
            <div key={category.id} className="border rounded-lg overflow-hidden">
              <button
                type="button"
                onClick={() => toggleCategory(category.name)}
                className="w-full px-3 py-2 bg-gray-50 hover:bg-gray-100 font-medium text-sm text-left flex items-center justify-between"
              >
                <span>{category.name}</span>
                <span className="text-xs text-gray-500">
                  {expanded[category.name] ? '▼' : '▶'}
                </span>
              </button>

              {expanded[category.name] && (
                <div className="p-3 space-y-2 bg-white">
                  {category.tags?.length > 0 ? (
                    category.tags.map(tag => (
                      <label key={tag.id} className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
                        <input
                          type="checkbox"
                          checked={selectedTagIds.includes(tag.id)}
                          onChange={() => toggleTag(tag.id)}
                          className="rounded"
                        />
                        <span className="text-sm">{tag.name}</span>
                      </label>
                    ))
                  ) : (
                    <p className="text-xs text-gray-500">Aucun tag</p>
                  )}
                </div>
              )}
            </div>
          ))}
      </div>
    </div>
  );
}

/**
 * Génère les tags auto basés sur les données de la plante
 * Les auto-tags sont ceux des 3 catégories: Emplacement, État de la plante, Luminosité
 */
function getAutoTagsForPlant(plant) {
  if (!plant || !plant.tags) return [];

  const autoCategories = ['Emplacement', 'État de la plante', 'Luminosité'];
  
  // Récupérer les tags existants de la plante qui appartiennent aux catégories auto
  const existingAutoTags = plant.tags.filter(tag => {
    // Vérifier si le tag appartient à une catégorie auto
    const catName = tag.tag_category?.name || tag.category?.name;
    return autoCategories.includes(catName);
  }) || [];

  return existingAutoTags;
}
