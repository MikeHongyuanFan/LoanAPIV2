<template>
  <div class="application-notes">
    <!-- Add Note Form -->
    <v-card class="mb-4">
      <v-card-text>
        <v-textarea
          v-model="newNote"
          label="Add a note"
          variant="outlined"
          rows="3"
          counter
          :rules="[v => v.length <= 1000 || 'Note must be less than 1000 characters']"
          :disabled="loading"
          :loading="loading"
          hide-details="auto"
          placeholder="Type your note here..."
          class="mb-2"
        ></v-textarea>
        
        <div class="d-flex align-center">
          <v-checkbox
            v-model="isPrivate"
            label="Private note (only visible to staff)"
            density="compact"
            hide-details
          ></v-checkbox>
          
          <v-spacer></v-spacer>
          
          <v-btn
            color="primary"
            :disabled="!newNote.trim() || loading"
            :loading="loading"
            @click="addNote"
          >
            Add Note
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    
    <!-- Notes List -->
    <div v-if="notes.length > 0">
      <v-card
        v-for="(note, index) in notes"
        :key="note.id"
        :class="{ 'mb-4': index < notes.length - 1 }"
        :color="note.is_private ? 'grey-lighten-5' : ''"
      >
        <v-card-text>
          <div class="d-flex align-center mb-2">
            <v-avatar size="32" :color="getUserColor(note.user)" class="mr-2">
              <span class="text-white">{{ getUserInitials(note.user) }}</span>
            </v-avatar>
            
            <div>
              <div class="font-weight-medium">{{ note.user.name }}</div>
              <div class="text-caption text-grey-darken-1">
                {{ formatDate(note.created_at) }}
              </div>
            </div>
            
            <v-spacer></v-spacer>
            
            <v-chip
              v-if="note.is_private"
              size="small"
              color="grey"
              variant="outlined"
              prepend-icon="mdi-eye-off"
            >
              Private
            </v-chip>
            
            <v-menu v-if="canEditNote(note)">
              <template v-slot:activator="{ props }">
                <v-btn
                  icon="mdi-dots-vertical"
                  variant="text"
                  size="small"
                  v-bind="props"
                ></v-btn>
              </template>
              
              <v-list density="compact">
                <v-list-item
                  @click="editNote(note)"
                  prepend-icon="mdi-pencil"
                  title="Edit"
                ></v-list-item>
                
                <v-list-item
                  @click="confirmDeleteNote(note)"
                  prepend-icon="mdi-delete"
                  title="Delete"
                  color="error"
                ></v-list-item>
              </v-list>
            </v-menu>
          </div>
          
          <div v-if="editingNote && editingNote.id === note.id">
            <v-textarea
              v-model="editingNote.content"
              variant="outlined"
              rows="3"
              counter
              :rules="[v => v.length <= 1000 || 'Note must be less than 1000 characters']"
              :disabled="loading"
              :loading="loading"
              hide-details="auto"
              class="mb-2"
            ></v-textarea>
            
            <div class="d-flex justify-end">
              <v-btn
                variant="text"
                @click="cancelEdit"
                :disabled="loading"
                class="mr-2"
              >
                Cancel
              </v-btn>
              
              <v-btn
                color="primary"
                :disabled="!editingNote.content.trim() || loading"
                :loading="loading"
                @click="saveEdit"
              >
                Save
              </v-btn>
            </div>
          </div>
          
          <div v-else class="text-body-1 white-space-pre-wrap">
            {{ note.content }}
          </div>
        </v-card-text>
      </v-card>
    </div>
    
    <!-- Empty State -->
    <v-card v-else class="text-center py-8">
      <v-icon size="64" color="grey-lighten-2" class="mb-4">mdi-comment-text-outline</v-icon>
      <h3 class="text-h6 text-grey-darken-1">No notes yet</h3>
      <p class="text-body-2 text-grey-darken-1">
        Add a note to keep track of important information about this application.
      </p>
    </v-card>
    
    <!-- Load More -->
    <div v-if="hasMoreNotes" class="text-center mt-4">
      <v-btn
        variant="text"
        color="primary"
        :loading="loadingMore"
        @click="loadMoreNotes"
      >
        Load More Notes
      </v-btn>
    </div>
    
    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h5">Delete Note</v-card-title>
        <v-card-text>
          Are you sure you want to delete this note? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="deleteDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            variant="flat"
            :loading="loading"
            @click="deleteNote"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { format } from 'date-fns'

// Props
const props = defineProps({
  applicationId: {
    type: [Number, String],
    required: true
  },
  initialNotes: {
    type: Array,
    default: () => []
  },
  currentUser: {
    type: Object,
    default: () => ({
      id: 1,
      name: 'Current User',
      role: 'admin'
    })
  }
})

// Emits
const emit = defineEmits(['note-added', 'note-updated', 'note-deleted'])

// State
const notes = ref([...props.initialNotes])
const newNote = ref('')
const isPrivate = ref(false)
const loading = ref(false)
const loadingMore = ref(false)
const hasMoreNotes = ref(props.initialNotes.length >= 10)
const page = ref(1)
const editingNote = ref(null)
const deleteDialog = ref(false)
const noteToDelete = ref(null)

// Methods
const addNote = async () => {
  if (!newNote.value.trim()) return
  
  loading.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await applicationService.addNote(props.applicationId, {
    //   content: newNote.value,
    //   is_private: isPrivate.value
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock response
    const createdNote = {
      id: Date.now(),
      content: newNote.value,
      is_private: isPrivate.value,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      user: props.currentUser
    }
    
    // Add to notes list
    notes.value.unshift(createdNote)
    
    // Clear form
    newNote.value = ''
    isPrivate.value = false
    
    // Emit event
    emit('note-added', createdNote)
  } catch (error) {
    console.error('Error adding note:', error)
    // Show error notification
  } finally {
    loading.value = false
  }
}

const loadMoreNotes = async () => {
  loadingMore.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await applicationService.getNotes(props.applicationId, {
    //   page: page.value + 1,
    //   limit: 10
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock response
    const moreNotes = []
    
    // Check if there are more notes to load
    hasMoreNotes.value = moreNotes.length >= 10
    
    // Add to notes list
    notes.value = [...notes.value, ...moreNotes]
    
    // Increment page
    page.value++
  } catch (error) {
    console.error('Error loading more notes:', error)
    // Show error notification
  } finally {
    loadingMore.value = false
  }
}

const editNote = (note) => {
  editingNote.value = {
    id: note.id,
    content: note.content,
    is_private: note.is_private
  }
}

const cancelEdit = () => {
  editingNote.value = null
}

const saveEdit = async () => {
  if (!editingNote.value || !editingNote.value.content.trim()) return
  
  loading.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await applicationService.updateNote(props.applicationId, editingNote.value.id, {
    //   content: editingNote.value.content,
    //   is_private: editingNote.value.is_private
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update note in list
    const noteIndex = notes.value.findIndex(note => note.id === editingNote.value.id)
    if (noteIndex !== -1) {
      notes.value[noteIndex] = {
        ...notes.value[noteIndex],
        content: editingNote.value.content,
        updated_at: new Date().toISOString()
      }
    }
    
    // Clear editing state
    const updatedNote = { ...notes.value[noteIndex] }
    editingNote.value = null
    
    // Emit event
    emit('note-updated', updatedNote)
  } catch (error) {
    console.error('Error updating note:', error)
    // Show error notification
  } finally {
    loading.value = false
  }
}

const confirmDeleteNote = (note) => {
  noteToDelete.value = note
  deleteDialog.value = true
}

const deleteNote = async () => {
  if (!noteToDelete.value) return
  
  loading.value = true
  
  try {
    // This would be an API call in a real application
    // await applicationService.deleteNote(props.applicationId, noteToDelete.value.id)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Remove note from list
    notes.value = notes.value.filter(note => note.id !== noteToDelete.value.id)
    
    // Close dialog
    deleteDialog.value = false
    
    // Emit event
    emit('note-deleted', noteToDelete.value.id)
  } catch (error) {
    console.error('Error deleting note:', error)
    // Show error notification
  } finally {
    loading.value = false
    noteToDelete.value = null
  }
}

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    return format(date, 'MMM d, yyyy h:mm a')
  } catch (error) {
    return dateString
  }
}

const getUserInitials = (user) => {
  if (!user || !user.name) return '?'
  
  return user.name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

const getUserColor = (user) => {
  if (!user || !user.id) return 'grey'
  
  // Generate a consistent color based on user ID
  const colors = ['primary', 'secondary', 'success', 'info', 'warning', 'error', 'purple', 'indigo', 'cyan', 'teal', 'orange', 'deep-orange']
  return colors[user.id % colors.length]
}

const canEditNote = (note) => {
  // Check if current user is the author or has admin/manager role
  return note.user.id === props.currentUser.id || 
         ['admin', 'manager'].includes(props.currentUser.role)
}
</script>

<style scoped>
.application-notes {
  width: 100%;
}

.white-space-pre-wrap {
  white-space: pre-wrap;
}
</style>
