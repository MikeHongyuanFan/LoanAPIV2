<template>
  <div v-if="loading" class="d-flex justify-center align-center" style="height: 400px;">
    <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
  </div>
  
  <div v-else-if="error" class="d-flex flex-column align-center justify-center" style="height: 400px;">
    <v-icon color="error" size="64" class="mb-4">mdi-alert-circle</v-icon>
    <h2 class="text-h5 text-center mb-4">{{ error }}</h2>
    <v-btn color="primary" @click="fetchApplication">Retry</v-btn>
  </div>

  <div v-else-if="application" class="application-detail">
    <!-- Page Header -->
    <div class="d-flex justify-space-between align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">
          Application #{{ application.reference_number }}
        </h1>
        <div class="d-flex align-center mt-2">
          <application-status-badge :status="application.status" class="mr-4" />
          <span class="text-subtitle-1 text-medium-emphasis">
            Created {{ formatDate(application.created_at) }}
          </span>
        </div>
      </div>
      <div class="d-flex">
        <v-btn
          v-if="canEditApplication"
          color="primary"
          variant="outlined"
          class="mr-2"
          prepend-icon="mdi-pencil"
          :to="`/applications/${applicationId}/edit`"
        >
          Edit
        </v-btn>
        <application-actions-menu :application="application" @action="handleAction" />
      </div>
    </div>

    <!-- Application Summary Card -->
    <v-card class="mb-6">
      <v-card-title class="bg-grey-lighten-4 py-3">
        <v-icon start class="mr-2">mdi-file-document-outline</v-icon>
        Application Summary
      </v-card-title>
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" md="6">
            <application-summary-details :application="application" />
          </v-col>
          <v-col cols="12" md="6">
            <application-financial-summary :application="application" />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Tabs Navigation -->
    <v-card>
      <v-tabs v-model="activeTab" bg-color="background">
        <v-tab value="details">
          <v-icon start>mdi-information-outline</v-icon>
          Details
        </v-tab>
        <v-tab value="borrowers">
          <v-icon start>mdi-account-outline</v-icon>
          Borrowers
        </v-tab>
        <v-tab value="documents">
          <v-icon start>mdi-file-document-multiple-outline</v-icon>
          Documents
        </v-tab>
        <v-tab value="notes">
          <v-icon start>mdi-note-text-outline</v-icon>
          Notes
        </v-tab>
        <v-tab value="timeline">
          <v-icon start>mdi-timeline-outline</v-icon>
          Timeline
        </v-tab>
        <v-tab value="repayments">
          <v-icon start>mdi-cash-multiple</v-icon>
          Repayments
        </v-tab>
        <v-tab value="fees">
          <v-icon start>mdi-currency-usd</v-icon>
          Fees
        </v-tab>
      </v-tabs>

      <v-card-text class="pa-4">
        <v-window v-model="activeTab">
          <!-- Details Tab -->
          <v-window-item value="details">
            <application-details-tab :application="application" />
          </v-window-item>

          <!-- Borrowers Tab -->
          <v-window-item value="borrowers">
            <application-borrowers-tab :application="application" />
          </v-window-item>

          <!-- Documents Tab -->
          <v-window-item value="documents">
            <application-documents-tab :application="application" />
          </v-window-item>

          <!-- Notes Tab -->
          <v-window-item value="notes">
            <application-notes-tab :application="application" />
          </v-window-item>

          <!-- Timeline Tab -->
          <v-window-item value="timeline">
            <application-timeline-tab :application="application" />
          </v-window-item>

          <!-- Repayments Tab -->
          <v-window-item value="repayments">
            <application-repayments-tab :application="application" />
          </v-window-item>

          <!-- Fees Tab -->
          <v-window-item value="fees">
            <application-fees-tab :application="application" />
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>

    <!-- Workflow Actions -->
    <application-workflow-actions 
      v-if="application.status !== 'COMPLETED' && application.status !== 'CANCELLED'"
      :application="application" 
      class="mt-6" 
      @action="handleWorkflowAction" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApplicationStore } from '@/stores/application';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { formatDate } from '@/utils/dateUtils';

// Components
import ApplicationStatusBadge from '@/components/application/ApplicationStatusBadge.vue';
import ApplicationActionsMenu from '@/components/application/ApplicationActionsMenu.vue';
import ApplicationSummaryDetails from '@/components/application/ApplicationSummaryDetails.vue';
import ApplicationFinancialSummary from '@/components/application/ApplicationFinancialSummary.vue';
import ApplicationDetailsTab from '@/components/application/ApplicationDetailsTab.vue';
import ApplicationBorrowersTab from '@/components/application/ApplicationBorrowersTab.vue';
import ApplicationDocumentsTab from '@/components/application/ApplicationDocumentsTab.vue';
import ApplicationNotesTab from '@/components/application/ApplicationNotesTab.vue';
import ApplicationTimelineTab from '@/components/application/ApplicationTimelineTab.vue';
import ApplicationRepaymentsTab from '@/components/application/ApplicationRepaymentsTab.vue';
import ApplicationFeesTab from '@/components/application/ApplicationFeesTab.vue';
import ApplicationWorkflowActions from '@/components/application/ApplicationWorkflowActions.vue';

// Store instances
const applicationStore = useApplicationStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

// Router
const route = useRoute();
const router = useRouter();

// State
const loading = ref(true);
const error = ref(null);
const application = ref(null);
const activeTab = ref('details');

// Computed
const applicationId = computed(() => route.params.id);
const canEditApplication = computed(() => {
  // Check if user has permission to edit this application
  return authStore.hasPermission('application:edit') && 
         ['DRAFT', 'PENDING', 'INFORMATION_REQUESTED'].includes(application.value?.status);
});

// Methods
const fetchApplication = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    application.value = await applicationStore.fetchApplicationById(applicationId.value);
  } catch (err) {
    console.error('Error fetching application:', err);
    error.value = 'Failed to load application details. Please try again.';
  } finally {
    loading.value = false;
  }
};

const handleAction = async (action, data) => {
  switch (action) {
    case 'delete':
      try {
        await applicationStore.deleteApplication(applicationId.value);
        notificationStore.showSuccess('Application deleted successfully');
        router.push('/applications');
      } catch (err) {
        notificationStore.showError('Failed to delete application');
      }
      break;
      
    case 'duplicate':
      try {
        const newApplicationId = await applicationStore.duplicateApplication(applicationId.value);
        notificationStore.showSuccess('Application duplicated successfully');
        router.push(`/applications/${newApplicationId}`);
      } catch (err) {
        notificationStore.showError('Failed to duplicate application');
      }
      break;
      
    case 'export':
      try {
        await applicationStore.exportApplication(applicationId.value, data.format);
        notificationStore.showSuccess(`Application exported as ${data.format.toUpperCase()}`);
      } catch (err) {
        notificationStore.showError('Failed to export application');
      }
      break;
      
    default:
      console.warn('Unknown action:', action);
  }
};

const handleWorkflowAction = async (action) => {
  try {
    await applicationStore.updateApplicationStatus(applicationId.value, action.targetStatus, action.comment);
    notificationStore.showSuccess(`Application status updated to ${action.label}`);
    fetchApplication(); // Refresh application data
  } catch (err) {
    notificationStore.showError(`Failed to update application status: ${err.message}`);
  }
};

// Lifecycle hooks
onMounted(() => {
  fetchApplication();
  
  // Set active tab from query parameter if available
  if (route.query.tab && ['details', 'borrowers', 'documents', 'notes', 'timeline', 'repayments', 'fees'].includes(route.query.tab)) {
    activeTab.value = route.query.tab;
  }
});
</script>

<style scoped>
.application-detail {
  padding-bottom: 2rem;
}
</style>
