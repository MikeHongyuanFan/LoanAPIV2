<template>
  <div class="borrower-merge-interface">
    <div v-if="loading" class="d-flex justify-center my-8">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else>
      <p class="text-body-1 mb-4">
        The following borrowers have been identified as possible duplicates. Review the information and select which data to keep.
      </p>

      <v-alert
        type="warning"
        variant="tonal"
        class="mb-4"
      >
        <div class="font-weight-bold">Warning</div>
        <div>Merging borrowers is permanent and cannot be undone. All applications, documents, and history from the secondary borrowers will be transferred to the primary borrower.</div>
      </v-alert>

      <v-card class="mb-6">
        <v-card-title class="bg-primary text-white py-3">
          <v-icon start class="mr-2">mdi-account-star</v-icon>
          Primary Borrower
        </v-card-title>
        <v-card-text class="pa-4">
          <div class="d-flex align-center mb-4">
            <v-avatar color="primary" class="mr-3">
              <v-img v-if="primaryBorrower.avatar" :src="primaryBorrower.avatar"></v-img>
              <v-icon v-else color="white">mdi-account</v-icon>
            </v-avatar>
            <div>
              <div class="text-h6">{{ primaryBorrower.full_name }}</div>
              <div class="text-subtitle-2">{{ primaryBorrower.email }}</div>
            </div>
          </div>

          <v-divider class="mb-4"></v-divider>

          <v-row>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Date of Birth</div>
                <div class="detail-value">{{ formatDate(primaryBorrower.date_of_birth) }}</div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Phone</div>
                <div class="detail-value">{{ primaryBorrower.phone }}</div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Address</div>
                <div class="detail-value">{{ formatAddress(primaryBorrower.residential_address) }}</div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Applications</div>
                <div class="detail-value">{{ primaryBorrower.applications?.length || 0 }} applications</div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <h3 class="text-h6 mb-3">Duplicate Borrowers</h3>

      <v-card
        v-for="(borrower, index) in duplicateBorrowers"
        :key="borrower.id"
        class="mb-4"
        :class="{ 'selected-duplicate': selectedDuplicates.includes(borrower.id) }"
      >
        <v-card-title class="py-3 d-flex justify-space-between">
          <div class="d-flex align-center">
            <v-checkbox
              v-model="selectedDuplicates"
              :value="borrower.id"
              hide-details
              class="mr-2"
            ></v-checkbox>
            <span>Duplicate #{{ index + 1 }}: {{ borrower.full_name }}</span>
          </div>
          <v-chip
            v-if="calculateMatchScore(borrower)"
            :color="getMatchScoreColor(calculateMatchScore(borrower))"
            size="small"
          >
            {{ calculateMatchScore(borrower) }}% Match
          </v-chip>
        </v-card-title>
        <v-card-text class="pa-4">
          <v-row>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Email</div>
                <div class="detail-value">
                  {{ borrower.email }}
                  <v-chip
                    v-if="borrower.email === primaryBorrower.email"
                    size="x-small"
                    color="success"
                    class="ml-2"
                  >
                    Match
                  </v-chip>
                </div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Phone</div>
                <div class="detail-value">
                  {{ borrower.phone }}
                  <v-chip
                    v-if="borrower.phone === primaryBorrower.phone"
                    size="x-small"
                    color="success"
                    class="ml-2"
                  >
                    Match
                  </v-chip>
                </div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Date of Birth</div>
                <div class="detail-value">
                  {{ formatDate(borrower.date_of_birth) }}
                  <v-chip
                    v-if="borrower.date_of_birth === primaryBorrower.date_of_birth"
                    size="x-small"
                    color="success"
                    class="ml-2"
                  >
                    Match
                  </v-chip>
                </div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Address</div>
                <div class="detail-value">
                  {{ formatAddress(borrower.residential_address) }}
                  <v-chip
                    v-if="isSameAddress(borrower.residential_address, primaryBorrower.residential_address)"
                    size="x-small"
                    color="success"
                    class="ml-2"
                  >
                    Match
                  </v-chip>
                </div>
              </div>
            </v-col>
          </v-row>

          <v-divider class="my-3"></v-divider>

          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="text-body-2">
                <strong>Applications:</strong> {{ borrower.applications?.length || 0 }}
              </div>
              <div class="text-body-2">
                <strong>Documents:</strong> {{ borrower.documents?.length || 0 }}
              </div>
            </div>
            <div>
              <v-btn
                color="primary"
                variant="text"
                size="small"
                prepend-icon="mdi-compare"
                @click="showComparisonDialog(borrower)"
              >
                Compare Details
              </v-btn>
            </div>
          </div>
        </v-card-text>
      </v-card>

      <v-divider class="my-6"></v-divider>

      <div class="d-flex justify-space-between align-center">
        <div>
          <v-checkbox
            v-model="selectAll"
            label="Select All Duplicates"
            @change="toggleSelectAll"
          ></v-checkbox>
        </div>
        <div>
          <v-btn
            color="grey-darken-1"
            variant="text"
            class="mr-2"
            @click="$emit('cancel')"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :disabled="selectedDuplicates.length === 0"
            :loading="merging"
            @click="mergeBorrowers"
          >
            Merge Selected ({{ selectedDuplicates.length }})
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Comparison Dialog -->
    <v-dialog v-model="showComparison" max-width="900px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-compare</v-icon>
          Detailed Comparison
        </v-card-title>
        <v-card-text class="pa-4">
          <v-table>
            <thead>
              <tr>
                <th>Field</th>
                <th>Primary Borrower</th>
                <th>Duplicate Borrower</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(field, index) in comparisonFields" :key="index">
                <td>{{ field.label }}</td>
                <td>{{ formatFieldValue(primaryBorrower, field.key) }}</td>
                <td>{{ formatFieldValue(comparisonBorrower, field.key) }}</td>
                <td>
                  <v-btn
                    v-if="isDifferent(primaryBorrower, comparisonBorrower, field.key)"
                    size="x-small"
                    color="primary"
                    variant="text"
                    @click="useValue(field.key)"
                  >
                    Use This Value
                  </v-btn>
                  <v-chip
                    v-else
                    size="x-small"
                    color="success"
                  >
                    Match
                  </v-chip>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="showComparison = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Confirmation Dialog -->
    <v-dialog v-model="showConfirmation" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Confirm Merge</v-card-title>
        <v-card-text>
          Are you sure you want to merge {{ selectedDuplicates.length }} duplicate borrower(s) into the primary borrower? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showConfirmation = false">Cancel</v-btn>
          <v-btn color="primary" variant="text" @click="confirmMerge" :loading="merging">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useBorrowerStore } from '@/stores/borrowerStore';
import { useNotificationStore } from '@/stores/notificationStore';
import { formatDate } from '@/utils/dateUtils';

const props = defineProps({
  primaryBorrower: {
    type: Object,
    required: true
  },
  duplicateBorrowers: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['merge-complete', 'cancel']);

// Stores
const borrowerStore = useBorrowerStore();
const notificationStore = useNotificationStore();

// State
const loading = ref(false);
const selectedDuplicates = ref([]);
const selectAll = ref(false);
const merging = ref(false);
const showConfirmation = ref(false);
const showComparison = ref(false);
const comparisonBorrower = ref(null);

// Comparison fields
const comparisonFields = [
  { key: 'first_name', label: 'First Name' },
  { key: 'last_name', label: 'Last Name' },
  { key: 'email', label: 'Email' },
  { key: 'phone', label: 'Phone' },
  { key: 'mobile', label: 'Mobile' },
  { key: 'date_of_birth', label: 'Date of Birth' },
  { key: 'gender', label: 'Gender' },
  { key: 'marital_status', label: 'Marital Status' },
  { key: 'residential_address.street', label: 'Street Address' },
  { key: 'residential_address.city', label: 'City' },
  { key: 'residential_address.state', label: 'State' },
  { key: 'residential_address.postal_code', label: 'Postal Code' },
  { key: 'residential_address.country', label: 'Country' },
  { key: 'tax_id', label: 'Tax ID' },
  { key: 'id_number', label: 'ID Number' }
];

// Watch for changes in duplicateBorrowers
watch(() => props.duplicateBorrowers, (newVal) => {
  // Pre-select duplicates with high match scores
  selectedDuplicates.value = newVal
    .filter(borrower => calculateMatchScore(borrower) >= 80)
    .map(borrower => borrower.id);
  
  // Update selectAll checkbox
  selectAll.value = selectedDuplicates.value.length === props.duplicateBorrowers.length;
}, { immediate: true });

// Methods
const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedDuplicates.value = props.duplicateBorrowers.map(b => b.id);
  } else {
    selectedDuplicates.value = [];
  }
};

const showComparisonDialog = (borrower) => {
  comparisonBorrower.value = borrower;
  showComparison.value = true;
};

const mergeBorrowers = () => {
  if (selectedDuplicates.value.length === 0) {
    notificationStore.showError('Please select at least one duplicate borrower to merge');
    return;
  }
  
  showConfirmation.value = true;
};

const confirmMerge = async () => {
  merging.value = true;
  
  try {
    await borrowerStore.mergeBorrowers(props.primaryBorrower.id, selectedDuplicates.value);
    
    notificationStore.showSuccess('Borrowers merged successfully');
    showConfirmation.value = false;
    emit('merge-complete');
  } catch (error) {
    notificationStore.showError('Failed to merge borrowers');
    console.error('Error merging borrowers:', error);
  } finally {
    merging.value = false;
  }
};

const useValue = (fieldKey) => {
  // In a real app, this would update the merge data
  // For now, we'll just show a notification
  notificationStore.showSuccess(`Value selected for ${fieldKey}`);
};

// Helper functions
const formatAddress = (address) => {
  if (!address) return 'Not specified';
  
  const parts = [];
  if (address.street) parts.push(address.street);
  if (address.city) parts.push(address.city);
  if (address.state) parts.push(address.state);
  if (address.postal_code) parts.push(address.postal_code);
  
  return parts.join(', ') || 'Not specified';
};

const isSameAddress = (address1, address2) => {
  if (!address1 || !address2) return false;
  
  return address1.street === address2.street &&
         address1.city === address2.city &&
         address1.state === address2.state &&
         address1.postal_code === address2.postal_code;
};

const calculateMatchScore = (borrower) => {
  let score = 0;
  let totalFields = 0;
  
  // Compare name
  if (borrower.first_name && props.primaryBorrower.first_name) {
    totalFields++;
    if (borrower.first_name.toLowerCase() === props.primaryBorrower.first_name.toLowerCase()) {
      score++;
    }
  }
  
  if (borrower.last_name && props.primaryBorrower.last_name) {
    totalFields++;
    if (borrower.last_name.toLowerCase() === props.primaryBorrower.last_name.toLowerCase()) {
      score++;
    }
  }
  
  // Compare email
  if (borrower.email && props.primaryBorrower.email) {
    totalFields++;
    if (borrower.email.toLowerCase() === props.primaryBorrower.email.toLowerCase()) {
      score++;
    }
  }
  
  // Compare phone
  if (borrower.phone && props.primaryBorrower.phone) {
    totalFields++;
    if (borrower.phone === props.primaryBorrower.phone) {
      score++;
    }
  }
  
  // Compare date of birth
  if (borrower.date_of_birth && props.primaryBorrower.date_of_birth) {
    totalFields++;
    if (borrower.date_of_birth === props.primaryBorrower.date_of_birth) {
      score++;
    }
  }
  
  // Compare address
  if (borrower.residential_address && props.primaryBorrower.residential_address) {
    if (borrower.residential_address.street && props.primaryBorrower.residential_address.street) {
      totalFields++;
      if (borrower.residential_address.street.toLowerCase() === props.primaryBorrower.residential_address.street.toLowerCase()) {
        score++;
      }
    }
    
    if (borrower.residential_address.city && props.primaryBorrower.residential_address.city) {
      totalFields++;
      if (borrower.residential_address.city.toLowerCase() === props.primaryBorrower.residential_address.city.toLowerCase()) {
        score++;
      }
    }
    
    if (borrower.residential_address.postal_code && props.primaryBorrower.residential_address.postal_code) {
      totalFields++;
      if (borrower.residential_address.postal_code === props.primaryBorrower.residential_address.postal_code) {
        score++;
      }
    }
  }
  
  // Calculate percentage
  return totalFields > 0 ? Math.round((score / totalFields) * 100) : 0;
};

const getMatchScoreColor = (score) => {
  if (score >= 80) return 'error'; // High match (red)
  if (score >= 60) return 'warning'; // Medium match (orange)
  return 'info'; // Low match (blue)
};

const formatFieldValue = (borrower, key) => {
  if (!borrower) return '';
  
  // Handle nested keys (e.g., 'residential_address.street')
  if (key.includes('.')) {
    const parts = key.split('.');
    let value = borrower;
    
    for (const part of parts) {
      if (!value || !value[part]) return 'Not specified';
      value = value[part];
    }
    
    return value || 'Not specified';
  }
  
  // Handle date fields
  if (key === 'date_of_birth' && borrower[key]) {
    return formatDate(borrower[key]);
  }
  
  return borrower[key] || 'Not specified';
};

const isDifferent = (borrower1, borrower2, key) => {
  const value1 = getNestedValue(borrower1, key);
  const value2 = getNestedValue(borrower2, key);
  
  return value1 !== value2;
};

const getNestedValue = (obj, key) => {
  if (!obj) return undefined;
  
  if (key.includes('.')) {
    const parts = key.split('.');
    let value = obj;
    
    for (const part of parts) {
      if (!value || !value[part]) return undefined;
      value = value[part];
    }
    
    return value;
  }
  
  return obj[key];
};
</script>

<style scoped>
.borrower-merge-interface {
  padding-bottom: 1rem;
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

.selected-duplicate {
  border: 2px solid var(--v-primary-base);
}
</style>
