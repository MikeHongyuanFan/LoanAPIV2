<template>
  <div class="borrower-contact-details">
    <h3 class="text-subtitle-1 font-weight-bold mb-4">Contact Information</h3>
    
    <div class="detail-grid">
      <div class="detail-item">
        <div class="detail-label">Email</div>
        <div class="detail-value">
          <a :href="`mailto:${borrower.email}`" class="text-decoration-none">
            {{ borrower.email }}
          </a>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Phone</div>
        <div class="detail-value">
          <a :href="`tel:${borrower.phone}`" class="text-decoration-none">
            {{ formatPhone(borrower.phone) }}
          </a>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Mobile</div>
        <div class="detail-value">
          <a v-if="borrower.mobile" :href="`tel:${borrower.mobile}`" class="text-decoration-none">
            {{ formatPhone(borrower.mobile) }}
          </a>
          <span v-else>Not specified</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Work Phone</div>
        <div class="detail-value">
          <a v-if="borrower.work_phone" :href="`tel:${borrower.work_phone}`" class="text-decoration-none">
            {{ formatPhone(borrower.work_phone) }}
          </a>
          <span v-else>Not specified</span>
        </div>
      </div>
    </div>
    
    <h3 class="text-subtitle-1 font-weight-bold mt-6 mb-4">Residential Address</h3>
    
    <div v-if="borrower.residential_address" class="address-card pa-4 mb-4">
      <div class="text-body-1">{{ formatAddressLine(borrower.residential_address) }}</div>
      <div class="text-body-1">{{ formatAddressCity(borrower.residential_address) }}</div>
      <div v-if="borrower.residential_address.country" class="text-body-1">
        {{ borrower.residential_address.country }}
      </div>
      
      <div class="mt-2 text-caption">
        <v-icon size="small" class="mr-1">mdi-home-outline</v-icon>
        {{ formatResidentialStatus(borrower.residential_status) }}
      </div>
      
      <div v-if="borrower.years_at_address" class="mt-1 text-caption">
        <v-icon size="small" class="mr-1">mdi-calendar-outline</v-icon>
        {{ formatYearsAtAddress(borrower.years_at_address) }}
      </div>
    </div>
    <div v-else class="text-body-1 text-medium-emphasis">No residential address provided</div>
    
    <h3 class="text-subtitle-1 font-weight-bold mt-6 mb-4">Mailing Address</h3>
    
    <div v-if="borrower.mailing_address" class="address-card pa-4">
      <div v-if="isSameAsResidential" class="text-body-1 text-medium-emphasis">
        Same as residential address
      </div>
      <template v-else>
        <div class="text-body-1">{{ formatAddressLine(borrower.mailing_address) }}</div>
        <div class="text-body-1">{{ formatAddressCity(borrower.mailing_address) }}</div>
        <div v-if="borrower.mailing_address.country" class="text-body-1">
          {{ borrower.mailing_address.country }}
        </div>
      </template>
    </div>
    <div v-else class="text-body-1 text-medium-emphasis">No mailing address provided</div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  borrower: {
    type: Object,
    required: true
  }
});

// Computed properties
const isSameAsResidential = computed(() => {
  if (!props.borrower.residential_address || !props.borrower.mailing_address) {
    return false;
  }
  
  const residential = props.borrower.residential_address;
  const mailing = props.borrower.mailing_address;
  
  return residential.street === mailing.street &&
         residential.city === mailing.city &&
         residential.state === mailing.state &&
         residential.postal_code === mailing.postal_code &&
         residential.country === mailing.country;
});

// Formatting functions
const formatPhone = (phone) => {
  if (!phone) return 'Not specified';
  
  // Simple formatting for display purposes
  // In a real app, you'd use a proper phone formatting library
  if (phone.length === 10) {
    return `(${phone.substring(0, 3)}) ${phone.substring(3, 6)}-${phone.substring(6)}`;
  }
  
  return phone;
};

const formatAddressLine = (address) => {
  if (!address) return '';
  
  let line = address.street || '';
  
  if (address.unit) {
    line = `${address.unit} ${line}`;
  }
  
  return line;
};

const formatAddressCity = (address) => {
  if (!address) return '';
  
  let parts = [];
  
  if (address.city) parts.push(address.city);
  if (address.state) parts.push(address.state);
  if (address.postal_code) parts.push(address.postal_code);
  
  return parts.join(', ');
};

const formatResidentialStatus = (status) => {
  if (!status) return 'Not specified';
  
  const statusMap = {
    'OWNER': 'Owner',
    'MORTGAGED': 'Mortgaged',
    'RENTING': 'Renting',
    'LIVING_WITH_PARENTS': 'Living with parents',
    'BOARDING': 'Boarding',
    'OTHER': 'Other'
  };
  
  return statusMap[status] || status;
};

const formatYearsAtAddress = (years) => {
  if (!years) return '';
  
  if (years < 1) {
    const months = Math.round(years * 12);
    return `${months} ${months === 1 ? 'month' : 'months'} at this address`;
  }
  
  return `${years} ${years === 1 ? 'year' : 'years'} at this address`;
};
</script>

<style scoped>
.borrower-contact-details {
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

.address-card {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 4px;
  background-color: rgba(0, 0, 0, 0.02);
}

@media (max-width: 600px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
