<template>
  <div class="form-section" :class="{ 'form-section--collapsible': collapsible }">
    <!-- Section Header -->
    <div 
      class="form-section__header d-flex align-center"
      :class="{ 'form-section__header--clickable': collapsible }"
      @click="collapsible && toggleCollapsed()"
    >
      <!-- Icon -->
      <v-icon
        v-if="icon"
        :color="iconColor"
        size="24"
        class="mr-2"
      >
        {{ icon }}
      </v-icon>
      
      <!-- Title -->
      <h3 class="text-h6 form-section__title">
        {{ title }}
        <span v-if="required" class="form-section__required">*</span>
      </h3>
      
      <!-- Subtitle -->
      <p v-if="subtitle" class="text-body-2 text-grey-darken-1 ml-2 mb-0">
        {{ subtitle }}
      </p>
      
      <v-spacer></v-spacer>
      
      <!-- Custom Actions -->
      <slot name="actions"></slot>
      
      <!-- Collapse Toggle -->
      <v-btn
        v-if="collapsible"
        :icon="isCollapsed ? 'mdi-chevron-down' : 'mdi-chevron-up'"
        variant="text"
        size="small"
        @click.stop="toggleCollapsed()"
      ></v-btn>
    </div>
    
    <!-- Divider -->
    <v-divider class="my-3"></v-divider>
    
    <!-- Section Content -->
    <v-expand-transition>
      <div v-show="!isCollapsed" class="form-section__content">
        <slot></slot>
      </div>
    </v-expand-transition>
    
    <!-- Help Text -->
    <div v-if="helpText && !isCollapsed" class="form-section__help mt-2">
      <v-alert
        type="info"
        variant="text"
        density="compact"
      >
        <div class="text-body-2">{{ helpText }}</div>
      </v-alert>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Props
const props = defineProps({
  // Section content
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  },
  
  // Section appearance
  icon: {
    type: String,
    default: ''
  },
  iconColor: {
    type: String,
    default: 'primary'
  },
  required: {
    type: Boolean,
    default: false
  },
  
  // Section behavior
  collapsible: {
    type: Boolean,
    default: false
  },
  collapsed: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:collapsed'])

// Local state
const localCollapsed = ref(props.collapsed)

// Computed
const isCollapsed = computed({
  get: () => props.collapsed,
  set: (value) => emit('update:collapsed', value)
})

// Methods
const toggleCollapsed = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.form-section {
  margin-bottom: 32px;
}

.form-section__header--clickable {
  cursor: pointer;
}

.form-section__title {
  margin-bottom: 0;
}

.form-section__required {
  color: #FF5252;
  margin-left: 4px;
}

.form-section__content {
  padding-top: 8px;
}
</style>
