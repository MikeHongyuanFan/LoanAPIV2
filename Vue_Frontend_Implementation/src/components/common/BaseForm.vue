<template>
  <div class="base-form">
    <v-form
      ref="form"
      v-model="valid"
      @submit.prevent="handleSubmit"
      :disabled="disabled || loading"
    >
      <!-- Form Content -->
      <slot></slot>
      
      <!-- Validation Summary -->
      <v-alert
        v-if="showValidationSummary && hasValidationErrors"
        type="error"
        variant="tonal"
        class="mt-4"
        closable
      >
        <div class="font-weight-medium mb-2">Please fix the following errors:</div>
        <ul class="ml-4">
          <li v-for="(error, index) in validationErrors" :key="index">
            {{ error }}
          </li>
        </ul>
      </v-alert>
      
      <!-- Server Error -->
      <v-alert
        v-if="serverError"
        type="error"
        variant="tonal"
        class="mt-4"
        closable
        @click:close="serverError = null"
      >
        {{ serverError }}
      </v-alert>
      
      <!-- Form Actions -->
      <div 
        v-if="$slots.actions || showDefaultActions" 
        class="base-form__actions"
        :class="actionsClass"
      >
        <slot name="actions">
          <v-btn
            v-if="showCancelButton"
            variant="outlined"
            :disabled="loading"
            @click="handleCancel"
          >
            {{ cancelText }}
          </v-btn>
          
          <v-btn
            type="submit"
            color="primary"
            :loading="loading"
            :disabled="disableSubmit || (validateOnSubmit ? false : !valid)"
          >
            {{ submitText }}
          </v-btn>
        </slot>
      </div>
    </v-form>
  </div>
</template>

<script setup>
import { ref, computed, provide } from 'vue'

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
  disabled: {
    type: Boolean,
    default: false
  },
  serverErrors: {
    type: Object,
    default: () => ({})
  },
  
  // Validation
  validateOnSubmit: {
    type: Boolean,
    default: false
  },
  showValidationSummary: {
    type: Boolean,
    default: true
  },
  
  // Actions
  showDefaultActions: {
    type: Boolean,
    default: true
  },
  actionsClass: {
    type: String,
    default: 'd-flex justify-end gap-3 mt-6'
  },
  submitText: {
    type: String,
    default: 'Submit'
  },
  showCancelButton: {
    type: Boolean,
    default: true
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  disableSubmit: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits([
  'update:modelValue',
  'submit',
  'cancel',
  'validation'
])

// Refs
const form = ref(null)
const valid = ref(true)
const validationErrors = ref([])
const serverError = ref(null)
const formData = ref({ ...props.modelValue })

// Computed
const hasValidationErrors = computed(() => validationErrors.value.length > 0)

// Methods
const validate = async () => {
  const { valid: isValid, errors } = await form.value.validate()
  validationErrors.value = errors?.map(e => e.errorMessages).flat() || []
  emit('validation', { valid: isValid, errors: validationErrors.value })
  return isValid
}

const reset = () => {
  form.value?.reset()
  validationErrors.value = []
  serverError.value = null
}

const resetValidation = () => {
  form.value?.resetValidation()
  validationErrors.value = []
  serverError.value = null
}

const handleSubmit = async () => {
  // Clear previous errors
  validationErrors.value = []
  serverError.value = null
  
  // Validate if needed
  let isValid = true
  if (props.validateOnSubmit) {
    isValid = await validate()
  }
  
  if (isValid) {
    emit('submit', formData.value)
  }
}

const handleCancel = () => {
  emit('cancel')
}

const setFieldValue = (field, value) => {
  formData.value = {
    ...formData.value,
    [field]: value
  }
  emit('update:modelValue', formData.value)
}

// Watch for server errors
watch(
  () => props.serverErrors,
  (newErrors) => {
    if (newErrors && Object.keys(newErrors).length > 0) {
      // Handle field-specific errors
      const fieldErrors = []
      
      Object.entries(newErrors).forEach(([field, errors]) => {
        if (field === 'non_field_errors' || field === 'detail') {
          // These are general errors, not tied to a specific field
          serverError.value = Array.isArray(errors) ? errors.join(' ') : errors
        } else {
          // Field-specific errors
          const errorMessage = Array.isArray(errors) ? errors.join(' ') : errors
          fieldErrors.push(`${field.replace('_', ' ')}: ${errorMessage}`)
        }
      })
      
      validationErrors.value = fieldErrors
    } else {
      serverError.value = null
      validationErrors.value = []
    }
  },
  { deep: true }
)

// Watch for model changes
watch(
  () => props.modelValue,
  (newValue) => {
    formData.value = { ...newValue }
  },
  { deep: true }
)

// Provide form context to child components
provide('formContext', {
  setFieldValue,
  formData,
  disabled: computed(() => props.disabled || props.loading)
})

// Expose methods to parent
defineExpose({
  validate,
  reset,
  resetValidation,
  form
})
</script>

<style scoped>
.base-form {
  width: 100%;
}
</style>
