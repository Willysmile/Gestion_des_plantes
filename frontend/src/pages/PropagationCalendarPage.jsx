import { useState, useMemo } from 'react';
import { useGetCalendarEvents } from '../hooks/usePropagations';
import { format, addMonths, subMonths, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isSameDay } from 'date-fns';
import { fr } from 'date-fns/locale';

const PropagationCalendarPage = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDay, setSelectedDay] = useState(null);
  const { data: allEvents } = useGetCalendarEvents(
    currentDate.getFullYear(),
    currentDate.getMonth() + 1
  );

  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(currentDate);
  const calendarDays = eachDayOfInterval({ start: monthStart, end: monthEnd });

  // Grouper les événements par jour
  const eventsByDay = useMemo(() => {
    const grouped = {};
    if (allEvents) {
      allEvents.forEach(event => {
        const dayKey = format(new Date(event.propagation_date), 'yyyy-MM-dd');
        if (!grouped[dayKey]) {
          grouped[dayKey] = [];
        }
        grouped[dayKey].push(event);
      });
    }
    return grouped;
  }, [allEvents]);

  const getEventsForDay = (day) => {
    const dayKey = format(day, 'yyyy-MM-dd');
    return eventsByDay[dayKey] || [];
  };

  const statusColors = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'rooting': 'bg-blue-100 text-blue-800',
    'rooted': 'bg-green-100 text-green-800',
    'growing': 'bg-green-100 text-green-800',
    'ready-to-pot': 'bg-lime-100 text-lime-800',
    'potted': 'bg-emerald-100 text-emerald-800',
    'transplanted': 'bg-teal-100 text-teal-800',
    'established': 'bg-green-200 text-green-800',
    'failed': 'bg-red-100 text-red-800',
    'abandoned': 'bg-gray-100 text-gray-800',
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Calendrier des Propagations</h1>
          <div className="flex gap-4">
            <button
              onClick={() => setCurrentDate(subMonths(currentDate, 1))}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
            >
              ← Précédent
            </button>
            <button
              onClick={() => setCurrentDate(new Date())}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Aujourd'hui
            </button>
            <button
              onClick={() => setCurrentDate(addMonths(currentDate, 1))}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
            >
              Suivant →
            </button>
          </div>
        </div>

        {/* Month Title */}
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          {format(currentDate, 'MMMM yyyy', { locale: fr })}
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Calendar Grid */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-md overflow-hidden">
            {/* Weekday Headers */}
            <div className="grid grid-cols-7 bg-gray-100 border-b">
              {['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'].map(day => (
                <div key={day} className="p-4 text-center font-semibold text-gray-700">
                  {day}
                </div>
              ))}
            </div>

            {/* Calendar Days */}
            <div className="grid grid-cols-7">
              {calendarDays.map(day => {
                const isCurrentMonth = isSameMonth(day, currentDate);
                const isSelected = selectedDay && isSameDay(day, selectedDay);
                const dayEvents = getEventsForDay(day);

                return (
                  <div
                    key={format(day, 'yyyy-MM-dd')}
                    onClick={() => setSelectedDay(day)}
                    className={`min-h-32 p-2 border cursor-pointer transition ${
                      isCurrentMonth ? 'bg-white hover:bg-gray-50' : 'bg-gray-50'
                    } ${isSelected ? 'ring-2 ring-blue-500 bg-blue-50' : ''}`}
                  >
                    <p className={`font-semibold mb-1 ${isCurrentMonth ? 'text-gray-900' : 'text-gray-400'}`}>
                      {format(day, 'd')}
                    </p>
                    <div className="space-y-1">
                      {dayEvents.slice(0, 2).map(event => (
                        <div
                          key={event.id}
                          className={`text-xs p-1 rounded truncate ${
                            statusColors[event.status] || 'bg-gray-100 text-gray-700'
                          }`}
                        >
                          {event.parent_plant_name}
                        </div>
                      ))}
                      {dayEvents.length > 2 && (
                        <p className="text-xs text-gray-500 font-semibold">
                          +{dayEvents.length - 2} plus
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Day Details Panel */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">
              {selectedDay
                ? format(selectedDay, 'd MMMM yyyy', { locale: fr })
                : 'Sélectionner un jour'}
            </h3>

            {selectedDay && (
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {getEventsForDay(selectedDay).length > 0 ? (
                  getEventsForDay(selectedDay).map(event => (
                    <div
                      key={event.id}
                      className={`p-4 rounded-lg border-l-4 cursor-pointer hover:shadow-md transition ${
                        statusColors[event.status] || 'bg-gray-100'
                      }`}
                    >
                      <p className="font-semibold text-gray-900">
                        {event.parent_plant_name}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {event.source_type} - {event.method}
                      </p>
                      <div className="mt-2 text-sm space-y-1">
                        <p>
                          <span className="font-semibold">État:</span> {event.status}
                        </p>
                        <p>
                          <span className="font-semibold">Durée:</span> {event.days_since_propagation}j / {event.expected_duration_days}j
                        </p>
                        <p>
                          <span className="font-semibold">Succès:</span> {event.success_rate_estimate}%
                        </p>
                      </div>
                      {event.is_overdue && (
                        <p className="text-xs text-red-600 font-semibold mt-2">
                          ⚠️ EN RETARD
                        </p>
                      )}
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500">Aucune propagation ce jour</p>
                )}
              </div>
            )}

            {/* Legend */}
            <div className="mt-6 pt-6 border-t">
              <p className="font-semibold text-gray-700 mb-3">Légende des états</p>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-yellow-200 rounded"></div>
                  <span>En attente</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-blue-200 rounded"></div>
                  <span>Enracinement</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-200 rounded"></div>
                  <span>Croissance</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-200 rounded"></div>
                  <span>Échoué</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropagationCalendarPage;
