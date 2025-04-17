<template>
  <div class="application-documents">
    <!-- Upload Document Section -->
    <v-card class="mb-4">
      <v-card-title class="d-flex align-center">
        <span>Upload Documents</span>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          prepend-icon="mdi-file-document-plus"
          @click="showGenerateDialog = true"
        >
          Generate Document
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <v-file-input
          v-model="files"
          label="Select files"
          variant="outlined"
          multiple
          show-size
          accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
          :loading="uploading"
          :disabled="uploading"
          prepend-icon="mdi-paperclip"
          @change="handleFileChange"
        ></v-file-input>
        
        <div v-if="files.length > 0" class="mt-2">
          <v-select
            v-model="documentType"
            label="Document Type"
            :items="documentTypeOptions"
            variant="outlined"
            :rules="[v => !!v || 'Document type is required']"
            required
          ></v-select>
          
          <div class="d-flex justify-end mt-2">
            <v-btn
              color="primary"
              :loading="uploading"
              :disabled="!documentType || files.length === 0"
              @click="uploadFiles"
            >
              Upload
            </v-btn>
          </div>
        </div>
      </v-card-text>
    </v-card>
    
    <!-- Required Documents Section -->
    <v-card class="mb-4">
      <v-card-title>Required Documents</v-card-title>
      
      <v-list>
        <v-list-item
          v-for="(doc, index) in requiredDocuments"
          :key="index"
          :title="doc.name"
          :subtitle="doc.description"
        >
          <template v-slot:prepend>
            <v-icon :color="doc.uploaded ? 'success' : 'grey'">
              {{ doc.uploaded ? 'mdi-check-circle' : 'mdi-circle-outline' }}
            </v-icon>
          </template>
          
          <template v-slot:append>
            <v-btn
              v-if="doc.uploaded"
              variant="text"
              color="primary"
              size="small"
              @click="viewDocument(doc.document_id)"
            >
              View
            </v-btn>
            <v-btn
              v-else
              variant="text"
              color="primary"
              size="small"
              @click="uploadForRequirement(doc)"
            >
              Upload
            </v-btn>
          </template>
        </v-list-item>
      </v-list>
    </v-card>
    
    <!-- All Documents Section -->
    <v-card>
      <v-card-title class="d-flex align-center">
        <span>All Documents</span>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-inner-icon="mdi-magnify"
          label="Search"
          density="compact"
          hide-details
          variant="outlined"
          style="max-width: 300px"
        ></v-text-field>
      </v-card-title>
      
      <v-data-table
        :headers="headers"
        :items="documents"
        :search="search"
        :loading="loading"
        :items-per-page="10"
      >
        <!-- Document Name Column -->
        <template v-slot:item.name="{ item }">
          <div class="d-flex align-center">
            <v-icon :color="getDocumentTypeColor(item.type)" class="mr-2">
              {{ getDocumentTypeIcon(item.type) }}
            </v-icon>
            <div>
              <div>{{ item.name }}</div>
              <div class="text-caption text-grey-darken-1">{{ item.type }}</div>
            </div>
          </div>
        </template>
        
        <!-- Status Column -->
        <template v-slot:item.status="{ item }">
          <v-chip
            size="small"
            :color="getDocumentStatusColor(item.status)"
          >
            {{ item.status }}
          </v-chip>
        </template>
        
        <!-- Date Column -->
        <template v-slot:item.uploaded_at="{ item }">
          {{ formatDate(item.uploaded_at) }}
        </template>
        
        <!-- Size Column -->
        <template v-slot:item.size="{ item }">
          {{ formatFileSize(item.size) }}
        </template>
        
        <!-- Actions Column -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex">
            <v-btn
              icon="mdi-eye"
              variant="text"
              size="small"
              color="primary"
              @click="viewDocument(item.id)"
              title="View"
            ></v-btn>
            
            <v-btn
              icon="mdi-download"
              variant="text"
              size="small"
              color="primary"
              @click="downloadDocument(item)"
              title="Download"
            ></v-btn>
            
            <v-menu>
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
                  @click="shareDocument(item)"
                  prepend-icon="mdi-share-variant"
                  title="Share"
                ></v-list-item>
                
                <v-list-item
                  @click="renameDocument(item)"
                  prepend-icon="mdi-pencil"
                  title="Rename"
                ></v-list-item>
                
                <v-list-item
                  @click="confirmDeleteDocument(item)"
                  prepend-icon="mdi-delete"
                  title="Delete"
                  color="error"
                ></v-list-item>
              </v-list>
            </v-menu>
          </div>
        </template>
        
        <!-- Empty State -->
        <template v-slot:no-data>
          <div class="d-flex flex-column align-center py-8">
            <v-icon size="64" color="grey-lighten-2" class="mb-4">mdi-file-document-outline</v-icon>
            <h3 class="text-h6 text-grey-darken-1">No documents yet</h3>
            <p class="text-body-2 text-grey-darken-1">
              Upload documents using the form above.
            </p>
          </div>
        </template>
      </v-data-table>
    </v-card>
    
    <!-- Document Preview Dialog -->
    <v-dialog v-model="previewDialog" max-width="900">
      <v-card>
        <v-card-title class="d-flex align-center">
          <span>{{ selectedDocument?.name || 'Document Preview' }}</span>
          <v-spacer></v-spacer>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            @click="previewDialog = false"
          ></v-btn>
        </v-card-title>
        
        <v-divider></v-divider>
        
        <v-card-text class="pa-0">
          <div v-if="selectedDocument" class="document-preview">
            <iframe
              v-if="isPDF(selectedDocument)"
              :src="getDocumentUrl(selectedDocument)"
              width="100%"
              height="600"
              frameborder="0"
            ></iframe>
            
            <img
              v-else-if="isImage(selectedDocument)"
              :src="getDocumentUrl(selectedDocument)"
              class="document-image"
              alt="Document Preview"
            />
            
            <div v-else class="document-fallback">
              <v-icon size="64" color="grey-lighten-2" class="mb-4">{{ getDocumentTypeIcon(selectedDocument.type) }}</v-icon>
              <p class="text-body-1">
                Preview not available for this document type.
                <a :href="getDocumentUrl(selectedDocument)" target="_blank" rel="noopener noreferrer">Open in new tab</a>
                or
                <a :href="getDocumentUrl(selectedDocument)" download>download</a>
                to view.
              </p>
            </div>
          </div>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions>
          <v-btn
            variant="text"
            prepend-icon="mdi-download"
            @click="downloadDocument(selectedDocument)"
          >
            Download
          </v-btn>
          
          <v-spacer></v-spacer>
          
          <v-btn
            color="primary"
            @click="previewDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Generate Document Dialog -->
    <v-dialog v-model="showGenerateDialog" max-width="600">
      <v-card>
        <v-card-title>Generate Document</v-card-title>
        
        <v-card-text>
          <v-select
            v-model="selectedTemplate"
            label="Document Template"
            :items="documentTemplates"
            item-title="name"
            item-value="id"
            variant="outlined"
            :rules="[v => !!v || 'Template is required']"
            required
          ></v-select>
          
          <div v-if="selectedTemplate" class="mt-4">
            <div class="text-subtitle-1 mb-2">Template Preview</div>
            <v-card variant="outlined" class="pa-4 bg-grey-lighten-5">
              <div class="text-body-2">
                {{ getTemplateDescription(selectedTemplate) }}
              </div>
            </v-card>
          </div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showGenerateDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="generating"
            :disabled="!selectedTemplate || generating"
            @click="generateDocument"
          >
            Generate
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Rename Document Dialog -->
    <v-dialog v-model="showRenameDialog" max-width="500">
      <v-card>
        <v-card-title>Rename Document</v-card-title>
        
        <v-card-text>
          <v-text-field
            v-model="newDocumentName"
            label="Document Name"
            variant="outlined"
            :rules="[v => !!v || 'Name is required']"
            required
          ></v-text-field>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showRenameDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="renaming"
            :disabled="!newDocumentName || renaming"
            @click="saveRename"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title>Delete Document</v-card-title>
        
        <v-card-text>
          Are you sure you want to delete <strong>{{ documentToDelete?.name }}</strong>?
          This action cannot be undone.
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showDeleteDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            @click="deleteDocument"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Share Document Dialog -->
    <v-dialog v-model="showShareDialog" max-width="500">
      <v-card>
        <v-card-title>Share Document</v-card-title>
        
        <v-card-text>
          <v-text-field
            v-model="shareEmail"
            label="Email Address"
            variant="outlined"
            type="email"
            :rules="[
              v => !!v || 'Email is required',
              v => /.+@.+\..+/.test(v) || 'Email must be valid'
            ]"
            required
          ></v-text-field>
          
          <v-textarea
            v-model="shareMessage"
            label="Message (Optional)"
            variant="outlined"
            rows="3"
          ></v-textarea>
          
          <v-checkbox
            v-model="shareRequireSignature"
            label="Require signature"
            hide-details
          ></v-checkbox>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showShareDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="sharing"
            :disabled="!shareEmail || !/.+@.+\..+/.test(shareEmail) || sharing"
            @click="shareDocumentByEmail"
          >
            Share
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
  initialDocuments: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits([
  'document-uploaded',
  'document-deleted',
  'document-renamed',
  'document-generated',
  'document-shared'
])

// State
const documents = ref([...props.initialDocuments])
const loading = ref(false)
const search = ref('')
const files = ref([])
const documentType = ref(null)
const uploading = ref(false)
const previewDialog = ref(false)
const selectedDocument = ref(null)
const showGenerateDialog = ref(false)
const selectedTemplate = ref(null)
const generating = ref(false)
const showRenameDialog = ref(false)
const documentToRename = ref(null)
const newDocumentName = ref('')
const renaming = ref(false)
const showDeleteDialog = ref(false)
const documentToDelete = ref(null)
const deleting = ref(false)
const showShareDialog = ref(false)
const documentToShare = ref(null)
const shareEmail = ref('')
const shareMessage = ref('')
const shareRequireSignature = ref(false)
const sharing = ref(false)

// Table headers
const headers = [
  { title: 'Document', key: 'name', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Uploaded', key: 'uploaded_at', sortable: true },
  { title: 'Size', key: 'size', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
]

// Document type options
const documentTypeOptions = [
  { title: 'ID Verification', value: 'id_verification' },
  { title: 'Proof of Income', value: 'proof_of_income' },
  { title: 'Bank Statement', value: 'bank_statement' },
  { title: 'Property Valuation', value: 'property_valuation' },
  { title: 'Loan Agreement', value: 'loan_agreement' },
  { title: 'Application Form', value: 'application_form' },
  { title: 'Credit Report', value: 'credit_report' },
  { title: 'Insurance Document', value: 'insurance' },
  { title: 'Other', value: 'other' }
]

// Required documents
const requiredDocuments = ref([
  { name: 'ID Verification', description: 'Government-issued ID', uploaded: false, document_id: null, type: 'id_verification' },
  { name: 'Proof of Income', description: 'Last 3 months of pay stubs', uploaded: false, document_id: null, type: 'proof_of_income' },
  { name: 'Bank Statements', description: 'Last 3 months of statements', uploaded: false, document_id: null, type: 'bank_statement' },
  { name: 'Property Valuation', description: 'For secured loans', uploaded: false, document_id: null, type: 'property_valuation' }
])

// Document templates
const documentTemplates = ref([
  { id: 1, name: 'Loan Agreement', description: 'Standard loan agreement with terms and conditions' },
  { id: 2, name: 'Application Summary', description: 'Summary of the loan application details' },
  { id: 3, name: 'Payment Schedule', description: 'Detailed repayment schedule with dates and amounts' },
  { id: 4, name: 'Disclosure Statement', description: 'Legal disclosures required by regulations' }
])

// Methods
const handleFileChange = (files) => {
  // Reset document type when files change
  if (files.length === 0) {
    documentType.value = null
  }
}

const uploadFiles = async () => {
  if (files.value.length === 0 || !documentType.value) return
  
  uploading.value = true
  
  try {
    // This would be an API call in a real application
    // const formData = new FormData()
    // files.value.forEach(file => {
    //   formData.append('files', file)
    // })
    // formData.append('type', documentType.value)
    // formData.append('application_id', props.applicationId)
    
    // const response = await documentService.uploadDocuments(formData)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock response
    const uploadedDocuments = files.value.map((file, index) => ({
      id: Date.now() + index,
      name: file.name,
      type: documentType.value,
      status: 'uploaded',
      uploaded_at: new Date().toISOString(),
      size: file.size,
      url: URL.createObjectURL(file)
    }))
    
    // Add to documents list
    documents.value = [...uploadedDocuments, ...documents.value]
    
    // Update required documents if applicable
    updateRequiredDocuments(documentType.value, uploadedDocuments[0].id)
    
    // Clear form
    files.value = []
    documentType.value = null
    
    // Emit event
    emit('document-uploaded', uploadedDocuments)
  } catch (error) {
    console.error('Error uploading documents:', error)
    // Show error notification
  } finally {
    uploading.value = false
  }
}

const updateRequiredDocuments = (type, documentId) => {
  const requiredDoc = requiredDocuments.value.find(doc => doc.type === type)
  if (requiredDoc) {
    requiredDoc.uploaded = true
    requiredDoc.document_id = documentId
  }
}

const uploadForRequirement = (doc) => {
  // Pre-select the document type based on the requirement
  documentType.value = doc.type
  
  // Scroll to upload section
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const viewDocument = (documentId) => {
  const doc = documents.value.find(d => d.id === documentId)
  if (doc) {
    selectedDocument.value = doc
    previewDialog.value = true
  }
}

const downloadDocument = (document) => {
  if (!document) return
  
  // In a real application, this would trigger a download
  // window.open(document.url, '_blank')
  
  // For demonstration, just log the action
  console.log('Downloading document:', document.name)
}

const generateDocument = async () => {
  if (!selectedTemplate.value) return
  
  generating.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await documentService.generateDocument(props.applicationId, {
    //   template_id: selectedTemplate.value
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock response
    const template = documentTemplates.value.find(t => t.id === selectedTemplate.value)
    const generatedDocument = {
      id: Date.now(),
      name: template.name,
      type: 'generated',
      status: 'generated',
      uploaded_at: new Date().toISOString(),
      size: 1024 * 1024, // 1MB mock size
      url: '#'
    }
    
    // Add to documents list
    documents.value = [generatedDocument, ...documents.value]
    
    // Close dialog
    showGenerateDialog.value = false
    selectedTemplate.value = null
    
    // Emit event
    emit('document-generated', generatedDocument)
  } catch (error) {
    console.error('Error generating document:', error)
    // Show error notification
  } finally {
    generating.value = false
  }
}

const renameDocument = (document) => {
  documentToRename.value = document
  newDocumentName.value = document.name
  showRenameDialog.value = true
}

const saveRename = async () => {
  if (!documentToRename.value || !newDocumentName.value.trim()) return
  
  renaming.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await documentService.renameDocument(documentToRename.value.id, {
    //   name: newDocumentName.value
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update document in list
    const docIndex = documents.value.findIndex(d => d.id === documentToRename.value.id)
    if (docIndex !== -1) {
      documents.value[docIndex] = {
        ...documents.value[docIndex],
        name: newDocumentName.value
      }
    }
    
    // Close dialog
    showRenameDialog.value = false
    documentToRename.value = null
    newDocumentName.value = ''
    
    // Emit event
    emit('document-renamed', documents.value[docIndex])
  } catch (error) {
    console.error('Error renaming document:', error)
    // Show error notification
  } finally {
    renaming.value = false
  }
}

const confirmDeleteDocument = (document) => {
  documentToDelete.value = document
  showDeleteDialog.value = true
}

const deleteDocument = async () => {
  if (!documentToDelete.value) return
  
  deleting.value = true
  
  try {
    // This would be an API call in a real application
    // await documentService.deleteDocument(documentToDelete.value.id)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Remove document from list
    documents.value = documents.value.filter(d => d.id !== documentToDelete.value.id)
    
    // Update required documents if applicable
    const requiredDoc = requiredDocuments.value.find(doc => doc.document_id === documentToDelete.value.id)
    if (requiredDoc) {
      requiredDoc.uploaded = false
      requiredDoc.document_id = null
    }
    
    // Close dialog
    showDeleteDialog.value = false
    
    // Emit event
    emit('document-deleted', documentToDelete.value.id)
  } catch (error) {
    console.error('Error deleting document:', error)
    // Show error notification
  } finally {
    deleting.value = false
    documentToDelete.value = null
  }
}

const shareDocument = (document) => {
  documentToShare.value = document
  shareEmail.value = ''
  shareMessage.value = ''
  shareRequireSignature.value = false
  showShareDialog.value = true
}

const shareDocumentByEmail = async () => {
  if (!documentToShare.value || !shareEmail.value) return
  
  sharing.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await documentService.shareDocument(documentToShare.value.id, {
    //   email: shareEmail.value,
    //   message: shareMessage.value,
    //   require_signature: shareRequireSignature.value
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Close dialog
    showShareDialog.value = false
    
    // Emit event
    emit('document-shared', {
      document_id: documentToShare.value.id,
      email: shareEmail.value,
      require_signature: shareRequireSignature.value
    })
  } catch (error) {
    console.error('Error sharing document:', error)
    // Show error notification
  } finally {
    sharing.value = false
    documentToShare.value = null
  }
}

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    return format(date, 'MMM d, yyyy')
  } catch (error) {
    return dateString
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getDocumentTypeIcon = (type) => {
  const icons = {
    id_verification: 'mdi-card-account-details',
    proof_of_income: 'mdi-cash-multiple',
    bank_statement: 'mdi-bank',
    property_valuation: 'mdi-home',
    loan_agreement: 'mdi-file-document-edit',
    application_form: 'mdi-file-document',
    credit_report: 'mdi-chart-line',
    insurance: 'mdi-shield',
    generated: 'mdi-file-document-outline',
    other: 'mdi-file'
  }
  
  return icons[type] || 'mdi-file'
}

const getDocumentTypeColor = (type) => {
  const colors = {
    id_verification: 'blue',
    proof_of_income: 'green',
    bank_statement: 'indigo',
    property_valuation: 'purple',
    loan_agreement: 'red',
    application_form: 'orange',
    credit_report: 'cyan',
    insurance: 'teal',
    generated: 'primary',
    other: 'grey'
  }
  
  return colors[type] || 'grey'
}

const getDocumentStatusColor = (status) => {
  const colors = {
    uploaded: 'success',
    pending: 'warning',
    rejected: 'error',
    approved: 'primary',
    generated: 'info',
    signed: 'purple'
  }
  
  return colors[status] || 'grey'
}

const getDocumentUrl = (document) => {
  // In a real application, this would return the actual URL
  return document.url || '#'
}

const isPDF = (document) => {
  return document.name.toLowerCase().endsWith('.pdf')
}

const isImage = (document) => {
  const extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
  return extensions.some(ext => document.name.toLowerCase().endsWith(ext))
}

const getTemplateDescription = (templateId) => {
  const template = documentTemplates.value.find(t => t.id === templateId)
  return template ? template.description : ''
}
</script>

<style scoped>
.application-documents {
  width: 100%;
}

.document-preview {
  width: 100%;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.document-image {
  max-width: 100%;
  max-height: 600px;
  object-fit: contain;
}

.document-fallback {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  text-align: center;
  padding: 24px;
}
</style>
