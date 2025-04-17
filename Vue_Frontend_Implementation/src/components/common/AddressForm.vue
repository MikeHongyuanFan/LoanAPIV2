<template>
  <div class="address-form">
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="localAddress.address_line1"
          :label="`${labelPrefix}Address Line 1`"
          variant="outlined"
          :rules="[v => !required || !!v || 'Address is required']"
          :required="required"
          :disabled="disabled"
          :readonly="readonly"
          @update:model-value="updateAddress"
        ></v-text-field>
      </v-col>
      
      <v-col cols="12">
        <v-text-field
          v-model="localAddress.address_line2"
          :label="`${labelPrefix}Address Line 2`"
          variant="outlined"
          :disabled="disabled"
          :readonly="readonly"
          @update:model-value="updateAddress"
        ></v-text-field>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localAddress.city"
          :label="`${labelPrefix}City`"
          variant="outlined"
          :rules="[v => !required || !!v || 'City is required']"
          :required="required"
          :disabled="disabled"
          :readonly="readonly"
          @update:model-value="updateAddress"
        ></v-text-field>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-select
          v-model="localAddress.state"
          :label="`${labelPrefix}State`"
          :items="stateOptions"
          variant="outlined"
          :rules="[v => !required || !!v || 'State is required']"
          :required="required"
          :disabled="disabled"
          :readonly="readonly"
          @update:model-value="updateAddress"
        ></v-select>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localAddress.zip_code"
          :label="`${labelPrefix}ZIP Code`"
          variant="outlined"
          :rules="[
            v => !required || !!v || 'ZIP code is required',
            v => !v || /^\d{5}(-\d{4})?$/.test(v) || 'ZIP code must be valid (XXXXX or XXXXX-XXXX)'
          ]"
          :required="required"
          :disabled="disabled"
          :readonly="readonly"
          @update:model-value="updateAddress"
        ></v-text-field>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-select
          v-model="localAddress.country"
          :label="`${labelPrefix}Country`"
          :items="countryOptions"
          variant="outlined"
          :rules="[v => !required || !!v || 'Country is required']"
          :required="required"
          :disabled="disabled"
          :readonly="readonly"
          @update:model-value="updateAddress"
        ></v-select>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// Props
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      address_line1: '',
      address_line2: '',
      city: '',
      state: '',
      zip_code: '',
      country: 'US'
    })
  },
  labelPrefix: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'change'])

// Local state
const localAddress = ref({ ...props.modelValue })

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

// Methods
const updateAddress = () => {
  emit('update:modelValue', { ...localAddress.value })
  emit('change', { ...localAddress.value })
}

// Computed
const formattedAddress = computed(() => {
  const address = localAddress.value
  const parts = []
  
  if (address.address_line1) {
    parts.push(address.address_line1)
  }
  
  if (address.address_line2) {
    parts.push(address.address_line2)
  }
  
  const cityStateZip = []
  if (address.city) {
    cityStateZip.push(address.city)
  }
  
  if (address.state) {
    cityStateZip.push(address.state)
  }
  
  if (address.zip_code) {
    cityStateZip.push(address.zip_code)
  }
  
  if (cityStateZip.length > 0) {
    parts.push(cityStateZip.join(', '))
  }
  
  if (address.country && address.country !== 'US') {
    const country = countryOptions.find(c => c.value === address.country)
    if (country) {
      parts.push(country.title)
    } else {
      parts.push(address.country)
    }
  }
  
  return parts.join('\n')
})

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  localAddress.value = { ...newValue }
}, { deep: true })

// Expose methods and computed properties
defineExpose({
  formattedAddress
})
</script>

<style scoped>
.address-form {
  width: 100%;
}
</style>
