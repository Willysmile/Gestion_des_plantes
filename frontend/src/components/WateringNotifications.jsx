import { Droplet, AlertCircle, Heart } from 'lucide-react'
import { useWateringStats, usePlantsToWater, usePlantsToFertilize, usePlantsInCare } from '../hooks/useWateringNotifications'
import { useModal } from '../contexts/ModalContext'

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
  const { openModal } = useModal()

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

  // Filtrer seulement les plantes qui ont besoin d'eau
  const plantsNeedingWater = plantsToWater.filter(p => p.needs_watering === true)

  if (plantsNeedingWater.length === 0) {
    return (
      <div className="text-center text-gray-500 py-4">
        ✅ Toutes vos plantes sont bien hydratées !
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <h3 className="font-semibold text-lg text-blue-700 mb-4">
        🌊 {plantsNeedingWater.length} plante(s) à arroser
      </h3>
      <div className="space-y-2">
        {plantsNeedingWater.map(plant => (
          <div
            key={plant.id}
            onClick={() => openModal(plant)}
            className={`flex items-center justify-between p-3 rounded-lg border cursor-pointer hover:shadow-md transition-shadow ${
              plant.warning
                ? 'bg-yellow-50 border-yellow-300'
                : 'bg-blue-50 border-blue-200'
            }`}
          >
            <div>
              <p className="font-medium text-blue-900">{plant.name}</p>
              <p className="text-sm text-blue-700">
                {plant.scientific_name}
              </p>
              {plant.warning && (
                <p className="text-xs text-yellow-700 font-semibold mt-1">
                  ⚠️ {plant.warning}
                </p>
              )}
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
  const { openModal } = useModal()

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

  // Filtrer seulement les plantes qui ont besoin d'engrais
  const plantsNeedingFertilizer = plantsToFertilize.filter(p => p.needs_fertilizing === true)

  if (plantsNeedingFertilizer.length === 0) {
    return (
      <div className="text-center text-gray-500 py-4">
        ✅ Toutes vos plantes ont été fertilisées récemment !
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <h3 className="font-semibold text-lg text-green-700 mb-4">
        🌿 {plantsNeedingFertilizer.length} plante(s) à fertiliser
      </h3>
      <div className="space-y-2">
        {plantsNeedingFertilizer.map(plant => (
          <div
            key={plant.id}
            onClick={() => openModal(plant)}
            className={`flex items-center justify-between p-3 rounded-lg border cursor-pointer hover:shadow-md transition-shadow ${
              plant.warning
                ? 'bg-yellow-50 border-yellow-300'
                : 'bg-green-50 border-green-200'
            }`}
          >
            <div>
              <p className="font-medium text-green-900">{plant.name}</p>
              <p className="text-sm text-green-700">
                {plant.scientific_name}
              </p>
              {plant.warning && (
                <p className="text-xs text-yellow-700 font-semibold mt-1">
                  ⚠️ {plant.warning}
                </p>
              )}
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

/**
 * Composant affichant la liste des plantes en cours de soin
 */
export function PlantsInCareList() {
  const { plantsInCare, loading, error, refresh } = usePlantsInCare()
  const { openModal } = useModal()

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

  if (plantsInCare.length === 0) {
    return (
      <div className="text-center text-gray-500 py-4">
        ✅ Toutes vos plantes sont en bonne santé !
      </div>
    )
  }

  const statusColors = {
    critical: { bg: 'bg-red-50', border: 'border-red-300', text: 'text-red-900' },
    sick: { bg: 'bg-orange-50', border: 'border-orange-300', text: 'text-orange-900' },
    treating: { bg: 'bg-yellow-50', border: 'border-yellow-300', text: 'text-yellow-900' },
    recovering: { bg: 'bg-blue-50', border: 'border-blue-300', text: 'text-blue-900' },
  }

  const statusLabels = {
    critical: '🚨 Critique',
    sick: '🤒 Malade',
    treating: '💊 En traitement',
    recovering: '💪 En récupération',
  }

  return (
    <div className="space-y-2">
      <h3 className="font-semibold text-lg text-red-700 mb-4">
        💔 {plantsInCare.length} plante(s) en cours de soin
      </h3>
      <div className="space-y-2">
        {plantsInCare.map(plant => {
          const colors = statusColors[plant.health_status] || statusColors.sick
          return (
            <div
              key={plant.id}
              onClick={() => openModal(plant)}
              className={`flex items-center justify-between p-3 rounded-lg border cursor-pointer hover:shadow-md transition-shadow ${colors.bg} ${colors.border}`}
            >
              <div>
                <p className={`font-medium ${colors.text}`}>{plant.name}</p>
                <p className={`text-sm ${colors.text}`}>
                  {plant.scientific_name}
                </p>
                <p className={`text-xs font-semibold ${colors.text} mt-1`}>
                  {statusLabels[plant.health_status]}
                </p>
              </div>
              <Heart className="w-6 h-6 text-red-500 fill-red-500" />
            </div>
          )
        })}
      </div>
    </div>
  )
}
