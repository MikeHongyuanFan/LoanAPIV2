<template>
  <div class="loan-calculator">
    <v-card>
      <v-card-title>Loan Calculator</v-card-title>
      
      <v-card-text>
        <v-row>
          <!-- Loan Parameters -->
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-4">Loan Parameters</div>
              
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="loanAmount"
                    label="Loan Amount"
                    variant="outlined"
                    type="number"
                    prefix="$"
                    :rules="[v => !!v || 'Amount is required', v => v > 0 || 'Amount must be greater than 0']"
                    @update:model-value="calculateLoan"
                    hide-details="auto"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-text-field
                    v-model="interestRate"
                    label="Interest Rate (%)"
                    variant="outlined"
                    type="number"
                    step="0.01"
                    suffix="%"
                    :rules="[v => !!v || 'Interest rate is required', v => v >= 0 || 'Interest rate must be non-negative']"
                    @update:model-value="calculateLoan"
                    hide-details="auto"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-text-field
                    v-model="loanTerm"
                    label="Loan Term (months)"
                    variant="outlined"
                    type="number"
                    :rules="[v => !!v || 'Term is required', v => v > 0 || 'Term must be greater than 0']"
                    @update:model-value="calculateLoan"
                    hide-details="auto"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-select
                    v-model="paymentFrequency"
                    label="Payment Frequency"
                    :items="paymentFrequencyOptions"
                    variant="outlined"
                    @update:model-value="calculateLoan"
                    hide-details="auto"
                  ></v-select>
                </v-col>
                
                <v-col cols="12">
                  <v-select
                    v-model="loanType"
                    label="Loan Type"
                    :items="loanTypeOptions"
                    variant="outlined"
                    @update:model-value="calculateLoan"
                    hide-details="auto"
                  ></v-select>
                </v-col>
                
                <v-col cols="12">
                  <v-text-field
                    v-model="startDate"
                    label="Start Date"
                    variant="outlined"
                    type="date"
                    @update:model-value="calculateLoan"
                    hide-details="auto"
                  ></v-text-field>
                </v-col>
              </v-row>
              
              <div class="d-flex justify-end mt-4">
                <v-btn
                  color="primary"
                  @click="calculateLoan"
                  :loading="calculating"
                >
                  Calculate
                </v-btn>
              </div>
            </v-card>
          </v-col>
          
          <!-- Calculation Results -->
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-4">Calculation Results</div>
              
              <div class="d-flex flex-column gap-4">
                <div class="result-item">
                  <div class="text-caption text-grey-darken-1">Monthly Payment</div>
                  <div class="text-h5 font-weight-bold">{{ formatCurrency(monthlyPayment) }}</div>
                </div>
                
                <v-divider></v-divider>
                
                <div class="result-item">
                  <div class="text-caption text-grey-darken-1">Total Payment</div>
                  <div class="text-h6">{{ formatCurrency(totalPayment) }}</div>
                </div>
                
                <div class="result-item">
                  <div class="text-caption text-grey-darken-1">Total Interest</div>
                  <div class="text-h6">{{ formatCurrency(totalInterest) }}</div>
                </div>
                
                <v-divider></v-divider>
                
                <div class="result-item">
                  <div class="text-caption text-grey-darken-1">Annual Percentage Rate (APR)</div>
                  <div class="text-h6">{{ apr }}%</div>
                </div>
                
                <div class="result-item">
                  <div class="text-caption text-grey-darken-1">Loan-to-Value Ratio (LTV)</div>
                  <div class="text-h6">{{ ltv }}%</div>
                </div>
                
                <v-divider></v-divider>
                
                <div class="result-item">
                  <div class="text-caption text-grey-darken-1">First Payment Date</div>
                  <div class="text-body-1">{{ formatDate(firstPaymentDate) }}</div>
                </div>
                
                <div class="result-item">
                  <div class="text-caption text-grey-darken-1">Last Payment Date</div>
                  <div class="text-body-1">{{ formatDate(lastPaymentDate) }}</div>
                </div>
              </div>
              
              <div class="d-flex justify-end mt-4">
                <v-btn
                  variant="outlined"
                  color="primary"
                  prepend-icon="mdi-file-chart"
                  @click="showAmortizationSchedule = true"
                >
                  View Amortization Schedule
                </v-btn>
              </div>
            </v-card>
          </v-col>
        </v-row>
        
        <!-- Payment Distribution Chart -->
        <v-row class="mt-4">
          <v-col cols="12">
            <v-card variant="outlined">
              <v-card-title>Payment Distribution</v-card-title>
              <v-card-text>
                <div class="d-flex justify-center">
                  <div class="chart-container" style="position: relative; height:300px; width:100%">
                    <canvas ref="paymentChart"></canvas>
                  </div>
                </div>
                
                <div class="d-flex justify-center mt-4">
                  <div class="d-flex align-center mr-4">
                    <div class="chart-legend-color" style="background-color: rgba(25, 118, 210, 0.6)"></div>
                    <span class="text-body-2">Principal ({{ formatCurrency(loanAmount) }})</span>
                  </div>
                  
                  <div class="d-flex align-center">
                    <div class="chart-legend-color" style="background-color: rgba(255, 82, 82, 0.6)"></div>
                    <span class="text-body-2">Interest ({{ formatCurrency(totalInterest) }})</span>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    
    <!-- Amortization Schedule Dialog -->
    <v-dialog v-model="showAmortizationSchedule" max-width="900">
      <v-card>
        <v-card-title class="d-flex align-center">
          <span>Amortization Schedule</span>
          <v-spacer></v-spacer>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            @click="showAmortizationSchedule = false"
          ></v-btn>
        </v-card-title>
        
        <v-divider></v-divider>
        
        <v-card-text class="pa-0">
          <v-data-table
            :headers="amortizationHeaders"
            :items="amortizationSchedule"
            :items-per-page="12"
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
          </v-data-table>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions>
          <v-btn
            variant="text"
            prepend-icon="mdi-download"
            @click="downloadAmortizationSchedule"
          >
            Download Schedule
          </v-btn>
          
          <v-spacer></v-spacer>
          
          <v-btn
            color="primary"
            @click="showAmortizationSchedule = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { format, addMonths } from 'date-fns'
import Chart from 'chart.js/auto'

// Props
const props = defineProps({
  initialAmount: {
    type: [Number, String],
    default: 0
  },
  initialRate: {
    type: [Number, String],
    default: 5
  },
  initialTerm: {
    type: [Number, String],
    default: 36
  },
  initialFrequency: {
    type: String,
    default: 'monthly'
  },
  initialType: {
    type: String,
    default: 'fixed'
  },
  propertyValue: {
    type: [Number, String],
    default: 0
  }
})

// Emits
const emit = defineEmits(['update:schedule', 'save-calculation'])

// State
const loanAmount = ref(props.initialAmount)
const interestRate = ref(props.initialRate)
const loanTerm = ref(props.initialTerm)
const paymentFrequency = ref(props.initialFrequency)
const loanType = ref(props.initialType)
const startDate = ref(format(new Date(), 'yyyy-MM-dd'))
const calculating = ref(false)

// Results
const monthlyPayment = ref(0)
const totalPayment = ref(0)
const totalInterest = ref(0)
const apr = ref(0)
const ltv = ref(0)
const firstPaymentDate = ref('')
const lastPaymentDate = ref('')
const amortizationSchedule = ref([])

// UI state
const showAmortizationSchedule = ref(false)
const paymentChart = ref(null)
const chartInstance = ref(null)

// Options
const paymentFrequencyOptions = [
  { title: 'Monthly', value: 'monthly' },
  { title: 'Bi-Weekly', value: 'bi_weekly' },
  { title: 'Weekly', value: 'weekly' }
]

const loanTypeOptions = [
  { title: 'Fixed Rate', value: 'fixed' },
  { title: 'Variable Rate', value: 'variable' },
  { title: 'Interest Only', value: 'interest_only' }
]

// Table headers for amortization schedule
const amortizationHeaders = [
  { title: 'Payment #', key: 'payment_number', sortable: true },
  { title: 'Payment Date', key: 'payment_date', sortable: true },
  { title: 'Payment Amount', key: 'payment_amount', sortable: true },
  { title: 'Principal', key: 'principal', sortable: true },
  { title: 'Interest', key: 'interest', sortable: true },
  { title: 'Remaining Balance', key: 'remaining_balance', sortable: true }
]

// Methods
const calculateLoan = async () => {
  if (!loanAmount.value || !interestRate.value || !loanTerm.value) return
  
  calculating.value = true
  
  try {
    // This would be an API call in a real application
    // const response = await calculatorService.calculateLoan({
    //   amount: parseFloat(loanAmount.value),
    //   interest_rate: parseFloat(interestRate.value),
    //   term: parseInt(loanTerm.value),
    //   payment_frequency: paymentFrequency.value,
    //   loan_type: loanType.value,
    //   start_date: startDate.value,
    //   property_value: parseFloat(props.propertyValue)
    // })
    
    // Mock delay for demonstration
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Calculate monthly payment (simplified formula for fixed rate)
    const principal = parseFloat(loanAmount.value)
    const rate = parseFloat(interestRate.value) / 100 / 12
    const term = parseInt(loanTerm.value)
    
    let payment = 0
    let schedule = []
    
    if (loanType.value === 'interest_only') {
      // Interest only loan
      payment = principal * rate
      
      // Generate amortization schedule
      let balance = principal
      let paymentDate = new Date(startDate.value)
      
      for (let i = 1; i <= term; i++) {
        paymentDate = addMonths(paymentDate, 1)
        const interest = balance * rate
        const principalPayment = i === term ? principal : 0
        
        schedule.push({
          payment_number: i,
          payment_date: format(paymentDate, 'yyyy-MM-dd'),
          payment_amount: i === term ? payment + principal : payment,
          principal: principalPayment,
          interest: interest,
          remaining_balance: i === term ? 0 : balance
        })
      }
    } else {
      // Standard amortization formula
      payment = principal * rate * Math.pow(1 + rate, term) / (Math.pow(1 + rate, term) - 1)
      
      // Generate amortization schedule
      let balance = principal
      let paymentDate = new Date(startDate.value)
      
      for (let i = 1; i <= term; i++) {
        paymentDate = addMonths(paymentDate, 1)
        const interest = balance * rate
        const principalPayment = payment - interest
        balance -= principalPayment
        
        schedule.push({
          payment_number: i,
          payment_date: format(paymentDate, 'yyyy-MM-dd'),
          payment_amount: payment,
          principal: principalPayment,
          interest: interest,
          remaining_balance: balance > 0 ? balance : 0
        })
      }
    }
    
    // Update results
    monthlyPayment.value = payment
    totalPayment.value = payment * term
    totalInterest.value = totalPayment.value - principal
    apr.value = parseFloat(interestRate.value).toFixed(2)
    ltv.value = props.propertyValue > 0 ? ((principal / props.propertyValue) * 100).toFixed(2) : 0
    
    // Set payment dates
    if (schedule.length > 0) {
      firstPaymentDate.value = schedule[0].payment_date
      lastPaymentDate.value = schedule[schedule.length - 1].payment_date
    }
    
    // Update amortization schedule
    amortizationSchedule.value = schedule
    
    // Update chart
    updateChart()
    
    // Emit event with schedule
    emit('update:schedule', schedule)
  } catch (error) {
    console.error('Error calculating loan:', error)
    // Show error notification
  } finally {
    calculating.value = false
  }
}

const updateChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
  
  const ctx = paymentChart.value.getContext('2d')
  
  chartInstance.value = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Principal', 'Interest'],
      datasets: [{
        data: [parseFloat(loanAmount.value), totalInterest.value],
        backgroundColor: [
          'rgba(25, 118, 210, 0.6)',
          'rgba(255, 82, 82, 0.6)'
        ],
        borderColor: [
          'rgba(25, 118, 210, 1)',
          'rgba(255, 82, 82, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
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

const downloadAmortizationSchedule = () => {
  // In a real application, this would generate a CSV or PDF file
  console.log('Downloading amortization schedule')
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
    const date = new Date(dateString)
    return format(date, 'MMM d, yyyy')
  } catch (error) {
    return dateString
  }
}

// Initialize
onMounted(() => {
  calculateLoan()
})

// Watch for prop changes
watch([
  () => props.initialAmount,
  () => props.initialRate,
  () => props.initialTerm,
  () => props.initialFrequency,
  () => props.initialType
], ([newAmount, newRate, newTerm, newFrequency, newType]) => {
  loanAmount.value = newAmount
  interestRate.value = newRate
  loanTerm.value = newTerm
  paymentFrequency.value = newFrequency
  loanType.value = newType
  
  calculateLoan()
}, { immediate: true })
</script>

<style scoped>
.loan-calculator {
  width: 100%;
}

.result-item {
  margin-bottom: 8px;
}

.chart-legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  margin-right: 8px;
}

.chart-container {
  max-height: 300px;
}
</style>
