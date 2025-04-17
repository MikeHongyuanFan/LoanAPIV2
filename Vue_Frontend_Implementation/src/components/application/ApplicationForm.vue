<template>
  <div class="application-form">
    <base-form
      v-model="formData"
      :loading="loading"
      :server-errors="serverErrors"
      :submit-text="submitText"
      @submit="handleSubmit"
      @cancel="handleCancel"
    >
      <!-- Multi-step form navigation -->
      <v-stepper v-model="currentStep" class="mb-6">
        <v-stepper-header>
          <v-stepper-item
            v-for="(step, index) in steps"
            :key="index"
            :value="index + 1"
            :complete="currentStep > index + 1"
            :title="step.title"
          ></v-stepper-item>
        </v-stepper-header>
        
        <v-divider class="my-4"></v-divider>
      </v-stepper>
      
      <!-- Step 1: Basic Information -->
      <v-window v-model="currentStep">
        <v-window-item :value="1">
          <form-section title="Basic Information" icon="mdi-information">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.reference"
                  label="Reference Number"
                  hint="Auto-generated if left empty"
                  persistent-hint
                  variant="outlined"
                  readonly
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.status"
                  label="Status"
                  :items="statusOptions"
                  variant="outlined"
                  :rules="[v => !!v || 'Status is required']"
                  required
                ></v-select>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.amount"
                  label="Loan Amount"
                  variant="outlined"
                  type="number"
                  prefix="$"
                  :rules="[
                    v => !!v || 'Amount is required',
                    v => v > 0 || 'Amount must be greater than 0'
                  ]"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.term"
                  label="Loan Term (months)"
                  variant="outlined"
                  type="number"
                  :rules="[
                    v => !!v || 'Term is required',
                    v => v > 0 || 'Term must be greater than 0'
                  ]"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.interest_rate"
                  label="Interest Rate (%)"
                  variant="outlined"
                  type="number"
                  step="0.01"
                  :rules="[
                    v => !!v || 'Interest rate is required',
                    v => v > 0 || 'Interest rate must be greater than 0'
                  ]"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.product_id"
                  label="Loan Product"
                  :items="productOptions"
                  variant="outlined"
                  :rules="[v => !!v || 'Loan product is required']"
                  required
                ></v-select>
              </v-col>
              
              <v-col cols="12">
                <v-textarea
                  v-model="formData.purpose"
                  label="Loan Purpose"
                  variant="outlined"
                  rows="3"
                  :rules="[v => !!v || 'Loan purpose is required']"
                  required
                ></v-textarea>
              </v-col>
            </v-row>
          </form-section>
          
          <div class="d-flex justify-end">
            <v-btn
              color="primary"
              @click="nextStep"
            >
              Next
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </div>
        </v-window-item>
        
        <!-- Step 2: Borrower Information -->
        <v-window-item :value="2">
          <form-section title="Borrower Information" icon="mdi-account">
            <v-row>
              <v-col cols="12" class="mb-4">
                <v-radio-group
                  v-model="borrowerType"
                  inline
                >
                  <v-radio
                    label="Existing Borrower"
                    value="existing"
                  ></v-radio>
                  <v-radio
                    label="New Borrower"
                    value="new"
                  ></v-radio>
                </v-radio-group>
              </v-col>
              
              <!-- Existing Borrower Selection -->
              <v-col v-if="borrowerType === 'existing'" cols="12">
                <v-autocomplete
                  v-model="formData.borrower_id"
                  label="Select Borrower"
                  :items="borrowerOptions"
                  variant="outlined"
                  :rules="[v => !!v || 'Borrower is required']"
                  required
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template v-slot:prepend>
                        <v-avatar color="primary" size="32">
                          <span class="text-white">{{ item.raw.name.charAt(0) }}</span>
                        </v-avatar>
                      </template>
                      <v-list-item-title>{{ item.raw.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ item.raw.email }}</v-list-item-subtitle>
                    </v-list-item>
                  </template>
                </v-autocomplete>
                
                <div v-if="formData.borrower_id" class="mt-4">
                  <v-card variant="outlined">
                    <v-card-text>
                      <div class="d-flex align-center mb-2">
                        <v-avatar color="primary" size="32" class="mr-2">
                          <span class="text-white">{{ selectedBorrower?.name.charAt(0) }}</span>
                        </v-avatar>
                        <div>
                          <div class="text-h6">{{ selectedBorrower?.name }}</div>
                          <div class="text-body-2">{{ selectedBorrower?.email }}</div>
                        </div>
                      </div>
                      
                      <v-divider class="my-3"></v-divider>
                      
                      <div class="d-flex flex-wrap">
                        <div class="mr-6 mb-2">
                          <div class="text-caption text-grey-darken-1">Phone</div>
                          <div>{{ selectedBorrower?.phone }}</div>
                        </div>
                        
                        <div class="mr-6 mb-2">
                          <div class="text-caption text-grey-darken-1">Address</div>
                          <div>{{ selectedBorrower?.address }}</div>
                        </div>
                        
                        <div class="mb-2">
                          <div class="text-caption text-grey-darken-1">Previous Applications</div>
                          <div>{{ selectedBorrower?.applications || 0 }}</div>
                        </div>
                      </div>
                    </v-card-text>
                    
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        variant="text"
                        color="primary"
                        @click="viewBorrower"
                      >
                        View Details
                      </v-btn>
                      <v-btn
                        variant="text"
                        color="primary"
                        @click="editBorrower"
                      >
                        Edit
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </div>
              </v-col>
              
              <!-- New Borrower Form -->
              <template v-if="borrowerType === 'new'">
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="newBorrower.first_name"
                    label="First Name"
                    variant="outlined"
                    :rules="[v => !!v || 'First name is required']"
                    required
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="newBorrower.last_name"
                    label="Last Name"
                    variant="outlined"
                    :rules="[v => !!v || 'Last name is required']"
                    required
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="newBorrower.email"
                    label="Email"
                    variant="outlined"
                    type="email"
                    :rules="[
                      v => !!v || 'Email is required',
                      v => /.+@.+\..+/.test(v) || 'Email must be valid'
                    ]"
                    required
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="newBorrower.phone"
                    label="Phone"
                    variant="outlined"
                    :rules="[v => !!v || 'Phone is required']"
                    required
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-text-field
                    v-model="newBorrower.address"
                    label="Address"
                    variant="outlined"
                    :rules="[v => !!v || 'Address is required']"
                    required
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="newBorrower.city"
                    label="City"
                    variant="outlined"
                    :rules="[v => !!v || 'City is required']"
                    required
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="newBorrower.state"
                    label="State"
                    variant="outlined"
                    :rules="[v => !!v || 'State is required']"
                    required
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="newBorrower.zip"
                    label="ZIP Code"
                    variant="outlined"
                    :rules="[v => !!v || 'ZIP code is required']"
                    required
                  ></v-text-field>
                </v-col>
              </template>
            </v-row>
          </form-section>
          
          <div class="d-flex justify-space-between">
            <v-btn
              variant="outlined"
              @click="prevStep"
            >
              <v-icon start>mdi-arrow-left</v-icon>
              Previous
            </v-btn>
            
            <v-btn
              color="primary"
              @click="nextStep"
            >
              Next
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </div>
        </v-window-item>
        
        <!-- Step 3: Broker Information -->
        <v-window-item :value="3">
          <form-section title="Broker Information" icon="mdi-account-tie">
            <v-row>
              <v-col cols="12">
                <v-select
                  v-model="formData.broker_id"
                  label="Select Broker"
                  :items="brokerOptions"
                  variant="outlined"
                  :rules="[v => !!v || 'Broker is required']"
                  required
                ></v-select>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.commission_rate"
                  label="Commission Rate (%)"
                  variant="outlined"
                  type="number"
                  step="0.01"
                  :rules="[
                    v => !!v || 'Commission rate is required',
                    v => v >= 0 || 'Commission rate must be non-negative'
                  ]"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.commission_amount"
                  label="Commission Amount"
                  variant="outlined"
                  type="number"
                  prefix="$"
                  readonly
                ></v-text-field>
              </v-col>
              
              <v-col cols="12">
                <v-textarea
                  v-model="formData.broker_notes"
                  label="Broker Notes"
                  variant="outlined"
                  rows="3"
                ></v-textarea>
              </v-col>
            </v-row>
          </form-section>
          
          <div class="d-flex justify-space-between">
            <v-btn
              variant="outlined"
              @click="prevStep"
            >
              <v-icon start>mdi-arrow-left</v-icon>
              Previous
            </v-btn>
            
            <v-btn
              color="primary"
              @click="nextStep"
            >
              Next
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </div>
        </v-window-item>
        
        <!-- Step 4: Documents -->
        <v-window-item :value="4">
          <form-section title="Documents" icon="mdi-file-document">
            <v-row>
              <v-col cols="12">
                <v-file-input
                  v-model="documents"
                  label="Upload Documents"
                  variant="outlined"
                  multiple
                  show-size
                  prepend-icon="mdi-paperclip"
                  accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                ></v-file-input>
              </v-col>
              
              <v-col cols="12">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-h6 mb-4">Required Documents</div>
                  
                  <v-list>
                    <v-list-item
                      v-for="(doc, index) in requiredDocuments"
                      :key="index"
                      :title="doc.name"
                      :subtitle="doc.description"
                    >
                      <template v-slot:prepend>
                        <v-icon :color="doc.uploaded ? 'success' : 'grey'">
                          {{ doc.uploaded ? 'mdi-check-circle' : 'mdi-circle-outline' }}
                        </v-icon>
                      </template>
                      
                      <template v-slot:append>
                        <v-btn
                          variant="text"
                          color="primary"
                          size="small"
                          @click="uploadDocument(doc)"
                        >
                          {{ doc.uploaded ? 'Replace' : 'Upload' }}
                        </v-btn>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>
            </v-row>
          </form-section>
          
          <div class="d-flex justify-space-between">
            <v-btn
              variant="outlined"
              @click="prevStep"
            >
              <v-icon start>mdi-arrow-left</v-icon>
              Previous
            </v-btn>
            
            <v-btn
              color="primary"
              type="submit"
            >
              {{ submitText }}
            </v-btn>
          </div>
        </v-window-item>
      </v-window>
    </base-form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import BaseForm from '@/components/common/BaseForm.vue'
import FormSection from '@/components/common/FormSection.vue'

// Props
const props = defineProps({
  // Form state
  modelValue: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  },
  serverErrors: {
    type: Object,
    default: () => ({})
  },
  
  // Form mode
  mode: {
    type: String,
    default: 'create',
    validator: (value) => ['create', 'edit'].includes(value)
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])

// Router
const router = useRouter()

// Form steps
const steps = [
  { title: 'Basic Information' },
  { title: 'Borrower' },
  { title: 'Broker' },
  { title: 'Documents' }
]

// Form state
const currentStep = ref(1)
const formData = ref({
  reference: '',
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
  broker_notes: '',
  ...props.modelValue
})

// Borrower state
const borrowerType = ref('existing')
const newBorrower = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address: '',
  city: '',
  state: '',
  zip: ''
})

// Document state
const documents = ref([])
const requiredDocuments = ref([
  { name: 'ID Verification', description: 'Government-issued ID', uploaded: false },
  { name: 'Proof of Income', description: 'Last 3 months of pay stubs', uploaded: false },
  { name: 'Bank Statements', description: 'Last 3 months of statements', uploaded: false },
  { name: 'Property Valuation', description: 'For secured loans', uploaded: false }
])

// Options for select fields
const statusOptions = [
  { title: 'Draft', value: 'draft' },
  { title: 'Submitted', value: 'submitted' },
  { title: 'In Review', value: 'in_review' },
  { title: 'Approved', value: 'approved' },
  { title: 'Rejected', value: 'rejected' },
  { title: 'Completed', value: 'completed' }
]

// Mock product options (would come from API)
const productOptions = [
  { title: 'Personal Loan', value: 1 },
  { title: 'Home Loan', value: 2 },
  { title: 'Business Loan', value: 3 },
  { title: 'Auto Loan', value: 4 }
]

// Mock borrower options (would come from API)
const borrowerOptions = [
  { title: 'John Doe', value: 1, name: 'John Doe', email: 'john.doe@example.com', phone: '(555) 123-4567', address: '123 Main St, Anytown, CA 12345', applications: 2 },
  { title: 'Jane Smith', value: 2, name: 'Jane Smith', email: 'jane.smith@example.com', phone: '(555) 987-6543', address: '456 Oak Ave, Somewhere, CA 67890', applications: 1 },
  { title: 'Robert Johnson', value: 3, name: 'Robert Johnson', email: 'robert.johnson@example.com', phone: '(555) 456-7890', address: '789 Pine St, Nowhere, CA 54321', applications: 0 }
]

// Mock broker options (would come from API)
const brokerOptions = [
  { title: 'John Smith', value: 1 },
  { title: 'Sarah Johnson', value: 2 },
  { title: 'Michael Brown', value: 3 },
  { title: 'Emily Davis', value: 4 }
]

// Computed
const submitText = computed(() => {
  return props.mode === 'create' ? 'Create Application' : 'Update Application'
})

const selectedBorrower = computed(() => {
  if (!formData.value.borrower_id) return null
  return borrowerOptions.find(b => b.value === formData.value.borrower_id)
})

// Methods
const nextStep = () => {
  if (currentStep.value < steps.length) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const handleSubmit = () => {
  // Prepare final data
  let finalData = { ...formData.value }
  
  // If creating a new borrower, add that data
  if (borrowerType.value === 'new') {
    finalData.new_borrower = newBorrower.value
    finalData.borrower_id = null
  }
  
  // Calculate commission amount if not set
  if (finalData.commission_rate && finalData.amount && !finalData.commission_amount) {
    finalData.commission_amount = (finalData.amount * finalData.commission_rate) / 100
  }
  
  emit('submit', finalData)
}

const handleCancel = () => {
  emit('cancel')
}

const viewBorrower = () => {
  if (formData.value.borrower_id) {
    router.push({ name: 'borrower-detail', params: { id: formData.value.borrower_id } })
  }
}

const editBorrower = () => {
  if (formData.value.borrower_id) {
    router.push({ name: 'borrower-edit', params: { id: formData.value.borrower_id } })
  }
}

const uploadDocument = (doc) => {
  // This would open a file picker or handle document upload
  // For now, just toggle the uploaded state for demonstration
  doc.uploaded = !doc.uploaded
}

// Watchers
watch(formData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

// Calculate commission amount when rate or amount changes
watch([() => formData.value.commission_rate, () => formData.value.amount], ([newRate, newAmount]) => {
  if (newRate && newAmount) {
    formData.value.commission_amount = (newAmount * newRate) / 100
  }
})

// Initialize form data from props
watch(() => props.modelValue, (newValue) => {
  formData.value = { ...formData.value, ...newValue }
}, { immediate: true, deep: true })
</script>

<style scoped>
.application-form {
  width: 100%;
}
</style>
