<template>
  <div class="borrower-applications-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Applications</h3>
      <v-btn
        color="primary"
        prepend-icon="mdi-file-plus"
        :to="`/applications/create?borrower_id=${borrower.id}`"
      >
        New Application
      </v-btn>
    </div>

    <div v-if="loading" class="d-flex justify-center my-8">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="!applications.length" class="text-center my-8">
      <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-file-document-outline</v-icon>
      <h3 class="text-h6 mb-2">No Applications</h3>
      <p class="text-body-1 text-medium-emphasis mb-4">
        This borrower doesn't have any applications yet.
      </p>
      <v-btn
        color="primary"
        prepend-icon="mdi-file-plus"
        :to="`/applications/create?borrower_id=${borrower.id}`"
      >
        Create Application
      </v-btn>
    </div>

    <div v-else>
      <!-- Applications Table -->
      <v-card>
        <v-data-table
          :headers="headers"
          :items="applications"
          :items-per-page="5"
          :footer-props="{
            'items-per-page-options': [5, 10, 15, -1],
            'items-per-page-text': 'Applications per page'
          }"
          class="elevation-1"
        >
          <!-- Reference Number Column -->
          <template v-slot:item.reference_number="{ item }">
            <router-link 
              :to="`/applications/${item.id}`"
              class="text-decoration-none font-weight-medium"
            >
              {{ item.reference_number }}
            </router-link>
          </template>

          <!-- Status Column -->
          <template v-slot:item.status="{ item }">
            <application-status-badge :status="item.status" />
          </template>

          <!-- Product Column -->
          <template v-slot:item.product="{ item }">
            {{ item.product?.name || 'N/A' }}
          </template>

          <!-- Loan Amount Column -->
          <template v-slot:item.loan_amount="{ item }">
            {{ formatCurrency(item.loan_amount) }}
          </template>

          <!-- Created Date Column -->
          <template v-slot:item.created_at="{ item }">
            {{ formatDate(item.created_at) }}
          </template>

          <!-- Actions Column -->
          <template v-slot:item.actions="{ item }">
            <div class="d-flex">
              <v-tooltip location="top" text="View">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-eye"
                    size="small"
                    variant="text"
                    :to="`/applications/${item.id}`"
                  ></v-btn>
                </template>
              </v-tooltip>

              <v-tooltip location="top" text="Edit" v-if="canEditApplication(item)">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-pencil"
                    size="small"
                    variant="text"
                    :to="`/applications/${item.id}/edit`"
                  ></v-btn>
                </template>
              </v-tooltip>

              <v-tooltip location="top" text="Duplicate">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-content-duplicate"
                    size="small"
                    variant="text"
                    @click="duplicateApplication(item)"
                  ></v-btn>
                </template>
              </v-tooltip>
            </div>
          </template>
        </v-data-table>
      </v-card>

      <!-- Application Summary -->
      <div class="mt-6">
        <h3 class="text-subtitle-1 font-weight-medium mb-3">Application Summary</h3>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-card class="summary-card">
              <v-card-text class="text-center">
                <div class="text-overline">Total Applications</div>
                <div class="text-h4 font-weight-bold">{{ applications.length }}</div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card class="summary-card">
              <v-card-text class="text-center">
                <div class="text-overline">Active Applications</div>
                <div class="text-h4 font-weight-bold">{{ activeApplicationsCount }}</div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card class="summary-card">
              <v-card-text class="text-center">
                <div class="text-overline">Total Loan Amount</div>
                <div class="text-h4 font-weight-bold">{{ formatCurrency(totalLoanAmount) }}</div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card class="summary-card">
              <v-card-text class="text-center">
                <div class="text-overline">Latest Application</div>
                <div class="text-h4 font-weight-bold">{{ latestApplicationDate }}</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useBorrowerStore } from '@/stores/borrowerStore';
import { useApplicationStore } from '@/stores/applicationStore';
import { useAuthStore } from '@/stores/authStore';
import { useNotificationStore } from '@/stores/notificationStore';
import { formatDate } from '@/utils/dateUtils';
import ApplicationStatusBadge from '@/components/application/ApplicationStatusBadge.vue';

const props = defineProps({
  borrower: {
    type: Object,
    required: true
  }
});

// Stores
const borrowerStore = useBorrowerStore();
const applicationStore = useApplicationStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

// Router
const router = useRouter();

// State
const loading = ref(true);
const applications = ref([]);

// Table headers
const headers = [
  { title: 'Reference', key: 'reference_number', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Product', key: 'product', sortable: true },
  { title: 'Loan Amount', key: 'loan_amount', sortable: true },
  { title: 'Created Date', key: 'created_at', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
];

// Computed properties
const activeApplicationsCount = computed(() => {
  return applications.value.filter(app => 
    !['COMPLETED', 'CANCELLED', 'REJECTED', 'WITHDRAWN'].includes(app.status)
  ).length;
});

const totalLoanAmount = computed(() => {
  return applications.value.reduce((sum, app) => sum + (app.loan_amount || 0), 0);
});

const latestApplicationDate = computed(() => {
  if (applications.value.length === 0) return 'N/A';
  
  const dates = applications.value.map(app => new Date(app.created_at));
  const latestDate = new Date(Math.max(...dates));
  
  return formatDate(latestDate);
});

// Methods
const fetchApplications = async () => {
  loading.value = true;
  
  try {
    applications.value = await borrowerStore.getBorrowerApplications(props.borrower.id);
  } catch (error) {
    console.error('Error fetching borrower applications:', error);
    notificationStore.showError('Failed to load applications');
  } finally {
    loading.value = false;
  }
};

const canEditApplication = (application) => {
  return authStore.hasPermission('application:edit') && 
         ['DRAFT', 'PENDING', 'INFORMATION_REQUESTED'].includes(application.status);
};

const duplicateApplication = async (application) => {
  try {
    const newApplicationId = await applicationStore.duplicateApplication(application.id);
    notificationStore.showSuccess('Application duplicated successfully');
    router.push(`/applications/${newApplicationId}`);
  } catch (error) {
    notificationStore.showError('Failed to duplicate application');
  }
};

const formatCurrency = (value) => {
  if (value === null || value === undefined) return 'N/A';
  
  return new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
};

// Lifecycle hooks
onMounted(() => {
  fetchApplications();
});
</script>

<style scoped>
.borrower-applications-tab {
  padding-bottom: 1rem;
}

.summary-card {
  height: 100%;
  border-left: 4px solid var(--v-primary-base);
}
</style>
