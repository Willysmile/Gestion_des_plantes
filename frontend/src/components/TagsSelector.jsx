import React, { useState, useEffect } from 'react';
import useTags from '../hooks/useTags';
import { X } from 'lucide-react';

/**
 * Composant pour sélectionner les tags manuels d'une plante en édition
 * Affiche les tags pré-remplis (auto) en read-only et laisse l'user choisir les manuels
 */
export default function TagsSelector({ plant, selectedTagIds = [], onChange }) {
  const { categories, getAutoTagCategories, getManualTagCategories } = useTags();
  const [expanded, setExpanded] = useState({});

  // Tags auto générés basés sur les données de la plante
  const autoTags = getAutoTagsForPlant(plant);
  const autoTagIds = autoTags.map(tag => tag.id);

  console.log('🏷️ TagsSelector DEBUG:', {
    plant_id: plant?.id,
    plant_tags_count: plant?.tags?.length || 0,
    autoTags_count: autoTags.length,
    autoTags: autoTags.map(t => ({ id: t.id, name: t.name, cat: t.tag_category?.name || t.category?.name })),
    autoTagIds,
    selectedTagIds,
  });

  // Tags manuels disponibles
  const manualCategories = getManualTagCategories();
  const manualTags = categories
    .filter(cat => manualCategories.includes(cat.name))
    .flatMap(cat => cat.tags || []);

  // Tags sélectionnés (combiner auto + manuel)
  const allSelectedTagIds = [...new Set([...autoTagIds, ...(selectedTagIds || [])])];

  // Basculer la sélection d'un tag manuel
  const toggleTag = (tagId) => {
    if (autoTagIds.includes(tagId)) {
      // Ne pas permettre de désélectionner les tags auto
      return;
    }

    const newIds = allSelectedTagIds.includes(tagId)
      ? allSelectedTagIds.filter(id => id !== tagId)
      : [...allSelectedTagIds, tagId];

    // Retourner seulement les tags manuels (exclure les auto)
    const manualOnly = newIds.filter(id => !autoTagIds.includes(id));
    onChange(manualOnly);
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
          <h4 className="text-sm font-semibold text-indigo-700 mb-2">Tags Automatiques (en lecture seule)</h4>
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

      {/* Tags Manuels - Sélectionnables */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-gray-700">Tags Personnalisés</h4>
        
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
                          checked={allSelectedTagIds.includes(tag.id)}
                          onChange={() => toggleTag(tag.id)}
                          disabled={autoTagIds.includes(tag.id)}
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

      {/* Résumé des tags sélectionnés */}
      {allSelectedTagIds.length > 0 && (
        <div className="p-2 bg-blue-50 rounded border border-blue-200 text-xs">
          <p className="text-blue-700">
            <strong>{allSelectedTagIds.length}</strong> tag(s) sélectionné(s)
            {autoTagIds.length > 0 && ` (${autoTagIds.length} auto + ${allSelectedTagIds.length - autoTagIds.length} manuel)`}
          </p>
        </div>
      )}
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
