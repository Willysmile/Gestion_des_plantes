import React, { useState, useMemo, useEffect } from 'react';
import useTags from '../hooks/useTags';

/**
 * Composant pour sélectionner les tags d'une plante en édition
 * Affiche tous les tags (auto + manuels) en chips cliquables sur 2 colonnes
 * Tags auto = couleur bleue, Tags manuels = couleur indigo
 * Confirmation nécessaire pour désélectionner les tags auto
 */
export default function TagsSelector({ formData, lookups = {}, selectedTagIds = [], onChange }) {
  const { categories, getAutoTagCategories, getManualTagCategories } = useTags();

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

  // Tags auto calculés dynamiquement basés sur formData
  const autoTagIds = useMemo(() => {
    if (!formData) return [];

    const locationId = formData.location_id;
    const healthStatus = formData.health_status;
    const lightRequirementId = formData.light_requirement_id;

    // Trouver les tags auto correspondants
    const autoTags = [];

    // Tag Emplacement
    if (locationId) {
      // Trouver le nom de la location correspondante
      const location = lookups.locations?.find(loc => loc.id === locationId);
      if (location) {
        const locationTag = allTags.find(t => {
          const catName = t.tag_category?.name || t.category?.name;
          return catName === 'Emplacement' && t.name === location.name;
        });
        if (locationTag) autoTags.push(locationTag.id);
      }
    }

    // Tag État de la plante
    if (healthStatus) {
      const healthMap = {
        healthy: 'Sain',
        sick: 'Malade',
        recovering: 'Rétablie',
        dead: 'Morte',  // Note: pas de "Morte" en base, mais on le garde au cas où
        critical: 'Critique',
        treating: 'En traitement',
        convalescent: 'En convalescence'
      };
      const healthTagName = healthMap[healthStatus];
      const healthTag = allTags.find(t => {
        const catName = t.tag_category?.name || t.category?.name;
        return catName === 'État de la plante' && t.name === healthTagName;
      });
      if (healthTag) autoTags.push(healthTag.id);
    }

    // Tag Luminosité
    if (lightRequirementId) {
      // Trouver le nom du light requirement correspondant
      const lightReq = lookups.lightRequirements?.find(lr => lr.id === lightRequirementId);
      if (lightReq) {
        const lightTag = allTags.find(t => {
          const catName = t.tag_category?.name || t.category?.name;
          return catName === 'Luminosité' && t.name === lightReq.name;
        });
        if (lightTag) autoTags.push(lightTag.id);
      }
    }

    return autoTags;
  }, [formData?.location_id, formData?.health_status, formData?.light_requirement_id, allTags, autoCategories, lookups.locations, lookups.lightRequirements]);

  // Toggle la sélection d'un tag
  const [previousAutoTagIds, setPreviousAutoTagIds] = useState([]);

  // Quand les auto tags changent, enlever les anciens et ajouter les nouveaux
  useEffect(() => {
    // Vérifier si autoTagIds a vraiment changé (pas juste une référence différente)
    const hasAutoTagsChanged = 
      autoTagIds.length !== previousAutoTagIds.length ||
      autoTagIds.some(id => !previousAutoTagIds.includes(id)) ||
      previousAutoTagIds.some(id => !autoTagIds.includes(id));

    if (!hasAutoTagsChanged) return; // Pas de changement, ne rien faire

    // Enlever les anciens auto tags qui ne sont plus dans la nouvelle liste
    const tagsToRemove = previousAutoTagIds.filter(id => !autoTagIds.includes(id));
    
    // Ajouter les nouveaux auto tags
    const tagsToAdd = autoTagIds.filter(id => !previousAutoTagIds.includes(id));

    if (tagsToRemove.length === 0 && tagsToAdd.length === 0) {
      // Aucun changement à faire
      setPreviousAutoTagIds(autoTagIds);
      return;
    }

    let updatedTags = selectedTagIds;

    // Retirer les anciens auto tags
    tagsToRemove.forEach(tagId => {
      updatedTags = updatedTags.filter(id => id !== tagId);
    });

    // Ajouter les nouveaux auto tags
    tagsToAdd.forEach(tagId => {
      if (!updatedTags.includes(tagId)) {
        updatedTags = [...updatedTags, tagId];
      }
    });

    onChange(updatedTags);
    setPreviousAutoTagIds(autoTagIds);
  }, [autoTagIds, previousAutoTagIds, selectedTagIds, onChange]);

  const toggleTag = (tagId) => {
    // Les tags auto ne peuvent pas être désélectionnés
    if (autoTagIds.includes(tagId)) {
      // Si c'est un tag auto et il est déjà sélectionné, l'empêcher de se désélectionner
      if (selectedTagIds.includes(tagId)) {
        return; // Bloquer la désélection
      }
      // Si c'est un tag auto mais pas encore sélectionné, l'ajouter
      selectTag(tagId);
      return;
    }

    // Les tags des catégories auto ne peuvent pas être sélectionnés manuellement
    const tag = categories.flatMap(c => c.tags).find(t => t.id === tagId);
    if (tag) {
      const catName = tag.tag_category?.name || tag.category?.name;
      const autoCategoryNames = ['Emplacement', 'État de la plante', 'Luminosité'];
      if (autoCategoryNames.includes(catName)) {
        return; // Bloquer la sélection manuelle
      }
    }

    // Pour les tags manuels, toggle normal
    if (selectedTagIds.includes(tagId)) {
      deselectTag(tagId);
    } else {
      selectTag(tagId);
    }
  };

  const selectTag = (tagId) => {
    onChange([...selectedTagIds, tagId]);
  };

  const deselectTag = (tagId) => {
    onChange(selectedTagIds.filter(id => id !== tagId));
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
                    const isAutoCategory = autoCategories.includes(category.name);
                    const isAutoTag = autoTagIds.includes(tag.id);
                    // Les tags auto des catégories auto sont toujours désactivés
                    const isAutoManaged = isAutoCategory && isAutoTag;
                    
                    return (
                      <button
                        key={tag.id}
                        type="button"
                        onClick={() => toggleTag(tag.id)}
                        disabled={isAutoManaged || (isAutoCategory && !isAutoTag)}
                        className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                          isAutoManaged || (isAutoCategory && !isAutoTag)
                            ? 'cursor-not-allowed'
                            : 'cursor-pointer'
                        } ${
                          isAutoManaged
                            ? 'bg-green-500 text-white'
                            : isAutoCategory
                            ? 'bg-gray-300 text-gray-600'
                            : isSelected
                            ? 'bg-indigo-500 text-white hover:bg-indigo-600'
                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                        title={
                          isAutoManaged
                            ? 'Ce tag est défini automatiquement'
                            : isAutoCategory && !isAutoTag
                            ? 'Les tags de cette catégorie auto ne peuvent pas être sélectionnés manuellement'
                            : ''
                        }
                      >
                        {tag.name}
                      </button>
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
