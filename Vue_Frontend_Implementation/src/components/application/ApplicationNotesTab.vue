<template>
  <div class="application-notes-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Notes & Comments</h3>
      <v-btn
        v-if="canAddNotes"
        color="primary"
        prepend-icon="mdi-plus"
        @click="showAddNoteDialog = true"
      >
        Add Note
      </v-btn>
    </div>

    <!-- Integrate the existing ApplicationNotes component -->
    <application-notes
      :application-id="application.id"
      @note-added="handleNoteAdded"
      @note-updated="handleNoteUpdated"
      @note-deleted="handleNoteDeleted"
    />

    <!-- Add Note Dialog -->
    <v-dialog v-model="showAddNoteDialog" max-width="600px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-note-plus</v-icon>
          Add Note
        </v-card-title>
        <v-card-text class="pa-4">
          <v-form ref="noteForm" @submit.prevent="addNote">
            <v-text-field
              v-model="noteTitle"
              label="Title"
              required
              :rules="[v => !!v || 'Title is required']"
            ></v-text-field>

            <v-select
              v-model="noteType"
              :items="noteTypes"
              label="Note Type"
              required
              :rules="[v => !!v || 'Note type is required']"
              class="mt-4"
            ></v-select>

            <v-textarea
              v-model="noteContent"
              label="Content"
              rows="5"
              required
              :rules="[v => !!v || 'Content is required']"
              class="mt-4"
            ></v-textarea>

            <v-checkbox
              v-model="isPrivate"
              label="Private Note"
              hint="Private notes are only visible to staff members"
              persistent-hint
              class="mt-2"
            ></v-checkbox>

            <v-checkbox
              v-model="isPinned"
              label="Pin Note"
              hint="Pinned notes appear at the top of the list"
              persistent-hint
              class="mt-2"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showAddNoteDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="addNote" :loading="adding">
            Add Note
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { useApplicationStore } from '@/stores/application';
import ApplicationNotes from '@/components/application/ApplicationNotes.vue';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

// Stores
const authStore = useAuthStore();
const notificationStore = useNotificationStore();
const applicationStore = useApplicationStore();

// State for adding notes
const showAddNoteDialog = ref(false);
const noteTitle = ref('');
const noteType = ref('GENERAL');
const noteContent = ref('');
const isPrivate = ref(false);
const isPinned = ref(false);
const adding = ref(false);

// Form ref
const noteForm = ref(null);

// Note types
const noteTypes = [
  { title: 'General', value: 'GENERAL' },
  { title: 'Client Communication', value: 'CLIENT_COMMUNICATION' },
  { title: 'Internal Discussion', value: 'INTERNAL_DISCUSSION' },
  { title: 'Decision', value: 'DECISION' },
  { title: 'Action Required', value: 'ACTION_REQUIRED' },
  { title: 'Warning', value: 'WARNING' }
];

// Computed properties
const canAddNotes = computed(() => {
  return authStore.hasPermission('application:edit') || 
         authStore.hasPermission('note:create');
});

// Methods
const addNote = async () => {
  if (!noteForm.value) return;
  
  const { valid } = await noteForm.value.validate();
  if (!valid) return;
  
  adding.value = true;
  
  try {
    await applicationStore.createNote(props.application.id, {
      title: noteTitle.value,
      content: noteContent.value,
      note_type: noteType.value,
      is_private: isPrivate.value,
      is_pinned: isPinned.value
    });
    
    notificationStore.showSuccess('Note added successfully');
    showAddNoteDialog.value = false;
    
    // Reset form
    noteTitle.value = '';
    noteType.value = 'GENERAL';
    noteContent.value = '';
    isPrivate.value = false;
    isPinned.value = false;
  } catch (error) {
    notificationStore.showError('Failed to add note');
    console.error('Error adding note:', error);
  } finally {
    adding.value = false;
  }
};

// Event handlers
const handleNoteAdded = () => {
  notificationStore.showSuccess('Note added successfully');
};

const handleNoteUpdated = () => {
  notificationStore.showSuccess('Note updated successfully');
};

const handleNoteDeleted = () => {
  notificationStore.showSuccess('Note deleted successfully');
};
</script>

<style scoped>
.application-notes-tab {
  padding-bottom: 1rem;
}
</style>
