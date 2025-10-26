#!/usr/bin/env node

/**
 * Test script pour valider que le refacteur fonctionne correctement
 * Teste la validation des champs temperature_min/max et humidity_level
 */

import { z } from 'zod'

// Copie minimaliste du schema pour tester
const testSchema = z.object({
  name: z.string().min(1, 'Le nom est obligatoire'),
  family: z.string().min(1, 'La famille est obligatoire'),
  temperature_min: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional(),

  temperature_max: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional(),

  humidity_level: z
    .union([z.string(), z.number()])
    .transform(val => {
      if (val === '' || val === null) return null
      return Number(val)
    })
    .nullable()
    .optional(),
}).refine(
  (data) => {
    const tempMin = data.temperature_min === '' || data.temperature_min === null ? null : Number(data.temperature_min)
    const tempMax = data.temperature_max === '' || data.temperature_max === null ? null : Number(data.temperature_max)
    
    if (tempMin !== null && tempMax !== null && tempMin > tempMax) {
      return false
    }
    return true
  },
  {
    message: 'La température minimale doit être inférieure ou égale à la température maximale',
    path: ['temperature_min'],
  }
)

// Test cases
const tests = [
  {
    name: 'Valid: temp_min < temp_max',
    data: { name: 'Test', family: 'TestFamily', temperature_min: '15', temperature_max: '25', humidity_level: '60' },
    shouldPass: true,
  },
  {
    name: 'Invalid: temp_min > temp_max',
    data: { name: 'Test', family: 'TestFamily', temperature_min: '30', temperature_max: '20', humidity_level: '60' },
    shouldPass: false,
    expectedError: 'temperature_min',
  },
  {
    name: 'Valid: empty temperatures',
    data: { name: 'Test', family: 'TestFamily', temperature_min: '', temperature_max: '', humidity_level: '60' },
    shouldPass: true,
  },
  {
    name: 'Valid: temp_min = temp_max',
    data: { name: 'Test', family: 'TestFamily', temperature_min: '20', temperature_max: '20', humidity_level: '60' },
    shouldPass: true,
  },
]

console.log('🧪 Running validation tests...\n')

let passed = 0
let failed = 0

tests.forEach(test => {
  const result = testSchema.safeParse(test.data)
  const isSuccess = result.success
  const testPassed = isSuccess === test.shouldPass

  if (testPassed) {
    console.log(`✅ ${test.name}`)
    passed++
  } else {
    console.log(`❌ ${test.name}`)
    console.log(`   Expected: ${test.shouldPass ? 'PASS' : 'FAIL'}`)
    console.log(`   Got: ${isSuccess ? 'PASS' : 'FAIL'}`)
    if (!isSuccess) {
      console.log(`   Errors: ${JSON.stringify(result.error.errors, null, 2)}`)
    }
    failed++
  }
})

console.log(`\n📊 Results: ${passed} passed, ${failed} failed`)

if (failed > 0) {
  process.exit(1)
}
