<template>
  <div class="borrower-documents-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Documents</h3>
      <div class="d-flex">
        <v-btn
          v-if="canGenerateDocuments"
          color="primary"
          variant="outlined"
          class="mr-2"
          prepend-icon="mdi-file-document-outline"
          @click="showGenerateDialog = true"
        >
          Generate Document
        </v-btn>
        <v-btn
          v-if="canUploadDocuments"
          color="primary"
          prepend-icon="mdi-upload"
          @click="showUploadDialog = true"
        >
          Upload Document
        </v-btn>
      </div>
    </div>

    <div v-if="loading" class="d-flex justify-center my-8">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="!documents.length" class="text-center my-8">
      <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-file-outline</v-icon>
      <h3 class="text-h6 mb-2">No Documents</h3>
      <p class="text-body-1 text-medium-emphasis mb-4">
        This borrower doesn't have any documents yet.
      </p>
      <div class="d-flex justify-center">
        <v-btn
          v-if="canGenerateDocuments"
          color="primary"
          variant="outlined"
          class="mr-2"
          prepend-icon="mdi-file-document-outline"
          @click="showGenerateDialog = true"
        >
          Generate Document
        </v-btn>
        <v-btn
          v-if="canUploadDocuments"
          color="primary"
          prepend-icon="mdi-upload"
          @click="showUploadDialog = true"
        >
          Upload Document
        </v-btn>
      </div>
    </div>

    <div v-else>
      <!-- Documents Table -->
      <v-card>
        <v-data-table
          :headers="headers"
          :items="documents"
          :items-per-page="10"
          :footer-props="{
            'items-per-page-options': [5, 10, 15, -1],
            'items-per-page-text': 'Documents per page'
          }"
          class="elevation-1"
        >
          <!-- Name Column -->
          <template v-slot:item.name="{ item }">
            <div class="d-flex align-center">
              <v-icon :icon="getDocumentIcon(item.file_type)" class="mr-2"></v-icon>
              <span>{{ item.name }}</span>
            </div>
          </template>

          <!-- Document Type Column -->
          <template v-slot:item.document_type="{ item }">
            <v-chip size="small" :color="getDocumentTypeColor(item.document_type)">
              {{ formatDocumentType(item.document_type) }}
            </v-chip>
          </template>

          <!-- Size Column -->
          <template v-slot:item.size="{ item }">
            {{ formatFileSize(item.size) }}
          </template>

          <!-- Created Date Column -->
          <template v-slot:item.created_at="{ item }">
            {{ formatDate(item.created_at) }}
          </template>

          <!-- Actions Column -->
          <template v-slot:item.actions="{ item }">
            <div class="d-flex">
              <v-tooltip location="top" text="View">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-eye"
                    size="small"
                    variant="text"
                    @click="viewDocument(item)"
                  ></v-btn>
                </template>
              </v-tooltip>

              <v-tooltip location="top" text="Download">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-download"
                    size="small"
                    variant="text"
                    @click="downloadDocument(item)"
                  ></v-btn>
                </template>
              </v-tooltip>

              <v-tooltip location="top" text="Delete" v-if="canDeleteDocuments">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-delete"
                    size="small"
                    variant="text"
                    color="error"
                    @click="confirmDeleteDocument(item)"
                  ></v-btn>
                </template>
              </v-tooltip>
            </div>
          </template>
        </v-data-table>
      </v-card>

      <!-- Document Categories -->
      <div class="mt-6">
        <h3 class="text-subtitle-1 font-weight-medium mb-3">Document Categories</h3>
        <v-row>
          <v-col 
            v-for="category in documentCategories" 
            :key="category.type" 
            cols="12" 
            sm="6" 
            md="4"
          >
            <v-card class="category-card">
              <v-card-text>
                <div class="d-flex align-center">
                  <v-avatar :color="category.color" class="mr-3">
                    <v-icon color="white">{{ category.icon }}</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-subtitle-1 font-weight-medium">{{ category.label }}</div>
                    <div class="text-body-2">{{ category.count }} documents</div>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>

    <!-- Generate Document Dialog -->
    <v-dialog v-model="showGenerateDialog" max-width="600px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-file-document-outline</v-icon>
          Generate Document
        </v-card-title>
        <v-card-text class="pa-4">
          <v-form ref="generateForm" @submit.prevent="generateDocument">
            <v-select
              v-model="selectedTemplate"
              :items="documentTemplates"
              item-title="name"
              item-value="id"
              label="Document Template"
              required
              :rules="[v => !!v || 'Template is required']"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props">
                  <template v-slot:prepend>
                    <v-icon :icon="getDocumentIcon(item.raw.file_type)"></v-icon>
                  </template>
                  <v-list-item-title>{{ item.raw.name }}</v-list-item-title>
                  <v-list-item-subtitle>{{ item.raw.description }}</v-list-item-subtitle>
                </v-list-item>
              </template>
            </v-select>

            <v-select
              v-model="selectedFormat"
              :items="documentFormats"
              label="Output Format"
              required
              :rules="[v => !!v || 'Format is required']"
              class="mt-4"
            ></v-select>

            <v-checkbox
              v-model="includeSignature"
              label="Include digital signature"
              hint="Add a digital signature placeholder to the document"
              persistent-hint
              class="mt-2"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showGenerateDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="generateDocument" :loading="generating">
            Generate
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Upload Document Dialog -->
    <v-dialog v-model="showUploadDialog" max-width="600px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-upload</v-icon>
          Upload Document
        </v-card-title>
        <v-card-text class="pa-4">
          <v-form ref="uploadForm" @submit.prevent="uploadDocument">
            <v-text-field
              v-model="documentName"
              label="Document Name"
              required
              :rules="[v => !!v || 'Document name is required']"
            ></v-text-field>

            <v-select
              v-model="documentType"
              :items="documentTypes"
              label="Document Type"
              required
              :rules="[v => !!v || 'Document type is required']"
              class="mt-4"
            ></v-select>

            <v-textarea
              v-model="documentDescription"
              label="Description"
              rows="3"
              class="mt-4"
            ></v-textarea>

            <v-file-input
              v-model="documentFile"
              label="Select File"
              accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png"
              show-size
              counter
              required
              :rules="[v => !!v || 'Document file is required']"
              class="mt-4"
            ></v-file-input>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showUploadDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="uploadDocument" :loading="uploading">
            Upload
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Delete Document</v-card-title>
        <v-card-text>
          Are you sure you want to delete "{{ documentToDelete?.name }}"? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" variant="text" @click="deleteDocument" :loading="deleting">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useDocumentStore } from '@/stores/documentStore';
import { useAuthStore } from '@/stores/authStore';
import { useNotificationStore } from '@/stores/notificationStore';
import { formatDate } from '@/utils/dateUtils';

const props = defineProps({
  borrower: {
    type: Object,
    required: true
  }
});

// Stores
const documentStore = useDocumentStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

// State
const loading = ref(true);
const documents = ref([]);
const showGenerateDialog = ref(false);
const showUploadDialog = ref(false);
const showPreviewDialog = ref(false);
const showDeleteDialog = ref(false);
const selectedTemplate = ref(null);
const selectedFormat = ref('pdf');
const includeSignature = ref(false);
const documentTemplates = ref([]);
const generating = ref(false);
const documentName = ref('');
const documentType = ref(null);
const documentDescription = ref('');
const documentFile = ref(null);
const uploading = ref(false);
const previewDocument = ref(null);
const documentToDelete = ref(null);
const deleting = ref(false);

// Form refs
const generateForm = ref(null);
const uploadForm = ref(null);

// Table headers
const headers = [
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Type', key: 'document_type', sortable: true },
  { title: 'Size', key: 'size', sortable: true },
  { title: 'Uploaded', key: 'created_at', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
];

// Document formats
const documentFormats = [
  { title: 'PDF Document', value: 'pdf' },
  { title: 'Word Document', value: 'docx' },
  { title: 'Excel Spreadsheet', value: 'xlsx' }
];

// Document types
const documentTypes = [
  { title: 'Identity Document', value: 'IDENTITY' },
  { title: 'Income Verification', value: 'INCOME' },
  { title: 'Bank Statement', value: 'BANK_STATEMENT' },
  { title: 'Tax Return', value: 'TAX_RETURN' },
  { title: 'Credit Report', value: 'CREDIT_REPORT' },
  { title: 'Property Document', value: 'PROPERTY' },
  { title: 'Contract', value: 'CONTRACT' },
  { title: 'Insurance', value: 'INSURANCE' },
  { title: 'Other', value: 'OTHER' }
];

// Computed properties
const canUploadDocuments = computed(() => {
  return authStore.hasPermission('document:upload');
});

const canGenerateDocuments = computed(() => {
  return authStore.hasPermission('document:generate');
});

const canDeleteDocuments = computed(() => {
  return authStore.hasPermission('document:delete');
});

const documentCategories = computed(() => {
  const categories = [
    { type: 'IDENTITY', label: 'Identity Documents', icon: 'mdi-card-account-details', color: 'primary' },
    { type: 'INCOME', label: 'Income Documents', icon: 'mdi-cash-multiple', color: 'success' },
    { type: 'BANK_STATEMENT', label: 'Bank Statements', icon: 'mdi-bank', color: 'info' },
    { type: 'TAX_RETURN', label: 'Tax Returns', icon: 'mdi-file-document', color: 'warning' },
    { type: 'CREDIT_REPORT', label: 'Credit Reports', icon: 'mdi-chart-line', color: 'error' },
    { type: 'PROPERTY', label: 'Property Documents', icon: 'mdi-home', color: 'purple' },
    { type: 'CONTRACT', label: 'Contracts', icon: 'mdi-file-sign', color: 'indigo' },
    { type: 'INSURANCE', label: 'Insurance', icon: 'mdi-shield', color: 'cyan' },
    { type: 'OTHER', label: 'Other Documents', icon: 'mdi-file', color: 'grey' }
  ];
  
  // Count documents in each category
  return categories.map(category => {
    const count = documents.value.filter(doc => doc.document_type === category.type).length;
    return { ...category, count };
  });
});

// Methods
const fetchDocuments = async () => {
  loading.value = true;
  
  try {
    // In a real app, this would be a dedicated API endpoint
    // For now, we'll use a generic document endpoint with a filter
    const result = await documentStore.getDocuments({ borrower_id: props.borrower.id });
    documents.value = result;
  } catch (error) {
    console.error('Error fetching documents:', error);
    notificationStore.showError('Failed to load documents');
  } finally {
    loading.value = false;
  }
};

const fetchDocumentTemplates = async () => {
  try {
    documentTemplates.value = await documentStore.getDocumentTemplates();
  } catch (error) {
    notificationStore.showError('Failed to load document templates');
    console.error('Error loading document templates:', error);
  }
};

const generateDocument = async () => {
  if (!generateForm.value) return;
  
  const { valid } = await generateForm.value.validate();
  if (!valid) return;
  
  generating.value = true;
  
  try {
    await documentStore.generateDocument({
      borrower_id: props.borrower.id,
      template_id: selectedTemplate.value,
      format: selectedFormat.value,
      include_signature: includeSignature.value
    });
    
    notificationStore.showSuccess('Document generated successfully');
    showGenerateDialog.value = false;
    
    // Reset form
    selectedTemplate.value = null;
    selectedFormat.value = 'pdf';
    includeSignature.value = false;
    
    // Refresh documents
    fetchDocuments();
  } catch (error) {
    notificationStore.showError('Failed to generate document');
    console.error('Error generating document:', error);
  } finally {
    generating.value = false;
  }
};

const uploadDocument = async () => {
  if (!uploadForm.value) return;
  
  const { valid } = await uploadForm.value.validate();
  if (!valid) return;
  
  uploading.value = true;
  
  try {
    const formData = new FormData();
    formData.append('file', documentFile.value);
    formData.append('name', documentName.value);
    formData.append('document_type', documentType.value);
    formData.append('description', documentDescription.value);
    formData.append('borrower_id', props.borrower.id);
    
    await documentStore.uploadDocument(formData);
    
    notificationStore.showSuccess('Document uploaded successfully');
    showUploadDialog.value = false;
    
    // Reset form
    documentName.value = '';
    documentType.value = null;
    documentDescription.value = '';
    documentFile.value = null;
    
    // Refresh documents
    fetchDocuments();
  } catch (error) {
    notificationStore.showError('Failed to upload document');
    console.error('Error uploading document:', error);
  } finally {
    uploading.value = false;
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

const confirmDeleteDocument = (document) => {
  documentToDelete.value = document;
  showDeleteDialog.value = true;
};

const deleteDocument = async () => {
  if (!documentToDelete.value) return;
  
  deleting.value = true;
  
  try {
    await documentStore.deleteDocument(documentToDelete.value.id);
    
    notificationStore.showSuccess('Document deleted successfully');
    showDeleteDialog.value = false;
    
    // Refresh documents
    fetchDocuments();
  } catch (error) {
    notificationStore.showError('Failed to delete document');
    console.error('Error deleting document:', error);
  } finally {
    deleting.value = false;
    documentToDelete.value = null;
  }
};

// Formatting functions
const getDocumentIcon = (fileType) => {
  const iconMap = {
    'pdf': 'mdi-file-pdf-box',
    'docx': 'mdi-file-word',
    'doc': 'mdi-file-word',
    'xlsx': 'mdi-file-excel',
    'xls': 'mdi-file-excel',
    'jpg': 'mdi-file-image',
    'jpeg': 'mdi-file-image',
    'png': 'mdi-file-image'
  };
  
  return iconMap[fileType] || 'mdi-file-document-outline';
};

const formatDocumentType = (type) => {
  if (!type) return 'Other';
  
  const typeMap = {
    'IDENTITY': 'Identity',
    'INCOME': 'Income',
    'BANK_STATEMENT': 'Bank Statement',
    'TAX_RETURN': 'Tax Return',
    'CREDIT_REPORT': 'Credit Report',
    'PROPERTY': 'Property',
    'CONTRACT': 'Contract',
    'INSURANCE': 'Insurance',
    'OTHER': 'Other'
  };
  
  return typeMap[type] || type;
};

const getDocumentTypeColor = (type) => {
  const colorMap = {
    'IDENTITY': 'primary',
    'INCOME': 'success',
    'BANK_STATEMENT': 'info',
    'TAX_RETURN': 'warning',
    'CREDIT_REPORT': 'error',
    'PROPERTY': 'purple',
    'CONTRACT': 'indigo',
    'INSURANCE': 'cyan',
    'OTHER': 'grey'
  };
  
  return colorMap[type] || 'grey';
};

const formatFileSize = (size) => {
  if (!size) return 'Unknown';
  
  const units = ['B', 'KB', 'MB', 'GB'];
  let fileSize = size;
  let unitIndex = 0;
  
  while (fileSize >= 1024 && unitIndex < units.length - 1) {
    fileSize /= 1024;
    unitIndex++;
  }
  
  return `${fileSize.toFixed(1)} ${units[unitIndex]}`;
};

// Lifecycle hooks
onMounted(() => {
  fetchDocuments();
  fetchDocumentTemplates();
});
</script>

<style scoped>
.borrower-documents-tab {
  padding-bottom: 1rem;
}

.document-preview {
  height: calc(100vh - 64px);
  width: 100%;
}

.category-card {
  height: 100%;
  border-left: 4px solid;
  border-left-color: var(--v-primary-base);
}
</style>
