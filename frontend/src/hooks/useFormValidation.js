import { useState } from 'react'
import { validateData } from '../lib/schemas'

/**
 * Hook personnalisé pour gérer la validation des formulaires avec Zod
 * @param {Object} initialData - Données initiales du formulaire
 * @param {Object} schema - Schéma Zod pour validation
 * @returns {Object} state et handlers
 */
export function useFormValidation(initialData, schema) {
  const [formData, setFormData] = useState(initialData)
  const [errors, setErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [hasSubmitted, setHasSubmitted] = useState(false)

  /**
   * Valide le formulaire complet
   * @returns {boolean} true si valide
   */
  const validateForm = () => {
    const result = validateData(formData, schema)
    if (!result.success) {
      setErrors(result.errors || {})
      return false
    }
    setErrors({})
    return true
  }

  /**
   * Valide un champ spécifique
   * @param {string} fieldName - Nom du champ
   * @param {any} value - Valeur du champ
   */
  const validateField = (fieldName, value) => {
    try {
      // Valider juste ce champ
      const fieldSchema = schema.pick({ [fieldName]: true })
      fieldSchema.parse({ [fieldName]: value })
      
      // Enlever l'erreur si validation réussie
      const newErrors = { ...errors }
      delete newErrors[fieldName]
      setErrors(newErrors)
    } catch (error) {
      if (error instanceof z.ZodError) {
        const fieldError = error.issues[0]?.message || 'Erreur'
        setErrors(prev => ({ ...prev, [fieldName]: fieldError }))
      }
    }
  }

  /**
   * Met à jour un champ et valide si le formulaire a été soumis
   * @param {string} fieldName - Nom du champ
   * @param {any} value - Nouvelle valeur
   */
  const updateField = (fieldName, value) => {
    setFormData(prev => ({ ...prev, [fieldName]: value }))
    if (hasSubmitted) {
      validateField(fieldName, value)
    }
  }

  /**
   * Réinitialise le formulaire
   */
  const resetForm = () => {
    setFormData(initialData)
    setErrors({})
    setHasSubmitted(false)
  }

  /**
   * Soumet le formulaire
   * @returns {Object|null} Données validées ou null si erreur
   */
  const submitForm = async (onSubmit) => {
    setHasSubmitted(true)
    if (!validateForm()) {
      return null
    }

    setIsSubmitting(true)
    try {
      const result = await onSubmit(formData)
      setIsSubmitting(false)
      return result
    } catch (error) {
      setIsSubmitting(false)
      setErrors({ general: error.message || 'Erreur lors de la soumission' })
      return null
    }
  }

  return {
    formData,
    errors,
    isSubmitting,
    hasSubmitted,
    updateField,
    validateField,
    validateForm,
    resetForm,
    submitForm,
    setFormData,
    setErrors,
  }
}

// Support for Zod import
import { z } from 'zod'
