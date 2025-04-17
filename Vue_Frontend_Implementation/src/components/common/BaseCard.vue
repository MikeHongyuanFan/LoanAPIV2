<template>
  <v-card
    :class="[
      'base-card',
      { 'base-card--clickable': clickable },
      { 'base-card--hover': hover },
      elevationClass
    ]"
    :variant="variant"
    :rounded="rounded"
    :border="border"
    @click="handleClick"
  >
    <!-- Card Header -->
    <div v-if="$slots.header || title || subtitle" class="base-card__header">
      <slot name="header">
        <v-card-item>
          <template v-slot:prepend v-if="$slots.icon || icon">
            <slot name="icon">
              <v-avatar
                :color="iconColor || 'primary'"
                :size="iconSize"
                :rounded="iconRounded"
                class="mr-4"
              >
                <v-icon :size="iconSize * 0.6">{{ icon }}</v-icon>
              </v-avatar>
            </slot>
          </template>
          
          <v-card-title v-if="title">{{ title }}</v-card-title>
          <v-card-subtitle v-if="subtitle">{{ subtitle }}</v-card-subtitle>
          
          <template v-slot:append v-if="$slots.action">
            <slot name="action"></slot>
          </template>
        </v-card-item>
      </slot>
    </div>
    
    <!-- Card Media -->
    <div v-if="$slots.media" class="base-card__media">
      <slot name="media"></slot>
    </div>
    
    <!-- Card Content -->
    <v-card-text v-if="$slots.default" :class="contentClass">
      <slot></slot>
    </v-card-text>
    
    <!-- Card Footer -->
    <v-card-actions v-if="$slots.footer" class="base-card__footer">
      <slot name="footer"></slot>
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
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  // Card appearance
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'elevated',
    validator: (value) => ['elevated', 'flat', 'tonal', 'outlined', 'text'].includes(value)
  },
  elevation: {
    type: [Number, String],
    default: null
  },
  rounded: {
    type: [Boolean, String, Number],
    default: 'md'
  },
  border: {
    type: Boolean,
    default: false
  },
  contentClass: {
    type: String,
    default: ''
  },
  
  // Icon
  icon: {
    type: String,
    default: ''
  },
  iconColor: {
    type: String,
    default: 'primary'
  },
  iconSize: {
    type: Number,
    default: 36
  },
  iconRounded: {
    type: [Boolean, String, Number],
    default: 'circle'
  },
  
  // Behavior
  clickable: {
    type: Boolean,
    default: false
  },
  hover: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['click'])

// Computed
const elevationClass = computed(() => {
  if (props.elevation !== null) {
    return `elevation-${props.elevation}`
  }
  return ''
})

// Methods
const handleClick = (event) => {
  if (props.clickable && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-card {
  position: relative;
  transition: all 0.3s ease;
}

.base-card--clickable {
  cursor: pointer;
}

.base-card--hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.base-card__header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.base-card__footer {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}
</style>
