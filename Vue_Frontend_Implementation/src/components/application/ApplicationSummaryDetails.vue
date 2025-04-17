<template>
  <div class="application-summary-details">
    <h3 class="text-subtitle-1 font-weight-bold mb-4">Application Details</h3>
    
    <div class="detail-grid">
      <div class="detail-item">
        <div class="detail-label">Reference Number</div>
        <div class="detail-value">{{ application.reference_number }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Application Type</div>
        <div class="detail-value">{{ application.application_type }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Product</div>
        <div class="detail-value">{{ application.product?.name || 'Not specified' }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Status</div>
        <div class="detail-value">
          <application-status-badge :status="application.status" />
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Created Date</div>
        <div class="detail-value">{{ formatDate(application.created_at) }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Last Updated</div>
        <div class="detail-value">{{ formatDate(application.updated_at) }}</div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Broker</div>
        <div class="detail-value">
          <template v-if="application.broker">
            <v-avatar size="24" class="mr-1">
              <v-img v-if="application.broker.avatar" :src="application.broker.avatar"></v-img>
              <v-icon v-else>mdi-account</v-icon>
            </v-avatar>
            {{ application.broker.name }}
          </template>
          <span v-else>Direct Application</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Primary Borrower</div>
        <div class="detail-value">
          <template v-if="primaryBorrower">
            <v-avatar size="24" class="mr-1">
              <v-img v-if="primaryBorrower.avatar" :src="primaryBorrower.avatar"></v-img>
              <v-icon v-else>mdi-account</v-icon>
            </v-avatar>
            {{ primaryBorrower.full_name }}
          </template>
          <span v-else>Not specified</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Co-Borrowers</div>
        <div class="detail-value">
          <template v-if="coBorrowers.length > 0">
            {{ coBorrowers.length }} co-borrower(s)
            <v-tooltip location="bottom">
              <template v-slot:activator="{ props }">
                <v-icon v-bind="props" size="small" class="ml-1">mdi-information-outline</v-icon>
              </template>
              <div>
                <div v-for="(borrower, index) in coBorrowers" :key="index">
                  {{ borrower.full_name }}
                </div>
              </div>
            </v-tooltip>
          </template>
          <span v-else>None</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-label">Purpose</div>
        <div class="detail-value">{{ application.purpose || 'Not specified' }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { formatDate } from '@/utils/dateUtils';
import ApplicationStatusBadge from '@/components/application/ApplicationStatusBadge.vue';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

// Computed properties
const primaryBorrower = computed(() => {
  if (!props.application.borrowers || props.application.borrowers.length === 0) {
    return null;
  }
  
  // Find the primary borrower (is_primary flag or first in the list)
  return props.application.borrowers.find(b => b.is_primary) || props.application.borrowers[0];
});

const coBorrowers = computed(() => {
  if (!props.application.borrowers || props.application.borrowers.length <= 1) {
    return [];
  }
  
  // Filter out the primary borrower
  return props.application.borrowers.filter(b => !b.is_primary);
});
</script>

<style scoped>
.application-summary-details {
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
  display: flex;
  align-items: center;
}

@media (max-width: 600px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
