<template>
  <div class="borrower-list-view">
    <!-- Page Header -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">Borrowers</h1>
        <p class="text-subtitle-1 text-grey-darken-1">
          Manage borrower information
        </p>
      </div>
      
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="navigateToCreate"
      >
        New Borrower
      </v-btn>
    </div>
    
    <!-- Borrower Filters -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="filters.search"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="comfortable"
              hide-details
              clearable
              @update:model-value="handleFilterChange"
              placeholder="Search by name, email, or phone"
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-select
              v-model="filters.type"
              label="Borrower Type"
              :items="borrowerTypeOptions"
              variant="outlined"
              density="comfortable"
              hide-details
              clearable
              @update:model-value="handleFilterChange"
            ></v-select>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-select
              v-model="filters.status"
              label="Status"
              :items="statusOptions"
              variant="outlined"
              density="comfortable"
              hide-details
              clearable
              @update:model-value="handleFilterChange"
            ></v-select>
          </v-col>
        </v-row>
        
        <div class="d-flex justify-end mt-4">
          <v-btn
            variant="text"
            prepend-icon="mdi-filter-remove"
            @click="clearFilters"
          >
            Clear Filters
          </v-btn>
          
          <v-btn
            color="primary"
            prepend-icon="mdi-filter"
            class="ml-2"
            @click="applyFilters"
          >
            Apply Filters
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    
    <!-- Borrower Grid/List Toggle -->
    <div class="d-flex justify-end mb-4">
      <v-btn-toggle
        v-model="viewMode"
        color="primary"
        density="comfortable"
        rounded="lg"
      >
        <v-btn value="grid" icon="mdi-view-grid"></v-btn>
        <v-btn value="list" icon="mdi-view-list"></v-btn>
      </v-btn-toggle>
    </div>
    
    <!-- Grid View -->
    <v-row v-if="viewMode === 'grid'">
      <v-col
        v-for="borrower in borrowers"
        :key="borrower.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <base-card
          hover
          clickable
          @click="viewBorrower(borrower)"
        >
          <template #header>
            <v-card-item>
              <template #prepend>
                <v-avatar color="primary">
                  <span class="text-white">{{ borrower.name.charAt(0) }}</span>
                </v-avatar>
              </template>
              
              <v-card-title>{{ borrower.name }}</v-card-title>
              <v-card-subtitle>{{ borrower.email }}</v-card-subtitle>
              
              <template #append>
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn
                      icon="mdi-dots-vertical"
                      variant="text"
                      size="small"
                      v-bind="props"
                      @click.stop
                    ></v-btn>
                  </template>
                  
                  <v-list>
                    <v-list-item
                      @click.stop="viewBorrower(borrower)"
                      prepend-icon="mdi-eye"
                      title="View"
                    ></v-list-item>
                    
                    <v-list-item
                      @click.stop="editBorrower(borrower)"
                      prepend-icon="mdi-pencil"
                      title="Edit"
                    ></v-list-item>
                    
                    <v-list-item
                      @click.stop="confirmDelete(borrower)"
                      prepend-icon="mdi-delete"
                      title="Delete"
                      color="error"
                    ></v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-card-item>
          </template>
          
          <v-divider></v-divider>
          
          <v-list density="compact" nav>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon size="small" color="grey-darken-1">mdi-phone</v-icon>
              </template>
              <v-list-item-title class="text-body-2">{{ borrower.phone }}</v-list-item-title>
            </v-list-item>
            
            <v-list-item>
              <template v-slot:prepend>
                <v-icon size="small" color="grey-darken-1">mdi-map-marker</v-icon>
              </template>
              <v-list-item-title class="text-body-2">{{ borrower.city }}, {{ borrower.state }}</v-list-item-title>
            </v-list-item>
            
            <v-list-item>
              <template v-slot:prepend>
                <v-icon size="small" color="grey-darken-1">mdi-file-document</v-icon>
              </template>
              <v-list-item-title class="text-body-2">{{ borrower.applications }} Applications</v-list-item-title>
            </v-list-item>
          </v-list>
          
          <template #footer>
            <v-chip
              :color="getBorrowerTypeColor(borrower.type)"
              size="small"
              class="mr-2"
            >
              {{ borrower.type }}
            </v-chip>
            
            <v-chip
              :color="getStatusColor(borrower.status)"
              size="small"
            >
              {{ borrower.status }}
            </v-chip>
            
            <v-spacer></v-spacer>
            
            <v-btn
              variant="text"
              color="primary"
              size="small"
              @click.stop="createApplication(borrower)"
            >
              New Application
            </v-btn>
          </template>
        </base-card>
      </v-col>
      
      <!-- Empty State for Grid View -->
      <v-col v-if="borrowers.length === 0" cols="12">
        <v-card class="pa-6 text-center">
          <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-account-off</v-icon>
          <h3 class="text-h6 text-grey-darken-1">No borrowers found</h3>
          <p class="text-body-2 text-grey-darken-1 mb-4">
            Try changing your search or filters, or create a new borrower
          </p>
          <v-btn
            color="primary"
            @click="navigateToCreate"
          >
            Create Borrower
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- List View -->
    <base-table
      v-if="viewMode === 'list'"
      :headers="headers"
      :items="borrowers"
      :loading="loading"
      :total-items="totalBorrowers"
      :server-side="true"
      @page-change="handlePageChange"
      @sort="handleSort"
    >
      <!-- Custom Name Column -->
      <template #item.name="{ item }">
        <div class="d-flex align-center">
          <v-avatar color="primary" size="32" class="mr-2">
            <span class="text-white">{{ item.name.charAt(0) }}</span>
          </v-avatar>
          <div>
            <div>{{ item.name }}</div>
            <div class="text-caption text-grey-darken-1">{{ item.email }}</div>
          </div>
        </div>
      </template>
      
      <!-- Custom Type Column -->
      <template #item.type="{ value }">
        <v-chip
          :color="getBorrowerTypeColor(value)"
          size="small"
          label
        >
          {{ value }}
        </v-chip>
      </template>
      
      <!-- Custom Status Column -->
      <template #item.status="{ value }">
        <v-chip
          :color="getStatusColor(value)"
          size="small"
          label
        >
          {{ value }}
        </v-chip>
      </template>
      
      <!-- Custom Date Column -->
      <template #item.created_at="{ value }">
        {{ formatDate(value) }}
      </template>
      
      <!-- Actions Column -->
      <template #item.actions="{ item }">
        <div class="d-flex justify-end">
          <v-btn
            icon="mdi-file-plus"
            variant="text"
            size="small"
            color="primary"
            @click="createApplication(item)"
            title="New Application"
          ></v-btn>
          
          <v-btn
            icon="mdi-eye"
            variant="text"
            size="small"
            color="primary"
            @click="viewBorrower(item)"
            title="View"
          ></v-btn>
          
          <v-btn
            icon="mdi-pencil"
            variant="text"
            size="small"
            color="primary"
            @click="editBorrower(item)"
            title="Edit"
          ></v-btn>
          
          <v-btn
            icon="mdi-delete"
            variant="text"
            size="small"
            color="error"
            @click="confirmDelete(item)"
            title="Delete"
          ></v-btn>
        </div>
      </template>
      
      <!-- Empty State -->
      <template #no-data-actions>
        <v-btn
          color="primary"
          class="mt-4"
          @click="navigateToCreate"
        >
          Create First Borrower
        </v-btn>
      </template>
    </base-table>
    
    <!-- Delete Confirmation Dialog -->
    <base-modal
      v-model="deleteDialog"
      title="Confirm Delete"
      :loading="deleteLoading"
      persistent
      max-width="400"
      @confirm="deleteBorrower"
    >
      <p>Are you sure you want to delete borrower <strong>{{ selectedBorrower?.name || '' }}</strong>?</p>
      <p class="text-body-2 text-grey-darken-1">This action cannot be undone.</p>
      
      <v-alert
        v-if="selectedBorrower?.applications > 0"
        type="warning"
        variant="tonal"
        class="mt-4"
      >
        This borrower has {{ selectedBorrower?.applications }} active applications.
        Deleting this borrower will affect these applications.
      </v-alert>
    </base-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { format } from 'date-fns'
import BaseTable from '@/components/common/BaseTable.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseModal from '@/components/common/BaseModal.vue'

// Router
const router = useRouter()

// Table headers
const headers = [
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Phone', key: 'phone', sortable: true },
  { title: 'Location', key: 'location', sortable: true },
  { title: 'Type', key: 'type', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Applications', key: 'applications', sortable: true, align: 'center' },
  { title: 'Created', key: 'created_at', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
]

// Filter options
const borrowerTypeOptions = [
  { title: 'Individual', value: 'individual' },
  { title: 'Business', value: 'business' },
  { title: 'Guarantor', value: 'guarantor' }
]

const statusOptions = [
  { title: 'Active', value: 'active' },
  { title: 'Inactive', value: 'inactive' },
  { title: 'Pending', value: 'pending' },
  { title: 'Blocked', value: 'blocked' }
]

// State
const viewMode = ref('grid')
const loading = ref(false)
const borrowers = ref([])
const totalBorrowers = ref(0)
const page = ref(1)
const itemsPerPage = ref(10)
const sortBy = ref([{ key: 'created_at', order: 'desc' }])
const filters = ref({
  search: '',
  type: null,
  status: null
})
const deleteDialog = ref(false)
const deleteLoading = ref(false)
const selectedBorrower = ref(null)

// Methods
const fetchBorrowers = async () => {
  loading.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await borrowerService.getBorrowers({
    //   page: page.value,
    //   limit: itemsPerPage.value,
    //   sort_by: sortBy.value[0]?.key || 'created_at',
    //   sort_order: sortBy.value[0]?.order || 'desc',
    //   ...filters.value
    // })
    
    // Mock data for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    borrowers.value = [
      {
        id: 1,
        name: 'John Doe',
        email: 'john.doe@example.com',
        phone: '(555) 123-4567',
        address: '123 Main St',
        city: 'New York',
        state: 'NY',
        zip: '10001',
        type: 'individual',
        status: 'active',
        applications: 2,
        created_at: '2025-03-15T10:30:00Z'
      },
      {
        id: 2,
        name: 'Jane Smith',
        email: 'jane.smith@example.com',
        phone: '(555) 987-6543',
        address: '456 Oak Ave',
        city: 'Los Angeles',
        state: 'CA',
        zip: '90001',
        type: 'individual',
        status: 'active',
        applications: 1,
        created_at: '2025-03-20T14:45:00Z'
      },
      {
        id: 3,
        name: 'Acme Corporation',
        email: 'contact@acmecorp.com',
        phone: '(555) 555-5555',
        address: '789 Business Blvd',
        city: 'Chicago',
        state: 'IL',
        zip: '60601',
        type: 'business',
        status: 'active',
        applications: 3,
        created_at: '2025-03-25T09:15:00Z'
      },
      {
        id: 4,
        name: 'Robert Johnson',
        email: 'robert.johnson@example.com',
        phone: '(555) 456-7890',
        address: '321 Pine St',
        city: 'Miami',
        state: 'FL',
        zip: '33101',
        type: 'individual',
        status: 'inactive',
        applications: 0,
        created_at: '2025-04-01T11:20:00Z'
      },
      {
        id: 5,
        name: 'Sarah Williams',
        email: 'sarah.williams@example.com',
        phone: '(555) 789-0123',
        address: '654 Maple Dr',
        city: 'Seattle',
        state: 'WA',
        zip: '98101',
        type: 'guarantor',
        status: 'pending',
        applications: 0,
        created_at: '2025-04-05T16:10:00Z'
      },
      {
        id: 6,
        name: 'Tech Innovations LLC',
        email: 'info@techinnovations.com',
        phone: '(555) 222-3333',
        address: '987 Tech Park',
        city: 'San Francisco',
        state: 'CA',
        zip: '94105',
        type: 'business',
        status: 'active',
        applications: 2,
        created_at: '2025-04-10T13:40:00Z'
      }
    ]
    
    totalBorrowers.value = 6
  } catch (error) {
    console.error('Error fetching borrowers:', error)
    // Show error notification
  } finally {
    loading.value = false
  }
}

const handlePageChange = (newPage) => {
  page.value = newPage
  fetchBorrowers()
}

const handleSort = (newSortBy) => {
  sortBy.value = newSortBy
  fetchBorrowers()
}

const handleFilterChange = () => {
  // This would be debounced in a real application
}

const clearFilters = () => {
  filters.value = {
    search: '',
    type: null,
    status: null
  }
  fetchBorrowers()
}

const applyFilters = () => {
  page.value = 1
  fetchBorrowers()
}

const navigateToCreate = () => {
  router.push({ name: 'borrower-create' })
}

const viewBorrower = (borrower) => {
  router.push({ name: 'borrower-detail', params: { id: borrower.id } })
}

const editBorrower = (borrower) => {
  router.push({ name: 'borrower-edit', params: { id: borrower.id } })
}

const createApplication = (borrower) => {
  router.push({ 
    name: 'application-create',
    query: { borrower_id: borrower.id }
  })
}

const confirmDelete = (borrower) => {
  selectedBorrower.value = borrower
  deleteDialog.value = true
}

const deleteBorrower = async () => {
  if (!selectedBorrower.value) return
  
  deleteLoading.value = true
  
  try {
    // This would be an API call in a real application
    // await borrowerService.deleteBorrower(selectedBorrower.value.id)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Remove from local list
    borrowers.value = borrowers.value.filter(b => b.id !== selectedBorrower.value.id)
    totalBorrowers.value--
    
    // Show success notification
    deleteDialog.value = false
  } catch (error) {
    console.error('Error deleting borrower:', error)
    // Show error notification
  } finally {
    deleteLoading.value = false
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

const getStatusColor = (status) => {
  const statusColors = {
    active: 'success',
    inactive: 'grey',
    pending: 'warning',
    blocked: 'error'
  }
  
  return statusColors[status] || 'grey'
}

const formatDate = (dateString) => {
  try {
    return format(new Date(dateString), 'MMM d, yyyy')
  } catch (error) {
    return dateString
  }
}

// Lifecycle hooks
onMounted(() => {
  fetchBorrowers()
})
</script>

<style scoped>
.borrower-list-view {
  padding: 24px;
}
</style>
