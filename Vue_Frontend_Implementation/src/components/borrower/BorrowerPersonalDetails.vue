<template>
  <div class="borrower-personal-details">
    <h3 class="text-subtitle-1 font-weight-bold mb-4">Personal Information</h3>
    
    <div class="detail-grid">
      <div class="detail-item">
        <div class="detail-label">Full Name</div>
        <div class="detail-value">{{ borrower.full_name }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Date of Birth</div>
        <div class="detail-value">{{ formatDate(borrower.date_of_birth) }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Gender</div>
        <div class="detail-value">{{ formatGender(borrower.gender) }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Marital Status</div>
        <div class="detail-value">{{ formatMaritalStatus(borrower.marital_status) }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Nationality</div>
        <div class="detail-value">{{ borrower.nationality || 'Not specified' }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Tax ID / SSN</div>
        <div class="detail-value">{{ borrower.tax_id || 'Not specified' }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">ID Type</div>
        <div class="detail-value">{{ formatIdType(borrower.id_type) }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">ID Number</div>
        <div class="detail-value">{{ borrower.id_number || 'Not specified' }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">ID Expiry</div>
        <div class="detail-value">{{ formatDate(borrower.id_expiry_date) || 'Not specified' }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Dependents</div>
        <div class="detail-value">{{ borrower.dependents || '0' }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDate } from '@/utils/dateUtils';

const props = defineProps({
  borrower: {
    type: Object,
    required: true
  }
});

// Formatting functions
const formatGender = (gender) => {
  if (!gender) return 'Not specified';
  
  const genderMap = {
    'MALE': 'Male',
    'FEMALE': 'Female',
    'OTHER': 'Other',
    'PREFER_NOT_TO_SAY': 'Prefer not to say'
  };
  
  return genderMap[gender] || gender;
};

const formatMaritalStatus = (status) => {
  if (!status) return 'Not specified';
  
  const statusMap = {
    'SINGLE': 'Single',
    'MARRIED': 'Married',
    'DIVORCED': 'Divorced',
    'WIDOWED': 'Widowed',
    'SEPARATED': 'Separated',
    'DOMESTIC_PARTNERSHIP': 'Domestic Partnership'
  };
  
  return statusMap[status] || status;
};

const formatIdType = (type) => {
  if (!type) return 'Not specified';
  
  const typeMap = {
    'PASSPORT': 'Passport',
    'DRIVERS_LICENSE': 'Driver\'s License',
    'NATIONAL_ID': 'National ID',
    'RESIDENCE_PERMIT': 'Residence Permit',
    'OTHER': 'Other'
  };
  
  return typeMap[type] || type;
};
</script>

<style scoped>
.borrower-personal-details {
  height: 100%;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.detail-item {
  margin-bottom: 8px;
}

.detail-label {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 4px;
}

.detail-value {
  font-size: 0.9375rem;
}

@media (max-width: 600px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
