<template>
  <div class="application-list-view">
    <!-- Page Header -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">Loan Applications</h1>
        <p class="text-subtitle-1 text-grey-darken-1">
          Manage and track all loan applications
        </p>
      </div>
      
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="navigateToCreate"
      >
        New Application
      </v-btn>
    </div>
    
    <!-- Application Filters -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="filters.search"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="comfortable"
              hide-details
              clearable
              @update:model-value="handleFilterChange"
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="3">
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
          
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.broker"
              label="Broker"
              :items="brokerOptions"
              variant="outlined"
              density="comfortable"
              hide-details
              clearable
              @update:model-value="handleFilterChange"
            ></v-select>
          </v-col>
          
          <v-col cols="12" md="3">
            <v-menu
              v-model="dateMenu"
              :close-on-content-click="false"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="dateRangeText"
                  label="Date Range"
                  prepend-inner-icon="mdi-calendar"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                  readonly
                  clearable
                  v-bind="props"
                  @click:clear="clearDateRange"
                ></v-text-field>
              </template>
              
              <v-card min-width="300">
                <v-card-text>
                  <v-date-picker
                    v-model="dateRange"
                    range
                    @update:model-value="handleDateRangeChange"
                  ></v-date-picker>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    variant="text"
                    @click="dateMenu = false"
                  >
                    Close
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-menu>
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
    
    <!-- Applications Table -->
    <base-table
      :headers="headers"
      :items="applications"
      :loading="loading"
      :total-items="totalApplications"
      :server-side="true"
      @page-change="handlePageChange"
      @sort="handleSort"
    >
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
      
      <!-- Custom Amount Column -->
      <template #item.amount="{ value }">
        {{ formatCurrency(value) }}
      </template>
      
      <!-- Custom Date Column -->
      <template #item.created_at="{ value }">
        {{ formatDate(value) }}
      </template>
      
      <!-- Actions Column -->
      <template #item.actions="{ item }">
        <div class="d-flex justify-end">
          <v-btn
            icon="mdi-eye"
            variant="text"
            size="small"
            color="primary"
            @click="viewApplication(item)"
            title="View"
          ></v-btn>
          
          <v-btn
            icon="mdi-pencil"
            variant="text"
            size="small"
            color="primary"
            @click="editApplication(item)"
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
          Create First Application
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
      @confirm="deleteApplication"
    >
      <p>Are you sure you want to delete application <strong>{{ selectedApplication?.reference || '' }}</strong>?</p>
      <p class="text-body-2 text-grey-darken-1">This action cannot be undone.</p>
    </base-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { format } from 'date-fns'
import BaseTable from '@/components/common/BaseTable.vue'
import BaseModal from '@/components/common/BaseModal.vue'

// Router
const router = useRouter()

// Table headers
const headers = [
  { title: 'Reference', key: 'reference', sortable: true },
  { title: 'Borrower', key: 'borrower_name', sortable: true },
  { title: 'Amount', key: 'amount', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Broker', key: 'broker_name', sortable: true },
  { title: 'Created', key: 'created_at', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
]

// Filter options
const statusOptions = [
  { title: 'Draft', value: 'draft' },
  { title: 'Submitted', value: 'submitted' },
  { title: 'In Review', value: 'in_review' },
  { title: 'Approved', value: 'approved' },
  { title: 'Rejected', value: 'rejected' },
  { title: 'Completed', value: 'completed' }
]

// Mock broker options (would come from API)
const brokerOptions = [
  { title: 'John Smith', value: 1 },
  { title: 'Sarah Johnson', value: 2 },
  { title: 'Michael Brown', value: 3 },
  { title: 'Emily Davis', value: 4 }
]

// State
const loading = ref(false)
const applications = ref([])
const totalApplications = ref(0)
const page = ref(1)
const itemsPerPage = ref(10)
const sortBy = ref([{ key: 'created_at', order: 'desc' }])
const filters = ref({
  search: '',
  status: null,
  broker: null,
  start_date: null,
  end_date: null
})
const dateRange = ref([])
const dateMenu = ref(false)
const deleteDialog = ref(false)
const deleteLoading = ref(false)
const selectedApplication = ref(null)

// Computed
const dateRangeText = computed(() => {
  if (dateRange.value && dateRange.value.length === 2) {
    return `${dateRange.value[0]} to ${dateRange.value[1]}`
  }
  return ''
})

// Methods
const fetchApplications = async () => {
  loading.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await applicationService.getApplications({
    //   page: page.value,
    //   limit: itemsPerPage.value,
    //   sort_by: sortBy.value[0]?.key || 'created_at',
    //   sort_order: sortBy.value[0]?.order || 'desc',
    //   ...filters.value
    // })
    
    // Mock data for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    applications.value = [
      {
        id: 1,
        reference: 'APP-2025-001',
        borrower_name: 'John Doe',
        amount: 250000,
        status: 'approved',
        broker_name: 'Sarah Johnson',
        created_at: '2025-04-10T14:30:00Z'
      },
      {
        id: 2,
        reference: 'APP-2025-002',
        borrower_name: 'Jane Smith',
        amount: 175000,
        status: 'in_review',
        broker_name: 'Michael Brown',
        created_at: '2025-04-12T09:15:00Z'
      },
      {
        id: 3,
        reference: 'APP-2025-003',
        borrower_name: 'Robert Johnson',
        amount: 320000,
        status: 'submitted',
        broker_name: 'John Smith',
        created_at: '2025-04-14T11:45:00Z'
      },
      {
        id: 4,
        reference: 'APP-2025-004',
        borrower_name: 'Emily Wilson',
        amount: 450000,
        status: 'draft',
        broker_name: 'Emily Davis',
        created_at: '2025-04-15T16:20:00Z'
      },
      {
        id: 5,
        reference: 'APP-2025-005',
        borrower_name: 'Michael Brown',
        amount: 195000,
        status: 'rejected',
        broker_name: 'Sarah Johnson',
        created_at: '2025-04-16T10:05:00Z'
      }
    ]
    
    totalApplications.value = 5
  } catch (error) {
    console.error('Error fetching applications:', error)
    // Show error notification
  } finally {
    loading.value = false
  }
}

const handlePageChange = (newPage) => {
  page.value = newPage
  fetchApplications()
}

const handleSort = (newSortBy) => {
  sortBy.value = newSortBy
  fetchApplications()
}

const handleFilterChange = () => {
  // This would be debounced in a real application
}

const handleDateRangeChange = () => {
  if (dateRange.value && dateRange.value.length === 2) {
    filters.value.start_date = dateRange.value[0]
    filters.value.end_date = dateRange.value[1]
    dateMenu.value = false
  }
}

const clearDateRange = () => {
  dateRange.value = []
  filters.value.start_date = null
  filters.value.end_date = null
}

const clearFilters = () => {
  filters.value = {
    search: '',
    status: null,
    broker: null,
    start_date: null,
    end_date: null
  }
  dateRange.value = []
  fetchApplications()
}

const applyFilters = () => {
  page.value = 1
  fetchApplications()
}

const navigateToCreate = () => {
  router.push({ name: 'application-create' })
}

const viewApplication = (item) => {
  router.push({ name: 'application-detail', params: { id: item.id } })
}

const editApplication = (item) => {
  router.push({ name: 'application-edit', params: { id: item.id } })
}

const confirmDelete = (item) => {
  selectedApplication.value = item
  deleteDialog.value = true
}

const deleteApplication = async () => {
  if (!selectedApplication.value) return
  
  deleteLoading.value = true
  
  try {
    // This would be an API call in a real application
    // await applicationService.deleteApplication(selectedApplication.value.id)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Remove from local list
    applications.value = applications.value.filter(app => app.id !== selectedApplication.value.id)
    totalApplications.value--
    
    // Show success notification
    deleteDialog.value = false
  } catch (error) {
    console.error('Error deleting application:', error)
    // Show error notification
  } finally {
    deleteLoading.value = false
  }
}

// Utility functions
const getStatusColor = (status) => {
  const statusColors = {
    draft: 'grey',
    submitted: 'info',
    in_review: 'warning',
    approved: 'success',
    rejected: 'error',
    completed: 'primary'
  }
  
  return statusColors[status] || 'grey'
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(value)
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
  fetchApplications()
})
</script>

<style scoped>
.application-list-view {
  padding: 24px;
}
</style>
