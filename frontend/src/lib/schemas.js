import { z } from 'zod'

/**
 * Zod Schemas pour validation client-side
 * Messages d'erreur en français
 * 
 * === RÈGLES DE TAXONOMIE ===
 * 
 * Exemples:
 * - "Phalaenopsis amabilis"                                    (minimal)
 * - "Phalaenopsis amabilis subsp. rosenstromii"                (+ subspecies)
 * - "Phalaenopsis amabilis var. alba"                          (+ variété)
 * - "Phalaenopsis amabilis 'White Dream'"                      (+ cultivar)
 * - "Phalaenopsis amabilis subsp. rosenstromii var. alba 'Pink Dream'" (complet)
 * 
 * Format des éléments:
 * | Élément   | Format        | Exemple              | Règles                                    |
 * |-----------|---------------|----------------------|-------------------------------------------|
 * | Genus     | Majuscule     | Phalaenopsis         | 1ère lettre MAJ, reste minuscule          |
 * | species   | minuscule     | amabilis             | Toujours minuscule                        |
 * | subspecies| "subsp. X"    | subsp. rosenstromii  | Préfixe "subsp." + minuscule (auto-ajouté)|
 * | variété   | "var. X"      | var. alba            | Préfixe "var." + minuscule (auto-ajouté)  |
 * | cultivar  | 'X'           | 'White Dream'        | Guillemets simples, peut être majuscule   |
 * 
 * Validations:
 * ✅ Genus obligatoire si species fourni
 * ✅ Subspecies/Variété toujours minuscule
 * ✅ Cultivar entre guillemets simples (auto-ajoutés)
 * ✅ Cultivar peut être en majuscules
 * ✅ Préfixes "subsp." et "var." auto-ajoutés si manquants
 */

// Énumérations valides
const HEALTH_STATUSES = ['healthy', 'sick', 'recovering', 'dead']
const SOIL_TYPES = ['terreau', 'terre', 'sable', 'tourbe', 'perlite']

/**
 * Schema principal pour une plante
 * Validation complète avec messages personnalisés en français
 */
export const plantSchema = z.object({
  // ===== INFORMATIONS DE BASE =====
  name: z
    .string()
    .min(1, 'Le nom est obligatoire')
    .min(2, 'Le nom doit contenir au moins 2 caractères')
    .max(100, 'Le nom doit contenir au maximum 100 caractères')
    .trim(),

  scientific_name: z
    .string()
    .max(150, 'Le nom scientifique doit contenir au maximum 150 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  family: z
    .string()
    .min(1, 'La famille est obligatoire')
    .min(2, 'La famille doit contenir au moins 2 caractères')
    .max(100, 'La famille doit contenir au maximum 100 caractères')
    .trim(),

  subfamily: z
    .string()
    .max(100, 'La sous-famille doit contenir au maximum 100 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  genus: z
    .string()
    .max(100, 'Le genre doit contenir au maximum 100 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  species: z
    .string()
    .max(100, 'L\'espèce doit contenir au maximum 100 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  subspecies: z
    .string()
    .max(100, 'La sous-espèce doit contenir au maximum 100 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  variety: z
    .string()
    .max(100, 'La variété doit contenir au maximum 100 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  cultivar: z
    .string()
    .max(100, 'Le cultivar doit contenir au maximum 100 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  reference: z
    .string()
    .max(50, 'La référence doit contenir au maximum 50 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  // ===== ENVIRONNEMENT =====
  temp_min: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional()
    .refine(val => val === null || (val >= -50 && val <= 50), {
      message: 'La température minimale doit être entre -50°C et 50°C'
    }),

  temp_max: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional()
    .refine(val => val === null || (val >= -50 && val <= 50), {
      message: 'La température maximale doit être entre -50°C et 50°C'
    }),

  humidity: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional()
    .refine(val => val === null || (val >= 0 && val <= 100), {
      message: 'L\'humidité doit être entre 0% et 100%'
    }),

  soil_type: z
    .string()
    .max(50, 'Le type de sol doit contenir au maximum 50 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  watering_frequency_id: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional(),

  light_requirement_id: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional(),

  location_id: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional(),

  // ===== DESCRIPTION =====
  description: z
    .string()
    .max(1000, 'La description doit contenir au maximum 1000 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  care_instructions: z
    .string()
    .max(1000, 'Les instructions de soin doivent contenir au maximum 1000 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  difficulty_level: z
    .enum(['easy', 'medium', 'hard'], {
      errorMap: () => ({ message: 'Sélectionnez un niveau de difficulté valide' })
    })
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  growth_speed: z
    .enum(['slow', 'medium', 'fast'], {
      errorMap: () => ({ message: 'Sélectionnez une vitesse de croissance valide' })
    })
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  flowering_season: z
    .string()
    .max(100, 'La saison de floraison doit contenir au maximum 100 caractères')
    .nullable()
    .optional()
    .transform(val => val === '' ? null : val),

  // ===== PROPRIÉTÉS =====
  is_favorite: z
    .boolean()
    .optional()
    .default(false),

  is_indoor: z
    .boolean()
    .optional()
    .default(false),

  is_outdoor: z
    .boolean()
    .optional()
    .default(false),

  is_toxic: z
    .boolean()
    .optional()
    .default(false),

  // ===== SANTÉ =====
  health_status: z
    .enum(HEALTH_STATUSES)
    .nullable()
    .optional()
    .default('healthy'),

  // ===== TAGS =====
  tags: z
    .array(z.number().int().positive())
    .nullable()
    .optional()
    .default([]),

}).refine(
  (data) => {
    // Règle: Si species est fourni, genus est obligatoire
    if ((data.species || '').trim() && !(data.genus || '').trim()) {
      return false
    }
    return true
  },
  {
    message: 'Le genre est obligatoire si l\'espèce est fournie',
    path: ['genus'],
  }
).refine(
  (data) => {
    // Règle: genus et species doivent être tous deux fournis ou tous deux vides
    const hasGenus = (data.genus || '').trim()
    const hasSpecies = (data.species || '').trim()
    
    if ((hasGenus && !hasSpecies) || (!hasGenus && hasSpecies)) {
      return false
    }
    return true
  },
  {
    message: 'Le genre et l\'espèce doivent être fournis ensemble',
    path: ['species'],
  }
).refine(
  (data) => {
    // Règle: temp_min doit être inférieure ou égale à temp_max
    // Convert to numbers for comparison
    const tempMin = data.temp_min === '' || data.temp_min === null ? null : Number(data.temp_min)
    const tempMax = data.temp_max === '' || data.temp_max === null ? null : Number(data.temp_max)
    
    if (tempMin !== null && tempMax !== null && tempMin > tempMax) {
      return false
    }
    return true
  },
  {
    message: 'La température minimale doit être inférieure ou égale à la température maximale',
    path: ['temp_min'],
  }
)

/**
 * Schema pour validation partielle (edit form)
 * Rend tous les champs optionnels sauf name et family
 */
export const plantUpdateSchema = plantSchema.partial().required({
  name: true,
  family: true,
})

/**
 * Schema pour validation création
 * Exclut les champs auto-générés (reference, scientific_name)
 */
export const plantCreateSchema = plantSchema.omit({ 
  reference: true,
  scientific_name: true 
})

/**
 * Fonction utilitaire pour valider une plante
 * Retourne {success, data, errors}
 */
export function validatePlant(data, isUpdate = false) {
  try {
    const schema = isUpdate ? plantUpdateSchema : plantCreateSchema
    const validated = schema.parse(data)
    return {
      success: true,
      data: validated,
      errors: {},
    }
  } catch (error) {
    if (error instanceof z.ZodError && error.issues) {
      const errors = {}
      error.issues.forEach(issue => {
        const path = issue.path.join('.')
        // Ensure error message is a string
        const message = typeof issue.message === 'string' ? issue.message : String(issue.message)
        errors[path] = message
      })
      return {
        success: false,
        data: null,
        errors,
      }
    }
    return {
      success: false,
      data: null,
      errors: { global: 'Erreur de validation inconnue' },
    }
  }
}

/**
 * Fonction pour formater les erreurs Zod en objet par champ
 */
export function formatValidationErrors(zodError) {
  const errors = {}
  if (zodError instanceof z.ZodError && zodError.issues) {
    zodError.issues.forEach(issue => {
      const field = issue.path.join('.')
      if (!errors[field]) {
        errors[field] = []
      }
      errors[field].push(issue.message)
    })
  }
  return errors
}
