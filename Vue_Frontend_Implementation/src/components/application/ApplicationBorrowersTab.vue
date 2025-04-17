<template>
  <div class="application-borrowers-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Borrowers</h3>
      <v-btn
        v-if="canAddBorrower"
        color="primary"
        prepend-icon="mdi-account-plus"
        @click="showAddBorrowerDialog = true"
      >
        Add Borrower
      </v-btn>
    </div>

    <div v-if="loading" class="d-flex justify-center my-8">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="!application.borrowers || application.borrowers.length === 0" class="text-center my-8">
      <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-account-group</v-icon>
      <h3 class="text-h6 mb-2">No Borrowers</h3>
      <p class="text-body-1 text-medium-emphasis mb-4">
        This application doesn't have any borrowers yet.
      </p>
      <v-btn
        v-if="canAddBorrower"
        color="primary"
        prepend-icon="mdi-account-plus"
        @click="showAddBorrowerDialog = true"
      >
        Add Borrower
      </v-btn>
    </div>

    <div v-else>
      <!-- Primary Borrower Card -->
      <v-card v-if="primaryBorrower" class="mb-4 primary-borrower-card">
        <v-card-title class="bg-primary text-white d-flex justify-space-between align-center py-3">
          <div class="d-flex align-center">
            <v-icon start class="mr-2">mdi-account-star</v-icon>
            Primary Borrower
          </div>
          <v-chip color="white" text-color="primary" size="small">Primary</v-chip>
        </v-card-title>
        
        <v-card-text class="pa-4">
          <borrower-detail-card 
            :borrower="primaryBorrower" 
            :application-id="application.id"
            @edit="editBorrower"
            @remove="confirmRemoveBorrower"
            @make-primary="makePrimaryBorrower"
          />
        </v-card-text>
      </v-card>

      <!-- Co-Borrowers -->
      <h3 v-if="coBorrowers.length > 0" class="text-subtitle-1 font-weight-medium mb-3">Co-Borrowers</h3>
      
      <v-row>
        <v-col 
          v-for="borrower in coBorrowers" 
          :key="borrower.id" 
          cols="12" 
          md="6"
        >
          <v-card>
            <v-card-text class="pa-4">
              <borrower-detail-card 
                :borrower="borrower" 
                :application-id="application.id"
                @edit="editBorrower"
                @remove="confirmRemoveBorrower"
                @make-primary="makePrimaryBorrower"
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Add Borrower Dialog -->
    <v-dialog v-model="showAddBorrowerDialog" max-width="800px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-account-plus</v-icon>
          Add Borrower
        </v-card-title>
        <v-card-text class="pa-4">
          <v-tabs v-model="addBorrowerTab">
            <v-tab value="existing">Existing Borrower</v-tab>
            <v-tab value="new">New Borrower</v-tab>
          </v-tabs>
          
          <v-window v-model="addBorrowerTab" class="mt-4">
            <v-window-item value="existing">
              <v-autocomplete
                v-model="selectedExistingBorrower"
                :items="availableBorrowers"
                item-title="full_name"
                item-value="id"
                label="Search Borrowers"
                placeholder="Start typing to search borrowers"
                return-object
                clearable
                :loading="searchingBorrowers"
                @update:search="searchBorrowers"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props">
                    <template v-slot:prepend>
                      <v-avatar size="32">
                        <v-img v-if="item.raw.avatar" :src="item.raw.avatar"></v-img>
                        <v-icon v-else>mdi-account</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>{{ item.raw.full_name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.raw.email }}</v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-autocomplete>
              
              <div v-if="selectedExistingBorrower" class="mt-4">
                <v-card variant="outlined">
                  <v-card-text>
                    <borrower-detail-card :borrower="selectedExistingBorrower" :show-actions="false" />
                  </v-card-text>
                </v-card>
              </div>
              
              <v-checkbox
                v-model="makePrimary"
                label="Make this the primary borrower"
                :disabled="!!primaryBorrower"
                hint="Only one borrower can be primary"
                persistent-hint
              ></v-checkbox>
            </v-window-item>
            
            <v-window-item value="new">
              <borrower-form ref="borrowerForm" />
              
              <v-checkbox
                v-model="makePrimary"
                label="Make this the primary borrower"
                :disabled="!!primaryBorrower"
                hint="Only one borrower can be primary"
                persistent-hint
              ></v-checkbox>
            </v-window-item>
          </v-window>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showAddBorrowerDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="addBorrower">
            Add Borrower
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Edit Borrower Dialog -->
    <v-dialog v-model="showEditBorrowerDialog" max-width="800px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-account-edit</v-icon>
          Edit Borrower
        </v-card-title>
        <v-card-text class="pa-4">
          <borrower-form 
            ref="editBorrowerForm" 
            :borrower="borrowerToEdit" 
            :edit-mode="true" 
          />
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showEditBorrowerDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="updateBorrower">
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Confirm Remove Dialog -->
    <v-dialog v-model="showRemoveDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Remove Borrower</v-card-title>
        <v-card-text>
          Are you sure you want to remove {{ borrowerToRemove?.full_name }} from this application?
          <div v-if="borrowerToRemove?.is_primary" class="mt-2 text-error">
            <v-icon start color="error">mdi-alert</v-icon>
            This is the primary borrower. Removing them will require setting a new primary borrower.
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showRemoveDialog = false">Cancel</v-btn>
          <v-btn color="error" variant="text" @click="removeBorrower">Remove</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useApplicationStore } from '@/stores/application';
import { useBorrowerStore } from '@/stores/borrower';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import BorrowerDetailCard from '@/components/borrower/BorrowerDetailCard.vue';
import BorrowerForm from '@/components/borrower/BorrowerForm.vue';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

// Stores
const applicationStore = useApplicationStore();
const borrowerStore = useBorrowerStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

// State
const loading = ref(false);
const showAddBorrowerDialog = ref(false);
const showEditBorrowerDialog = ref(false);
const showRemoveDialog = ref(false);
const addBorrowerTab = ref('existing');
const selectedExistingBorrower = ref(null);
const availableBorrowers = ref([]);
const searchingBorrowers = ref(false);
const makePrimary = ref(false);
const borrowerToEdit = ref(null);
const borrowerToRemove = ref(null);

// Computed
const primaryBorrower = computed(() => {
  if (!props.application.borrowers || props.application.borrowers.length === 0) {
    return null;
  }
  
  return props.application.borrowers.find(b => b.is_primary);
});

const coBorrowers = computed(() => {
  if (!props.application.borrowers || props.application.borrowers.length === 0) {
    return [];
  }
  
  return props.application.borrowers.filter(b => !b.is_primary);
});

const canAddBorrower = computed(() => {
  return authStore.hasPermission('application:edit') && 
         ['DRAFT', 'PENDING', 'INFORMATION_REQUESTED'].includes(props.application.status);
});

// Methods
const searchBorrowers = async (query) => {
  if (!query || query.length < 2) return;
  
  searchingBorrowers.value = true;
  try {
    const result = await borrowerStore.searchBorrowers(query);
    
    // Filter out borrowers already in the application
    const existingBorrowerIds = props.application.borrowers.map(b => b.id);
    availableBorrowers.value = result.filter(b => !existingBorrowerIds.includes(b.id));
  } catch (error) {
    notificationStore.showError('Failed to search borrowers');
    console.error('Error searching borrowers:', error);
  } finally {
    searchingBorrowers.value = false;
  }
};

const addBorrower = async () => {
  try {
    if (addBorrowerTab.value === 'existing') {
      if (!selectedExistingBorrower.value) {
        notificationStore.showError('Please select a borrower');
        return;
      }
      
      await applicationStore.addBorrowerToApplication(
        props.application.id, 
        selectedExistingBorrower.value.id,
        makePrimary.value
      );
      
      notificationStore.showSuccess('Borrower added to application');
    } else {
      // New borrower
      const borrowerForm = document.querySelector('#borrowerForm');
      if (!borrowerForm) {
        notificationStore.showError('Borrower form not found');
        return;
      }
      
      const isValid = await borrowerForm.__vueParentInstance.exposed.validate();
      if (!isValid) {
        notificationStore.showError('Please fix the errors in the form');
        return;
      }
      
      const borrowerData = borrowerForm.__vueParentInstance.exposed.getBorrowerData();
      const newBorrower = await borrowerStore.createBorrower(borrowerData);
      
      await applicationStore.addBorrowerToApplication(
        props.application.id, 
        newBorrower.id,
        makePrimary.value
      );
      
      notificationStore.showSuccess('New borrower added to application');
    }
    
    // Reset form and close dialog
    showAddBorrowerDialog.value = false;
    selectedExistingBorrower.value = null;
    makePrimary.value = false;
    addBorrowerTab.value = 'existing';
    
    // Refresh application data
    await applicationStore.fetchApplicationById(props.application.id);
  } catch (error) {
    notificationStore.showError('Failed to add borrower to application');
    console.error('Error adding borrower:', error);
  }
};

const editBorrower = (borrower) => {
  borrowerToEdit.value = borrower;
  showEditBorrowerDialog.value = true;
};

const updateBorrower = async () => {
  try {
    const borrowerForm = document.querySelector('#editBorrowerForm');
    if (!borrowerForm) {
      notificationStore.showError('Borrower form not found');
      return;
    }
    
    const isValid = await borrowerForm.__vueParentInstance.exposed.validate();
    if (!isValid) {
      notificationStore.showError('Please fix the errors in the form');
      return;
    }
    
    const borrowerData = borrowerForm.__vueParentInstance.exposed.getBorrowerData();
    await borrowerStore.updateBorrower(borrowerToEdit.value.id, borrowerData);
    
    notificationStore.showSuccess('Borrower updated successfully');
    
    // Reset form and close dialog
    showEditBorrowerDialog.value = false;
    borrowerToEdit.value = null;
    
    // Refresh application data
    await applicationStore.fetchApplicationById(props.application.id);
  } catch (error) {
    notificationStore.showError('Failed to update borrower');
    console.error('Error updating borrower:', error);
  }
};

const confirmRemoveBorrower = (borrower) => {
  borrowerToRemove.value = borrower;
  showRemoveDialog.value = true;
};

const removeBorrower = async () => {
  try {
    await applicationStore.removeBorrowerFromApplication(
      props.application.id, 
      borrowerToRemove.value.id
    );
    
    notificationStore.showSuccess('Borrower removed from application');
    
    // Reset and close dialog
    showRemoveDialog.value = false;
    borrowerToRemove.value = null;
    
    // Refresh application data
    await applicationStore.fetchApplicationById(props.application.id);
  } catch (error) {
    notificationStore.showError('Failed to remove borrower from application');
    console.error('Error removing borrower:', error);
  }
};

const makePrimaryBorrower = async (borrower) => {
  try {
    await applicationStore.updateApplicationBorrower(
      props.application.id,
      borrower.id,
      { is_primary: true }
    );
    
    notificationStore.showSuccess(`${borrower.full_name} is now the primary borrower`);
    
    // Refresh application data
    await applicationStore.fetchApplicationById(props.application.id);
  } catch (error) {
    notificationStore.showError('Failed to update primary borrower');
    console.error('Error updating primary borrower:', error);
  }
};

// Lifecycle hooks
onMounted(async () => {
  // Load initial borrowers for search
  try {
    const result = await borrowerStore.getBorrowers({ limit: 10 });
    
    // Filter out borrowers already in the application
    const existingBorrowerIds = props.application.borrowers.map(b => b.id);
    availableBorrowers.value = result.items.filter(b => !existingBorrowerIds.includes(b.id));
  } catch (error) {
    console.error('Error loading initial borrowers:', error);
  }
});
</script>

<style scoped>
.primary-borrower-card {
  border: 2px solid var(--v-primary-base);
}

.borrower-card {
  height: 100%;
}
</style>
