<template>
  <div class="borrower-duplicate-check">
    <!-- Search Form -->
    <v-card class="mb-6">
      <v-card-title>Check for Duplicate Borrowers</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              v-model="searchParams.type"
              label="Borrower Type"
              :items="borrowerTypeOptions"
              variant="outlined"
              hide-details
              clearable
            ></v-select>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchParams.name"
              label="Name"
              variant="outlined"
              hide-details
              clearable
              placeholder="First name, last name, or business name"
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchParams.email"
              label="Email"
              variant="outlined"
              hide-details
              clearable
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchParams.phone"
              label="Phone"
              variant="outlined"
              hide-details
              clearable
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchParams.ssn"
              label="SSN / Tax ID"
              variant="outlined"
              hide-details
              clearable
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchParams.address"
              label="Address"
              variant="outlined"
              hide-details
              clearable
            ></v-text-field>
          </v-col>
        </v-row>
        
        <div class="d-flex justify-end mt-4">
          <v-btn
            variant="text"
            prepend-icon="mdi-refresh"
            @click="resetSearch"
          >
            Reset
          </v-btn>
          
          <v-btn
            color="primary"
            prepend-icon="mdi-magnify"
            class="ml-2"
            :loading="loading"
            @click="searchDuplicates"
          >
            Search
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    
    <!-- Results -->
    <v-card v-if="hasSearched">
      <v-card-title class="d-flex align-center">
        <span>Search Results</span>
        <v-chip
          class="ml-2"
          :color="potentialDuplicates.length > 0 ? 'warning' : 'success'"
        >
          {{ potentialDuplicates.length }} {{ potentialDuplicates.length === 1 ? 'match' : 'matches' }}
        </v-chip>
        <v-spacer></v-spacer>
        <v-btn
          v-if="potentialDuplicates.length > 1"
          color="primary"
          variant="text"
          prepend-icon="mdi-compare"
          @click="showMergeDialog = true"
        >
          Compare & Merge
        </v-btn>
      </v-card-title>
      
      <v-divider></v-divider>
      
      <!-- No Results -->
      <v-card-text v-if="potentialDuplicates.length === 0">
        <div class="d-flex flex-column align-center py-8">
          <v-icon size="64" color="success" class="mb-4">mdi-check-circle</v-icon>
          <h3 class="text-h6">No duplicates found</h3>
          <p class="text-body-2 text-grey-darken-1">
            No potential duplicate borrowers were found matching your search criteria.
          </p>
        </div>
      </v-card-text>
      
      <!-- Results List -->
      <v-list v-else>
        <v-list-item
          v-for="borrower in potentialDuplicates"
          :key="borrower.id"
          :value="borrower.id"
        >
          <template v-slot:prepend>
            <v-checkbox
              v-model="selectedBorrowers"
              :value="borrower.id"
              hide-details
            ></v-checkbox>
          </template>
          
          <v-list-item-title>
            {{ borrower.name }}
            <v-chip
              size="x-small"
              :color="getBorrowerTypeColor(borrower.type)"
              class="ml-2"
            >
              {{ borrower.type }}
            </v-chip>
          </v-list-item-title>
          
          <v-list-item-subtitle>
            <v-icon size="small" color="grey-darken-1" class="mr-1">mdi-email</v-icon>
            {{ borrower.email }}
            <span class="mx-2">|</span>
            <v-icon size="small" color="grey-darken-1" class="mr-1">mdi-phone</v-icon>
            {{ borrower.phone }}
          </v-list-item-subtitle>
          
          <template v-slot:append>
            <div class="d-flex align-center">
              <v-chip
                size="small"
                :color="getMatchScoreColor(borrower.match_score)"
                class="mr-2"
              >
                {{ Math.round(borrower.match_score * 100) }}% match
              </v-chip>
              
              <v-btn
                icon="mdi-eye"
                variant="text"
                size="small"
                color="primary"
                @click="viewBorrower(borrower)"
                title="View"
              ></v-btn>
            </div>
          </template>
        </v-list-item>
      </v-list>
    </v-card>
    
    <!-- Merge Dialog -->
    <base-modal
      v-model="showMergeDialog"
      title="Compare & Merge Borrowers"
      max-width="900"
      :loading="mergeLoading"
      persistent
      @confirm="mergeBorrowers"
    >
      <div v-if="selectedBorrowers.length < 2" class="text-center py-4">
        <v-alert
          type="warning"
          variant="tonal"
        >
          Please select at least 2 borrowers to compare and merge.
        </v-alert>
      </div>
      
      <div v-else>
        <p class="mb-4">
          Select which data to keep for the merged borrower record. The primary record will be kept,
          and data from other records will be merged into it.
        </p>
        
        <v-card variant="outlined" class="mb-4">
          <v-card-text>
            <div class="d-flex align-center mb-4">
              <div class="text-subtitle-1 font-weight-medium">Primary Record</div>
              <v-spacer></v-spacer>
              <v-select
                v-model="primaryBorrowerId"
                :items="selectedBorrowersOptions"
                variant="outlined"
                density="compact"
                hide-details
                style="max-width: 300px"
              ></v-select>
            </div>
            
            <v-alert
              type="info"
              variant="tonal"
              density="compact"
            >
              The primary record will be kept, and all applications and documents from other records will be transferred to it.
            </v-alert>
          </v-card-text>
        </v-card>
        
        <v-table>
          <thead>
            <tr>
              <th>Field</th>
              <th v-for="borrower in selectedBorrowersData" :key="borrower.id">
                {{ borrower.name }}
                <v-chip
                  size="x-small"
                  :color="borrower.id === primaryBorrowerId ? 'primary' : ''"
                  class="ml-1"
                >
                  {{ borrower.id === primaryBorrowerId ? 'Primary' : '' }}
                </v-chip>
              </th>
              <th>Keep</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="field in mergeFields" :key="field.key">
              <td>{{ field.label }}</td>
              <td v-for="borrower in selectedBorrowersData" :key="`${field.key}-${borrower.id}`">
                {{ borrower[field.key] || '-' }}
              </td>
              <td>
                <v-select
                  v-model="mergeSelections[field.key]"
                  :items="selectedBorrowersOptions"
                  variant="outlined"
                  density="compact"
                  hide-details
                ></v-select>
              </td>
            </tr>
          </tbody>
        </v-table>
        
        <v-alert
          type="warning"
          variant="tonal"
          class="mt-4"
        >
          This action will merge the selected borrowers into a single record. The non-primary records will be marked as duplicates and hidden from search results.
        </v-alert>
      </div>
    </base-modal>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseModal from '@/components/common/BaseModal.vue'

// Router
const router = useRouter()

// Props
const props = defineProps({
  initialSearchParams: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['duplicate-found', 'merge-complete'])

// State
const searchParams = ref({
  type: '',
  name: '',
  email: '',
  phone: '',
  ssn: '',
  address: '',
  ...props.initialSearchParams
})
const loading = ref(false)
const hasSearched = ref(false)
const potentialDuplicates = ref([])
const selectedBorrowers = ref([])
const showMergeDialog = ref(false)
const primaryBorrowerId = ref(null)
const mergeSelections = ref({})
const mergeLoading = ref(false)

// Options
const borrowerTypeOptions = [
  { title: 'Individual', value: 'individual' },
  { title: 'Business', value: 'business' },
  { title: 'Guarantor', value: 'guarantor' }
]

// Merge fields
const mergeFields = [
  { key: 'email', label: 'Email' },
  { key: 'phone', label: 'Phone' },
  { key: 'address_line1', label: 'Address Line 1' },
  { key: 'city', label: 'City' },
  { key: 'state', label: 'State' },
  { key: 'zip_code', label: 'ZIP Code' },
  { key: 'status', label: 'Status' }
]

// Computed
const selectedBorrowersData = computed(() => {
  return potentialDuplicates.value.filter(b => selectedBorrowers.value.includes(b.id))
})

const selectedBorrowersOptions = computed(() => {
  return selectedBorrowersData.value.map(b => ({
    title: b.name,
    value: b.id
  }))
})

// Methods
const searchDuplicates = async () => {
  loading.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await borrowerService.checkDuplicates(searchParams.value)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock data for demonstration
    if (
      searchParams.value.name?.toLowerCase().includes('john') ||
      searchParams.value.email?.toLowerCase().includes('john') ||
      searchParams.value.phone?.includes('555')
    ) {
      potentialDuplicates.value = [
        {
          id: 1,
          name: 'John Doe',
          email: 'john.doe@example.com',
          phone: '(555) 123-4567',
          address_line1: '123 Main St',
          city: 'New York',
          state: 'NY',
          zip_code: '10001',
          type: 'individual',
          status: 'active',
          match_score: 0.95
        },
        {
          id: 2,
          name: 'John D.',
          email: 'johnd@example.com',
          phone: '(555) 987-6543',
          address_line1: '123 Main Street',
          city: 'New York',
          state: 'NY',
          zip_code: '10001',
          type: 'individual',
          status: 'inactive',
          match_score: 0.85
        },
        {
          id: 3,
          name: 'Johnny Doe',
          email: 'johnny.doe@example.com',
          phone: '(555) 456-7890',
          address_line1: '456 Oak Ave',
          city: 'Brooklyn',
          state: 'NY',
          zip_code: '11201',
          type: 'individual',
          status: 'active',
          match_score: 0.75
        }
      ]
    } else if (
      searchParams.value.name?.toLowerCase().includes('acme') ||
      searchParams.value.email?.toLowerCase().includes('acme')
    ) {
      potentialDuplicates.value = [
        {
          id: 4,
          name: 'Acme Corporation',
          email: 'info@acmecorp.com',
          phone: '(555) 555-5555',
          address_line1: '789 Business Blvd',
          city: 'Chicago',
          state: 'IL',
          zip_code: '60601',
          type: 'business',
          status: 'active',
          match_score: 0.98
        },
        {
          id: 5,
          name: 'ACME Corp.',
          email: 'contact@acmecorp.com',
          phone: '(555) 555-5556',
          address_line1: '789 Business Boulevard',
          city: 'Chicago',
          state: 'IL',
          zip_code: '60601',
          type: 'business',
          status: 'active',
          match_score: 0.90
        }
      ]
    } else {
      potentialDuplicates.value = []
    }
    
    hasSearched.value = true
    
    // Emit event if duplicates found
    if (potentialDuplicates.value.length > 0) {
      emit('duplicate-found', potentialDuplicates.value)
    }
    
    // Reset selections
    selectedBorrowers.value = []
    primaryBorrowerId.value = null
    mergeSelections.value = {}
  } catch (error) {
    console.error('Error searching for duplicates:', error)
    // Show error notification
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  searchParams.value = {
    type: '',
    name: '',
    email: '',
    phone: '',
    ssn: '',
    address: ''
  }
  hasSearched.value = false
  potentialDuplicates.value = []
  selectedBorrowers.value = []
}

const viewBorrower = (borrower) => {
  router.push({ name: 'borrower-detail', params: { id: borrower.id } })
}

const mergeBorrowers = async () => {
  if (selectedBorrowers.value.length < 2 || !primaryBorrowerId.value) {
    return
  }
  
  mergeLoading.value = true
  
  try {
    // Prepare merge data
    const mergeData = {
      primary_id: primaryBorrowerId.value,
      secondary_ids: selectedBorrowers.value.filter(id => id !== primaryBorrowerId.value),
      field_selections: { ...mergeSelections.value }
    }
    
    // This would be an API call in a real application
    // const response = await borrowerService.mergeBorrowers(mergeData)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Show success notification
    
    // Close dialog
    showMergeDialog.value = false
    
    // Reset selections
    selectedBorrowers.value = []
    primaryBorrowerId.value = null
    mergeSelections.value = {}
    
    // Refresh search results
    await searchDuplicates()
    
    // Emit event
    emit('merge-complete', primaryBorrowerId.value)
  } catch (error) {
    console.error('Error merging borrowers:', error)
    // Show error notification
  } finally {
    mergeLoading.value = false
  }
}

// Utility functions
const getBorrowerTypeColor = (type) => {
  const typeColors = {
    individual: 'primary',
    business: 'purple',
    guarantor: 'indigo'
  }
  
  return typeColors[type] || 'grey'
}

const getMatchScoreColor = (score) => {
  if (score >= 0.9) {
    return 'error'
  } else if (score >= 0.7) {
    return 'warning'
  } else {
    return 'info'
  }
}

// Initialize
watch(() => selectedBorrowers.value, (newValue) => {
  if (newValue.length > 0 && !primaryBorrowerId.value) {
    // Set the first selected borrower as primary by default
    primaryBorrowerId.value = newValue[0]
    
    // Initialize merge selections with primary borrower
    mergeFields.forEach(field => {
      mergeSelections.value[field.key] = primaryBorrowerId.value
    })
  } else if (newValue.length === 0) {
    primaryBorrowerId.value = null
    mergeSelections.value = {}
  }
}, { immediate: true })

// Watch for primary borrower changes
watch(() => primaryBorrowerId.value, (newValue) => {
  if (newValue) {
    // Update any unset merge selections to use the primary borrower
    mergeFields.forEach(field => {
      if (!mergeSelections.value[field.key] || !selectedBorrowers.value.includes(mergeSelections.value[field.key])) {
        mergeSelections.value[field.key] = newValue
      }
    })
  }
})
</script>

<style scoped>
.borrower-duplicate-check {
  width: 100%;
}
</style>
