<template>
  <div class="borrower-form">
    <base-form
      v-model="formData"
      :loading="loading"
      :server-errors="serverErrors"
      :submit-text="submitText"
      @submit="handleSubmit"
      @cancel="handleCancel"
    >
      <!-- Borrower Type Selection -->
      <form-section title="Borrower Type" icon="mdi-account-details">
        <v-row>
          <v-col cols="12">
            <v-radio-group
              v-model="formData.type"
              inline
              :rules="[v => !!v || 'Borrower type is required']"
              required
            >
              <v-radio
                label="Individual"
                value="individual"
              ></v-radio>
              <v-radio
                label="Business"
                value="business"
              ></v-radio>
              <v-radio
                label="Guarantor"
                value="guarantor"
              ></v-radio>
            </v-radio-group>
          </v-col>
        </v-row>
      </form-section>
      
      <!-- Personal Information -->
      <form-section 
        title="Personal Information" 
        icon="mdi-account" 
        :subtitle="formData.type === 'business' ? 'Primary Contact' : ''"
      >
        <v-row>
          <!-- Individual or Guarantor Fields -->
          <template v-if="formData.type !== 'business'">
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.first_name"
                label="First Name"
                variant="outlined"
                :rules="[v => !!v || 'First name is required']"
                required
                @input="checkForDuplicates"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.last_name"
                label="Last Name"
                variant="outlined"
                :rules="[v => !!v || 'Last name is required']"
                required
                @input="checkForDuplicates"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.date_of_birth"
                label="Date of Birth"
                variant="outlined"
                type="date"
                :rules="[v => !!v || 'Date of birth is required']"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.gender"
                label="Gender"
                :items="genderOptions"
                variant="outlined"
              ></v-select>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.ssn"
                label="Social Security Number"
                variant="outlined"
                :rules="[
                  v => !v || /^\d{3}-\d{2}-\d{4}$/.test(v) || 'SSN must be in format XXX-XX-XXXX'
                ]"
                hint="Format: XXX-XX-XXXX"
                persistent-hint
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.marital_status"
                label="Marital Status"
                :items="maritalStatusOptions"
                variant="outlined"
              ></v-select>
            </v-col>
          </template>
          
          <!-- Business Fields -->
          <template v-else>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.business_name"
                label="Business Name"
                variant="outlined"
                :rules="[v => !!v || 'Business name is required']"
                required
                @input="checkForDuplicates"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.tax_id"
                label="Tax ID / EIN"
                variant="outlined"
                :rules="[
                  v => !!v || 'Tax ID is required',
                  v => /^\d{2}-\d{7}$/.test(v) || 'Tax ID must be in format XX-XXXXXXX'
                ]"
                hint="Format: XX-XXXXXXX"
                persistent-hint
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.business_type"
                label="Business Type"
                variant="outlined"
                :rules="[v => !!v || 'Business type is required']"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.year_established"
                label="Year Established"
                variant="outlined"
                type="number"
                :rules="[
                  v => !!v || 'Year established is required',
                  v => (v && v <= new Date().getFullYear()) || 'Year cannot be in the future'
                ]"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12">
              <v-divider class="my-4"></v-divider>
              <p class="text-subtitle-1 mb-4">Primary Contact</p>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.contact_first_name"
                label="Contact First Name"
                variant="outlined"
                :rules="[v => !!v || 'Contact first name is required']"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.contact_last_name"
                label="Contact Last Name"
                variant="outlined"
                :rules="[v => !!v || 'Contact last name is required']"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.contact_title"
                label="Contact Title"
                variant="outlined"
                :rules="[v => !!v || 'Contact title is required']"
                required
              ></v-text-field>
            </v-col>
          </template>
        </v-row>
      </form-section>
      
      <!-- Contact Information -->
      <form-section title="Contact Information" icon="mdi-phone">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.email"
              label="Email"
              variant="outlined"
              type="email"
              :rules="[
                v => !!v || 'Email is required',
                v => /.+@.+\..+/.test(v) || 'Email must be valid'
              ]"
              required
              @input="checkForDuplicates"
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.phone"
              label="Phone"
              variant="outlined"
              :rules="[
                v => !!v || 'Phone is required',
                v => /^\(\d{3}\) \d{3}-\d{4}$/.test(v) || 'Phone must be in format (XXX) XXX-XXXX'
              ]"
              hint="Format: (XXX) XXX-XXXX"
              persistent-hint
              required
              @input="checkForDuplicates"
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.mobile_phone"
              label="Mobile Phone"
              variant="outlined"
              :rules="[
                v => !v || /^\(\d{3}\) \d{3}-\d{4}$/.test(v) || 'Mobile phone must be in format (XXX) XXX-XXXX'
              ]"
              hint="Format: (XXX) XXX-XXXX"
              persistent-hint
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.fax"
              label="Fax"
              variant="outlined"
              :rules="[
                v => !v || /^\(\d{3}\) \d{3}-\d{4}$/.test(v) || 'Fax must be in format (XXX) XXX-XXXX'
              ]"
              hint="Format: (XXX) XXX-XXXX"
              persistent-hint
            ></v-text-field>
          </v-col>
          
          <v-col cols="12">
            <v-text-field
              v-model="formData.website"
              label="Website"
              variant="outlined"
              :rules="[
                v => !v || /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(v) || 'Website must be valid'
              ]"
              hint="e.g., https://example.com"
              persistent-hint
            ></v-text-field>
          </v-col>
        </v-row>
      </form-section>
      
      <!-- Address Information -->
      <form-section title="Address Information" icon="mdi-map-marker">
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="formData.address_line1"
              label="Address Line 1"
              variant="outlined"
              :rules="[v => !!v || 'Address is required']"
              required
            ></v-text-field>
          </v-col>
          
          <v-col cols="12">
            <v-text-field
              v-model="formData.address_line2"
              label="Address Line 2"
              variant="outlined"
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.city"
              label="City"
              variant="outlined"
              :rules="[v => !!v || 'City is required']"
              required
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-select
              v-model="formData.state"
              label="State"
              :items="stateOptions"
              variant="outlined"
              :rules="[v => !!v || 'State is required']"
              required
            ></v-select>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.zip_code"
              label="ZIP Code"
              variant="outlined"
              :rules="[
                v => !!v || 'ZIP code is required',
                v => /^\d{5}(-\d{4})?$/.test(v) || 'ZIP code must be valid (XXXXX or XXXXX-XXXX)'
              ]"
              required
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-select
              v-model="formData.country"
              label="Country"
              :items="countryOptions"
              variant="outlined"
              :rules="[v => !!v || 'Country is required']"
              required
            ></v-select>
          </v-col>
          
          <v-col cols="12">
            <v-checkbox
              v-model="formData.is_mailing_address_different"
              label="Mailing address is different from physical address"
            ></v-checkbox>
          </v-col>
        </v-row>
        
        <!-- Mailing Address -->
        <v-expand-transition>
          <div v-if="formData.is_mailing_address_different">
            <v-divider class="my-4"></v-divider>
            <p class="text-subtitle-1 mb-4">Mailing Address</p>
            
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.mailing_address_line1"
                  label="Address Line 1"
                  variant="outlined"
                  :rules="[v => !formData.is_mailing_address_different || !!v || 'Mailing address is required']"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12">
                <v-text-field
                  v-model="formData.mailing_address_line2"
                  label="Address Line 2"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.mailing_city"
                  label="City"
                  variant="outlined"
                  :rules="[v => !formData.is_mailing_address_different || !!v || 'City is required']"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.mailing_state"
                  label="State"
                  :items="stateOptions"
                  variant="outlined"
                  :rules="[v => !formData.is_mailing_address_different || !!v || 'State is required']"
                  required
                ></v-select>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.mailing_zip_code"
                  label="ZIP Code"
                  variant="outlined"
                  :rules="[
                    v => !formData.is_mailing_address_different || !!v || 'ZIP code is required',
                    v => !formData.is_mailing_address_different || !v || /^\d{5}(-\d{4})?$/.test(v) || 'ZIP code must be valid (XXXXX or XXXXX-XXXX)'
                  ]"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.mailing_country"
                  label="Country"
                  :items="countryOptions"
                  variant="outlined"
                  :rules="[v => !formData.is_mailing_address_different || !!v || 'Country is required']"
                  required
                ></v-select>
              </v-col>
            </v-row>
          </div>
        </v-expand-transition>
      </form-section>
      
      <!-- Additional Information -->
      <form-section title="Additional Information" icon="mdi-information" collapsible>
        <v-row>
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
            <v-select
              v-model="formData.source"
              label="Source"
              :items="sourceOptions"
              variant="outlined"
            ></v-select>
          </v-col>
          
          <v-col cols="12">
            <v-textarea
              v-model="formData.notes"
              label="Notes"
              variant="outlined"
              rows="3"
            ></v-textarea>
          </v-col>
        </v-row>
      </form-section>
      
      <!-- Duplicate Detection Alert -->
      <v-alert
        v-if="duplicates.length > 0"
        type="warning"
        variant="tonal"
        class="mt-6"
      >
        <div class="font-weight-medium mb-2">Potential duplicate borrowers found:</div>
        <v-list density="compact">
          <v-list-item
            v-for="duplicate in duplicates"
            :key="duplicate.id"
            :title="duplicate.name"
            :subtitle="duplicate.email"
          >
            <template v-slot:prepend>
              <v-avatar color="warning" size="32">
                <span class="text-white">{{ duplicate.name.charAt(0) }}</span>
              </v-avatar>
            </template>
            
            <template v-slot:append>
              <v-btn
                color="primary"
                variant="text"
                size="small"
                @click="viewDuplicate(duplicate)"
              >
                View
              </v-btn>
            </template>
          </v-list-item>
        </v-list>
        
        <div class="d-flex justify-end mt-2">
          <v-btn
            color="primary"
            variant="text"
            @click="ignoreDuplicates"
          >
            Ignore and Continue
          </v-btn>
        </div>
      </v-alert>
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

// Form state
const formData = ref({
  type: 'individual',
  status: 'active',
  first_name: '',
  last_name: '',
  date_of_birth: '',
  gender: '',
  ssn: '',
  marital_status: '',
  business_name: '',
  tax_id: '',
  business_type: '',
  year_established: '',
  contact_first_name: '',
  contact_last_name: '',
  contact_title: '',
  email: '',
  phone: '',
  mobile_phone: '',
  fax: '',
  website: '',
  address_line1: '',
  address_line2: '',
  city: '',
  state: '',
  zip_code: '',
  country: 'US',
  is_mailing_address_different: false,
  mailing_address_line1: '',
  mailing_address_line2: '',
  mailing_city: '',
  mailing_state: '',
  mailing_zip_code: '',
  mailing_country: 'US',
  source: '',
  notes: '',
  ...props.modelValue
})

// Duplicate detection
const duplicates = ref([])
const duplicateCheckTimeout = ref(null)
const duplicateCheckIgnored = ref(false)

// Options for select fields
const genderOptions = [
  { title: 'Male', value: 'male' },
  { title: 'Female', value: 'female' },
  { title: 'Non-binary', value: 'non-binary' },
  { title: 'Prefer not to say', value: 'not_specified' }
]

const maritalStatusOptions = [
  { title: 'Single', value: 'single' },
  { title: 'Married', value: 'married' },
  { title: 'Divorced', value: 'divorced' },
  { title: 'Widowed', value: 'widowed' },
  { title: 'Separated', value: 'separated' }
]

const statusOptions = [
  { title: 'Active', value: 'active' },
  { title: 'Inactive', value: 'inactive' },
  { title: 'Pending', value: 'pending' },
  { title: 'Blocked', value: 'blocked' }
]

const sourceOptions = [
  { title: 'Website', value: 'website' },
  { title: 'Referral', value: 'referral' },
  { title: 'Direct', value: 'direct' },
  { title: 'Partner', value: 'partner' },
  { title: 'Advertisement', value: 'advertisement' },
  { title: 'Other', value: 'other' }
]

// Mock state options (would come from API)
const stateOptions = [
  { title: 'Alabama', value: 'AL' },
  { title: 'Alaska', value: 'AK' },
  { title: 'Arizona', value: 'AZ' },
  { title: 'Arkansas', value: 'AR' },
  { title: 'California', value: 'CA' },
  { title: 'Colorado', value: 'CO' },
  { title: 'Connecticut', value: 'CT' },
  { title: 'Delaware', value: 'DE' },
  { title: 'Florida', value: 'FL' },
  { title: 'Georgia', value: 'GA' },
  { title: 'Hawaii', value: 'HI' },
  { title: 'Idaho', value: 'ID' },
  { title: 'Illinois', value: 'IL' },
  { title: 'Indiana', value: 'IN' },
  { title: 'Iowa', value: 'IA' },
  { title: 'Kansas', value: 'KS' },
  { title: 'Kentucky', value: 'KY' },
  { title: 'Louisiana', value: 'LA' },
  { title: 'Maine', value: 'ME' },
  { title: 'Maryland', value: 'MD' },
  { title: 'Massachusetts', value: 'MA' },
  { title: 'Michigan', value: 'MI' },
  { title: 'Minnesota', value: 'MN' },
  { title: 'Mississippi', value: 'MS' },
  { title: 'Missouri', value: 'MO' },
  { title: 'Montana', value: 'MT' },
  { title: 'Nebraska', value: 'NE' },
  { title: 'Nevada', value: 'NV' },
  { title: 'New Hampshire', value: 'NH' },
  { title: 'New Jersey', value: 'NJ' },
  { title: 'New Mexico', value: 'NM' },
  { title: 'New York', value: 'NY' },
  { title: 'North Carolina', value: 'NC' },
  { title: 'North Dakota', value: 'ND' },
  { title: 'Ohio', value: 'OH' },
  { title: 'Oklahoma', value: 'OK' },
  { title: 'Oregon', value: 'OR' },
  { title: 'Pennsylvania', value: 'PA' },
  { title: 'Rhode Island', value: 'RI' },
  { title: 'South Carolina', value: 'SC' },
  { title: 'South Dakota', value: 'SD' },
  { title: 'Tennessee', value: 'TN' },
  { title: 'Texas', value: 'TX' },
  { title: 'Utah', value: 'UT' },
  { title: 'Vermont', value: 'VT' },
  { title: 'Virginia', value: 'VA' },
  { title: 'Washington', value: 'WA' },
  { title: 'West Virginia', value: 'WV' },
  { title: 'Wisconsin', value: 'WI' },
  { title: 'Wyoming', value: 'WY' }
]

// Mock country options (would come from API)
const countryOptions = [
  { title: 'United States', value: 'US' },
  { title: 'Canada', value: 'CA' },
  { title: 'Mexico', value: 'MX' },
  { title: 'United Kingdom', value: 'GB' }
]

// Computed
const submitText = computed(() => {
  return props.mode === 'create' ? 'Create Borrower' : 'Update Borrower'
})

// Methods
const handleSubmit = () => {
  // Check for duplicates one last time if not already ignored
  if (!duplicateCheckIgnored.value) {
    checkForDuplicatesImmediate()
    
    // If duplicates are found, don't submit yet
    if (duplicates.value.length > 0) {
      return
    }
  }
  
  // Prepare final data
  let finalData = { ...formData.value }
  
  // Set name based on type
  if (finalData.type === 'business') {
    finalData.name = finalData.business_name
  } else {
    finalData.name = `${finalData.first_name} ${finalData.last_name}`
  }
  
  emit('submit', finalData)
}

const handleCancel = () => {
  emit('cancel')
}

const checkForDuplicates = () => {
  // Clear any existing timeout
  if (duplicateCheckTimeout.value) {
    clearTimeout(duplicateCheckTimeout.value)
  }
  
  // Don't check if user has already ignored duplicates
  if (duplicateCheckIgnored.value) {
    return
  }
  
  // Set a new timeout to avoid too many API calls
  duplicateCheckTimeout.value = setTimeout(() => {
    checkForDuplicatesImmediate()
  }, 500)
}

const checkForDuplicatesImmediate = async () => {
  // Only check if we have enough data
  if (
    (formData.value.type === 'individual' && (!formData.value.first_name || !formData.value.last_name)) ||
    (formData.value.type === 'business' && !formData.value.business_name) ||
    (!formData.value.email && !formData.value.phone)
  ) {
    duplicates.value = []
    return
  }
  
  try {
    // This would be an API call in a real application
    // const response = await borrowerService.checkDuplicates({
    //   type: formData.value.type,
    //   first_name: formData.value.first_name,
    //   last_name: formData.value.last_name,
    //   business_name: formData.value.business_name,
    //   email: formData.value.email,
    //   phone: formData.value.phone
    // })
    
    // Mock data for demonstration
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Mock duplicate detection based on form data
    if (
      (formData.value.type === 'individual' && 
       formData.value.first_name === 'John' && 
       formData.value.last_name === 'Doe') ||
      (formData.value.type === 'business' && 
       formData.value.business_name === 'Acme Corporation') ||
      formData.value.email === 'john.doe@example.com' ||
      formData.value.phone === '(555) 123-4567'
    ) {
      duplicates.value = [
        {
          id: 1,
          name: 'John Doe',
          email: 'john.doe@example.com',
          phone: '(555) 123-4567',
          address: '123 Main St, New York, NY 10001',
          type: 'individual',
          status: 'active'
        }
      ]
    } else {
      duplicates.value = []
    }
  } catch (error) {
    console.error('Error checking for duplicates:', error)
    duplicates.value = []
  }
}

const viewDuplicate = (duplicate) => {
  router.push({ name: 'borrower-detail', params: { id: duplicate.id } })
}

const ignoreDuplicates = () => {
  duplicateCheckIgnored.value = true
  duplicates.value = []
}

// Watchers
watch(formData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

// Initialize form data from props
watch(() => props.modelValue, (newValue) => {
  formData.value = { ...formData.value, ...newValue }
}, { immediate: true, deep: true })

// Reset duplicate check when type changes
watch(() => formData.value.type, () => {
  duplicates.value = []
  duplicateCheckIgnored.value = false
})

// Clean up on unmount
onBeforeUnmount(() => {
  if (duplicateCheckTimeout.value) {
    clearTimeout(duplicateCheckTimeout.value)
  }
})
</script>

<style scoped>
.borrower-form {
  width: 100%;
}
</style>
