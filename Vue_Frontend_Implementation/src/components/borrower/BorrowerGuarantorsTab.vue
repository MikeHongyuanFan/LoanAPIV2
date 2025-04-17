<template>
  <div class="borrower-guarantors-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Guarantors</h3>
      <v-btn
        v-if="canAddGuarantor"
        color="primary"
        prepend-icon="mdi-account-plus"
        @click="showAddGuarantorDialog = true"
      >
        Add Guarantor
      </v-btn>
    </div>

    <div v-if="loading" class="d-flex justify-center my-8">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="!guarantors.length" class="text-center my-8">
      <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-account-group</v-icon>
      <h3 class="text-h6 mb-2">No Guarantors</h3>
      <p class="text-body-1 text-medium-emphasis mb-4">
        This borrower doesn't have any guarantors yet.
      </p>
      <v-btn
        v-if="canAddGuarantor"
        color="primary"
        prepend-icon="mdi-account-plus"
        @click="showAddGuarantorDialog = true"
      >
        Add Guarantor
      </v-btn>
    </div>

    <div v-else>
      <v-row>
        <v-col 
          v-for="guarantor in guarantors" 
          :key="guarantor.id" 
          cols="12" 
          md="6"
        >
          <v-card>
            <v-card-text class="pa-4">
              <div class="d-flex justify-space-between">
                <div class="d-flex align-center">
                  <v-avatar color="primary" class="mr-3">
                    <v-icon color="white">mdi-account</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-h6">{{ guarantor.full_name }}</div>
                    <div class="text-subtitle-2 text-medium-emphasis">
                      {{ formatRelationship(guarantor.relationship) }}
                    </div>
                  </div>
                </div>
                <div>
                  <v-menu location="bottom end">
                    <template v-slot:activator="{ props }">
                      <v-btn
                        icon="mdi-dots-vertical"
                        variant="text"
                        v-bind="props"
                      ></v-btn>
                    </template>
                    <v-list>
                      <v-list-item
                        @click="editGuarantor(guarantor)"
                      >
                        <template v-slot:prepend>
                          <v-icon>mdi-pencil</v-icon>
                        </template>
                        <v-list-item-title>Edit</v-list-item-title>
                      </v-list-item>
                      <v-list-item
                        @click="confirmRemoveGuarantor(guarantor)"
                      >
                        <template v-slot:prepend>
                          <v-icon>mdi-delete</v-icon>
                        </template>
                        <v-list-item-title>Remove</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </div>
              </div>

              <v-divider class="my-3"></v-divider>

              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-label">Email</div>
                  <div class="detail-value">
                    <a :href="`mailto:${guarantor.email}`" class="text-decoration-none">
                      {{ guarantor.email }}
                    </a>
                  </div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Phone</div>
                  <div class="detail-value">
                    <a :href="`tel:${guarantor.phone}`" class="text-decoration-none">
                      {{ guarantor.phone }}
                    </a>
                  </div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Date of Birth</div>
                  <div class="detail-value">{{ formatDate(guarantor.date_of_birth) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Address</div>
                  <div class="detail-value">{{ formatAddress(guarantor.address) }}</div>
                </div>
              </div>

              <v-divider class="my-3"></v-divider>

              <div class="detail-item">
                <div class="detail-label">Applications</div>
                <div class="detail-value">
                  <div v-if="guarantor.applications && guarantor.applications.length > 0">
                    <v-chip
                      v-for="app in guarantor.applications"
                      :key="app.id"
                      size="small"
                      class="mr-1 mb-1"
                      :to="`/applications/${app.id}`"
                    >
                      {{ app.reference_number }}
                    </v-chip>
                  </div>
                  <div v-else class="text-medium-emphasis">
                    No applications
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Add Guarantor Dialog -->
    <v-dialog v-model="showAddGuarantorDialog" max-width="800px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-account-plus</v-icon>
          Add Guarantor
        </v-card-title>
        <v-card-text class="pa-4">
          <v-tabs v-model="addGuarantorTab">
            <v-tab value="existing">Existing Borrower</v-tab>
            <v-tab value="new">New Guarantor</v-tab>
          </v-tabs>
          
          <v-window v-model="addGuarantorTab" class="mt-4">
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
              
              <v-select
                v-model="guarantorRelationship"
                :items="relationshipTypes"
                label="Relationship to Borrower"
                class="mt-4"
                :rules="[v => !!v || 'Relationship is required']"
              ></v-select>
              
              <div v-if="selectedExistingBorrower" class="mt-4">
                <v-card variant="outlined">
                  <v-card-text>
                    <div class="d-flex align-center">
                      <v-avatar color="primary" class="mr-3">
                        <v-img v-if="selectedExistingBorrower.avatar" :src="selectedExistingBorrower.avatar"></v-img>
                        <v-icon v-else color="white">mdi-account</v-icon>
                      </v-avatar>
                      <div>
                        <div class="text-h6">{{ selectedExistingBorrower.full_name }}</div>
                        <div class="text-subtitle-2">{{ selectedExistingBorrower.email }}</div>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </v-window-item>
            
            <v-window-item value="new">
              <v-form ref="guarantorForm">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.first_name"
                      label="First Name"
                      required
                      :rules="[v => !!v || 'First name is required']"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.last_name"
                      label="Last Name"
                      required
                      :rules="[v => !!v || 'Last name is required']"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.email"
                      label="Email"
                      type="email"
                      required
                      :rules="[
                        v => !!v || 'Email is required',
                        v => /.+@.+\..+/.test(v) || 'Email must be valid'
                      ]"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.phone"
                      label="Phone"
                      required
                      :rules="[v => !!v || 'Phone is required']"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.date_of_birth"
                      label="Date of Birth"
                      type="date"
                      required
                      :rules="[v => !!v || 'Date of birth is required']"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="newGuarantor.relationship"
                      :items="relationshipTypes"
                      label="Relationship to Borrower"
                      required
                      :rules="[v => !!v || 'Relationship is required']"
                    ></v-select>
                  </v-col>
                  
                  <v-col cols="12">
                    <v-text-field
                      v-model="newGuarantor.address.street"
                      label="Street Address"
                      required
                      :rules="[v => !!v || 'Street address is required']"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.address.city"
                      label="City"
                      required
                      :rules="[v => !!v || 'City is required']"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.address.state"
                      label="State/Province"
                      required
                      :rules="[v => !!v || 'State is required']"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.address.postal_code"
                      label="Postal Code"
                      required
                      :rules="[v => !!v || 'Postal code is required']"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newGuarantor.address.country"
                      label="Country"
                      required
                      :rules="[v => !!v || 'Country is required']"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-form>
            </v-window-item>
          </v-window>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showAddGuarantorDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="addGuarantor" :loading="adding">
            Add Guarantor
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Edit Guarantor Dialog -->
    <v-dialog v-model="showEditGuarantorDialog" max-width="800px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-account-edit</v-icon>
          Edit Guarantor
        </v-card-title>
        <v-card-text class="pa-4">
          <v-form ref="editGuarantorForm">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.first_name"
                  label="First Name"
                  required
                  :rules="[v => !!v || 'First name is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.last_name"
                  label="Last Name"
                  required
                  :rules="[v => !!v || 'Last name is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.email"
                  label="Email"
                  type="email"
                  required
                  :rules="[
                    v => !!v || 'Email is required',
                    v => /.+@.+\..+/.test(v) || 'Email must be valid'
                  ]"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.phone"
                  label="Phone"
                  required
                  :rules="[v => !!v || 'Phone is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.date_of_birth"
                  label="Date of Birth"
                  type="date"
                  required
                  :rules="[v => !!v || 'Date of birth is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="editingGuarantor.relationship"
                  :items="relationshipTypes"
                  label="Relationship to Borrower"
                  required
                  :rules="[v => !!v || 'Relationship is required']"
                ></v-select>
              </v-col>
              
              <v-col cols="12">
                <v-text-field
                  v-model="editingGuarantor.address.street"
                  label="Street Address"
                  required
                  :rules="[v => !!v || 'Street address is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.address.city"
                  label="City"
                  required
                  :rules="[v => !!v || 'City is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.address.state"
                  label="State/Province"
                  required
                  :rules="[v => !!v || 'State is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.address.postal_code"
                  label="Postal Code"
                  required
                  :rules="[v => !!v || 'Postal code is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editingGuarantor.address.country"
                  label="Country"
                  required
                  :rules="[v => !!v || 'Country is required']"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showEditGuarantorDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="updateGuarantor" :loading="updating">
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Confirm Remove Dialog -->
    <v-dialog v-model="showRemoveDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Remove Guarantor</v-card-title>
        <v-card-text>
          Are you sure you want to remove {{ guarantorToRemove?.full_name }} as a guarantor?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showRemoveDialog = false">Cancel</v-btn>
          <v-btn color="error" variant="text" @click="removeGuarantor" :loading="removing">Remove</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useBorrowerStore } from '@/stores/borrowerStore';
import { useAuthStore } from '@/stores/authStore';
import { useNotificationStore } from '@/stores/notificationStore';
import { formatDate } from '@/utils/dateUtils';

const props = defineProps({
  borrower: {
    type: Object,
    required: true
  }
});

// Stores
const borrowerStore = useBorrowerStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

// State
const loading = ref(true);
const guarantors = ref([]);
const showAddGuarantorDialog = ref(false);
const showEditGuarantorDialog = ref(false);
const showRemoveDialog = ref(false);
const addGuarantorTab = ref('existing');
const selectedExistingBorrower = ref(null);
const guarantorRelationship = ref(null);
const availableBorrowers = ref([]);
const searchingBorrowers = ref(false);
const adding = ref(false);
const updating = ref(false);
const removing = ref(false);
const guarantorToRemove = ref(null);
const editingGuarantor = ref(null);

// New guarantor form data
const newGuarantor = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: '',
  relationship: '',
  address: {
    street: '',
    city: '',
    state: '',
    postal_code: '',
    country: ''
  }
});

// Form refs
const guarantorForm = ref(null);
const editGuarantorForm = ref(null);

// Relationship types
const relationshipTypes = [
  { title: 'Spouse', value: 'SPOUSE' },
  { title: 'Parent', value: 'PARENT' },
  { title: 'Child', value: 'CHILD' },
  { title: 'Sibling', value: 'SIBLING' },
  { title: 'Friend', value: 'FRIEND' },
  { title: 'Business Partner', value: 'BUSINESS_PARTNER' },
  { title: 'Other', value: 'OTHER' }
];

// Computed properties
const canAddGuarantor = computed(() => {
  return authStore.hasPermission('borrower:edit');
});

// Methods
const fetchGuarantors = async () => {
  loading.value = true;
  
  try {
    // In a real app, this would be a dedicated API endpoint
    // For now, we'll assume guarantors are stored in the borrower object
    guarantors.value = props.borrower.guarantors || [];
  } catch (error) {
    console.error('Error fetching guarantors:', error);
    notificationStore.showError('Failed to load guarantors');
  } finally {
    loading.value = false;
  }
};

const searchBorrowers = async (query) => {
  if (!query || query.length < 2) return;
  
  searchingBorrowers.value = true;
  try {
    const result = await borrowerStore.searchBorrowers(query);
    
    // Filter out the current borrower and existing guarantors
    const existingIds = [props.borrower.id, ...guarantors.value.map(g => g.id)];
    availableBorrowers.value = result.filter(b => !existingIds.includes(b.id));
  } catch (error) {
    notificationStore.showError('Failed to search borrowers');
    console.error('Error searching borrowers:', error);
  } finally {
    searchingBorrowers.value = false;
  }
};

const addGuarantor = async () => {
  if (addGuarantorTab.value === 'existing') {
    if (!selectedExistingBorrower.value || !guarantorRelationship.value) {
      notificationStore.showError('Please select a borrower and relationship');
      return;
    }
    
    adding.value = true;
    try {
      // Create guarantor from existing borrower
      const guarantorData = {
        ...selectedExistingBorrower.value,
        relationship: guarantorRelationship.value,
        borrower_id: props.borrower.id
      };
      
      // In a real app, this would be a dedicated API endpoint
      // For now, we'll just add to the local array
      guarantors.value.push(guarantorData);
      
      notificationStore.showSuccess('Guarantor added successfully');
      showAddGuarantorDialog.value = false;
      resetAddGuarantorForm();
    } catch (error) {
      notificationStore.showError('Failed to add guarantor');
      console.error('Error adding guarantor:', error);
    } finally {
      adding.value = false;
    }
  } else {
    // Validate form
    const { valid } = await guarantorForm.value.validate();
    if (!valid) {
      notificationStore.showError('Please fix the errors in the form');
      return;
    }
    
    adding.value = true;
    try {
      // Create new guarantor
      const guarantorData = {
        ...newGuarantor.value,
        full_name: `${newGuarantor.value.first_name} ${newGuarantor.value.last_name}`,
        borrower_id: props.borrower.id,
        id: Date.now() // Temporary ID for demo purposes
      };
      
      // In a real app, this would be a dedicated API endpoint
      // For now, we'll just add to the local array
      guarantors.value.push(guarantorData);
      
      notificationStore.showSuccess('Guarantor added successfully');
      showAddGuarantorDialog.value = false;
      resetAddGuarantorForm();
    } catch (error) {
      notificationStore.showError('Failed to add guarantor');
      console.error('Error adding guarantor:', error);
    } finally {
      adding.value = false;
    }
  }
};

const resetAddGuarantorForm = () => {
  selectedExistingBorrower.value = null;
  guarantorRelationship.value = null;
  addGuarantorTab.value = 'existing';
  
  newGuarantor.value = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    relationship: '',
    address: {
      street: '',
      city: '',
      state: '',
      postal_code: '',
      country: ''
    }
  };
};

const editGuarantor = (guarantor) => {
  editingGuarantor.value = JSON.parse(JSON.stringify(guarantor)); // Deep copy
  showEditGuarantorDialog.value = true;
};

const updateGuarantor = async () => {
  // Validate form
  const { valid } = await editGuarantorForm.value.validate();
  if (!valid) {
    notificationStore.showError('Please fix the errors in the form');
    return;
  }
  
  updating.value = true;
  try {
    // Update guarantor
    const index = guarantors.value.findIndex(g => g.id === editingGuarantor.value.id);
    if (index !== -1) {
      // Update full_name
      editingGuarantor.value.full_name = `${editingGuarantor.value.first_name} ${editingGuarantor.value.last_name}`;
      
      // In a real app, this would be a dedicated API endpoint
      // For now, we'll just update the local array
      guarantors.value[index] = editingGuarantor.value;
      
      notificationStore.showSuccess('Guarantor updated successfully');
      showEditGuarantorDialog.value = false;
      editingGuarantor.value = null;
    }
  } catch (error) {
    notificationStore.showError('Failed to update guarantor');
    console.error('Error updating guarantor:', error);
  } finally {
    updating.value = false;
  }
};

const confirmRemoveGuarantor = (guarantor) => {
  guarantorToRemove.value = guarantor;
  showRemoveDialog.value = true;
};

const removeGuarantor = async () => {
  removing.value = true;
  try {
    // In a real app, this would be a dedicated API endpoint
    // For now, we'll just remove from the local array
    guarantors.value = guarantors.value.filter(g => g.id !== guarantorToRemove.value.id);
    
    notificationStore.showSuccess('Guarantor removed successfully');
    showRemoveDialog.value = false;
    guarantorToRemove.value = null;
  } catch (error) {
    notificationStore.showError('Failed to remove guarantor');
    console.error('Error removing guarantor:', error);
  } finally {
    removing.value = false;
  }
};

// Formatting functions
const formatRelationship = (relationship) => {
  if (!relationship) return 'Not specified';
  
  const relationshipMap = {
    'SPOUSE': 'Spouse',
    'PARENT': 'Parent',
    'CHILD': 'Child',
    'SIBLING': 'Sibling',
    'FRIEND': 'Friend',
    'BUSINESS_PARTNER': 'Business Partner',
    'OTHER': 'Other'
  };
  
  return relationshipMap[relationship] || relationship;
};

const formatAddress = (address) => {
  if (!address) return 'Not specified';
  
  const parts = [];
  if (address.street) parts.push(address.street);
  if (address.city) parts.push(address.city);
  if (address.state) parts.push(address.state);
  if (address.postal_code) parts.push(address.postal_code);
  
  return parts.join(', ') || 'Not specified';
};

// Lifecycle hooks
onMounted(() => {
  fetchGuarantors();
});
</script>

<style scoped>
.borrower-guarantors-tab {
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
