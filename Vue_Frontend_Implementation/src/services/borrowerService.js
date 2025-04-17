import apiClient from './apiClient';

const borrowerService = {
  /**
   * Get all borrowers with optional filters
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with borrowers data
   */
  getBorrowers(filters = {}) {
    return apiClient.get('/borrowers/', { params: filters });
  },

  /**
   * Get borrower by ID
   * @param {string|number} id - Borrower ID
   * @returns {Promise} - Promise with borrower data
   */
  getBorrower(id) {
    return apiClient.get(`/borrowers/${id}/`);
  },

  /**
   * Create a new borrower
   * @param {Object} borrowerData - Borrower data
   * @returns {Promise} - Promise with created borrower data
   */
  createBorrower(borrowerData) {
    return apiClient.post('/borrowers/', borrowerData);
  },

  /**
   * Update a borrower
   * @param {string|number} id - Borrower ID
   * @param {Object} borrowerData - Borrower data to update
   * @returns {Promise} - Promise with updated borrower data
   */
  updateBorrower(id, borrowerData) {
    return apiClient.patch(`/borrowers/${id}/`, borrowerData);
  },

  /**
   * Delete a borrower
   * @param {string|number} id - Borrower ID
   * @returns {Promise} - Promise with deletion status
   */
  deleteBorrower(id) {
    return apiClient.delete(`/borrowers/${id}/`);
  },

  /**
   * Search borrowers
   * @param {string} query - Search query
   * @returns {Promise} - Promise with search results
   */
  searchBorrowers(query) {
    return apiClient.get('/borrowers/search/', { params: { query } });
  },

  /**
   * Get borrower applications
   * @param {string|number} id - Borrower ID
   * @returns {Promise} - Promise with borrower applications data
   */
  getBorrowerApplications(id) {
    return apiClient.get(`/borrowers/${id}/applications/`);
  },

  /**
   * Check for duplicate borrowers
   * @param {Object} borrowerData - Borrower data to check
   * @returns {Promise} - Promise with potential duplicates
   */
  checkDuplicates(borrowerData) {
    return apiClient.post('/borrowers/check-duplicates/', borrowerData);
  },

  /**
   * Merge borrowers
   * @param {Object} mergeData - Merge data with primary and secondary IDs
   * @returns {Promise} - Promise with merge result
   */
  mergeBorrowers(mergeData) {
    return apiClient.post('/borrowers/merge/', mergeData);
  },

  /**
   * Get merge history
   * @returns {Promise} - Promise with merge history data
   */
  getMergeHistory() {
    return apiClient.get('/borrowers/merge-history/');
  }
};

export default borrowerService;
