import apiClient from './apiClient'

const brokerService = {
  /**
   * Get all brokers with optional filters
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with brokers data
   */
  getBrokers(filters = {}) {
    return apiClient.get('/brokers/', { params: filters })
  },

  /**
   * Get broker by ID
   * @param {string|number} id - Broker ID
   * @returns {Promise} - Promise with broker data
   */
  getBroker(id) {
    return apiClient.get(`/brokers/${id}/`)
  },

  /**
   * Create a new broker
   * @param {Object} brokerData - Broker data
   * @returns {Promise} - Promise with created broker data
   */
  createBroker(brokerData) {
    return apiClient.post('/brokers/', brokerData)
  },

  /**
   * Update a broker
   * @param {string|number} id - Broker ID
   * @param {Object} brokerData - Broker data to update
   * @returns {Promise} - Promise with updated broker data
   */
  updateBroker(id, brokerData) {
    return apiClient.patch(`/brokers/${id}/`, brokerData)
  },

  /**
   * Delete a broker
   * @param {string|number} id - Broker ID
   * @returns {Promise} - Promise with deletion status
   */
  deleteBroker(id) {
    return apiClient.delete(`/brokers/${id}/`)
  },

  /**
   * Get applications linked to a broker
   * @param {string|number} id - Broker ID
   * @returns {Promise} - Promise with applications data
   */
  getBrokerApplications(id) {
    return apiClient.get(`/brokers/${id}/applications/`)
  },

  /**
   * Get borrowers linked to a broker
   * @param {string|number} id - Broker ID
   * @returns {Promise} - Promise with borrowers data
   */
  getBrokerBorrowers(id) {
    return apiClient.get(`/brokers/${id}/borrowers/`)
  },

  /**
   * Get commissions for a broker
   * @param {string|number} id - Broker ID
   * @returns {Promise} - Promise with commissions data
   */
  getBrokerCommissions(id) {
    return apiClient.get(`/brokers/${id}/commissions/`)
  },

  /**
   * Get commission summary for a broker
   * @param {string|number} id - Broker ID
   * @returns {Promise} - Promise with commission summary data
   */
  getBrokerCommissionSummary(id) {
    return apiClient.get(`/brokers/${id}/commission-summary/`)
  },

  /**
   * Get all commissions
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with commissions data
   */
  getCommissions(filters = {}) {
    return apiClient.get('/commissions/', { params: filters })
  },

  /**
   * Get commission by ID
   * @param {string|number} id - Commission ID
   * @returns {Promise} - Promise with commission data
   */
  getCommission(id) {
    return apiClient.get(`/commissions/${id}/`)
  },

  /**
   * Get all commission payments
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with commission payments data
   */
  getCommissionPayments(filters = {}) {
    return apiClient.get('/commission-payments/', { params: filters })
  },

  /**
   * Create a commission payment
   * @param {Object} paymentData - Payment data
   * @returns {Promise} - Promise with created payment data
   */
  createCommissionPayment(paymentData) {
    return apiClient.post('/commission-payments/', paymentData)
  },

  /**
   * Get commission payment by ID
   * @param {string|number} id - Commission payment ID
   * @returns {Promise} - Promise with commission payment data
   */
  getCommissionPayment(id) {
    return apiClient.get(`/commission-payments/${id}/`)
  }
}

export default brokerService
