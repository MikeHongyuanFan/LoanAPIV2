<template>
  <v-dialog
    v-model="localModelValue"
    :max-width="maxWidth"
    :persistent="persistent"
    :scrollable="scrollable"
    :fullscreen="fullscreen"
    :transition="transition"
    @click:outside="handleClickOutside"
    @keydown.esc="handleEscKey"
  >
    <v-card :class="['base-modal', cardClass]">
      <!-- Modal Header -->
      <v-card-item v-if="$slots.header || title" class="base-modal__header">
        <slot name="header">
          <v-card-title class="text-h5">{{ title }}</v-card-title>
          <template v-slot:append>
            <v-btn
              v-if="showCloseButton"
              icon="mdi-close"
              variant="text"
              size="small"
              @click="close"
            ></v-btn>
          </template>
        </slot>
      </v-card-item>
      
      <!-- Modal Content -->
      <v-card-text :class="['base-modal__content', contentClass]">
        <slot></slot>
      </v-card-text>
      
      <!-- Modal Footer -->
      <v-card-actions v-if="$slots.footer || showDefaultFooter" class="base-modal__footer">
        <slot name="footer">
          <v-spacer></v-spacer>
          <v-btn
            v-if="showCancelButton"
            variant="outlined"
            :disabled="loading"
            @click="handleCancel"
          >
            {{ cancelText }}
          </v-btn>
          <v-btn
            v-if="showConfirmButton"
            color="primary"
            :loading="loading"
            @click="handleConfirm"
          >
            {{ confirmText }}
          </v-btn>
        </slot>
      </v-card-actions>
      
      <!-- Loading Overlay -->
      <v-overlay
        v-if="loading"
        :model-value="loading"
        class="align-center justify-center"
        contained
      >
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-overlay>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// Props
const props = defineProps({
  // Dialog state
  modelValue: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  
  // Dialog appearance
  title: {
    type: String,
    default: ''
  },
  maxWidth: {
    type: [String, Number],
    default: 600
  },
  fullscreen: {
    type: Boolean,
    default: false
  },
  scrollable: {
    type: Boolean,
    default: false
  },
  transition: {
    type: String,
    default: 'dialog-transition'
  },
  cardClass: {
    type: String,
    default: ''
  },
  contentClass: {
    type: String,
    default: ''
  },
  
  // Dialog behavior
  persistent: {
    type: Boolean,
    default: false
  },
  hideOnClickOutside: {
    type: Boolean,
    default: true
  },
  hideOnEsc: {
    type: Boolean,
    default: true
  },
  
  // Dialog controls
  showCloseButton: {
    type: Boolean,
    default: true
  },
  showDefaultFooter: {
    type: Boolean,
    default: true
  },
  showCancelButton: {
    type: Boolean,
    default: true
  },
  showConfirmButton: {
    type: Boolean,
    default: true
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  }
})

// Emits
const emit = defineEmits([
  'update:modelValue',
  'cancel',
  'confirm',
  'close'
])

// Local state
const localModelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Methods
const close = () => {
  localModelValue.value = false
  emit('close')
}

const handleCancel = () => {
  emit('cancel')
  if (!props.persistent) {
    close()
  }
}

const handleConfirm = () => {
  emit('confirm')
}

const handleClickOutside = () => {
  if (props.hideOnClickOutside && !props.persistent && !props.loading) {
    close()
  }
}

const handleEscKey = () => {
  if (props.hideOnEsc && !props.persistent && !props.loading) {
    close()
  }
}

// Expose methods to parent
defineExpose({
  close
})
</script>

<style scoped>
.base-modal__header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.base-modal__content {
  padding: 24px;
}

.base-modal__footer {
  padding: 16px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}
</style>
