<template>
  <div class="repayment-schedule">
    <v-card>
      <v-card-title class="d-flex align-center">
        <span>Repayment Schedule</span>
        <v-spacer></v-spacer>
        <v-btn
          variant="text"
          color="primary"
          prepend-icon="mdi-download"
          @click="downloadSchedule"
        >
          Download
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <!-- Summary Section -->
        <v-row>
          <v-col cols="12" md="4">
            <v-card variant="outlined" class="pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-2">Loan Details</div>
              <div class="d-flex flex-column gap-2">
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Principal</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(loanAmount) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Interest Rate</span>
                  <span class="text-body-2 font-weight-medium">{{ interestRate }}%</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Term</span>
                  <span class="text-body-2 font-weight-medium">{{ loanTerm }} months</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Start Date</span>
                  <span class="text-body-2 font-weight-medium">{{ formatDate(startDate) }}</span>
                </div>
              </div>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-card variant="outlined" class="pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-2">Payment Summary</div>
              <div class="d-flex flex-column gap-2">
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Monthly Payment</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(monthlyPayment) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Total Payments</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(totalPayment) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Total Interest</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(totalInterest) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Last Payment Date</span>
                  <span class="text-body-2 font-weight-medium">{{ formatDate(lastPaymentDate) }}</span>
                </div>
              </div>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-card variant="outlined" class="pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-2">Payment Status</div>
              <div class="d-flex flex-column gap-2">
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Payments Made</span>
                  <span class="text-body-2 font-weight-medium">{{ paymentsMade }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Payments Remaining</span>
                  <span class="text-body-2 font-weight-medium">{{ paymentsRemaining }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Principal Paid</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(principalPaid) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption text-grey-darken-1">Principal Remaining</span>
                  <span class="text-body-2 font-weight-medium">{{ formatCurrency(principalRemaining) }}</span>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
        
        <!-- Progress Bar -->
        <v-card variant="outlined" class="pa-4 mt-4">
          <div class="d-flex justify-space-between mb-2">
            <span class="text-caption text-grey-darken-1">Loan Progress</span>
            <span class="text-caption text-grey-darken-1">{{ Math.round(loanProgress) }}% Complete</span>
          </div>
          <v-progress-linear
            v-model="loanProgress"
            color="primary"
            height="10"
            rounded
          ></v-progress-linear>
          <div class="d-flex justify-space-between mt-2">
            <span class="text-caption text-grey-darken-1">{{ formatDate(startDate) }}</span>
            <span class="text-caption text-grey-darken-1">{{ formatDate(lastPaymentDate) }}</span>
          </div>
        </v-card>
        
        <!-- Payment Breakdown Chart -->
        <v-card variant="outlined" class="pa-4 mt-4">
          <div class="text-subtitle-1 font-weight-medium mb-4">Payment Breakdown Over Time</div>
          <div class="chart-container" style="position: relative; height:300px; width:100%">
            <canvas ref="paymentChart"></canvas>
          </div>
        </v-card>
        
        <!-- Schedule Table -->
        <v-card variant="outlined" class="mt-4">
          <v-card-title class="d-flex align-center">
            <span>Payment Schedule</span>
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
            :items="schedule"
            :search="search"
            :loading="loading"
            :items-per-page="10"
          >
            <!-- Payment Number Column -->
            <template v-slot:item.payment_number="{ item }">
              {{ item.payment_number }}
            </template>
            
            <!-- Payment Date Column -->
            <template v-slot:item.payment_date="{ item }">
              {{ formatDate(item.payment_date) }}
            </template>
            
            <!-- Payment Amount Column -->
            <template v-slot:item.payment_amount="{ item }">
              {{ formatCurrency(item.payment_amount) }}
            </template>
            
            <!-- Principal Column -->
            <template v-slot:item.principal="{ item }">
              {{ formatCurrency(item.principal) }}
            </template>
            
            <!-- Interest Column -->
            <template v-slot:item.interest="{ item }">
              {{ formatCurrency(item.interest) }}
            </template>
            
            <!-- Remaining Balance Column -->
            <template v-slot:item.remaining_balance="{ item }">
              {{ formatCurrency(item.remaining_balance) }}
            </template>
            
            <!-- Status Column -->
            <template v-slot:item.status="{ item }">
              <v-chip
                size="small"
                :color="getPaymentStatusColor(item.status)"
              >
                {{ item.status }}
              </v-chip>
            </template>
          </v-data-table>
        </v-card>
      </v-card-text>
    </v-card>
    
    <!-- Make Payment Dialog -->
    <v-dialog v-model="showPaymentDialog" max-width="500">
      <v-card>
        <v-card-title>Make Payment</v-card-title>
        
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="paymentAmount"
                label="Payment Amount"
                variant="outlined"
                type="number"
                prefix="$"
                :rules="[v => !!v || 'Amount is required', v => v > 0 || 'Amount must be greater than 0']"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12">
              <v-text-field
                v-model="paymentDate"
                label="Payment Date"
                variant="outlined"
                type="date"
                :rules="[v => !!v || 'Date is required']"
                required
              ></v-text-field>
            </v-col>
            
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
              <v-textarea
                v-model="paymentNotes"
                label="Notes (Optional)"
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
            @click="showPaymentDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="processingPayment"
            :disabled="!isValidPayment"
            @click="processPayment"
          >
            Make Payment
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { format, parseISO, differenceInDays } from 'date-fns'
import Chart from 'chart.js/auto'

// Props
const props = defineProps({
  applicationId: {
    type: [Number, String],
    required: true
  },
  loanAmount: {
    type: Number,
    default: 0
  },
  interestRate: {
    type: Number,
    default: 0
  },
  loanTerm: {
    type: Number,
    default: 0
  },
  startDate: {
    type: String,
    default: ''
  },
  schedule: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['payment-made', 'download'])

// State
const search = ref('')
const paymentChart = ref(null)
const chartInstance = ref(null)
const showPaymentDialog = ref(false)
const paymentAmount = ref(0)
const paymentDate = ref(format(new Date(), 'yyyy-MM-dd'))
const paymentMethod = ref('')
const paymentNotes = ref('')
const processingPayment = ref(false)

// Table headers
const headers = [
  { title: 'Payment #', key: 'payment_number', sortable: true },
  { title: 'Due Date', key: 'payment_date', sortable: true },
  { title: 'Payment', key: 'payment_amount', sortable: true },
  { title: 'Principal', key: 'principal', sortable: true },
  { title: 'Interest', key: 'interest', sortable: true },
  { title: 'Remaining Balance', key: 'remaining_balance', sortable: true },
  { title: 'Status', key: 'status', sortable: true }
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
const monthlyPayment = computed(() => {
  if (props.schedule.length > 0) {
    return props.schedule[0].payment_amount
  }
  return 0
})

const totalPayment = computed(() => {
  return props.schedule.reduce((sum, payment) => sum + payment.payment_amount, 0)
})

const totalInterest = computed(() => {
  return props.schedule.reduce((sum, payment) => sum + payment.interest, 0)
})

const lastPaymentDate = computed(() => {
  if (props.schedule.length > 0) {
    return props.schedule[props.schedule.length - 1].payment_date
  }
  return ''
})

const paymentsMade = computed(() => {
  return props.schedule.filter(payment => payment.status === 'paid').length
})

const paymentsRemaining = computed(() => {
  return props.schedule.filter(payment => payment.status !== 'paid').length
})

const principalPaid = computed(() => {
  return props.schedule
    .filter(payment => payment.status === 'paid')
    .reduce((sum, payment) => sum + payment.principal, 0)
})

const principalRemaining = computed(() => {
  return props.loanAmount - principalPaid.value
})

const loanProgress = computed(() => {
  if (props.loanAmount === 0) return 0
  return (principalPaid.value / props.loanAmount) * 100
})

const isValidPayment = computed(() => {
  return paymentAmount.value > 0 && paymentDate.value && paymentMethod.value
})

// Methods
const downloadSchedule = () => {
  emit('download')
}

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
    const date = typeof dateString === 'string' ? parseISO(dateString) : dateString
    return format(date, 'MMM d, yyyy')
  } catch (error) {
    return dateString
  }
}

const getPaymentStatusColor = (status) => {
  const statusColors = {
    paid: 'success',
    due: 'warning',
    upcoming: 'info',
    late: 'error',
    partial: 'amber'
  }
  
  return statusColors[status] || 'grey'
}

const updateChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
  
  if (!paymentChart.value) return
  
  const ctx = paymentChart.value.getContext('2d')
  
  // Prepare data for chart
  const labels = []
  const principalData = []
  const interestData = []
  
  // Use a subset of payments for better visualization
  const step = Math.max(1, Math.floor(props.schedule.length / 12))
  for (let i = 0; i < props.schedule.length; i += step) {
    const payment = props.schedule[i]
    labels.push(`Payment ${payment.payment_number}`)
    principalData.push(payment.principal)
    interestData.push(payment.interest)
  }
  
  chartInstance.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Principal',
          data: principalData,
          backgroundColor: 'rgba(25, 118, 210, 0.6)',
          borderColor: 'rgba(25, 118, 210, 1)',
          borderWidth: 1
        },
        {
          label: 'Interest',
          data: interestData,
          backgroundColor: 'rgba(255, 82, 82, 0.6)',
          borderColor: 'rgba(255, 82, 82, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true
        },
        y: {
          stacked: true,
          ticks: {
            callback: function(value) {
              return '$' + value.toLocaleString()
            }
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.dataset.label || '';
              const value = context.raw;
              return `${label}: ${formatCurrency(value)}`;
            }
          }
        }
      }
    }
  })
}

const openPaymentDialog = () => {
  // Find the next due payment
  const nextPayment = props.schedule.find(payment => payment.status === 'due' || payment.status === 'late')
  
  if (nextPayment) {
    paymentAmount.value = nextPayment.payment_amount
    paymentDate.value = format(new Date(), 'yyyy-MM-dd')
  } else {
    paymentAmount.value = 0
    paymentDate.value = format(new Date(), 'yyyy-MM-dd')
  }
  
  paymentMethod.value = ''
  paymentNotes.value = ''
  showPaymentDialog.value = true
}

const processPayment = async () => {
  if (!isValidPayment.value) return
  
  processingPayment.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await paymentService.makePayment(props.applicationId, {
    //   amount: parseFloat(paymentAmount.value),
    //   date: paymentDate.value,
    //   method: paymentMethod.value,
    //   notes: paymentNotes.value
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Close dialog
    showPaymentDialog.value = false
    
    // Emit event
    emit('payment-made', {
      amount: parseFloat(paymentAmount.value),
      date: paymentDate.value,
      method: paymentMethod.value,
      notes: paymentNotes.value
    })
  } catch (error) {
    console.error('Error processing payment:', error)
    // Show error notification
  } finally {
    processingPayment.value = false
  }
}

// Initialize
onMounted(() => {
  updateChart()
})

// Watch for schedule changes
watch(() => props.schedule, () => {
  updateChart()
}, { deep: true })

// Expose methods to parent
defineExpose({
  openPaymentDialog
})
</script>

<style scoped>
.repayment-schedule {
  width: 100%;
}

.chart-container {
  max-height: 300px;
}
</style>
