import { Droplet, AlertCircle } from 'lucide-react'
import { useWateringStats, usePlantsToWater, usePlantsToFertilize } from '../hooks/useWateringNotifications'

/**
 * Badge affichant le nombre de plantes à arroser
 * À placer dans la navbar ou le header
 */
export function WateringNotificationBadge({ className = '' }) {
  const { toWater, toFertilize, total } = useWateringStats()

  if (total === 0) {
    return null
  }

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {toWater > 0 && (
        <div className="flex items-center gap-1 bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">
          <Droplet className="w-4 h-4" />
          <span>{toWater} à arroser</span>
        </div>
      )}
      {toFertilize > 0 && (
        <div className="flex items-center gap-1 bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
          <AlertCircle className="w-4 h-4" />
          <span>{toFertilize} à fertiliser</span>
        </div>
      )}
    </div>
  )
}

/**
 * Composant affichant la liste des plantes à arroser
 */
export function PlantsToWaterList() {
  const { plantsToWater, loading, error, refresh } = usePlantsToWater()

  if (loading) {
    return <div className="text-center text-gray-500">Chargement...</div>
  }

  if (error) {
    return (
      <div className="text-center text-red-500">
        <p>Erreur: {error}</p>
        <button
          onClick={refresh}
          className="mt-2 text-blue-600 hover:underline text-sm"
        >
          Réessayer
        </button>
      </div>
    )
  }

  if (plantsToWater.length === 0) {
    return (
      <div className="text-center text-gray-500 py-4">
        ✅ Toutes vos plantes sont bien hydratées !
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <h3 className="font-semibold text-lg text-blue-700 mb-4">
        🌊 {plantsToWater.length} plante(s) à arroser
      </h3>
      <div className="space-y-2">
        {plantsToWater.map(plant => (
          <div
            key={plant.id}
            className="flex items-center justify-between p-3 bg-blue-50 rounded-lg border border-blue-200"
          >
            <div>
              <p className="font-medium text-blue-900">{plant.name}</p>
              <p className="text-sm text-blue-700">
                {plant.scientific_name}
              </p>
              {plant.days_since_watering && (
                <p className="text-xs text-blue-600">
                  Dernier arrosage: {plant.days_since_watering} jours
                </p>
              )}
            </div>
            <Droplet className="w-6 h-6 text-blue-500" />
          </div>
        ))}
      </div>
    </div>
  )
}

/**
 * Composant affichant la liste des plantes à fertiliser
 */
export function PlantsToFertilizeList() {
  const { plantsToFertilize, loading, error, refresh } = usePlantsToFertilize()

  if (loading) {
    return <div className="text-center text-gray-500">Chargement...</div>
  }

  if (error) {
    return (
      <div className="text-center text-red-500">
        <p>Erreur: {error}</p>
        <button
          onClick={refresh}
          className="mt-2 text-blue-600 hover:underline text-sm"
        >
          Réessayer
        </button>
      </div>
    )
  }

  if (plantsToFertilize.length === 0) {
    return (
      <div className="text-center text-gray-500 py-4">
        ✅ Toutes vos plantes ont été fertilisées récemment !
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <h3 className="font-semibold text-lg text-green-700 mb-4">
        🌿 {plantsToFertilize.length} plante(s) à fertiliser
      </h3>
      <div className="space-y-2">
        {plantsToFertilize.map(plant => (
          <div
            key={plant.id}
            className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200"
          >
            <div>
              <p className="font-medium text-green-900">{plant.name}</p>
              <p className="text-sm text-green-700">
                {plant.scientific_name}
              </p>
              {plant.days_since_fertilizing && (
                <p className="text-xs text-green-600">
                  Dernière fertilisation: {plant.days_since_fertilizing} jours
                </p>
              )}
            </div>
            <AlertCircle className="w-6 h-6 text-green-500" />
          </div>
        ))}
      </div>
    </div>
  )
}
