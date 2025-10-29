/**
 * Get today's date in YYYY-MM-DD format for date input max attribute
 */
export const getTodayDateString = () => {
  return new Date().toISOString().split('T')[0]
}

/**
 * Check if a date is in the future
 */
export const isFutureDate = (dateString) => {
  const selectedDate = new Date(dateString)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  selectedDate.setHours(0, 0, 0, 0)
  return selectedDate > today
}
