import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import PlantDetailPage from './pages/PlantDetailPage'
import PlantFormPage from './pages/PlantFormPage'
import WateringHistoryPage from './pages/WateringHistoryPage'
import FertilizingHistoryPage from './pages/FertilizingHistoryPage'
import RepottingHistoryPage from './pages/RepottingHistoryPage'
import DiseaseHistoryPage from './pages/DiseaseHistoryPage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/plants/new" element={<PlantFormPage />} />
          <Route path="/plants/:id" element={<PlantDetailPage />} />
          <Route path="/plants/:id/edit" element={<PlantFormPage />} />
          <Route path="/plants/:id/watering-history" element={<WateringHistoryPage />} />
          <Route path="/plants/:id/fertilizing-history" element={<FertilizingHistoryPage />} />
          <Route path="/plants/:id/repotting-history" element={<RepottingHistoryPage />} />
          <Route path="/plants/:id/disease-history" element={<DiseaseHistoryPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
