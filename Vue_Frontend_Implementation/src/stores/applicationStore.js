import { defineStore } from 'pinia';
import applicationService from '@/services/applicationService';

export const useApplicationStore = defineStore('application', {
  state: () => ({
    applications: [],
    currentApplication: null,
    pagination: {
      total: 0,
      page: 1,
      limit: 10
    },
    loading: false,
    error: null
  }),

  getters: {
    getApplicationById: (state) => (id) => {
      return state.applications.find(app => app.id === id) || null;
    }
  },

  actions: {
    async fetchApplications(params = {}) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await applicationService.getApplications(params);
        this.applications = response.items || response;
        
        if (response.pagination) {
          this.pagination = response.pagination;
        }
        
        return this.applications;
      } catch (error) {
        this.error = error.message || 'Failed to fetch applications';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async fetchApplicationById(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const application = await applicationService.getApplication(id);
        this.currentApplication = application;
        return application;
      } catch (error) {
        this.error = error.message || 'Failed to fetch application';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async createApplication(applicationData) {
      this.loading = true;
      this.error = null;
      
      try {
        const application = await applicationService.createApplication(applicationData);
        this.applications.unshift(application);
        return application;
      } catch (error) {
        this.error = error.message || 'Failed to create application';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async updateApplication(id, applicationData) {
      this.loading = true;
      this.error = null;
      
      try {
        const application = await applicationService.updateApplication(id, applicationData);
        
        // Update in applications array if exists
        const index = this.applications.findIndex(app => app.id === id);
        if (index !== -1) {
          this.applications[index] = application;
        }
        
        // Update current application if it's the same
        if (this.currentApplication && this.currentApplication.id === id) {
          this.currentApplication = application;
        }
        
        return application;
      } catch (error) {
        this.error = error.message || 'Failed to update application';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async deleteApplication(id) {
      this.loading = true;
      this.error = null;
      
      try {
        await applicationService.deleteApplication(id);
        
        // Remove from applications array
        this.applications = this.applications.filter(app => app.id !== id);
        
        // Clear current application if it's the same
        if (this.currentApplication && this.currentApplication.id === id) {
          this.currentApplication = null;
        }
        
        return true;
      } catch (error) {
        this.error = error.message || 'Failed to delete application';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async duplicateApplication(id, options = {}) {
      this.loading = true;
      this.error = null;
      
      try {
        const application = await applicationService.duplicateApplication(id, options);
        this.applications.unshift(application);
        return application.id;
      } catch (error) {
        this.error = error.message || 'Failed to duplicate application';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async updateApplicationStatus(id, status, comment = '') {
      this.loading = true;
      this.error = null;
      
      try {
        const data = { status, comment };
        const application = await applicationService.updateApplication(id, data);
        
        // Update in applications array if exists
        const index = this.applications.findIndex(app => app.id === id);
        if (index !== -1) {
          this.applications[index] = application;
        }
        
        // Update current application if it's the same
        if (this.currentApplication && this.currentApplication.id === id) {
          this.currentApplication = application;
        }
        
        return application;
      } catch (error) {
        this.error = error.message || 'Failed to update application status';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async uploadDocuments(id, formData) {
      this.loading = true;
      this.error = null;
      
      try {
        const result = await applicationService.uploadDocuments(id, formData);
        return result;
      } catch (error) {
        this.error = error.message || 'Failed to upload documents';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async generateDocuments(id, options) {
      this.loading = true;
      this.error = null;
      
      try {
        const result = await applicationService.generateDocuments(id, options);
        return result;
      } catch (error) {
        this.error = error.message || 'Failed to generate documents';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async createNote(id, noteData) {
      this.loading = true;
      this.error = null;
      
      try {
        const note = await applicationService.createNote(id, noteData);
        return note;
      } catch (error) {
        this.error = error.message || 'Failed to create note';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getNotes(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const notes = await applicationService.getNotes(id);
        return notes;
      } catch (error) {
        this.error = error.message || 'Failed to fetch notes';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async calculateLoan(id, calculatorData) {
      this.loading = true;
      this.error = null;
      
      try {
        const result = await applicationService.calculateLoan(id, calculatorData);
        return result;
      } catch (error) {
        this.error = error.message || 'Failed to calculate loan';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async createRepaymentSchedule(id, repaymentData) {
      this.loading = true;
      this.error = null;
      
      try {
        const result = await applicationService.createRepaymentSchedule(id, repaymentData);
        return result;
      } catch (error) {
        this.error = error.message || 'Failed to create repayment schedule';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getRepaymentSchedule(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const schedule = await applicationService.getRepaymentSchedule(id);
        return schedule;
      } catch (error) {
        this.error = error.message || 'Failed to fetch repayment schedule';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async createFee(id, feeData) {
      this.loading = true;
      this.error = null;
      
      try {
        const fee = await applicationService.createFee(id, feeData);
        return fee;
      } catch (error) {
        this.error = error.message || 'Failed to create fee';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getFees(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const fees = await applicationService.getFees(id);
        return fees;
      } catch (error) {
        this.error = error.message || 'Failed to fetch fees';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async addBorrowerToApplication(applicationId, borrowerId, isPrimary = false) {
      this.loading = true;
      this.error = null;
      
      try {
        const data = {
          borrower_id: borrowerId,
          is_primary: isPrimary
        };
        
        // This would typically be a custom endpoint, but we're using updateApplication as a fallback
        const application = await applicationService.updateApplication(applicationId, {
          borrowers: [...(this.currentApplication?.borrowers || []), data]
        });
        
        if (this.currentApplication && this.currentApplication.id === applicationId) {
          this.currentApplication = application;
        }
        
        return application;
      } catch (error) {
        this.error = error.message || 'Failed to add borrower to application';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async removeBorrowerFromApplication(applicationId, borrowerId) {
      this.loading = true;
      this.error = null;
      
      try {
        // This would typically be a custom endpoint, but we're using updateApplication as a fallback
        const updatedBorrowers = (this.currentApplication?.borrowers || [])
          .filter(b => b.id !== borrowerId);
        
        const application = await applicationService.updateApplication(applicationId, {
          borrowers: updatedBorrowers
        });
        
        if (this.currentApplication && this.currentApplication.id === applicationId) {
          this.currentApplication = application;
        }
        
        return application;
      } catch (error) {
        this.error = error.message || 'Failed to remove borrower from application';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async updateApplicationBorrower(applicationId, borrowerId, data) {
      this.loading = true;
      this.error = null;
      
      try {
        // This would typically be a custom endpoint, but we're using updateApplication as a fallback
        const updatedBorrowers = (this.currentApplication?.borrowers || [])
          .map(b => b.id === borrowerId ? { ...b, ...data } : b);
        
        const application = await applicationService.updateApplication(applicationId, {
          borrowers: updatedBorrowers
        });
        
        if (this.currentApplication && this.currentApplication.id === applicationId) {
          this.currentApplication = application;
        }
        
        return application;
      } catch (error) {
        this.error = error.message || 'Failed to update application borrower';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async exportApplication(id, format = 'pdf') {
      this.loading = true;
      this.error = null;
      
      try {
        // This would typically be a custom endpoint
        const result = await applicationService.generateDocuments(id, {
          template: 'APPLICATION_SUMMARY',
          format: format
        });
        
        return result;
      } catch (error) {
        this.error = error.message || 'Failed to export application';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async exportRepaymentSchedule(id, format = 'pdf') {
      this.loading = true;
      this.error = null;
      
      try {
        // This would typically be a custom endpoint
        const result = await applicationService.generateDocuments(id, {
          template: 'REPAYMENT_SCHEDULE',
          format: format
        });
        
        return result;
      } catch (error) {
        this.error = error.message || 'Failed to export repayment schedule';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
