import { defineStore } from 'pinia';
import documentService from '@/services/documentService';

export const useDocumentStore = defineStore('document', {
  state: () => ({
    documents: [],
    documentTemplates: [],
    loading: false,
    error: null
  }),

  getters: {
    getDocumentById: (state) => (id) => {
      return state.documents.find(doc => doc.id === id) || null;
    },
    
    getTemplateById: (state) => (id) => {
      return state.documentTemplates.find(template => template.id === id) || null;
    }
  },

  actions: {
    async getDocuments(params = {}) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await documentService.getDocuments(params);
        this.documents = response.items || response;
        return this.documents;
      } catch (error) {
        this.error = error.message || 'Failed to fetch documents';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getDocument(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const document = await documentService.getDocument(id);
        return document;
      } catch (error) {
        this.error = error.message || 'Failed to fetch document';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async uploadDocument(formData) {
      this.loading = true;
      this.error = null;
      
      try {
        const document = await documentService.uploadDocument(formData);
        this.documents.unshift(document);
        return document;
      } catch (error) {
        this.error = error.message || 'Failed to upload document';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async deleteDocument(id) {
      this.loading = true;
      this.error = null;
      
      try {
        await documentService.deleteDocument(id);
        this.documents = this.documents.filter(doc => doc.id !== id);
        return true;
      } catch (error) {
        this.error = error.message || 'Failed to delete document';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async generateDocument(options) {
      this.loading = true;
      this.error = null;
      
      try {
        const document = await documentService.generateDocument(options);
        this.documents.unshift(document);
        return document;
      } catch (error) {
        this.error = error.message || 'Failed to generate document';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getDocumentTemplates() {
      this.loading = true;
      this.error = null;
      
      try {
        const templates = await documentService.getDocumentTemplates();
        this.documentTemplates = templates;
        return templates;
      } catch (error) {
        this.error = error.message || 'Failed to fetch document templates';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getDocumentTemplate(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const template = await documentService.getDocumentTemplate(id);
        return template;
      } catch (error) {
        this.error = error.message || 'Failed to fetch document template';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async createDocumentTemplate(templateData) {
      this.loading = true;
      this.error = null;
      
      try {
        const template = await documentService.createDocumentTemplate(templateData);
        this.documentTemplates.unshift(template);
        return template;
      } catch (error) {
        this.error = error.message || 'Failed to create document template';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async updateDocumentTemplate(id, templateData) {
      this.loading = true;
      this.error = null;
      
      try {
        const template = await documentService.updateDocumentTemplate(id, templateData);
        
        const index = this.documentTemplates.findIndex(t => t.id === id);
        if (index !== -1) {
          this.documentTemplates[index] = template;
        }
        
        return template;
      } catch (error) {
        this.error = error.message || 'Failed to update document template';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async deleteDocumentTemplate(id) {
      this.loading = true;
      this.error = null;
      
      try {
        await documentService.deleteDocumentTemplate(id);
        this.documentTemplates = this.documentTemplates.filter(t => t.id !== id);
        return true;
      } catch (error) {
        this.error = error.message || 'Failed to delete document template';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async sendForSigning(documentId, signingData) {
      this.loading = true;
      this.error = null;
      
      try {
        const result = await documentService.sendForSigning(documentId, signingData);
        return result;
      } catch (error) {
        this.error = error.message || 'Failed to send document for signing';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getDocumentVersions(documentId) {
      this.loading = true;
      this.error = null;
      
      try {
        const versions = await documentService.getDocumentVersions(documentId);
        return versions;
      } catch (error) {
        this.error = error.message || 'Failed to fetch document versions';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
