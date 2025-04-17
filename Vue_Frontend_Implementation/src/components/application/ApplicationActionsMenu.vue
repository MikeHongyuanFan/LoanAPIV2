<template>
  <v-menu location="bottom end">
    <template v-slot:activator="{ props }">
      <v-btn
        color="primary"
        variant="text"
        v-bind="props"
        icon="mdi-dots-vertical"
      ></v-btn>
    </template>
    <v-list>
      <v-list-item
        v-for="(action, index) in availableActions"
        :key="index"
        :value="action.value"
        @click="handleAction(action.value)"
      >
        <template v-slot:prepend>
          <v-icon :icon="action.icon"></v-icon>
        </template>
        <v-list-item-title>{{ action.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>

  <!-- Confirmation Dialog for Delete -->
  <v-dialog v-model="showDeleteDialog" max-width="500px">
    <v-card>
      <v-card-title class="text-h5">Delete Application</v-card-title>
      <v-card-text>
        Are you sure you want to delete this application? This action cannot be undone.
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey-darken-1" variant="text" @click="showDeleteDialog = false">Cancel</v-btn>
        <v-btn color="error" variant="text" @click="confirmDelete">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Export Format Dialog -->
  <v-dialog v-model="showExportDialog" max-width="500px">
    <v-card>
      <v-card-title class="text-h5">Export Application</v-card-title>
      <v-card-text>
        <v-radio-group v-model="exportFormat">
          <v-radio label="PDF Document" value="pdf"></v-radio>
          <v-radio label="Excel Spreadsheet" value="xlsx"></v-radio>
          <v-radio label="CSV File" value="csv"></v-radio>
        </v-radio-group>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey-darken-1" variant="text" @click="showExportDialog = false">Cancel</v-btn>
        <v-btn color="primary" variant="text" @click="confirmExport">Export</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['action']);

// Store
const authStore = useAuthStore();

// State
const showDeleteDialog = ref(false);
const showExportDialog = ref(false);
const exportFormat = ref('pdf');

// Computed
const availableActions = computed(() => {
  const actions = [];
  
  // View action is always available
  actions.push({
    title: 'View Details',
    value: 'view',
    icon: 'mdi-eye'
  });
  
  // Edit action is available if user has permission and application is in editable state
  if (authStore.hasPermission('application:edit') && 
      ['DRAFT', 'PENDING', 'INFORMATION_REQUESTED'].includes(props.application.status)) {
    actions.push({
      title: 'Edit Application',
      value: 'edit',
      icon: 'mdi-pencil'
    });
  }
  
  // Duplicate action is available if user has permission
  if (authStore.hasPermission('application:create')) {
    actions.push({
      title: 'Duplicate Application',
      value: 'duplicate',
      icon: 'mdi-content-duplicate'
    });
  }
  
  // Export action is always available
  actions.push({
    title: 'Export Application',
    value: 'export',
    icon: 'mdi-export'
  });
  
  // Print action is always available
  actions.push({
    title: 'Print Application',
    value: 'print',
    icon: 'mdi-printer'
  });
  
  // Share action is available if user has permission
  if (authStore.hasPermission('application:share')) {
    actions.push({
      title: 'Share Application',
      value: 'share',
      icon: 'mdi-share-variant'
    });
  }
  
  // Delete action is available if user has permission
  if (authStore.hasPermission('application:delete')) {
    actions.push({
      title: 'Delete Application',
      value: 'delete',
      icon: 'mdi-delete',
      color: 'error'
    });
  }
  
  return actions;
});

// Methods
const handleAction = (action) => {
  switch (action) {
    case 'delete':
      showDeleteDialog.value = true;
      break;
    case 'export':
      showExportDialog.value = true;
      break;
    case 'print':
      window.print();
      break;
    default:
      emit('action', action);
      break;
  }
};

const confirmDelete = () => {
  emit('action', 'delete');
  showDeleteDialog.value = false;
};

const confirmExport = () => {
  emit('action', 'export', { format: exportFormat.value });
  showExportDialog.value = false;
};
</script>

<style scoped>
/* Additional styling if needed */
</style>
