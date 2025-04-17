<template>
  <div class="borrower-details-tab">
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="bg-grey-lighten-4 py-3">
            <v-icon start class="mr-2">mdi-briefcase-outline</v-icon>
            Employment Information
          </v-card-title>
          <v-card-text class="pa-4">
            <div v-if="borrower.employment">
              <div class="d-flex align-center mb-4">
                <v-avatar color="primary" class="mr-3">
                  <v-icon color="white">mdi-domain</v-icon>
                </v-avatar>
                <div>
                  <div class="text-subtitle-1 font-weight-medium">{{ borrower.employment.employer_name }}</div>
                  <div class="text-body-2 text-medium-emphasis">{{ borrower.employment.position }}</div>
                </div>
              </div>
              
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-label">Employment Status</div>
                  <div class="detail-value">{{ formatEmploymentStatus(borrower.employment.status) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Industry</div>
                  <div class="detail-value">{{ borrower.employment.industry || 'Not specified' }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Start Date</div>
                  <div class="detail-value">{{ formatDate(borrower.employment.start_date) || 'Not specified' }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">End Date</div>
                  <div class="detail-value">{{ formatDate(borrower.employment.end_date) || 'Current' }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Years in Job</div>
                  <div class="detail-value">{{ formatYearsInJob(borrower.employment.years_in_job) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Years in Industry</div>
                  <div class="detail-value">{{ formatYearsInJob(borrower.employment.years_in_industry) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Employer Phone</div>
                  <div class="detail-value">
                    <a v-if="borrower.employment.employer_phone" :href="`tel:${borrower.employment.employer_phone}`" class="text-decoration-none">
                      {{ borrower.employment.employer_phone }}
                    </a>
                    <span v-else>Not specified</span>
                  </div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Employer Address</div>
                  <div class="detail-value">{{ formatEmployerAddress(borrower.employment) }}</div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-briefcase-off</v-icon>
              <div class="text-body-1">No employment information available</div>
            </div>
          </v-card-text>
        </v-card>
        
        <v-card class="mt-4">
          <v-card-title class="bg-grey-lighten-4 py-3">
            <v-icon start class="mr-2">mdi-bank-outline</v-icon>
            Banking Information
          </v-card-title>
          <v-card-text class="pa-4">
            <div v-if="borrower.banking">
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-label">Bank Name</div>
                  <div class="detail-value">{{ borrower.banking.bank_name || 'Not specified' }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Account Type</div>
                  <div class="detail-value">{{ formatAccountType(borrower.banking.account_type) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Account Number</div>
                  <div class="detail-value">{{ formatAccountNumber(borrower.banking.account_number) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">BSB / Routing Number</div>
                  <div class="detail-value">{{ borrower.banking.bsb || 'Not specified' }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Account Holder Name</div>
                  <div class="detail-value">{{ borrower.banking.account_holder_name || 'Not specified' }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Years with Bank</div>
                  <div class="detail-value">{{ formatYearsWithBank(borrower.banking.years_with_bank) }}</div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-bank-off</v-icon>
              <div class="text-body-1">No banking information available</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="bg-grey-lighten-4 py-3">
            <v-icon start class="mr-2">mdi-cash-multiple</v-icon>
            Financial Information
          </v-card-title>
          <v-card-text class="pa-4">
            <div v-if="borrower.financial">
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-label">Annual Income</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.annual_income) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Additional Income</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.additional_income) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Income Frequency</div>
                  <div class="detail-value">{{ formatIncomeFrequency(borrower.financial.income_frequency) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Total Assets</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.total_assets) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Total Liabilities</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.total_liabilities) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Net Worth</div>
                  <div class="detail-value">{{ formatCurrency(calculateNetWorth) }}</div>
                </div>
              </div>
              
              <v-divider class="my-4"></v-divider>
              
              <h4 class="text-subtitle-2 font-weight-medium mb-3">Monthly Expenses</h4>
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-label">Housing</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.monthly_expenses?.housing) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Utilities</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.monthly_expenses?.utilities) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Transportation</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.monthly_expenses?.transportation) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Food</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.monthly_expenses?.food) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Loan Repayments</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.monthly_expenses?.loan_repayments) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Other</div>
                  <div class="detail-value">{{ formatCurrency(borrower.financial.monthly_expenses?.other) }}</div>
                </div>
                
                <div class="detail-item">
                  <div class="detail-label">Total Monthly Expenses</div>
                  <div class="detail-value font-weight-bold">{{ formatCurrency(calculateTotalMonthlyExpenses) }}</div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-cash-off</v-icon>
              <div class="text-body-1">No financial information available</div>
            </div>
          </v-card-text>
        </v-card>
        
        <v-card class="mt-4">
          <v-card-title class="bg-grey-lighten-4 py-3">
            <v-icon start class="mr-2">mdi-note-text-outline</v-icon>
            Additional Information
          </v-card-title>
          <v-card-text class="pa-4">
            <div v-if="borrower.additional_info">
              <div class="detail-item mb-4">
                <div class="detail-label">Notes</div>
                <div class="detail-value">{{ borrower.additional_info.notes || 'No notes available' }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Tags</div>
                <div class="detail-value">
                  <v-chip
                    v-for="(tag, index) in borrower.additional_info.tags"
                    :key="index"
                    size="small"
                    class="mr-1 mb-1"
                  >
                    {{ tag }}
                  </v-chip>
                  <span v-if="!borrower.additional_info.tags || borrower.additional_info.tags.length === 0">
                    No tags
                  </span>
                </div>
              </div>
              
              <div class="detail-item mt-4">
                <div class="detail-label">Referral Source</div>
                <div class="detail-value">{{ borrower.additional_info.referral_source || 'Not specified' }}</div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-note-off</v-icon>
              <div class="text-body-1">No additional information available</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { formatDate } from '@/utils/dateUtils';

const props = defineProps({
  borrower: {
    type: Object,
    required: true
  }
});

// Computed properties
const calculateNetWorth = computed(() => {
  if (!props.borrower.financial) return 0;
  
  const assets = props.borrower.financial.total_assets || 0;
  const liabilities = props.borrower.financial.total_liabilities || 0;
  
  return assets - liabilities;
});

const calculateTotalMonthlyExpenses = computed(() => {
  if (!props.borrower.financial || !props.borrower.financial.monthly_expenses) return 0;
  
  const expenses = props.borrower.financial.monthly_expenses;
  
  return (expenses.housing || 0) +
         (expenses.utilities || 0) +
         (expenses.transportation || 0) +
         (expenses.food || 0) +
         (expenses.loan_repayments || 0) +
         (expenses.other || 0);
});

// Formatting functions
const formatEmploymentStatus = (status) => {
  if (!status) return 'Not specified';
  
  const statusMap = {
    'FULL_TIME': 'Full-time',
    'PART_TIME': 'Part-time',
    'CASUAL': 'Casual',
    'SELF_EMPLOYED': 'Self-employed',
    'CONTRACT': 'Contract',
    'UNEMPLOYED': 'Unemployed',
    'RETIRED': 'Retired',
    'STUDENT': 'Student'
  };
  
  return statusMap[status] || status;
};

const formatYearsInJob = (years) => {
  if (!years) return 'Not specified';
  
  if (years < 1) {
    const months = Math.round(years * 12);
    return `${months} ${months === 1 ? 'month' : 'months'}`;
  }
  
  return `${years} ${years === 1 ? 'year' : 'years'}`;
};

const formatEmployerAddress = (employment) => {
  if (!employment || !employment.employer_address) return 'Not specified';
  
  const address = employment.employer_address;
  const parts = [];
  
  if (address.street) parts.push(address.street);
  if (address.city) parts.push(address.city);
  if (address.state) parts.push(address.state);
  if (address.postal_code) parts.push(address.postal_code);
  
  return parts.join(', ') || 'Not specified';
};

const formatAccountType = (type) => {
  if (!type) return 'Not specified';
  
  const typeMap = {
    'CHECKING': 'Checking',
    'SAVINGS': 'Savings',
    'CREDIT_CARD': 'Credit Card',
    'LOAN': 'Loan',
    'INVESTMENT': 'Investment'
  };
  
  return typeMap[type] || type;
};

const formatAccountNumber = (number) => {
  if (!number) return 'Not specified';
  
  // Mask account number for security
  const lastFour = number.slice(-4);
  return `XXXX-XXXX-${lastFour}`;
};

const formatYearsWithBank = (years) => {
  if (!years) return 'Not specified';
  
  if (years < 1) {
    const months = Math.round(years * 12);
    return `${months} ${months === 1 ? 'month' : 'months'}`;
  }
  
  return `${years} ${years === 1 ? 'year' : 'years'}`;
};

const formatCurrency = (value) => {
  if (value === null || value === undefined) return 'Not specified';
  
  return new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD',
    minimumFractionDigits: 2
  }).format(value);
};

const formatIncomeFrequency = (frequency) => {
  if (!frequency) return 'Not specified';
  
  const frequencyMap = {
    'WEEKLY': 'Weekly',
    'FORTNIGHTLY': 'Fortnightly',
    'MONTHLY': 'Monthly',
    'QUARTERLY': 'Quarterly',
    'ANNUALLY': 'Annually'
  };
  
  return frequencyMap[frequency] || frequency;
};
</script>

<style scoped>
.borrower-details-tab {
  padding-bottom: 1rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.detail-item {
  margin-bottom: 8px;
}

.detail-label {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 4px;
}

.detail-value {
  font-size: 0.9375rem;
}

@media (max-width: 600px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
