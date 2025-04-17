<template>
  <div class="application-workflow-actions">
    <v-card>
      <v-card-title class="bg-grey-lighten-4 py-3">
        <v-icon start class="mr-2">mdi-arrow-decision</v-icon>
        Workflow Actions
      </v-card-title>
      <v-card-text class="pa-4">
        <div v-if="loading" class="d-flex justify-center py-4">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>
        
        <div v-else-if="!availableActions.length" class="text-center py-4">
          <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-check-circle</v-icon>
          <div class="text-body-1">No actions available</div>
          <div class="text-caption text-medium-emphasis">
            This application is in {{ application.status.replace(/_/g, ' ').toLowerCase() }} status and no further actions are required.
          </div>
        </div>
        
        <div v-else>
          <p class="text-body-1 mb-4">
            The following actions are available for this application:
          </p>
          
          <div class="d-flex flex-wrap gap-2">
            <v-btn
              v-for="action in availableActions"
              :key="action.targetStatus"
              :color="getActionColor(action.type)"
              :variant="action.type === 'negative' ? 'outlined' : 'elevated'"
              class="mr-2 mb-2"
              @click="selectAction(action)"
            >
              <v-icon start>{{ getActionIcon(action.type) }}</v-icon>
              {{ action.label }}
            </v-btn>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Action Confirmation Dialog -->
    <v-dialog v-model="showConfirmDialog" max-width="600px">
      <v-card>
        <v-card-title :class="['py-3', getActionHeaderClass(selectedAction?.type)]">
          <v-icon start class="mr-2">{{ getActionIcon(selectedAction?.type) }}</v-icon>
          {{ selectedAction?.label }}
        </v-card-title>
        <v-card-text class="pa-4">
          <p class="text-body-1 mb-4">
            {{ getActionConfirmationMessage(selectedAction) }}
          </p>
          
          <v-textarea
            v-model="actionComment"
            label="Comment"
            rows="3"
            :placeholder="getActionCommentPlaceholder(selectedAction)"
            :rules="[v => selectedAction?.requiresComment ? !!v || 'Comment is required' : true]"
          ></v-textarea>
          
          <v-checkbox
            v-if="selectedAction?.requiresNotification"
            v-model="sendNotification"
            label="Send notification to borrower"
            hint="An email notification will be sent to the borrower"
            persistent-hint
          ></v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showConfirmDialog = false">
            Cancel
          </v-btn>
          <v-btn 
            :color="getActionColor(selectedAction?.type)" 
            @click="confirmAction"
            :loading="processing"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['action']);

// Stores
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

// State
const loading = ref(false);
const showConfirmDialog = ref(false);
const selectedAction = ref(null);
const actionComment = ref('');
const sendNotification = ref(true);
const processing = ref(false);

// Computed properties
const availableActions = computed(() => {
  const actions = [];
  const status = props.application.status;
  const hasEditPermission = authStore.hasPermission('application:edit');
  const hasApprovePermission = authStore.hasPermission('application:approve');
  const hasRejectPermission = authStore.hasPermission('application:reject');
  
  // Actions based on current status
  switch (status) {
    case 'DRAFT':
      if (hasEditPermission) {
        actions.push({
          label: 'Submit Application',
          targetStatus: 'PENDING',
          type: 'positive',
          requiresComment: false,
          requiresNotification: true
        });
      }
      break;
      
    case 'PENDING':
      if (hasEditPermission) {
        actions.push({
          label: 'Start Review',
          targetStatus: 'UNDER_REVIEW',
          type: 'neutral',
          requiresComment: false,
          requiresNotification: false
        });
      }
      if (hasEditPermission) {
        actions.push({
          label: 'Request Information',
          targetStatus: 'INFORMATION_REQUESTED',
          type: 'warning',
          requiresComment: true,
          requiresNotification: true
        });
      }
      break;
      
    case 'UNDER_REVIEW':
      if (hasApprovePermission) {
        actions.push({
          label: 'Approve Application',
          targetStatus: 'APPROVED',
          type: 'positive',
          requiresComment: false,
          requiresNotification: true
        });
      }
      if (hasApprovePermission) {
        actions.push({
          label: 'Conditionally Approve',
          targetStatus: 'CONDITIONALLY_APPROVED',
          type: 'warning',
          requiresComment: true,
          requiresNotification: true
        });
      }
      if (hasRejectPermission) {
        actions.push({
          label: 'Reject Application',
          targetStatus: 'REJECTED',
          type: 'negative',
          requiresComment: true,
          requiresNotification: true
        });
      }
      if (hasEditPermission) {
        actions.push({
          label: 'Request Information',
          targetStatus: 'INFORMATION_REQUESTED',
          type: 'warning',
          requiresComment: true,
          requiresNotification: true
        });
      }
      break;
      
    case 'INFORMATION_REQUESTED':
      if (hasEditPermission) {
        actions.push({
          label: 'Resume Review',
          targetStatus: 'UNDER_REVIEW',
          type: 'neutral',
          requiresComment: false,
          requiresNotification: false
        });
      }
      break;
      
    case 'APPROVED':
      if (hasEditPermission) {
        actions.push({
          label: 'Complete Application',
          targetStatus: 'COMPLETED',
          type: 'positive',
          requiresComment: false,
          requiresNotification: true
        });
      }
      break;
      
    case 'CONDITIONALLY_APPROVED':
      if (hasApprovePermission) {
        actions.push({
          label: 'Fully Approve',
          targetStatus: 'APPROVED',
          type: 'positive',
          requiresComment: false,
          requiresNotification: true
        });
      }
      if (hasEditPermission) {
        actions.push({
          label: 'Request Information',
          targetStatus: 'INFORMATION_REQUESTED',
          type: 'warning',
          requiresComment: true,
          requiresNotification: true
        });
      }
      break;
  }
  
  // Common actions for most statuses
  if (['DRAFT', 'PENDING', 'UNDER_REVIEW', 'INFORMATION_REQUESTED', 'CONDITIONALLY_APPROVED'].includes(status)) {
    if (hasEditPermission) {
      actions.push({
        label: 'Cancel Application',
        targetStatus: 'CANCELLED',
        type: 'negative',
        requiresComment: true,
        requiresNotification: true
      });
    }
  }
  
  if (['DRAFT', 'PENDING', 'INFORMATION_REQUESTED'].includes(status)) {
    if (hasEditPermission) {
      actions.push({
        label: 'Mark as Withdrawn',
        targetStatus: 'WITHDRAWN',
        type: 'negative',
        requiresComment: true,
        requiresNotification: false
      });
    }
  }
  
  return actions;
});

// Methods
const getActionColor = (type) => {
  const colorMap = {
    'positive': 'success',
    'neutral': 'primary',
    'warning': 'warning',
    'negative': 'error'
  };
  
  return colorMap[type] || 'primary';
};

const getActionIcon = (type) => {
  const iconMap = {
    'positive': 'mdi-check-circle',
    'neutral': 'mdi-arrow-right-circle',
    'warning': 'mdi-alert-circle',
    'negative': 'mdi-close-circle'
  };
  
  return iconMap[type] || 'mdi-arrow-right-circle';
};

const getActionHeaderClass = (type) => {
  const classMap = {
    'positive': 'bg-success text-white',
    'neutral': 'bg-primary text-white',
    'warning': 'bg-warning',
    'negative': 'bg-error text-white'
  };
  
  return classMap[type] || 'bg-grey-lighten-4';
};

const getActionConfirmationMessage = (action) => {
  if (!action) return '';
  
  const messageMap = {
    'PENDING': `Are you sure you want to submit this application for review? This will notify the loan officer.`,
    'UNDER_REVIEW': `Are you sure you want to start reviewing this application?`,
    'INFORMATION_REQUESTED': `Please specify what additional information is needed from the borrower.`,
    'APPROVED': `Are you sure you want to approve this application? This will notify the borrower.`,
    'CONDITIONALLY_APPROVED': `Please specify the conditions that must be met for full approval.`,
    'REJECTED': `Please specify the reason for rejecting this application.`,
    'COMPLETED': `Are you sure you want to mark this application as completed? This will finalize the loan.`,
    'CANCELLED': `Please specify the reason for cancelling this application.`,
    'WITHDRAWN': `Please specify the reason for marking this application as withdrawn.`
  };
  
  return messageMap[action.targetStatus] || `Are you sure you want to change the status to ${action.targetStatus.replace(/_/g, ' ').toLowerCase()}?`;
};

const getActionCommentPlaceholder = (action) => {
  if (!action) return '';
  
  const placeholderMap = {
    'INFORMATION_REQUESTED': 'Please provide the following additional information...',
    'CONDITIONALLY_APPROVED': 'This application is approved subject to the following conditions...',
    'REJECTED': 'This application has been rejected for the following reasons...',
    'CANCELLED': 'This application has been cancelled because...',
    'WITHDRAWN': 'This application has been withdrawn because...'
  };
  
  return placeholderMap[action.targetStatus] || 'Add a comment (optional)';
};

const selectAction = (action) => {
  selectedAction.value = action;
  actionComment.value = '';
  sendNotification.value = action.requiresNotification;
  showConfirmDialog.value = true;
};

const confirmAction = async () => {
  if (selectedAction.value.requiresComment && !actionComment.value) {
    notificationStore.showError('Please add a comment');
    return;
  }
  
  processing.value = true;
  
  try {
    emit('action', {
      ...selectedAction.value,
      comment: actionComment.value,
      sendNotification: sendNotification.value
    });
    
    showConfirmDialog.value = false;
  } catch (error) {
    notificationStore.showError('Failed to process action');
    console.error('Error processing action:', error);
  } finally {
    processing.value = false;
  }
};

// Lifecycle hooks
onMounted(() => {
  // Any initialization if needed
});
</script>

<style scoped>
.application-workflow-actions {
  margin-bottom: 1rem;
}

.gap-2 {
  gap: 8px;
}
</style>
