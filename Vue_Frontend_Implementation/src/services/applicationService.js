import apiClient from './apiClient'

const applicationService = {
  /**
   * Get all applications with optional filters
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with applications data
   */
  getApplications(filters = {}) {
    return apiClient.get('/applications/', { params: filters })
  },

  /**
   * Get application by ID
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with application data
   */
  getApplication(id) {
    return apiClient.get(`/applications/${id}/`)
  },

  /**
   * Create a new application
   * @param {Object} applicationData - Application data
   * @returns {Promise} - Promise with created application data
   */
  createApplication(applicationData) {
    return apiClient.post('/applications/', applicationData)
  },

  /**
   * Update an application
   * @param {string|number} id - Application ID
   * @param {Object} applicationData - Application data to update
   * @returns {Promise} - Promise with updated application data
   */
  updateApplication(id, applicationData) {
    return apiClient.patch(`/applications/${id}/`, applicationData)
  },

  /**
   * Delete an application
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with deletion status
   */
  deleteApplication(id) {
    return apiClient.delete(`/applications/${id}/`)
  },

  /**
   * Upload documents to an application
   * @param {string|number} id - Application ID
   * @param {FormData} formData - Form data with files
   * @returns {Promise} - Promise with upload status
   */
  uploadDocuments(id, formData) {
    return apiClient.post(`/applications/${id}/documents/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * Generate documents for an application
   * @param {string|number} id - Application ID
   * @param {Object} options - Document generation options
   * @returns {Promise} - Promise with generated documents
   */
  generateDocuments(id, options = {}) {
    return apiClient.post(`/applications/${id}/generate-documents/`, options)
  },

  /**
   * Create a note for an application
   * @param {string|number} id - Application ID
   * @param {Object} noteData - Note data
   * @returns {Promise} - Promise with created note data
   */
  createNote(id, noteData) {
    return apiClient.post(`/applications/${id}/notes/`, noteData)
  },

  /**
   * Get all notes for an application
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with notes data
   */
  getNotes(id) {
    return apiClient.get(`/applications/${id}/notes/list/`)
  },

  /**
   * Calculate loan amounts and repayments
   * @param {string|number} id - Application ID
   * @param {Object} calculatorData - Calculator data
   * @returns {Promise} - Promise with calculation results
   */
  calculateLoan(id, calculatorData) {
    return apiClient.post(`/applications/${id}/calculator/`, calculatorData)
  },

  /**
   * Create repayment schedule for an application
   * @param {string|number} id - Application ID
   * @param {Object} repaymentData - Repayment data
   * @returns {Promise} - Promise with created repayment schedule
   */
  createRepaymentSchedule(id, repaymentData) {
    return apiClient.post(`/applications/${id}/repayments/`, repaymentData)
  },

  /**
   * Get repayment schedule for an application
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with repayment schedule data
   */
  getRepaymentSchedule(id) {
    return apiClient.get(`/applications/${id}/repayments/`)
  },

  /**
   * Create loan extension for an application
   * @param {string|number} id - Application ID
   * @param {Object} extensionData - Extension data
   * @returns {Promise} - Promise with created extension data
   */
  createExtension(id, extensionData) {
    return apiClient.post(`/applications/${id}/extension/`, extensionData)
  },

  /**
   * Get loan extensions for an application
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with extension data
   */
  getExtensions(id) {
    return apiClient.get(`/applications/${id}/extension/`)
  },

  /**
   * Duplicate an application
   * @param {string|number} id - Application ID
   * @param {Object} options - Duplication options
   * @returns {Promise} - Promise with duplicated application data
   */
  duplicateApplication(id, options = {}) {
    return apiClient.post(`/applications/${id}/duplicate/`, options)
  },

  /**
   * Get fees for an application
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with fees data
   */
  getFees(id) {
    return apiClient.get(`/applications/${id}/fees/`)
  },

  /**
   * Create a fee for an application
   * @param {string|number} id - Application ID
   * @param {Object} feeData - Fee data
   * @returns {Promise} - Promise with created fee data
   */
  createFee(id, feeData) {
    return apiClient.post(`/applications/${id}/fees/`, feeData)
  },

  /**
   * Get payments for an application
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with payments data
   */
  getPayments(id) {
    return apiClient.get(`/applications/${id}/payments/`)
  },

  /**
   * Create a payment for an application
   * @param {string|number} id - Application ID
   * @param {Object} paymentData - Payment data
   * @returns {Promise} - Promise with created payment data
   */
  createPayment(id, paymentData) {
    return apiClient.post(`/applications/${id}/payments/`, paymentData)
  },

  /**
   * Submit an application for review
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with submission status
   */
  submitApplication(id) {
    return apiClient.post(`/applications/${id}/submit/`)
  },

  /**
   * Review an application
   * @param {string|number} id - Application ID
   * @param {Object} reviewData - Review data
   * @returns {Promise} - Promise with review status
   */
  reviewApplication(id, reviewData) {
    return apiClient.post(`/applications/${id}/review/`, reviewData)
  },

  /**
   * Finalize an application
   * @param {string|number} id - Application ID
   * @returns {Promise} - Promise with finalization status
   */
  finalizeApplication(id) {
    return apiClient.post(`/applications/${id}/finalize/`)
  },

  /**
   * Search applications
   * @param {Object} searchParams - Search parameters
   * @returns {Promise} - Promise with search results
   */
  searchApplications(searchParams) {
    return apiClient.get('/search/advanced/', { params: searchParams })
  }
}

export default applicationService
