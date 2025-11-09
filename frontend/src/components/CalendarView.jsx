import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, RefreshCw, AlertCircle } from 'lucide-react';
import { getCalendarEvents } from '../utils/api';

export default function CalendarView() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth() + 1;

  useEffect(() => {
    const fetchCalendar = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getCalendarEvents(year, month);
        setEvents(data.events || []);
        setSummary(data.summary || {});
      } catch (error) {
        console.error('Erreur chargement calendrier:', error);
        setError(error.message || 'Erreur lors du chargement');
        setEvents([]);
        setSummary({});
      } finally {
        setLoading(false);
      }
    };

    fetchCalendar();
  }, [year, month]);

  // Obtenir les jours du mois
  const getDaysInMonth = () => {
    return new Date(year, month, 0).getDate();
  };

  // Obtenir le premier jour de la semaine du mois (0 = dimanche)
  const getFirstDayOfMonth = () => {
    return new Date(year, month - 1, 1).getDay();
  };

  // Créer un map date -> events
  const eventsByDate = {};
  events.forEach(event => {
    if (!eventsByDate[event.date]) {
      eventsByDate[event.date] = [];
    }
    eventsByDate[event.date].push(event);
  });

  // Générer les jours du calendrier
  const generateCalendarDays = () => {
    const daysInMonth = getDaysInMonth();
    const firstDay = getFirstDayOfMonth();
    const days = [];

    // Jours vides du mois précédent
    for (let i = 0; i < firstDay; i++) {
      days.push(null);
    }

    // Jours du mois actuel
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(day);
    }

    return days;
  };

  const calendarDays = generateCalendarDays();

  // Formater le mois
  const monthNames = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
  ];

  const handlePrevMonth = () => {
    setCurrentDate(new Date(year, month - 2, 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(year, month, 1));
  };

  const handleRefresh = async () => {
    const data = await getCalendarEvents(year, month);
    setEvents(data.events || []);
    setSummary(data.summary || {});
  };

  const formatDate = (day) => {
    return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  };

  const getEventsForDay = (day) => {
    if (!day) return [];
    return eventsByDate[formatDate(day)] || [];
  };

  const getWateringCount = (day) => {
    return getEventsForDay(day).filter(e => e.type === 'watering').length;
  };

  const getFertilizingCount = (day) => {
    return getEventsForDay(day).filter(e => e.type === 'fertilizing').length;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={handlePrevMonth}
          className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
          title="Mois précédent"
        >
          <ChevronLeft size={20} />
        </button>

        <h2 className="text-2xl font-bold">
          {monthNames[month - 1]} {year}
        </h2>

        <div className="flex gap-2">
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="p-2 hover:bg-gray-200 rounded-lg transition-colors disabled:opacity-50"
            title="Rafraîchir"
          >
            <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
          </button>
          <button
            onClick={handleNextMonth}
            className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
            title="Mois suivant"
          >
            <ChevronRight size={20} />
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3">
          <AlertCircle size={20} className="text-red-600 flex-shrink-0" />
          <div>
            <p className="text-red-800 font-semibold">Erreur</p>
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Résumé */}
      {summary && (
        <div className="grid grid-cols-4 gap-4 mb-6 bg-gray-50 p-4 rounded-lg">
          <div>
            <p className="text-sm text-gray-600">Jours actifs</p>
            <p className="text-2xl font-bold text-blue-600">{summary.active_days || 0}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Arrosages</p>
            <p className="text-2xl font-bold text-blue-400">{summary.water_events || 0}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Fertilisations</p>
            <p className="text-2xl font-bold text-amber-500">{summary.fertilize_events || 0}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Total événements</p>
            <p className="text-2xl font-bold text-gray-700">{summary.total_events || 0}</p>
          </div>
        </div>
      )}

      {/* Calendrier */}
      {loading ? (
        <div className="text-center py-8">
          <p className="text-gray-500">Chargement du calendrier...</p>
        </div>
      ) : (
        <div>
          {/* Jours de la semaine */}
          <div className="grid grid-cols-7 gap-2 mb-2">
            {['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'].map(day => (
              <div key={day} className="text-center font-semibold text-gray-600 text-sm py-2">
                {day}
              </div>
            ))}
          </div>

          {/* Grille des jours */}
          <div className="grid grid-cols-7 gap-2">
            {calendarDays.map((day, index) => {
              if (!day) {
                return <div key={`empty-${index}`} className="h-24 bg-gray-50 rounded-lg" />;
              }

              const dayEvents = getEventsForDay(day);
              const wateringCount = getWateringCount(day);
              const fertilizingCount = getFertilizingCount(day);
              const hasEvents = dayEvents.length > 0;

              return (
                <div
                  key={day}
                  className={`h-24 p-2 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md ${
                    hasEvents
                      ? 'border-green-400 bg-green-50'
                      : 'border-gray-200 bg-white'
                  }`}
                  title={dayEvents.map(e => `${e.plant_name} (${e.type})`).join('\n')}
                >
                  <p className="font-bold text-sm mb-1">{day}</p>

                  {hasEvents && (
                    <div className="text-xs space-y-1">
                      {wateringCount > 0 && (
                        <div className="flex items-center text-blue-600">
                          <span className="inline-block w-2 h-2 bg-blue-400 rounded-full mr-1" />
                          <span>{wateringCount} arrosage{wateringCount > 1 ? 's' : ''}</span>
                        </div>
                      )}
                      {fertilizingCount > 0 && (
                        <div className="flex items-center text-amber-600">
                          <span className="inline-block w-2 h-2 bg-amber-400 rounded-full mr-1" />
                          <span>{fertilizingCount} fertilisant{fertilizingCount > 1 ? 's' : ''}</span>
                        </div>
                      )}
                    </div>
                  )}

                  {!hasEvents && (
                    <p className="text-xs text-gray-400">Aucun événement</p>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Légende */}
      <div className="mt-6 pt-6 border-t flex gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-blue-400 rounded-full" />
          <span className="text-gray-700">Arrosage</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-amber-400 rounded-full" />
          <span className="text-gray-700">Fertilisation</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-400 rounded-full" />
          <span className="text-gray-700">Jour avec événements</span>
        </div>
      </div>
    </div>
  );
}
