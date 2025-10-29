// Test pour vérifier que l'API fonctionne correctement
const API_BASE = 'http://127.0.0.1:8002/api'
const plantId = 1

try {
  const res = await fetch(`${API_BASE}/plants/${plantId}/watering-history`)
  const data = await res.json()
  console.log('✅ API Response:', data)
  
  if (data.length > 0) {
    const sorted = data.sort((a, b) => new Date(b.date) - new Date(a.date))
    const lastWatering = sorted[0]
    console.log('✅ Last watering:', lastWatering)
    console.log('📅 Date:', new Date(lastWatering.date).toLocaleDateString('fr-FR'))
    console.log('💧 Amount:', lastWatering.amount_ml, 'ml')
    console.log('📝 Notes:', lastWatering.notes)
  } else {
    console.log('❌ No watering found')
  }
} catch (e) {
  console.error('❌ Error:', e)
}
