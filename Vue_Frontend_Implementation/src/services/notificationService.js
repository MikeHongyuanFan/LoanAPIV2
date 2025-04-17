import apiClient from './apiClient'

const notificationService = {
  /**
   * Get all notifications with optional filters
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with notifications data
   */
  getNotifications(filters = {}) {
    return apiClient.get('/notifications/', { params: filters })
  },

  /**
   * Get notification by ID
   * @param {string|number} id - Notification ID
   * @returns {Promise} - Promise with notification data
   */
  getNotification(id) {
    return apiClient.get(`/notifications/${id}/`)
  },

  /**
   * Create a new notification
   * @param {Object} notificationData - Notification data
   * @returns {Promise} - Promise with created notification data
   */
  createNotification(notificationData) {
    return apiClient.post('/notifications/', notificationData)
  },

  /**
   * Update a notification
   * @param {string|number} id - Notification ID
   * @param {Object} notificationData - Notification data to update
   * @returns {Promise} - Promise with updated notification data
   */
  updateNotification(id, notificationData) {
    return apiClient.patch(`/notifications/${id}/`, notificationData)
  },

  /**
   * Delete a notification
   * @param {string|number} id - Notification ID
   * @returns {Promise} - Promise with deletion status
   */
  deleteNotification(id) {
    return apiClient.delete(`/notifications/${id}/`)
  },

  /**
   * Send a specific notification
   * @param {string|number} id - Notification ID
   * @returns {Promise} - Promise with send status
   */
  sendNotification(id) {
    return apiClient.post(`/notifications/${id}/send/`)
  },

  /**
   * Mark a notification as read
   * @param {string|number} id - Notification ID
   * @returns {Promise} - Promise with update status
   */
  markAsRead(id) {
    return apiClient.patch(`/notifications/${id}/`, { read: true })
  },

  /**
   * Mark all notifications as read
   * @returns {Promise} - Promise with update status
   */
  markAllAsRead() {
    return apiClient.post('/notifications/mark-all-read/')
  },

  /**
   * Get notification settings
   * @returns {Promise} - Promise with notification settings
   */
  getNotificationSettings() {
    return apiClient.get('/notifications/settings/')
  },

  /**
   * Update notification settings
   * @param {Object} settingsData - Settings data
   * @returns {Promise} - Promise with updated settings
   */
  updateNotificationSettings(settingsData) {
    return apiClient.post('/notifications/settings/', settingsData)
  },

  /**
   * Get all notification templates
   * @returns {Promise} - Promise with notification templates
   */
  getNotificationTemplates() {
    return apiClient.get('/notifications/templates/')
  },

  /**
   * Get notification template by ID
   * @param {string|number} id - Template ID
   * @returns {Promise} - Promise with notification template
   */
  getNotificationTemplate(id) {
    return apiClient.get(`/notifications/templates/${id}/`)
  },

  /**
   * Create a notification template
   * @param {Object} templateData - Template data
   * @returns {Promise} - Promise with created template
   */
  createNotificationTemplate(templateData) {
    return apiClient.post('/notifications/templates/', templateData)
  },

  /**
   * Update a notification template
   * @param {string|number} id - Template ID
   * @param {Object} templateData - Template data to update
   * @returns {Promise} - Promise with updated template
   */
  updateNotificationTemplate(id, templateData) {
    return apiClient.patch(`/notifications/templates/${id}/`, templateData)
  },

  /**
   * Delete a notification template
   * @param {string|number} id - Template ID
   * @returns {Promise} - Promise with deletion status
   */
  deleteNotificationTemplate(id) {
    return apiClient.delete(`/notifications/templates/${id}/`)
  },

  /**
   * Preview a notification template
   * @param {string|number} id - Template ID
   * @returns {Promise} - Promise with template preview
   */
  previewNotificationTemplate(id) {
    return apiClient.get(`/notifications/templates/${id}/preview/`)
  },

  /**
   * Send a test notification using a template
   * @param {string|number} id - Template ID
   * @param {Object} testData - Test data
   * @returns {Promise} - Promise with test status
   */
  sendTestNotification(id, testData) {
    return apiClient.post(`/notifications/templates/${id}/send-test/`, testData)
  },

  /**
   * Send an SMS notification
   * @param {Object} smsData - SMS data
   * @returns {Promise} - Promise with send status
   */
  sendSMS(smsData) {
    return apiClient.post('/notifications/send-sms/', smsData)
  }
}

export default notificationService
