<template>
  <div class="borrower-create-view">
    <!-- Page Header -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">Create New Borrower</h1>
        <p class="text-subtitle-1 text-grey-darken-1">
          Add a new borrower to the system
        </p>
      </div>
      
      <v-btn
        variant="outlined"
        prepend-icon="mdi-arrow-left"
        @click="navigateBack"
      >
        Back to Borrowers
      </v-btn>
    </div>
    
    <!-- Borrower Form -->
    <v-card>
      <v-card-text>
        <borrower-form
          v-model="borrowerData"
          :loading="loading"
          :server-errors="serverErrors"
          mode="create"
          @submit="createBorrower"
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
import BorrowerForm from '@/components/borrower/BorrowerForm.vue'
import BaseModal from '@/components/common/BaseModal.vue'

// Router
const router = useRouter()

// State
const borrowerData = ref({
  type: 'individual',
  status: 'active',
  country: 'US',
  mailing_country: 'US'
})
const loading = ref(false)
const serverErrors = ref({})
const discardDialog = ref(false)
const hasChanges = ref(false)

// Methods
const createBorrower = async (data) => {
  loading.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await borrowerService.createBorrower(data)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Show success notification
    
    // Navigate to the borrower detail page
    router.push({ 
      name: 'borrower-detail', 
      params: { id: 1 } // In a real app, this would be the ID from the API response
    })
  } catch (error) {
    console.error('Error creating borrower:', error)
    
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
    router.push({ name: 'borrower-list' })
  }
}

const confirmDiscard = () => {
  discardDialog.value = false
  router.push({ name: 'borrower-list' })
}

const hasUnsavedChanges = () => {
  // In a real app, this would compare the current form data with the original data
  // For now, just return the hasChanges flag
  return hasChanges.value
}

// Watch for changes to mark the form as dirty
watch(borrowerData, () => {
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
.borrower-create-view {
  padding: 24px;
}
</style>
