/**
 * Test pour la fonction pluralizeUnit
 * Vérifie la bonne pluralisation des unités en français
 */

const pluralizeUnit = (unit, amount) => {
  // Remplacer "unité" par "bâton d'engrais"
  let displayUnit = unit === 'unité' ? 'bâton d\'engrais' : unit
  
  if (!amount || amount === 1) return displayUnit
  // Certaines unités ont des formes plurielles en français
  const plurals = {
    'bâton d\'engrais': 'bâtons d\'engrais',
    'bâton': 'bâtons',
    'pastille': 'pastilles',
    'cuillère': 'cuillères',
    'dose': 'doses',
    'unité': 'unités'
  }
  return plurals[displayUnit] || displayUnit
}

describe('pluralizeUnit', () => {
  describe('Singulier (amount === 1)', () => {
    test('1 ml -> ml', () => {
      expect(pluralizeUnit('ml', 1)).toBe('ml')
    })
    test('1 bâton -> bâton', () => {
      expect(pluralizeUnit('bâton', 1)).toBe('bâton')
    })
    test('1 bâton d\'engrais -> bâton d\'engrais', () => {
      expect(pluralizeUnit('bâton d\'engrais', 1)).toBe('bâton d\'engrais')
    })
    test('1 unité -> bâton d\'engrais', () => {
      expect(pluralizeUnit('unité', 1)).toBe('bâton d\'engrais')
    })
    test('1 pastille -> pastille', () => {
      expect(pluralizeUnit('pastille', 1)).toBe('pastille')
    })
  })

  describe('Pluriel (amount > 1)', () => {
    test('2 ml -> ml (invariant)', () => {
      expect(pluralizeUnit('ml', 2)).toBe('ml')
    })
    test('2 bâton -> bâtons', () => {
      expect(pluralizeUnit('bâton', 2)).toBe('bâtons')
    })
    test('2 bâton d\'engrais -> bâtons d\'engrais', () => {
      expect(pluralizeUnit('bâton d\'engrais', 2)).toBe('bâtons d\'engrais')
    })
    test('2 unité -> bâtons d\'engrais', () => {
      expect(pluralizeUnit('unité', 2)).toBe('bâtons d\'engrais')
    })
    test('2 pastille -> pastilles', () => {
      expect(pluralizeUnit('pastille', 2)).toBe('pastilles')
    })
    test('2 cuillère -> cuillères', () => {
      expect(pluralizeUnit('cuillère', 2)).toBe('cuillères')
    })
    test('2 dose -> doses', () => {
      expect(pluralizeUnit('dose', 2)).toBe('doses')
    })
  })

  describe('Edge cases', () => {
    test('0 bâton -> bâton (singular for 0)', () => {
      expect(pluralizeUnit('bâton', 0)).toBe('bâton')
    })
    test('null amount -> unité (singulier)', () => {
      expect(pluralizeUnit('unité', null)).toBe('bâton d\'engrais')
    })
    test('undefined amount -> unité (singulier)', () => {
      expect(pluralizeUnit('unité', undefined)).toBe('bâton d\'engrais')
    })
    test('Unité inconnue -> inchangée', () => {
      expect(pluralizeUnit('kg', 5)).toBe('kg')
    })
    test('String amount -> conversion ignorée, utilise valeur truthy', () => {
      // "5" est truthy, donc pluriel
      expect(pluralizeUnit('bâton', "5")).toBe('bâtons')
    })
  })
})
