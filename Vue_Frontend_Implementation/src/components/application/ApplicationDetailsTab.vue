<template>
  <div class="application-details-tab">
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="bg-grey-lighten-4 py-3">
            <v-icon start class="mr-2">mdi-information-outline</v-icon>
            General Information
          </v-card-title>
          <v-card-text class="pa-4">
            <div class="detail-grid">
              <div class="detail-item">
                <div class="detail-label">Application Type</div>
                <div class="detail-value">{{ application.application_type }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Purpose</div>
                <div class="detail-value">{{ application.purpose || 'Not specified' }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Product</div>
                <div class="detail-value">{{ application.product?.name || 'Not specified' }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Loan Amount</div>
                <div class="detail-value">{{ formatCurrency(application.loan_amount) }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Interest Rate</div>
                <div class="detail-value">{{ formatPercentage(application.interest_rate) }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Loan Term</div>
                <div class="detail-value">{{ formatTerm(application.loan_term, application.loan_term_unit) }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Repayment Frequency</div>
                <div class="detail-value">{{ formatFrequency(application.repayment_frequency) }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Estimated Settlement Date</div>
                <div class="detail-value">{{ formatDate(application.estimated_settlement_date) || 'Not specified' }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
        
        <v-card class="mt-4">
          <v-card-title class="bg-grey-lighten-4 py-3">
            <v-icon start class="mr-2">mdi-account-outline</v-icon>
            Broker Information
          </v-card-title>
          <v-card-text class="pa-4">
            <div v-if="application.broker">
              <div class="d-flex align-center mb-4">
                <v-avatar size="40" class="mr-3">
                  <v-img v-if="application.broker.avatar" :src="application.broker.avatar"></v-img>
                  <v-icon v-else size="24">mdi-account</v-icon>
                </v-avatar>
                <div>
                  <div class="text-subtitle-1 font-weight-medium">{{ application.broker.name }}</div>
                  <div class="text-body-2 text-medium-emphasis">{{ application.broker.company }}</div>
                </div>
              </div>
              
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-label">Email</div>
                  <div class="detail-value">{{ application.broker.email }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Phone</div>
                  <div class="detail-value">{{ application.broker.phone }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">License Number</div>
                  <div class="detail-value">{{ application.broker.license_number }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Commission Rate</div>
                  <div class="detail-value">{{ formatPercentage(application.broker.commission_rate) }}</div>
                </div>
              </div>
              
              <v-btn
                color="primary"
                variant="text"
                class="mt-2"
                prepend-icon="mdi-account"
                :to="`/brokers/${application.broker.id}`"
              >
                View Broker Profile
              </v-btn>
            </div>
            <div v-else class="text-center py-4">
              <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-account-off</v-icon>
              <div class="text-body-1">No broker associated with this application</div>
              <div class="text-caption text-medium-emphasis">This is a direct application</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="bg-grey-lighten-4 py-3">
            <v-icon start class="mr-2">mdi-home-outline</v-icon>
            Security Information
          </v-card-title>
          <v-card-text class="pa-4">
            <div v-if="application.security">
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-label">Security Type</div>
                  <div class="detail-value">{{ application.security.type }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Security Value</div>
                  <div class="detail-value">{{ formatCurrency(application.security.value) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Address</div>
                  <div class="detail-value">{{ formatAddress(application.security.address) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Valuation Date</div>
                  <div class="detail-value">{{ formatDate(application.security.valuation_date) || 'Not specified' }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Valuation Type</div>
                  <div class="detail-value">{{ application.security.valuation_type || 'Not specified' }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">LVR</div>
                  <div class="detail-value">
                    <template v-if="calculatedLVR !== null">
                      {{ formatPercentage(calculatedLVR) }}
                      <v-chip
                        size="x-small"
                        :color="lvrColor"
                        class="ml-2"
                      >
                        {{ lvrRating }}
                      </v-chip>
                    </template>
                    <span v-else>N/A</span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-home-remove</v-icon>
              <div class="text-body-1">No security information available</div>
              <div class="text-caption text-medium-emphasis">Security details have not been provided</div>
            </div>
          </v-card-text>
        </v-card>
        
        <v-card class="mt-4">
          <v-card-title class="bg-grey-lighten-4 py-3">
            <v-icon start class="mr-2">mdi-text-box-outline</v-icon>
            Additional Information
          </v-card-title>
          <v-card-text class="pa-4">
            <div v-if="application.additional_info">
              <div class="detail-item mb-4">
                <div class="detail-label">Description</div>
                <div class="detail-value">{{ application.additional_info.description || 'No description provided' }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Special Conditions</div>
                <div class="detail-value">{{ application.additional_info.special_conditions || 'No special conditions' }}</div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-text-box-remove</v-icon>
              <div class="text-body-1">No additional information available</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { formatDate } from '@/utils/dateUtils';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

// Formatting functions
const formatCurrency = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD',
    minimumFractionDigits: 2
  }).format(value);
};

const formatPercentage = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return new Intl.NumberFormat('en-AU', {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value / 100);
};

const formatTerm = (term, unit) => {
  if (!term) return 'N/A';
  
  const unitMap = {
    'YEARS': term === 1 ? 'year' : 'years',
    'MONTHS': term === 1 ? 'month' : 'months',
    'WEEKS': term === 1 ? 'week' : 'weeks',
    'DAYS': term === 1 ? 'day' : 'days'
  };
  
  return `${term} ${unitMap[unit] || unit.toLowerCase()}`;
};

const formatFrequency = (frequency) => {
  if (!frequency) return 'N/A';
  
  const frequencyMap = {
    'WEEKLY': 'Weekly',
    'FORTNIGHTLY': 'Fortnightly',
    'MONTHLY': 'Monthly',
    'QUARTERLY': 'Quarterly',
    'ANNUALLY': 'Annually'
  };
  
  return frequencyMap[frequency] || frequency;
};

const formatAddress = (address) => {
  if (!address) return 'N/A';
  
  const parts = [];
  if (address.street) parts.push(address.street);
  if (address.city) parts.push(address.city);
  if (address.state) parts.push(address.state);
  if (address.postal_code) parts.push(address.postal_code);
  if (address.country) parts.push(address.country);
  
  return parts.join(', ') || 'N/A';
};

// Computed properties
const calculatedLVR = computed(() => {
  if (!props.application.loan_amount || !props.application.security?.value) return null;
  return (props.application.loan_amount / props.application.security.value) * 100;
});

const lvrRating = computed(() => {
  if (calculatedLVR.value === null) return '';
  
  if (calculatedLVR.value <= 60) return 'Excellent';
  if (calculatedLVR.value <= 75) return 'Good';
  if (calculatedLVR.value <= 85) return 'Fair';
  return 'High';
});

const lvrColor = computed(() => {
  if (calculatedLVR.value === null) return '';
  
  if (calculatedLVR.value <= 60) return 'success';
  if (calculatedLVR.value <= 75) return 'light-green';
  if (calculatedLVR.value <= 85) return 'amber';
  return 'error';
});
</script>

<style scoped>
.application-details-tab {
  padding-bottom: 1rem;
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
