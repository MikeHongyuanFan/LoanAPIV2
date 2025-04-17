<template>
  <div class="application-financial-summary">
    <h3 class="text-subtitle-1 font-weight-bold mb-4">Financial Summary</h3>
    
    <div class="financial-grid">
      <div class="financial-item">
        <div class="financial-label">Loan Amount</div>
        <div class="financial-value">{{ formatCurrency(application.loan_amount) }}</div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Interest Rate</div>
        <div class="financial-value">{{ formatPercentage(application.interest_rate) }}</div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Loan Term</div>
        <div class="financial-value">{{ formatTerm(application.loan_term, application.loan_term_unit) }}</div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Repayment Frequency</div>
        <div class="financial-value">{{ formatFrequency(application.repayment_frequency) }}</div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Monthly Repayment</div>
        <div class="financial-value">{{ formatCurrency(calculatedMonthlyRepayment) }}</div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Total Repayment</div>
        <div class="financial-value">{{ formatCurrency(calculatedTotalRepayment) }}</div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Total Interest</div>
        <div class="financial-value">{{ formatCurrency(calculatedTotalInterest) }}</div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Loan-to-Value Ratio</div>
        <div class="financial-value">
          <template v-if="calculatedLTV !== null">
            {{ formatPercentage(calculatedLTV) }}
            <v-chip
              size="x-small"
              :color="ltvColor"
              class="ml-2"
            >
              {{ ltvRating }}
            </v-chip>
          </template>
          <span v-else>N/A</span>
        </div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Security Value</div>
        <div class="financial-value">{{ formatCurrency(application.security_value) }}</div>
      </div>
      
      <div class="financial-item">
        <div class="financial-label">Application Fee</div>
        <div class="financial-value">{{ formatCurrency(application.application_fee) }}</div>
      </div>
    </div>
    
    <v-divider class="my-4"></v-divider>
    
    <div class="d-flex justify-space-between align-center">
      <div>
        <div class="text-subtitle-2 font-weight-bold">Estimated Settlement Date</div>
        <div>{{ formatDate(application.estimated_settlement_date) || 'Not specified' }}</div>
      </div>
      
      <v-btn
        color="primary"
        variant="text"
        prepend-icon="mdi-calculator"
        @click="openCalculator"
      >
        Loan Calculator
      </v-btn>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { formatDate } from '@/utils/dateUtils';
import { useRouter } from 'vue-router';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

const router = useRouter();

// Formatting functions
const formatCurrency = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD',
    minimumFractionDigits: 2
  }).format(value);
};

const formatPercentage = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return new Intl.NumberFormat('en-AU', {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value / 100);
};

const formatTerm = (term, unit) => {
  if (!term) return 'N/A';
  
  const unitMap = {
    'YEARS': term === 1 ? 'year' : 'years',
    'MONTHS': term === 1 ? 'month' : 'months',
    'WEEKS': term === 1 ? 'week' : 'weeks',
    'DAYS': term === 1 ? 'day' : 'days'
  };
  
  return `${term} ${unitMap[unit] || unit.toLowerCase()}`;
};

const formatFrequency = (frequency) => {
  if (!frequency) return 'N/A';
  
  const frequencyMap = {
    'WEEKLY': 'Weekly',
    'FORTNIGHTLY': 'Fortnightly',
    'MONTHLY': 'Monthly',
    'QUARTERLY': 'Quarterly',
    'ANNUALLY': 'Annually'
  };
  
  return frequencyMap[frequency] || frequency;
};

// Computed properties
const calculatedMonthlyRepayment = computed(() => {
  // This is a simplified calculation - in a real app, you'd use the actual calculation from the backend
  if (!props.application.loan_amount || !props.application.interest_rate || !props.application.loan_term) {
    return null;
  }
  
  const principal = props.application.loan_amount;
  const monthlyRate = (props.application.interest_rate / 100) / 12;
  let termInMonths = props.application.loan_term;
  
  // Convert term to months if needed
  if (props.application.loan_term_unit === 'YEARS') {
    termInMonths = props.application.loan_term * 12;
  } else if (props.application.loan_term_unit === 'WEEKS') {
    termInMonths = props.application.loan_term / 4.33;
  } else if (props.application.loan_term_unit === 'DAYS') {
    termInMonths = props.application.loan_term / 30.44;
  }
  
  // Calculate monthly payment using the formula: P * r * (1 + r)^n / ((1 + r)^n - 1)
  const payment = principal * monthlyRate * Math.pow(1 + monthlyRate, termInMonths) / 
                 (Math.pow(1 + monthlyRate, termInMonths) - 1);
  
  return isNaN(payment) ? null : payment;
});

const calculatedTotalRepayment = computed(() => {
  if (calculatedMonthlyRepayment.value === null) return null;
  
  let termInMonths = props.application.loan_term;
  
  // Convert term to months if needed
  if (props.application.loan_term_unit === 'YEARS') {
    termInMonths = props.application.loan_term * 12;
  } else if (props.application.loan_term_unit === 'WEEKS') {
    termInMonths = props.application.loan_term / 4.33;
  } else if (props.application.loan_term_unit === 'DAYS') {
    termInMonths = props.application.loan_term / 30.44;
  }
  
  return calculatedMonthlyRepayment.value * termInMonths;
});

const calculatedTotalInterest = computed(() => {
  if (calculatedTotalRepayment.value === null || !props.application.loan_amount) return null;
  return calculatedTotalRepayment.value - props.application.loan_amount;
});

const calculatedLTV = computed(() => {
  if (!props.application.loan_amount || !props.application.security_value) return null;
  return (props.application.loan_amount / props.application.security_value) * 100;
});

const ltvRating = computed(() => {
  if (calculatedLTV.value === null) return '';
  
  if (calculatedLTV.value <= 60) return 'Excellent';
  if (calculatedLTV.value <= 75) return 'Good';
  if (calculatedLTV.value <= 85) return 'Fair';
  return 'High';
});

const ltvColor = computed(() => {
  if (calculatedLTV.value === null) return '';
  
  if (calculatedLTV.value <= 60) return 'success';
  if (calculatedLTV.value <= 75) return 'light-green';
  if (calculatedLTV.value <= 85) return 'amber';
  return 'error';
});

// Methods
const openCalculator = () => {
  router.push({
    name: 'LoanCalculator',
    params: { id: props.application.id }
  });
};
</script>

<style scoped>
.application-financial-summary {
  height: 100%;
}

.financial-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.financial-item {
  margin-bottom: 8px;
}

.financial-label {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 4px;
}

.financial-value {
  font-size: 0.9375rem;
  font-weight: 500;
  display: flex;
  align-items: center;
}

@media (max-width: 600px) {
  .financial-grid {
    grid-template-columns: 1fr;
  }
}
</style>
