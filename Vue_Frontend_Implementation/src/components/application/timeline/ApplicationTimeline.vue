<template>
  <div class="application-timeline">
    <v-timeline
      :side="timelineSide"
      :density="density"
      :line-thickness="2"
      line-color="grey-lighten-2"
    >
      <v-timeline-item
        v-for="(event, index) in timelineEvents"
        :key="index"
        :dot-color="getEventColor(event.type)"
        :icon="getEventIcon(event.type)"
        :size="getEventSize(event.type)"
        :fill-dot="isImportantEvent(event.type)"
      >
        <template v-slot:opposite>
          <div class="text-caption" :class="{'text-right': timelineSide === 'end'}">
            {{ formatDate(event.timestamp) }}
          </div>
        </template>
        
        <v-card
          :color="isImportantEvent(event.type) ? `${getEventColor(event.type)}-lighten-5` : ''"
          variant="flat"
          class="mb-4"
        >
          <v-card-title class="text-subtitle-1 font-weight-medium pb-1">
            {{ event.title }}
          </v-card-title>
          
          <v-card-text class="pt-1">
            <p class="text-body-2 mb-2">{{ event.description }}</p>
            
            <!-- Status Change -->
            <template v-if="event.type === 'status_change'">
              <div class="d-flex align-center">
                <v-chip
                  size="small"
                  :color="getStatusColor(event.data.old_status)"
                  class="mr-2"
                >
                  {{ event.data.old_status }}
                </v-chip>
                <v-icon size="small" class="mx-2">mdi-arrow-right</v-icon>
                <v-chip
                  size="small"
                  :color="getStatusColor(event.data.new_status)"
                >
                  {{ event.data.new_status }}
                </v-chip>
              </div>
            </template>
            
            <!-- Document -->
            <template v-else-if="event.type === 'document'">
              <v-btn
                variant="text"
                size="small"
                color="primary"
                prepend-icon="mdi-file-document"
                @click="viewDocument(event.data.document_id)"
              >
                View Document
              </v-btn>
            </template>
            
            <!-- Note -->
            <template v-else-if="event.type === 'note'">
              <div class="text-body-2 pa-2 bg-grey-lighten-4 rounded">
                {{ event.data.note_text }}
              </div>
            </template>
            
            <!-- Payment -->
            <template v-else-if="event.type === 'payment'">
              <div class="d-flex align-center">
                <v-chip
                  size="small"
                  color="success"
                  class="mr-2"
                >
                  {{ formatCurrency(event.data.amount) }}
                </v-chip>
                <span class="text-caption">{{ event.data.payment_method }}</span>
              </div>
            </template>
            
            <!-- User Info -->
            <div class="d-flex align-center mt-2">
              <v-avatar size="24" color="grey-lighten-3" class="mr-2">
                <span class="text-caption">{{ event.user.initials }}</span>
              </v-avatar>
              <span class="text-caption">{{ event.user.name }}</span>
            </div>
          </v-card-text>
        </v-card>
      </v-timeline-item>
    </v-timeline>
    
    <!-- Empty State -->
    <div v-if="timelineEvents.length === 0" class="text-center py-8">
      <v-icon size="64" color="grey-lighten-2" class="mb-4">mdi-timeline-clock</v-icon>
      <h3 class="text-h6 text-grey-darken-1">No timeline events</h3>
      <p class="text-body-2 text-grey-darken-1">
        This application doesn't have any activity yet.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { format } from 'date-fns'

// Props
const props = defineProps({
  events: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  density: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'comfortable', 'compact'].includes(value)
  },
  side: {
    type: String,
    default: 'end',
    validator: (value) => ['start', 'end', 'alternate'].includes(value)
  }
})

// Emits
const emit = defineEmits(['view-document'])

// Computed
const timelineEvents = computed(() => {
  return [...props.events].sort((a, b) => {
    return new Date(b.timestamp) - new Date(a.timestamp)
  })
})

const timelineSide = computed(() => {
  return props.side
})

// Methods
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    return format(date, 'MMM d, yyyy h:mm a')
  } catch (error) {
    return dateString
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  }).format(value)
}

const getEventColor = (type) => {
  const eventColors = {
    creation: 'primary',
    status_change: 'info',
    document: 'purple',
    note: 'grey',
    payment: 'success',
    fee: 'amber',
    approval: 'success',
    rejection: 'error',
    submission: 'info',
    completion: 'success'
  }
  
  return eventColors[type] || 'grey'
}

const getEventIcon = (type) => {
  const eventIcons = {
    creation: 'mdi-plus-circle',
    status_change: 'mdi-swap-horizontal',
    document: 'mdi-file-document',
    note: 'mdi-comment-text',
    payment: 'mdi-cash',
    fee: 'mdi-cash-multiple',
    approval: 'mdi-check-circle',
    rejection: 'mdi-close-circle',
    submission: 'mdi-send',
    completion: 'mdi-flag-checkered'
  }
  
  return eventIcons[type] || 'mdi-circle'
}

const getEventSize = (type) => {
  return isImportantEvent(type) ? 'large' : 'small'
}

const isImportantEvent = (type) => {
  return ['creation', 'approval', 'rejection', 'submission', 'completion'].includes(type)
}

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

const viewDocument = (documentId) => {
  emit('view-document', documentId)
}
</script>

<style scoped>
.application-timeline {
  width: 100%;
}
</style>
