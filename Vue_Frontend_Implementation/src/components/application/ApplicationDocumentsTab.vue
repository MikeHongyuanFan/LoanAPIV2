<template>
  <div class="application-documents-tab">
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

    <!-- Integrate the existing ApplicationDocuments component -->
    <application-documents
      :application-id="application.id"
      @document-uploaded="handleDocumentUploaded"
      @document-deleted="handleDocumentDeleted"
      @document-generated="handleDocumentGenerated"
    />

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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { useDocumentStore } from '@/stores/document';
import ApplicationDocuments from '@/components/application/ApplicationDocuments.vue';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

// Stores
const authStore = useAuthStore();
const notificationStore = useNotificationStore();
const documentStore = useDocumentStore();

// State for document generation
const showGenerateDialog = ref(false);
const selectedTemplate = ref(null);
const selectedFormat = ref('pdf');
const includeSignature = ref(false);
const documentTemplates = ref([]);
const generating = ref(false);

// State for document upload
const showUploadDialog = ref(false);
const documentName = ref('');
const documentType = ref(null);
const documentDescription = ref('');
const documentFile = ref(null);
const uploading = ref(false);

// Form refs
const generateForm = ref(null);
const uploadForm = ref(null);

// Document formats
const documentFormats = [
  { title: 'PDF Document', value: 'pdf' },
  { title: 'Word Document', value: 'docx' },
  { title: 'Excel Spreadsheet', value: 'xlsx' }
];

// Document types
const documentTypes = [
  { title: 'Application Form', value: 'APPLICATION_FORM' },
  { title: 'Identity Document', value: 'IDENTITY' },
  { title: 'Income Verification', value: 'INCOME' },
  { title: 'Bank Statement', value: 'BANK_STATEMENT' },
  { title: 'Property Valuation', value: 'VALUATION' },
  { title: 'Credit Report', value: 'CREDIT_REPORT' },
  { title: 'Contract', value: 'CONTRACT' },
  { title: 'Insurance', value: 'INSURANCE' },
  { title: 'Other', value: 'OTHER' }
];

// Computed properties
const canUploadDocuments = computed(() => {
  return authStore.hasPermission('document:upload') && 
         !['COMPLETED', 'CANCELLED'].includes(props.application.status);
});

const canGenerateDocuments = computed(() => {
  return authStore.hasPermission('document:generate') && 
         !['COMPLETED', 'CANCELLED'].includes(props.application.status);
});

// Methods
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
      application_id: props.application.id,
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
    formData.append('application_id', props.application.id);
    
    await documentStore.uploadDocument(formData);
    
    notificationStore.showSuccess('Document uploaded successfully');
    showUploadDialog.value = false;
    
    // Reset form
    documentName.value = '';
    documentType.value = null;
    documentDescription.value = '';
    documentFile.value = null;
  } catch (error) {
    notificationStore.showError('Failed to upload document');
    console.error('Error uploading document:', error);
  } finally {
    uploading.value = false;
  }
};

// Event handlers
const handleDocumentUploaded = () => {
  notificationStore.showSuccess('Document uploaded successfully');
};

const handleDocumentDeleted = () => {
  notificationStore.showSuccess('Document deleted successfully');
};

const handleDocumentGenerated = () => {
  notificationStore.showSuccess('Document generated successfully');
};

// Lifecycle hooks
onMounted(() => {
  fetchDocumentTemplates();
});
</script>

<style scoped>
.application-documents-tab {
  padding-bottom: 1rem;
}
</style>
