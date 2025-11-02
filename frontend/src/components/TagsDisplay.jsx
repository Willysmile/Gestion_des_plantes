import React from 'react';

/**
 * Composant pour afficher les tags d'une plante en read-only
 * Tags divisés en : Auto (Emplacement, État, Luminosité) et Manuels
 */
export default function TagsDisplay({ plant, tags = [] }) {
  if (!tags || tags.length === 0) {
    return null;
  }

  // Catégories auto
  const autoCategories = ['Emplacement', 'État de la plante', 'Luminosité'];
  
  // Séparer les tags auto et manuels
  const autoTags = tags.filter(tag => autoCategories.includes(tag.category?.name));
  const manualTags = tags.filter(tag => !autoCategories.includes(tag.category?.name));

  return (
    <div className="space-y-4">
      {/* Tags Auto */}
      {autoTags.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-indigo-700 mb-2">Tags Automatiques</h4>
          <div className="flex flex-wrap gap-2">
            {autoTags.map(tag => (
              <span
                key={tag.id}
                className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
              >
                {tag.name}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Tags Manuels */}
      {manualTags.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-indigo-700 mb-2">Tags Personnalisés</h4>
          <div className="flex flex-wrap gap-2">
            {manualTags.map(tag => (
              <span
                key={tag.id}
                className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-200"
              >
                {tag.name}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
