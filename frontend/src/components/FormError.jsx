/**
 * Composant pour afficher les erreurs de validation
 * Utilisable partout où on a besoin d'afficher des erreurs Zod
 */

export function FormError({ error, className = '' }) {
  if (!error) return null
  return (
    <p className={`text-sm text-red-600 mt-1 ${className}`}>
      🔴 {error}
    </p>
  )
}

export function FieldError({ fieldName, errors, className = '' }) {
  const error = errors?.[fieldName]
  return <FormError error={error} className={className} />
}

/**
 * Fonction utilitaire pour déterminer si un champ a une erreur
 */
export function hasFieldError(fieldName, errors) {
  return Boolean(errors?.[fieldName])
}

/**
 * Classe CSS dynamique pour les champs en erreur
 */
export function getFieldInputClasses(fieldName, errors, baseClasses = '') {
  const isError = hasFieldError(fieldName, errors)
  return `${baseClasses} ${isError ? 'border-red-500 border-2' : 'border-gray-300'}`
}

/**
 * Classe CSS pour les labels d'erreurs
 */
export function getLabelClasses(fieldName, errors) {
  const isError = hasFieldError(fieldName, errors)
  return `${isError ? 'text-red-600' : 'text-gray-700'}`
}
