<template>
  <div v-if="loading" class="d-flex justify-center align-center" style="height: 400px;">
    <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
  </div>
  
  <div v-else-if="error" class="d-flex flex-column align-center justify-center" style="height: 400px;">
    <v-icon color="error" size="64" class="mb-4">mdi-alert-circle</v-icon>
    <h2 class="text-h5 text-center mb-4">{{ error }}</h2>
    <v-btn color="primary" @click="fetchBorrower">Retry</v-btn>
  </div>

  <div v-else-if="borrower" class="borrower-detail">
    <!-- Page Header -->
    <div class="d-flex justify-space-between align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">
          {{ borrower.full_name }}
        </h1>
        <div class="d-flex align-center mt-2">
          <v-chip
            :color="borrower.is_active ? 'success' : 'grey'"
            size="small"
            class="mr-4"
          >
            {{ borrower.is_active ? 'Active' : 'Inactive' }}
          </v-chip>
          <span class="text-subtitle-1 text-medium-emphasis">
            Customer since {{ formatDate(borrower.created_at) }}
          </span>
        </div>
      </div>
      <div class="d-flex">
        <v-btn
          v-if="canEditBorrower"
          color="primary"
          variant="outlined"
          class="mr-2"
          prepend-icon="mdi-pencil"
          :to="`/borrowers/${borrowerId}/edit`"
        >
          Edit
        </v-btn>
        <v-menu location="bottom end">
          <template v-slot:activator="{ props }">
            <v-btn
              color="primary"
              variant="text"
              v-bind="props"
              icon="mdi-dots-vertical"
            ></v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="(action, index) in availableActions"
              :key="index"
              :value="action.value"
              @click="handleAction(action.value)"
            >
              <template v-slot:prepend>
                <v-icon :icon="action.icon"></v-icon>
              </template>
              <v-list-item-title>{{ action.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>

    <!-- Borrower Summary Card -->
    <v-card class="mb-6">
      <v-card-title class="bg-grey-lighten-4 py-3">
        <v-icon start class="mr-2">mdi-account-outline</v-icon>
        Borrower Summary
      </v-card-title>
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" md="6">
            <borrower-personal-details :borrower="borrower" />
          </v-col>
          <v-col cols="12" md="6">
            <borrower-contact-details :borrower="borrower" />
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
        <v-tab value="applications">
          <v-icon start>mdi-file-document-multiple-outline</v-icon>
          Applications
        </v-tab>
        <v-tab value="guarantors">
          <v-icon start>mdi-account-multiple-outline</v-icon>
          Guarantors
        </v-tab>
        <v-tab value="documents">
          <v-icon start>mdi-file-outline</v-icon>
          Documents
        </v-tab>
        <v-tab value="history">
          <v-icon start>mdi-history</v-icon>
          History
        </v-tab>
      </v-tabs>

      <v-card-text class="pa-4">
        <v-window v-model="activeTab">
          <!-- Details Tab -->
          <v-window-item value="details">
            <borrower-details-tab :borrower="borrower" />
          </v-window-item>

          <!-- Applications Tab -->
          <v-window-item value="applications">
            <borrower-applications-tab :borrower="borrower" />
          </v-window-item>

          <!-- Guarantors Tab -->
          <v-window-item value="guarantors">
            <borrower-guarantors-tab :borrower="borrower" />
          </v-window-item>

          <!-- Documents Tab -->
          <v-window-item value="documents">
            <borrower-documents-tab :borrower="borrower" />
          </v-window-item>

          <!-- History Tab -->
          <v-window-item value="history">
            <borrower-history-tab :borrower="borrower" />
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>

    <!-- Duplicate Check Section -->
    <v-card v-if="canManageDuplicates && possibleDuplicates.length > 0" class="mt-6">
      <v-card-title class="bg-warning py-3">
        <v-icon start class="mr-2">mdi-account-alert</v-icon>
        Possible Duplicate Borrowers
      </v-card-title>
      <v-card-text class="pa-4">
        <p class="text-body-1 mb-4">
          We've identified {{ possibleDuplicates.length }} possible duplicate records for this borrower.
        </p>
        <v-btn
          color="primary"
          prepend-icon="mdi-account-multiple-check"
          @click="showMergeDialog = true"
        >
          Manage Duplicates
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- Merge Dialog -->
    <v-dialog v-model="showMergeDialog" max-width="900px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-account-multiple-check</v-icon>
          Manage Duplicate Borrowers
        </v-card-title>
        <v-card-text class="pa-4">
          <borrower-merge-interface
            :primary-borrower="borrower"
            :duplicate-borrowers="possibleDuplicates"
            @merge-complete="handleMergeComplete"
          />
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Delete Borrower</v-card-title>
        <v-card-text>
          Are you sure you want to delete this borrower? This action cannot be undone.
          <div v-if="borrowerApplicationsCount > 0" class="mt-2 text-error">
            <v-icon start color="error">mdi-alert</v-icon>
            This borrower has {{ borrowerApplicationsCount }} active applications. Deleting this borrower will affect these applications.
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" variant="text" @click="confirmDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useBorrowerStore } from '@/stores/borrowerStore';
import { useAuthStore } from '@/stores/authStore';
import { useNotificationStore } from '@/stores/notificationStore';
import { formatDate } from '@/utils/dateUtils';

// Components
import BorrowerPersonalDetails from '@/components/borrower/BorrowerPersonalDetails.vue';
import BorrowerContactDetails from '@/components/borrower/BorrowerContactDetails.vue';
import BorrowerDetailsTab from '@/components/borrower/BorrowerDetailsTab.vue';
import BorrowerApplicationsTab from '@/components/borrower/BorrowerApplicationsTab.vue';
import BorrowerGuarantorsTab from '@/components/borrower/BorrowerGuarantorsTab.vue';
import BorrowerDocumentsTab from '@/components/borrower/BorrowerDocumentsTab.vue';
import BorrowerHistoryTab from '@/components/borrower/BorrowerHistoryTab.vue';
import BorrowerMergeInterface from '@/components/borrower/BorrowerMergeInterface.vue';

// Store instances
const borrowerStore = useBorrowerStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

// Router
const route = useRoute();
const router = useRouter();

// State
const loading = ref(true);
const error = ref(null);
const borrower = ref(null);
const activeTab = ref('details');
const possibleDuplicates = ref([]);
const showMergeDialog = ref(false);
const showDeleteDialog = ref(false);
const borrowerApplicationsCount = ref(0);

// Computed
const borrowerId = computed(() => route.params.id);
const canEditBorrower = computed(() => {
  return authStore.hasPermission('borrower:edit');
});
const canManageDuplicates = computed(() => {
  return authStore.hasPermission('borrower:merge');
});

// Available actions for the borrower
const availableActions = computed(() => {
  const actions = [
    {
      title: 'Create Application',
      value: 'create-application',
      icon: 'mdi-file-plus'
    }
  ];
  
  if (authStore.hasPermission('borrower:delete')) {
    actions.push({
      title: 'Delete Borrower',
      value: 'delete',
      icon: 'mdi-delete'
    });
  }
  
  return actions;
});

// Methods
const fetchBorrower = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    borrower.value = await borrowerStore.getBorrower(borrowerId.value);
    await fetchBorrowerApplications();
    await checkForDuplicates();
  } catch (err) {
    console.error('Error fetching borrower:', err);
    error.value = 'Failed to load borrower details. Please try again.';
  } finally {
    loading.value = false;
  }
};

const fetchBorrowerApplications = async () => {
  try {
    const applications = await borrowerStore.getBorrowerApplications(borrowerId.value);
    borrowerApplicationsCount.value = applications.length;
  } catch (err) {
    console.error('Error fetching borrower applications:', err);
  }
};

const checkForDuplicates = async () => {
  if (!canManageDuplicates.value || !borrower.value) return;
  
  try {
    const duplicates = await borrowerStore.checkDuplicates({
      first_name: borrower.value.first_name,
      last_name: borrower.value.last_name,
      email: borrower.value.email,
      phone: borrower.value.phone,
      date_of_birth: borrower.value.date_of_birth
    });
    
    // Filter out the current borrower from duplicates
    possibleDuplicates.value = duplicates.filter(dup => dup.id !== borrower.value.id);
  } catch (err) {
    console.error('Error checking for duplicates:', err);
  }
};

const handleAction = (action) => {
  switch (action) {
    case 'create-application':
      router.push({
        name: 'ApplicationCreate',
        query: { borrower_id: borrowerId.value }
      });
      break;
      
    case 'delete':
      showDeleteDialog.value = true;
      break;
      
    default:
      console.warn('Unknown action:', action);
  }
};

const confirmDelete = async () => {
  try {
    await borrowerStore.deleteBorrower(borrowerId.value);
    notificationStore.showSuccess('Borrower deleted successfully');
    router.push('/borrowers');
  } catch (err) {
    notificationStore.showError('Failed to delete borrower');
  } finally {
    showDeleteDialog.value = false;
  }
};

const handleMergeComplete = async () => {
  showMergeDialog.value = false;
  notificationStore.showSuccess('Borrowers merged successfully');
  await fetchBorrower();
};

// Lifecycle hooks
onMounted(() => {
  fetchBorrower();
  
  // Set active tab from query parameter if available
  if (route.query.tab && ['details', 'applications', 'guarantors', 'documents', 'history'].includes(route.query.tab)) {
    activeTab.value = route.query.tab;
  }
});
</script>

<style scoped>
.borrower-detail {
  padding-bottom: 2rem;
}
</style>
