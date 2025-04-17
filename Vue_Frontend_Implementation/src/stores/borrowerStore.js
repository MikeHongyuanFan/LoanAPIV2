import { defineStore } from 'pinia';
import borrowerService from '@/services/borrowerService';

export const useBorrowerStore = defineStore('borrower', {
  state: () => ({
    borrowers: [],
    currentBorrower: null,
    pagination: {
      total: 0,
      page: 1,
      limit: 10
    },
    loading: false,
    error: null
  }),

  getters: {
    getBorrowerById: (state) => (id) => {
      return state.borrowers.find(borrower => borrower.id === id) || null;
    }
  },

  actions: {
    async getBorrowers(params = {}) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await borrowerService.getBorrowers(params);
        this.borrowers = response.items || response;
        
        if (response.pagination) {
          this.pagination = response.pagination;
        }
        
        return response;
      } catch (error) {
        this.error = error.message || 'Failed to fetch borrowers';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getBorrower(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const borrower = await borrowerService.getBorrower(id);
        this.currentBorrower = borrower;
        return borrower;
      } catch (error) {
        this.error = error.message || 'Failed to fetch borrower';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async createBorrower(borrowerData) {
      this.loading = true;
      this.error = null;
      
      try {
        const borrower = await borrowerService.createBorrower(borrowerData);
        this.borrowers.unshift(borrower);
        return borrower;
      } catch (error) {
        this.error = error.message || 'Failed to create borrower';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async updateBorrower(id, borrowerData) {
      this.loading = true;
      this.error = null;
      
      try {
        const borrower = await borrowerService.updateBorrower(id, borrowerData);
        
        // Update in borrowers array if exists
        const index = this.borrowers.findIndex(b => b.id === id);
        if (index !== -1) {
          this.borrowers[index] = borrower;
        }
        
        // Update current borrower if it's the same
        if (this.currentBorrower && this.currentBorrower.id === id) {
          this.currentBorrower = borrower;
        }
        
        return borrower;
      } catch (error) {
        this.error = error.message || 'Failed to update borrower';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async deleteBorrower(id) {
      this.loading = true;
      this.error = null;
      
      try {
        await borrowerService.deleteBorrower(id);
        
        // Remove from borrowers array
        this.borrowers = this.borrowers.filter(b => b.id !== id);
        
        // Clear current borrower if it's the same
        if (this.currentBorrower && this.currentBorrower.id === id) {
          this.currentBorrower = null;
        }
        
        return true;
      } catch (error) {
        this.error = error.message || 'Failed to delete borrower';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async searchBorrowers(query) {
      this.loading = true;
      this.error = null;
      
      try {
        const borrowers = await borrowerService.searchBorrowers(query);
        return borrowers;
      } catch (error) {
        this.error = error.message || 'Failed to search borrowers';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getBorrowerApplications(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const applications = await borrowerService.getBorrowerApplications(id);
        return applications;
      } catch (error) {
        this.error = error.message || 'Failed to fetch borrower applications';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async checkDuplicates(borrowerData) {
      this.loading = true;
      this.error = null;
      
      try {
        const duplicates = await borrowerService.checkDuplicates(borrowerData);
        return duplicates;
      } catch (error) {
        this.error = error.message || 'Failed to check for duplicates';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async mergeBorrowers(primaryId, secondaryIds) {
      this.loading = true;
      this.error = null;
      
      try {
        const result = await borrowerService.mergeBorrowers({
          primary_id: primaryId,
          secondary_ids: secondaryIds
        });
        
        // Update borrowers list
        await this.getBorrowers();
        
        return result;
      } catch (error) {
        this.error = error.message || 'Failed to merge borrowers';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async getMergeHistory() {
      this.loading = true;
      this.error = null;
      
      try {
        const history = await borrowerService.getMergeHistory();
        return history;
      } catch (error) {
        this.error = error.message || 'Failed to fetch merge history';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
