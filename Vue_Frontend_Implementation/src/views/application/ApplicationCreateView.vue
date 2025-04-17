<template>
  <div class="application-create-view">
    <!-- Page Header -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">Create New Application</h1>
        <p class="text-subtitle-1 text-grey-darken-1">
          Create a new loan application
        </p>
      </div>
      
      <v-btn
        variant="outlined"
        prepend-icon="mdi-arrow-left"
        @click="navigateBack"
      >
        Back to Applications
      </v-btn>
    </div>
    
    <!-- Application Form -->
    <v-card>
      <v-card-text>
        <application-form
          v-model="applicationData"
          :loading="loading"
          :server-errors="serverErrors"
          mode="create"
          @submit="createApplication"
          @cancel="navigateBack"
        />
      </v-card-text>
    </v-card>
    
    <!-- Discard Changes Dialog -->
    <base-modal
      v-model="discardDialog"
      title="Discard Changes"
      max-width="400"
      @confirm="confirmDiscard"
    >
      <p>Are you sure you want to discard your changes?</p>
      <p class="text-body-2 text-grey-darken-1">This action cannot be undone.</p>
    </base-modal>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ApplicationForm from '@/components/application/ApplicationForm.vue'
import BaseModal from '@/components/common/BaseModal.vue'

// Router
const router = useRouter()

// State
const applicationData = ref({
  status: 'draft',
  amount: null,
  term: null,
  interest_rate: null,
  product_id: null,
  purpose: '',
  borrower_id: null,
  broker_id: null,
  commission_rate: null,
  commission_amount: null,
  broker_notes: ''
})
const loading = ref(false)
const serverErrors = ref({})
const discardDialog = ref(false)
const hasChanges = ref(false)

// Methods
const createApplication = async (data) => {
  loading.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await applicationService.createApplication(data)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Show success notification
    
    // Navigate to the application detail page
    router.push({ 
      name: 'application-detail', 
      params: { id: 1 } // In a real app, this would be the ID from the API response
    })
  } catch (error) {
    console.error('Error creating application:', error)
    
    // Handle server errors
    if (error.response?.data) {
      serverErrors.value = error.response.data
    } else {
      // Show generic error notification
    }
  } finally {
    loading.value = false
  }
}

const navigateBack = () => {
  // Check if there are unsaved changes
  if (hasUnsavedChanges()) {
    discardDialog.value = true
  } else {
    router.push({ name: 'application-list' })
  }
}

const confirmDiscard = () => {
  discardDialog.value = false
  router.push({ name: 'application-list' })
}

const hasUnsavedChanges = () => {
  // In a real app, this would compare the current form data with the original data
  // For now, just return the hasChanges flag
  return hasChanges.value
}

// Watch for changes to mark the form as dirty
watch(applicationData, () => {
  hasChanges.value = true
}, { deep: true })

// Add navigation guard
onBeforeRouteLeave((to, from, next) => {
  if (hasUnsavedChanges()) {
    discardDialog.value = true
    next(false)
  } else {
    next()
  }
})
</script>

<style scoped>
.application-create-view {
  padding: 24px;
}
</style>
