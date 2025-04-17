<template>
  <div class="application-fees">
    <v-card>
      <v-card-title class="d-flex align-center">
        <span>Fees & Charges</span>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showAddFeeDialog = true"
        >
          Add Fee
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <!-- Fee Summary -->
        <v-row>
          <v-col cols="12" md="4">
            <v-card variant="outlined" class="pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-2">Fee Summary</div>
              <div class="d-flex flex-column gap-2">
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Total Fees</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(totalFees) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Paid Fees</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(paidFees) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Unpaid Fees</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(unpaidFees) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Waived Fees</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(waivedFees) }}</span>
                </div>
              </div>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="8">
            <v-card variant="outlined" class="pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-4">Fee Breakdown</div>
              <div class="chart-container" style="position: relative; height:200px; width:100%">
                <canvas ref="feeChart"></canvas>
              </div>
            </v-card>
          </v-col>
        </v-row>
        
        <!-- Fee Table -->
        <v-card variant="outlined" class="mt-4">
          <v-data-table
            :headers="headers"
            :items="fees"
            :loading="loading"
            :items-per-page="10"
          >
            <!-- Fee Name Column -->
            <template v-slot:item.name="{ item }">
              <div class="d-flex align-center">
                <v-icon :color="getFeeTypeColor(item.type)" class="mr-2" size="small">
                  {{ getFeeTypeIcon(item.type) }}
                </v-icon>
                <div>
                  <div>{{ item.name }}</div>
                  <div class="text-caption text-grey-darken-1">{{ item.type }}</div>
                </div>
              </div>
            </template>
            
            <!-- Amount Column -->
            <template v-slot:item.amount="{ item }">
              {{ formatCurrency(item.amount) }}
            </template>
            
            <!-- Date Column -->
            <template v-slot:item.date="{ item }">
              {{ formatDate(item.date) }}
            </template>
            
            <!-- Status Column -->
            <template v-slot:item.status="{ item }">
              <v-chip
                size="small"
                :color="getFeeStatusColor(item.status)"
              >
                {{ item.status }}
              </v-chip>
            </template>
            
            <!-- Actions Column -->
            <template v-slot:item.actions="{ item }">
              <div class="d-flex">
                <v-btn
                  v-if="item.status === 'unpaid'"
                  icon="mdi-cash"
                  variant="text"
                  size="small"
                  color="success"
                  @click="payFee(item)"
                  title="Pay"
                ></v-btn>
                
                <v-btn
                  v-if="item.status === 'unpaid'"
                  icon="mdi-cancel"
                  variant="text"
                  size="small"
                  color="warning"
                  @click="waiveFee(item)"
                  title="Waive"
                ></v-btn>
                
                <v-btn
                  icon="mdi-pencil"
                  variant="text"
                  size="small"
                  color="primary"
                  @click="editFee(item)"
                  title="Edit"
                  :disabled="item.status !== 'unpaid'"
                ></v-btn>
                
                <v-btn
                  icon="mdi-delete"
                  variant="text"
                  size="small"
                  color="error"
                  @click="confirmDeleteFee(item)"
                  title="Delete"
                  :disabled="item.status === 'paid'"
                ></v-btn>
              </div>
            </template>
            
            <!-- Empty State -->
            <template v-slot:no-data>
              <div class="d-flex flex-column align-center py-8">
                <v-icon size="64" color="grey-lighten-2" class="mb-4">mdi-cash-remove</v-icon>
                <h3 class="text-h6 text-grey-darken-1">No fees yet</h3>
                <p class="text-body-2 text-grey-darken-1 mb-4">
                  No fees have been added to this application yet.
                </p>
                <v-btn
                  color="primary"
                  prepend-icon="mdi-plus"
                  @click="showAddFeeDialog = true"
                >
                  Add Fee
                </v-btn>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-card-text>
    </v-card>
    
    <!-- Add/Edit Fee Dialog -->
    <v-dialog v-model="showAddFeeDialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingFee ? 'Edit Fee' : 'Add Fee' }}</v-card-title>
        
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="feeForm.name"
                label="Fee Name"
                variant="outlined"
                :rules="[v => !!v || 'Fee name is required']"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12">
              <v-select
                v-model="feeForm.type"
                label="Fee Type"
                :items="feeTypeOptions"
                variant="outlined"
                :rules="[v => !!v || 'Fee type is required']"
                required
              ></v-select>
            </v-col>
            
            <v-col cols="12">
              <v-text-field
                v-model="feeForm.amount"
                label="Amount"
                variant="outlined"
                type="number"
                prefix="$"
                :rules="[v => !!v || 'Amount is required', v => v > 0 || 'Amount must be greater than 0']"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12">
              <v-text-field
                v-model="feeForm.date"
                label="Date"
                variant="outlined"
                type="date"
                :rules="[v => !!v || 'Date is required']"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12">
              <v-textarea
                v-model="feeForm.description"
                label="Description (Optional)"
                variant="outlined"
                rows="3"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showAddFeeDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="savingFee"
            :disabled="!isValidFeeForm"
            @click="saveFee"
          >
            {{ editingFee ? 'Update' : 'Add' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Pay Fee Dialog -->
    <v-dialog v-model="showPayFeeDialog" max-width="500">
      <v-card>
        <v-card-title>Pay Fee</v-card-title>
        
        <v-card-text>
          <p class="mb-4">
            You are about to pay the following fee:
          </p>
          
          <v-card variant="outlined" class="pa-4 mb-4">
            <div class="d-flex flex-column gap-2">
              <div class="d-flex justify-space-between">
                <span class="text-caption text-grey-darken-1">Fee Name</span>
                <span class="text-body-2 font-weight-medium">{{ selectedFee?.name }}</span>
              </div>
              <div class="d-flex justify-space-between">
                <span class="text-caption text-grey-darken-1">Type</span>
                <span class="text-body-2 font-weight-medium">{{ selectedFee?.type }}</span>
              </div>
              <div class="d-flex justify-space-between">
                <span class="text-caption text-grey-darken-1">Amount</span>
                <span class="text-body-2 font-weight-medium">{{ formatCurrency(selectedFee?.amount) }}</span>
              </div>
              <div class="d-flex justify-space-between">
                <span class="text-caption text-grey-darken-1">Date</span>
                <span class="text-body-2 font-weight-medium">{{ formatDate(selectedFee?.date) }}</span>
              </div>
            </div>
          </v-card>
          
          <v-row>
            <v-col cols="12">
              <v-select
                v-model="paymentMethod"
                label="Payment Method"
                :items="paymentMethodOptions"
                variant="outlined"
                :rules="[v => !!v || 'Payment method is required']"
                required
              ></v-select>
            </v-col>
            
            <v-col cols="12">
              <v-text-field
                v-model="paymentReference"
                label="Payment Reference (Optional)"
                variant="outlined"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showPayFeeDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="success"
            :loading="processingPayment"
            :disabled="!paymentMethod"
            @click="processFeePayment"
          >
            Pay Fee
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Waive Fee Dialog -->
    <v-dialog v-model="showWaiveFeeDialog" max-width="500">
      <v-card>
        <v-card-title>Waive Fee</v-card-title>
        
        <v-card-text>
          <p class="mb-4">
            You are about to waive the following fee:
          </p>
          
          <v-card variant="outlined" class="pa-4 mb-4">
            <div class="d-flex flex-column gap-2">
              <div class="d-flex justify-space-between">
                <span class="text-caption text-grey-darken-1">Fee Name</span>
                <span class="text-body-2 font-weight-medium">{{ selectedFee?.name }}</span>
              </div>
              <div class="d-flex justify-space-between">
                <span class="text-caption text-grey-darken-1">Type</span>
                <span class="text-body-2 font-weight-medium">{{ selectedFee?.type }}</span>
              </div>
              <div class="d-flex justify-space-between">
                <span class="text-caption text-grey-darken-1">Amount</span>
                <span class="text-body-2 font-weight-medium">{{ formatCurrency(selectedFee?.amount) }}</span>
              </div>
            </div>
          </v-card>
          
          <v-row>
            <v-col cols="12">
              <v-textarea
                v-model="waiveReason"
                label="Reason for Waiving Fee"
                variant="outlined"
                rows="3"
                :rules="[v => !!v || 'Reason is required']"
                required
              ></v-textarea>
            </v-col>
          </v-row>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showWaiveFeeDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="warning"
            :loading="processingWaive"
            :disabled="!waiveReason"
            @click="processWaiveFee"
          >
            Waive Fee
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Delete Fee Dialog -->
    <v-dialog v-model="showDeleteFeeDialog" max-width="400">
      <v-card>
        <v-card-title>Delete Fee</v-card-title>
        
        <v-card-text>
          Are you sure you want to delete the fee <strong>{{ selectedFee?.name }}</strong>?
          This action cannot be undone.
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showDeleteFeeDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            :loading="deletingFee"
            @click="deleteFee"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { format } from 'date-fns'
import Chart from 'chart.js/auto'

// Props
const props = defineProps({
  applicationId: {
    type: [Number, String],
    required: true
  },
  initialFees: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits([
  'fee-added',
  'fee-updated',
  'fee-deleted',
  'fee-paid',
  'fee-waived'
])

// State
const fees = ref([...props.initialFees])
const feeChart = ref(null)
const chartInstance = ref(null)
const showAddFeeDialog = ref(false)
const showPayFeeDialog = ref(false)
const showWaiveFeeDialog = ref(false)
const showDeleteFeeDialog = ref(false)
const editingFee = ref(null)
const selectedFee = ref(null)
const savingFee = ref(false)
const processingPayment = ref(false)
const processingWaive = ref(false)
const deletingFee = ref(false)
const paymentMethod = ref('')
const paymentReference = ref('')
const waiveReason = ref('')

// Form state
const feeForm = ref({
  name: '',
  type: '',
  amount: '',
  date: format(new Date(), 'yyyy-MM-dd'),
  description: ''
})

// Table headers
const headers = [
  { title: 'Fee', key: 'name', sortable: true },
  { title: 'Amount', key: 'amount', sortable: true },
  { title: 'Date', key: 'date', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
]

// Fee type options
const feeTypeOptions = [
  { title: 'Application Fee', value: 'application' },
  { title: 'Origination Fee', value: 'origination' },
  { title: 'Processing Fee', value: 'processing' },
  { title: 'Appraisal Fee', value: 'appraisal' },
  { title: 'Credit Report Fee', value: 'credit_report' },
  { title: 'Late Payment Fee', value: 'late_payment' },
  { title: 'Documentation Fee', value: 'documentation' },
  { title: 'Wire Transfer Fee', value: 'wire_transfer' },
  { title: 'Other', value: 'other' }
]

// Payment method options
const paymentMethodOptions = [
  { title: 'Credit Card', value: 'credit_card' },
  { title: 'Bank Transfer', value: 'bank_transfer' },
  { title: 'Direct Debit', value: 'direct_debit' },
  { title: 'Check', value: 'check' },
  { title: 'Cash', value: 'cash' }
]

// Computed
const totalFees = computed(() => {
  return fees.value.reduce((sum, fee) => sum + fee.amount, 0)
})

const paidFees = computed(() => {
  return fees.value
    .filter(fee => fee.status === 'paid')
    .reduce((sum, fee) => sum + fee.amount, 0)
})

const unpaidFees = computed(() => {
  return fees.value
    .filter(fee => fee.status === 'unpaid')
    .reduce((sum, fee) => sum + fee.amount, 0)
})

const waivedFees = computed(() => {
  return fees.value
    .filter(fee => fee.status === 'waived')
    .reduce((sum, fee) => sum + fee.amount, 0)
})

const isValidFeeForm = computed(() => {
  return (
    feeForm.value.name &&
    feeForm.value.type &&
    feeForm.value.amount > 0 &&
    feeForm.value.date
  )
})

// Methods
const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  }).format(value)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    return format(date, 'MMM d, yyyy')
  } catch (error) {
    return dateString
  }
}

const getFeeTypeColor = (type) => {
  const typeColors = {
    application: 'primary',
    origination: 'purple',
    processing: 'indigo',
    appraisal: 'cyan',
    credit_report: 'teal',
    late_payment: 'error',
    documentation: 'amber',
    wire_transfer: 'orange',
    other: 'grey'
  }
  
  return typeColors[type] || 'grey'
}

const getFeeTypeIcon = (type) => {
  const typeIcons = {
    application: 'mdi-file-document',
    origination: 'mdi-bank',
    processing: 'mdi-cogs',
    appraisal: 'mdi-home',
    credit_report: 'mdi-chart-line',
    late_payment: 'mdi-clock-alert',
    documentation: 'mdi-file-multiple',
    wire_transfer: 'mdi-bank-transfer',
    other: 'mdi-cash'
  }
  
  return typeIcons[type] || 'mdi-cash'
}

const getFeeStatusColor = (status) => {
  const statusColors = {
    paid: 'success',
    unpaid: 'warning',
    waived: 'grey'
  }
  
  return statusColors[status] || 'grey'
}

const updateChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
  
  if (!feeChart.value) return
  
  const ctx = feeChart.value.getContext('2d')
  
  // Group fees by type
  const feesByType = {}
  fees.value.forEach(fee => {
    if (!feesByType[fee.type]) {
      feesByType[fee.type] = 0
    }
    feesByType[fee.type] += fee.amount
  })
  
  // Prepare data for chart
  const labels = Object.keys(feesByType).map(type => {
    const option = feeTypeOptions.find(opt => opt.value === type)
    return option ? option.title : type
  })
  
  const data = Object.values(feesByType)
  const backgroundColor = Object.keys(feesByType).map(type => {
    const color = getFeeTypeColor(type)
    return `rgba(var(--v-theme-${color}), 0.6)`
  })
  
  chartInstance.value = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: backgroundColor,
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            boxWidth: 15
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.raw;
              return `${label}: ${formatCurrency(value)}`;
            }
          }
        }
      }
    }
  })
}

const resetFeeForm = () => {
  feeForm.value = {
    name: '',
    type: '',
    amount: '',
    date: format(new Date(), 'yyyy-MM-dd'),
    description: ''
  }
  editingFee.value = null
}

const editFee = (fee) => {
  editingFee.value = fee
  feeForm.value = {
    name: fee.name,
    type: fee.type,
    amount: fee.amount,
    date: fee.date,
    description: fee.description || ''
  }
  showAddFeeDialog.value = true
}

const saveFee = async () => {
  if (!isValidFeeForm.value) return
  
  savingFee.value = true
  
  try {
    const feeData = {
      name: feeForm.value.name,
      type: feeForm.value.type,
      amount: parseFloat(feeForm.value.amount),
      date: feeForm.value.date,
      description: feeForm.value.description,
      status: 'unpaid'
    }
    
    if (editingFee.value) {
      // Update existing fee
      // This would be an API call in a real application
      // const response = await feeService.updateFee(props.applicationId, editingFee.value.id, feeData)
      
      // Mock delay for demonstration
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Update fee in list
      const index = fees.value.findIndex(f => f.id === editingFee.value.id)
      if (index !== -1) {
        fees.value[index] = {
          ...fees.value[index],
          ...feeData
        }
      }
      
      // Emit event
      emit('fee-updated', fees.value[index])
    } else {
      // Add new fee
      // This would be an API call in a real application
      // const response = await feeService.addFee(props.applicationId, feeData)
      
      // Mock delay for demonstration
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock response
      const newFee = {
        id: Date.now(),
        ...feeData
      }
      
      // Add to fees list
      fees.value.push(newFee)
      
      // Emit event
      emit('fee-added', newFee)
    }
    
    // Close dialog and reset form
    showAddFeeDialog.value = false
    resetFeeForm()
    
    // Update chart
    updateChart()
  } catch (error) {
    console.error('Error saving fee:', error)
    // Show error notification
  } finally {
    savingFee.value = false
  }
}

const payFee = (fee) => {
  selectedFee.value = fee
  paymentMethod.value = ''
  paymentReference.value = ''
  showPayFeeDialog.value = true
}

const processFeePayment = async () => {
  if (!selectedFee.value || !paymentMethod.value) return
  
  processingPayment.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await feeService.payFee(props.applicationId, selectedFee.value.id, {
    //   payment_method: paymentMethod.value,
    //   payment_reference: paymentReference.value,
    //   payment_date: new Date().toISOString()
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Update fee in list
    const index = fees.value.findIndex(f => f.id === selectedFee.value.id)
    if (index !== -1) {
      fees.value[index] = {
        ...fees.value[index],
        status: 'paid',
        payment_method: paymentMethod.value,
        payment_reference: paymentReference.value,
        payment_date: new Date().toISOString()
      }
    }
    
    // Close dialog
    showPayFeeDialog.value = false
    
    // Update chart
    updateChart()
    
    // Emit event
    emit('fee-paid', fees.value[index])
  } catch (error) {
    console.error('Error paying fee:', error)
    // Show error notification
  } finally {
    processingPayment.value = false
    selectedFee.value = null
  }
}

const waiveFee = (fee) => {
  selectedFee.value = fee
  waiveReason.value = ''
  showWaiveFeeDialog.value = true
}

const processWaiveFee = async () => {
  if (!selectedFee.value || !waiveReason.value) return
  
  processingWaive.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await feeService.waiveFee(props.applicationId, selectedFee.value.id, {
    //   reason: waiveReason.value,
    //   waived_date: new Date().toISOString()
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Update fee in list
    const index = fees.value.findIndex(f => f.id === selectedFee.value.id)
    if (index !== -1) {
      fees.value[index] = {
        ...fees.value[index],
        status: 'waived',
        waive_reason: waiveReason.value,
        waived_date: new Date().toISOString()
      }
    }
    
    // Close dialog
    showWaiveFeeDialog.value = false
    
    // Update chart
    updateChart()
    
    // Emit event
    emit('fee-waived', fees.value[index])
  } catch (error) {
    console.error('Error waiving fee:', error)
    // Show error notification
  } finally {
    processingWaive.value = false
    selectedFee.value = null
  }
}

const confirmDeleteFee = (fee) => {
  selectedFee.value = fee
  showDeleteFeeDialog.value = true
}

const deleteFee = async () => {
  if (!selectedFee.value) return
  
  deletingFee.value = true
  
  try {
    // This would be an API call in a real application
    // await feeService.deleteFee(props.applicationId, selectedFee.value.id)
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Remove fee from list
    fees.value = fees.value.filter(f => f.id !== selectedFee.value.id)
    
    // Close dialog
    showDeleteFeeDialog.value = false
    
    // Update chart
    updateChart()
    
    // Emit event
    emit('fee-deleted', selectedFee.value.id)
  } catch (error) {
    console.error('Error deleting fee:', error)
    // Show error notification
  } finally {
    deletingFee.value = false
    selectedFee.value = null
  }
}

// Initialize
onMounted(() => {
  updateChart()
})

// Watch for fees changes
watch(() => props.initialFees, (newFees) => {
  fees.value = [...newFees]
  updateChart()
}, { deep: true })
</script>

<style scoped>
.application-fees {
  width: 100%;
}

.chart-container {
  max-height: 200px;
}
</style>
