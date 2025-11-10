/**
 * AuditCharts.jsx
 * Composants graphiques Recharts pour visualiser les statistiques d'audit
 * - LineChart: Tendances INSERT/UPDATE/DELETE par jour
 * - PieChart: Distribution par type d'entité
 * - BarChart: Activité par utilisateur
 */

import React from 'react';
import {
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
} from 'recharts';

// Couleurs cohérentes avec l'app
const COLORS = {
  INSERT: '#10b981', // vert (création)
  UPDATE: '#3b82f6', // bleu (modification)
  DELETE: '#ef4444', // rouge (suppression)
  Plant: '#8b5cf6',
  Photo: '#f59e0b',
  WateringHistory: '#06b6d4',
  FertilizingHistory: '#ec4899',
  default: '#6b7280',
};

/**
 * AuditDailyActivityChart
 * Line chart des tendances INSERT/UPDATE/DELETE par jour
 * Utilise: /api/audit/stats/daily-activity
 */
export function AuditDailyActivityChart({ data, isLoading }) {
  if (isLoading) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Chargement des tendances...</p>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Aucune donnée disponible</p>
      </div>
    );
  }

  return (
    <div className="w-full bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold mb-4">📈 Activité Quotidienne</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="date" 
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="#6b7280" />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '6px',
            }}
            labelStyle={{ color: '#1f2937' }}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="line"
          />
          <Line
            type="monotone"
            dataKey="INSERT"
            stroke={COLORS.INSERT}
            strokeWidth={2}
            dot={{ fill: COLORS.INSERT, r: 4 }}
            activeDot={{ r: 6 }}
            name="Créations"
          />
          <Line
            type="monotone"
            dataKey="UPDATE"
            stroke={COLORS.UPDATE}
            strokeWidth={2}
            dot={{ fill: COLORS.UPDATE, r: 4 }}
            activeDot={{ r: 6 }}
            name="Modifications"
          />
          <Line
            type="monotone"
            dataKey="DELETE"
            stroke={COLORS.DELETE}
            strokeWidth={2}
            dot={{ fill: COLORS.DELETE, r: 4 }}
            activeDot={{ r: 6 }}
            name="Suppressions"
          />
        </LineChart>
      </ResponsiveContainer>
      <div className="mt-4 text-xs text-gray-600">
        <p>Total: {data.reduce((sum, d) => sum + (d.total || 0), 0)} modifications</p>
      </div>
    </div>
  );
}

/**
 * AuditEntityBreakdownChart
 * Pie chart de la distribution par type d'entité
 * Utilise: /api/audit/stats/entity-breakdown
 */
export function AuditEntityBreakdownChart({ data, isLoading }) {
  if (isLoading) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Chargement de la distribution...</p>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Aucune donnée disponible</p>
      </div>
    );
  }

  // Mapper les données pour Recharts
  const chartData = data.map(item => ({
    name: item.entity_type,
    value: item.count,
  }));

  return (
    <div className="w-full bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold mb-4">🔍 Distribution par Entité</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={true}
            label={(entry) => `${entry.name}: ${entry.value}`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[entry.name] || COLORS.default}
              />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '6px',
            }}
            formatter={(value) => `${value} modifications`}
          />
        </PieChart>
      </ResponsiveContainer>
      <div className="mt-4 text-xs text-gray-600">
        <p>Total: {data.reduce((sum, d) => sum + d.count, 0)} modifications</p>
      </div>
    </div>
  );
}

/**
 * AuditUserActivityChart
 * Bar chart de l'activité par utilisateur (top 10)
 * Utilise: /api/audit/stats/user-activity
 */
export function AuditUserActivityChart({ data, isLoading }) {
  if (isLoading) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Chargement de l'activité utilisateur...</p>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Aucune donnée disponible</p>
      </div>
    );
  }

  // Formatter les données pour afficher user_id ou "admin" et count
  const chartData = data.map(item => ({
    name: item.user_id ? `User ${item.user_id}` : 'Admin',
    count: item.count,
    ...item,
  }));

  return (
    <div className="w-full bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold mb-4">👥 Activité par Utilisateur</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 0, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="name"
            angle={-45}
            textAnchor="end"
            height={100}
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="#6b7280" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '6px',
            }}
            labelStyle={{ color: '#1f2937' }}
            formatter={(value) => `${value} modifications`}
          />
          <Bar
            dataKey="count"
            fill="#8b5cf6"
            radius={[8, 8, 0, 0]}
            animationDuration={500}
          />
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-4 text-xs text-gray-600">
        <p>Total: {data.reduce((sum, d) => sum + d.count, 0)} modifications par {data.length} utilisateur(s)</p>
      </div>
    </div>
  );
}

/**
 * AuditActionByEntityChart
 * Composed chart: Stacked bar avec INSERT/UPDATE/DELETE par entity type
 * Utilise: /api/audit/stats/action-by-entity
 */
export function AuditActionByEntityChart({ data, isLoading }) {
  if (isLoading) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Chargement du tableau croisé...</p>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Aucune donnée disponible</p>
      </div>
    );
  }

  return (
    <div className="w-full bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold mb-4">📊 Actions par Entité</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 0, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="entity_type"
            angle={-45}
            textAnchor="end"
            height={100}
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="#6b7280" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '6px',
            }}
            labelStyle={{ color: '#1f2937' }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Bar dataKey="INSERT" stackId="a" fill={COLORS.INSERT} name="Créations" />
          <Bar dataKey="UPDATE" stackId="a" fill={COLORS.UPDATE} name="Modifications" />
          <Bar dataKey="DELETE" stackId="a" fill={COLORS.DELETE} name="Suppressions" />
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-4 text-xs text-gray-600">
        <p>Total: {data.reduce((sum, d) => sum + (d.INSERT || 0) + (d.UPDATE || 0) + (d.DELETE || 0), 0)} modifications</p>
      </div>
    </div>
  );
}

export default {
  AuditDailyActivityChart,
  AuditEntityBreakdownChart,
  AuditUserActivityChart,
  AuditActionByEntityChart,
};
