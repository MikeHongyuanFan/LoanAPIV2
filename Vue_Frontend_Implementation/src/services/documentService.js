import apiClient from './apiClient';

const documentService = {
  /**
   * Get all documents with optional filters
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with documents data
   */
  getDocuments(filters = {}) {
    return apiClient.get('/documents/', { params: filters });
  },

  /**
   * Get document by ID
   * @param {string|number} id - Document ID
   * @returns {Promise} - Promise with document data
   */
  getDocument(id) {
    return apiClient.get(`/documents/${id}/`);
  },

  /**
   * Update a document
   * @param {string|number} id - Document ID
   * @param {Object} documentData - Document data to update
   * @returns {Promise} - Promise with updated document data
   */
  updateDocument(id, documentData) {
    return apiClient.patch(`/documents/${id}/`, documentData);
  },

  /**
   * Delete a document
   * @param {string|number} id - Document ID
   * @returns {Promise} - Promise with deletion status
   */
  deleteDocument(id) {
    return apiClient.delete(`/documents/${id}/`);
  },

  /**
   * Upload a document
   * @param {FormData} formData - Form data with file and metadata
   * @returns {Promise} - Promise with uploaded document data
   */
  uploadDocument(formData) {
    return apiClient.post('/documents/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  /**
   * Generate a document
   * @param {Object} options - Document generation options
   * @returns {Promise} - Promise with generated document data
   */
  generateDocument(options) {
    return apiClient.post('/documents/generate/', options);
  },

  /**
   * Get all document templates
   * @returns {Promise} - Promise with document templates data
   */
  getDocumentTemplates() {
    return apiClient.get('/documents/templates/');
  },

  /**
   * Get document template by ID
   * @param {string|number} id - Template ID
   * @returns {Promise} - Promise with document template data
   */
  getDocumentTemplate(id) {
    return apiClient.get(`/documents/templates/${id}/`);
  },

  /**
   * Create a document template
   * @param {Object} templateData - Template data
   * @returns {Promise} - Promise with created template data
   */
  createDocumentTemplate(templateData) {
    return apiClient.post('/documents/templates/', templateData);
  },

  /**
   * Update a document template
   * @param {string|number} id - Template ID
   * @param {Object} templateData - Template data to update
   * @returns {Promise} - Promise with updated template data
   */
  updateDocumentTemplate(id, templateData) {
    return apiClient.patch(`/documents/templates/${id}/`, templateData);
  },

  /**
   * Delete a document template
   * @param {string|number} id - Template ID
   * @returns {Promise} - Promise with deletion status
   */
  deleteDocumentTemplate(id) {
    return apiClient.delete(`/documents/templates/${id}/`);
  },

  /**
   * Send document for signing
   * @param {string|number} documentId - Document ID
   * @param {Object} signingData - Signing request data
   * @returns {Promise} - Promise with signing request data
   */
  sendForSigning(documentId, signingData) {
    return apiClient.post('/documents/send-for-signing/', {
      document_id: documentId,
      ...signingData
    });
  },

  /**
   * Get signing requests
   * @param {Object} filters - Optional filters
   * @returns {Promise} - Promise with signing requests data
   */
  getSigningRequests(filters = {}) {
    return apiClient.get('/documents/signing-requests/', { params: filters });
  },

  /**
   * Get signing request by ID
   * @param {string|number} id - Signing request ID
   * @returns {Promise} - Promise with signing request data
   */
  getSigningRequest(id) {
    return apiClient.get(`/documents/signing-requests/${id}/`);
  },

  /**
   * Get document versions
   * @param {string|number} documentId - Document ID
   * @returns {Promise} - Promise with document versions data
   */
  getDocumentVersions(documentId) {
    return apiClient.get(`/documents/${documentId}/versions/`);
  },

  /**
   * Create document version
   * @param {string|number} documentId - Document ID
   * @param {FormData} formData - Form data with file and metadata
   * @returns {Promise} - Promise with created version data
   */
  createDocumentVersion(documentId, formData) {
    return apiClient.post(`/documents/${documentId}/versions/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }
};

export default documentService;
