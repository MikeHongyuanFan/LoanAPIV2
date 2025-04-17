<template>
  <div class="borrower-history-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Borrower History</h3>
      <v-btn-group>
        <v-btn
          :color="historyFilter === 'all' ? 'primary' : ''"
          variant="text"
          @click="historyFilter = 'all'"
        >
          All
        </v-btn>
        <v-btn
          :color="historyFilter === 'applications' ? 'primary' : ''"
          variant="text"
          @click="historyFilter = 'applications'"
        >
          Applications
        </v-btn>
        <v-btn
          :color="historyFilter === 'documents' ? 'primary' : ''"
          variant="text"
          @click="historyFilter = 'documents'"
        >
          Documents
        </v-btn>
        <v-btn
          :color="historyFilter === 'changes' ? 'primary' : ''"
          variant="text"
          @click="historyFilter = 'changes'"
        >
          Changes
        </v-btn>
      </v-btn-group>
    </div>

    <div v-if="loading" class="d-flex justify-center my-8">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="!filteredHistory.length" class="text-center my-8">
      <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-history</v-icon>
      <h3 class="text-h6 mb-2">No History</h3>
      <p class="text-body-1 text-medium-emphasis">
        No {{ historyFilter === 'all' ? 'historical' : historyFilter }} records found for this borrower.
      </p>
    </div>

    <div v-else>
      <v-timeline side="end" align="start" line-thickness="2">
        <v-timeline-item
          v-for="(item, index) in filteredHistory"
          :key="index"
          :dot-color="getEventColor(item.type)"
          :icon="getEventIcon(item.type)"
          :size="item.important ? 'large' : 'small'"
        >
          <template v-slot:opposite>
            <div class="text-caption">{{ formatDate(item.timestamp) }}</div>
            <div class="text-caption">{{ formatTime(item.timestamp) }}</div>
          </template>
          
          <v-card>
            <v-card-title class="text-subtitle-1 py-2">
              {{ item.title }}
            </v-card-title>
            
            <v-card-text class="py-2">
              <p>{{ item.description }}</p>
              
              <div v-if="item.details" class="mt-2">
                <v-expansion-panels variant="accordion">
                  <v-expansion-panel>
                    <v-expansion-panel-title>View Details</v-expansion-panel-title>
                    <v-expansion-panel-text>
                      <pre class="details-pre">{{ JSON.stringify(item.details, null, 2) }}</pre>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>
              
              <div v-if="item.related_entity" class="mt-2">
                <v-btn
                  v-if="item.related_entity.type === 'application'"
                  size="small"
                  variant="text"
                  color="primary"
                  :to="`/applications/${item.related_entity.id}`"
                >
                  View Application
                </v-btn>
                
                <v-btn
                  v-else-if="item.related_entity.type === 'document'"
                  size="small"
                  variant="text"
                  color="primary"
                  @click="viewDocument(item.related_entity)"
                >
                  View Document
                </v-btn>
              </div>
            </v-card-text>
            
            <v-card-actions v-if="item.user">
              <v-spacer></v-spacer>
              <div class="text-caption text-medium-emphasis">
                By {{ item.user.name }} ({{ item.user.role }})
              </div>
            </v-card-actions>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </div>

    <!-- Document Preview Dialog -->
    <v-dialog v-model="showPreviewDialog" max-width="900px" fullscreen>
      <v-card>
        <v-toolbar color="primary" dark>
          <v-btn icon @click="showPreviewDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>{{ previewDocument?.name }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="downloadDocument(previewDocument)">
            <v-icon>mdi-download</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text class="pa-0">
          <div class="document-preview">
            <iframe v-if="previewDocument" :src="previewDocument.url" width="100%" height="100%"></iframe>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Merge History Dialog -->
    <v-dialog v-model="showMergeHistoryDialog" max-width="800px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-account-multiple-check</v-icon>
          Merge History
        </v-card-title>
        <v-card-text class="pa-4">
          <div v-if="mergeHistory.length === 0" class="text-center py-4">
            <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-account-multiple</v-icon>
            <div class="text-body-1">No merge history available</div>
          </div>
          <div v-else>
            <v-timeline side="end" align="start" line-thickness="2">
              <v-timeline-item
                v-for="(merge, index) in mergeHistory"
                :key="index"
                dot-color="primary"
                icon="mdi-account-multiple-check"
              >
                <template v-slot:opposite>
                  <div class="text-caption">{{ formatDate(merge.timestamp) }}</div>
                  <div class="text-caption">{{ formatTime(merge.timestamp) }}</div>
                </template>
                
                <v-card>
                  <v-card-title class="text-subtitle-1 py-2">
                    Borrower Records Merged
                  </v-card-title>
                  
                  <v-card-text class="py-2">
                    <p>
                      <strong>Primary Record:</strong> {{ merge.primary_borrower.full_name }}
                    </p>
                    <p>
                      <strong>Merged Records:</strong>
                      <ul>
                        <li v-for="(secondary, idx) in merge.secondary_borrowers" :key="idx">
                          {{ secondary.full_name }}
                        </li>
                      </ul>
                    </p>
                  </v-card-text>
                  
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <div class="text-caption text-medium-emphasis">
                      By {{ merge.user.name }} ({{ merge.user.role }})
                    </div>
                  </v-card-actions>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="showMergeHistoryDialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useBorrowerStore } from '@/stores/borrowerStore';
import { useNotificationStore } from '@/stores/notificationStore';
import { formatDate } from '@/utils/dateUtils';

const props = defineProps({
  borrower: {
    type: Object,
    required: true
  }
});

// Stores
const borrowerStore = useBorrowerStore();
const notificationStore = useNotificationStore();

// State
const loading = ref(true);
const history = ref([]);
const historyFilter = ref('all');
const showPreviewDialog = ref(false);
const previewDocument = ref(null);
const showMergeHistoryDialog = ref(false);
const mergeHistory = ref([]);

// Computed properties
const filteredHistory = computed(() => {
  if (historyFilter.value === 'all') {
    return history.value;
  }
  
  return history.value.filter(item => item.category === historyFilter.value);
});

// Methods
const fetchHistory = async () => {
  loading.value = true;
  
  try {
    // In a real app, this would be a dedicated API endpoint
    // For now, we'll generate some sample history data
    history.value = generateSampleHistory();
  } catch (error) {
    console.error('Error fetching borrower history:', error);
    notificationStore.showError('Failed to load borrower history');
  } finally {
    loading.value = false;
  }
};

const fetchMergeHistory = async () => {
  try {
    // In a real app, this would be a dedicated API endpoint
    // For now, we'll generate some sample merge history data
    mergeHistory.value = generateSampleMergeHistory();
  } catch (error) {
    console.error('Error fetching merge history:', error);
    notificationStore.showError('Failed to load merge history');
  }
};

const viewDocument = (document) => {
  previewDocument.value = document;
  showPreviewDialog.value = true;
};

const downloadDocument = (document) => {
  // In a real app, this would trigger a download
  // For now, we'll just show a notification
  notificationStore.showSuccess(`Downloading ${document.name}`);
  
  // Simulate download with a link
  const link = document.url || `https://example.com/documents/${document.id}`;
  window.open(link, '_blank');
};

const viewMergeHistory = () => {
  fetchMergeHistory();
  showMergeHistoryDialog.value = true;
};

// Helper functions
const getEventColor = (type) => {
  const colorMap = {
    'create': 'success',
    'update': 'info',
    'delete': 'error',
    'upload': 'primary',
    'download': 'secondary',
    'application': 'indigo',
    'merge': 'purple',
    'note': 'amber',
    'other': 'grey'
  };
  
  return colorMap[type] || 'grey';
};

const getEventIcon = (type) => {
  const iconMap = {
    'create': 'mdi-plus-circle',
    'update': 'mdi-pencil',
    'delete': 'mdi-delete',
    'upload': 'mdi-upload',
    'download': 'mdi-download',
    'application': 'mdi-file-document',
    'merge': 'mdi-account-multiple',
    'note': 'mdi-note-text',
    'other': 'mdi-information'
  };
  
  return iconMap[type] || 'mdi-information';
};

const formatTime = (timestamp) => {
  if (!timestamp) return '';
  
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

// Sample data generators
const generateSampleHistory = () => {
  const now = new Date();
  const oneDay = 24 * 60 * 60 * 1000;
  const oneWeek = 7 * oneDay;
  
  return [
    {
      type: 'create',
      category: 'changes',
      title: 'Borrower Created',
      description: 'Borrower record was created in the system.',
      timestamp: new Date(now.getTime() - oneWeek).toISOString(),
      important: true,
      user: {
        name: 'John Smith',
        role: 'Loan Officer'
      }
    },
    {
      type: 'application',
      category: 'applications',
      title: 'Application Created',
      description: 'New loan application #APP-2025-0042 was created.',
      timestamp: new Date(now.getTime() - oneWeek + oneDay).toISOString(),
      important: true,
      related_entity: {
        type: 'application',
        id: '12345',
        reference: 'APP-2025-0042'
      },
      user: {
        name: 'John Smith',
        role: 'Loan Officer'
      }
    },
    {
      type: 'upload',
      category: 'documents',
      title: 'Document Uploaded',
      description: 'Identity document "Drivers License.pdf" was uploaded.',
      timestamp: new Date(now.getTime() - oneWeek + oneDay + 2 * 60 * 60 * 1000).toISOString(),
      related_entity: {
        type: 'document',
        id: '67890',
        name: 'Drivers License.pdf',
        url: 'https://example.com/documents/67890'
      },
      user: {
        name: 'John Smith',
        role: 'Loan Officer'
      }
    },
    {
      type: 'upload',
      category: 'documents',
      title: 'Document Uploaded',
      description: 'Income document "Pay Slip.pdf" was uploaded.',
      timestamp: new Date(now.getTime() - oneWeek + oneDay + 3 * 60 * 60 * 1000).toISOString(),
      related_entity: {
        type: 'document',
        id: '67891',
        name: 'Pay Slip.pdf',
        url: 'https://example.com/documents/67891'
      },
      user: {
        name: 'John Smith',
        role: 'Loan Officer'
      }
    },
    {
      type: 'update',
      category: 'changes',
      title: 'Borrower Updated',
      description: 'Contact information was updated.',
      timestamp: new Date(now.getTime() - oneWeek + 2 * oneDay).toISOString(),
      details: {
        changes: {
          phone: {
            old: '0412345678',
            new: '0498765432'
          },
          email: {
            old: 'old.email@example.com',
            new: 'new.email@example.com'
          }
        }
      },
      user: {
        name: 'Jane Doe',
        role: 'Customer Service'
      }
    },
    {
      type: 'application',
      category: 'applications',
      title: 'Application Status Changed',
      description: 'Application #APP-2025-0042 status changed to "Under Review".',
      timestamp: new Date(now.getTime() - oneWeek + 3 * oneDay).toISOString(),
      related_entity: {
        type: 'application',
        id: '12345',
        reference: 'APP-2025-0042'
      },
      user: {
        name: 'Michael Johnson',
        role: 'Credit Analyst'
      }
    },
    {
      type: 'note',
      category: 'changes',
      title: 'Note Added',
      description: 'A note was added to the borrower record: "Customer called to update employment details."',
      timestamp: new Date(now.getTime() - oneWeek + 4 * oneDay).toISOString(),
      user: {
        name: 'Jane Doe',
        role: 'Customer Service'
      }
    },
    {
      type: 'application',
      category: 'applications',
      title: 'Application Approved',
      description: 'Application #APP-2025-0042 was approved.',
      timestamp: new Date(now.getTime() - oneWeek + 5 * oneDay).toISOString(),
      important: true,
      related_entity: {
        type: 'application',
        id: '12345',
        reference: 'APP-2025-0042'
      },
      user: {
        name: 'Robert Williams',
        role: 'Senior Credit Analyst'
      }
    },
    {
      type: 'merge',
      category: 'changes',
      title: 'Duplicate Records Merged',
      description: 'Duplicate borrower records were merged into this record.',
      timestamp: new Date(now.getTime() - 2 * oneDay).toISOString(),
      important: true,
      user: {
        name: 'Admin User',
        role: 'System Administrator'
      }
    }
  ];
};

const generateSampleMergeHistory = () => {
  const now = new Date();
  const oneDay = 24 * 60 * 60 * 1000;
  
  return [
    {
      timestamp: new Date(now.getTime() - 2 * oneDay).toISOString(),
      primary_borrower: {
        id: props.borrower.id,
        full_name: props.borrower.full_name
      },
      secondary_borrowers: [
        {
          id: '98765',
          full_name: 'John A. Smith'
        }
      ],
      user: {
        name: 'Admin User',
        role: 'System Administrator'
      }
    }
  ];
};

// Lifecycle hooks
onMounted(() => {
  fetchHistory();
});
</script>

<style scoped>
.borrower-history-tab {
  padding-bottom: 1rem;
}

.document-preview {
  height: calc(100vh - 64px);
  width: 100%;
}

.details-pre {
  background-color: rgba(0, 0, 0, 0.03);
  padding: 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  overflow-x: auto;
}
</style>
