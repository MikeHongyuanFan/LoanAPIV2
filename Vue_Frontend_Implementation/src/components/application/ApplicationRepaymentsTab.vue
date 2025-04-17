<template>
  <div class="application-repayments-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Repayment Schedule</h3>
      <div class="d-flex">
        <v-btn
          v-if="canRecalculateRepayments"
          color="primary"
          variant="outlined"
          class="mr-2"
          prepend-icon="mdi-calculator"
          @click="showCalculatorDialog = true"
        >
          Recalculate
        </v-btn>
        <v-btn
          v-if="canExportRepayments"
          color="primary"
          prepend-icon="mdi-export"
          @click="exportRepaymentSchedule"
        >
          Export
        </v-btn>
      </div>
    </div>

    <v-card v-if="!hasRepaymentSchedule" class="mb-4">
      <v-card-text class="text-center py-8">
        <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-calendar-blank</v-icon>
        <h3 class="text-h6 mb-2">No Repayment Schedule</h3>
        <p class="text-body-1 text-medium-emphasis mb-4">
          This application doesn't have a repayment schedule yet.
        </p>
        <v-btn
          v-if="canCreateRepayments"
          color="primary"
          prepend-icon="mdi-calculator"
          @click="showCalculatorDialog = true"
        >
          Create Repayment Schedule
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- Loan Summary Card -->
    <v-card v-if="hasRepaymentSchedule" class="mb-4">
      <v-card-title class="bg-grey-lighten-4 py-3">
        <v-icon start class="mr-2">mdi-cash-multiple</v-icon>
        Loan Summary
      </v-card-title>
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <div class="text-overline">Principal</div>
            <div class="text-h6">{{ formatCurrency(application.loan_amount) }}</div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-overline">Interest Rate</div>
            <div class="text-h6">{{ formatPercentage(application.interest_rate) }}</div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-overline">Term</div>
            <div class="text-h6">{{ formatTerm(application.loan_term, application.loan_term_unit) }}</div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-overline">Frequency</div>
            <div class="text-h6">{{ formatFrequency(application.repayment_frequency) }}</div>
          </v-col>
        </v-row>
        <v-divider class="my-4"></v-divider>
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <div class="text-overline">Regular Payment</div>
            <div class="text-h6">{{ formatCurrency(repaymentSummary.regular_payment) }}</div>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <div class="text-overline">Total Interest</div>
            <div class="text-h6">{{ formatCurrency(repaymentSummary.total_interest) }}</div>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <div class="text-overline">Total Repayment</div>
            <div class="text-h6">{{ formatCurrency(repaymentSummary.total_repayment) }}</div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Integrate the existing RepaymentSchedule component -->
    <repayment-schedule
      v-if="hasRepaymentSchedule"
      :application-id="application.id"
      @schedule-updated="handleScheduleUpdated"
    />

    <!-- Calculator Dialog -->
    <v-dialog v-model="showCalculatorDialog" max-width="800px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-calculator</v-icon>
          Loan Calculator
        </v-card-title>
        <v-card-text class="pa-4">
          <loan-calculator
            :application="application"
            :is-dialog="true"
            @calculation-saved="handleCalculationSaved"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showCalculatorDialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Export Format Dialog -->
    <v-dialog v-model="showExportDialog" max-width="500px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-export</v-icon>
          Export Repayment Schedule
        </v-card-title>
        <v-card-text class="pa-4">
          <v-radio-group v-model="exportFormat">
            <v-radio label="PDF Document" value="pdf"></v-radio>
            <v-radio label="Excel Spreadsheet" value="xlsx"></v-radio>
            <v-radio label="CSV File" value="csv"></v-radio>
          </v-radio-group>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showExportDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="confirmExport" :loading="exporting">
            Export
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
import { useApplicationStore } from '@/stores/application';
import RepaymentSchedule from '@/components/application/RepaymentSchedule.vue';
import LoanCalculator from '@/components/application/LoanCalculator.vue';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

// Stores
const authStore = useAuthStore();
const notificationStore = useNotificationStore();
const applicationStore = useApplicationStore();

// State
const repaymentSummary = ref({
  regular_payment: 0,
  total_interest: 0,
  total_repayment: 0
});
const hasRepaymentSchedule = ref(false);
const showCalculatorDialog = ref(false);
const showExportDialog = ref(false);
const exportFormat = ref('pdf');
const exporting = ref(false);

// Computed properties
const canCreateRepayments = computed(() => {
  return authStore.hasPermission('application:edit') && 
         !['COMPLETED', 'CANCELLED'].includes(props.application.status);
});

const canRecalculateRepayments = computed(() => {
  return authStore.hasPermission('application:edit') && 
         hasRepaymentSchedule.value && 
         !['COMPLETED', 'CANCELLED'].includes(props.application.status);
});

const canExportRepayments = computed(() => {
  return hasRepaymentSchedule.value;
});

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

// Methods
const fetchRepaymentSummary = async () => {
  try {
    const schedule = await applicationStore.getRepaymentSchedule(props.application.id);
    if (schedule && schedule.summary) {
      repaymentSummary.value = schedule.summary;
      hasRepaymentSchedule.value = true;
    } else {
      hasRepaymentSchedule.value = false;
    }
  } catch (error) {
    console.error('Error fetching repayment schedule:', error);
    hasRepaymentSchedule.value = false;
  }
};

const exportRepaymentSchedule = () => {
  showExportDialog.value = true;
};

const confirmExport = async () => {
  exporting.value = true;
  
  try {
    await applicationStore.exportRepaymentSchedule(props.application.id, exportFormat.value);
    notificationStore.showSuccess(`Repayment schedule exported as ${exportFormat.value.toUpperCase()}`);
    showExportDialog.value = false;
  } catch (error) {
    notificationStore.showError('Failed to export repayment schedule');
    console.error('Error exporting repayment schedule:', error);
  } finally {
    exporting.value = false;
  }
};

// Event handlers
const handleCalculationSaved = () => {
  showCalculatorDialog.value = false;
  fetchRepaymentSummary();
  notificationStore.showSuccess('Repayment schedule updated successfully');
};

const handleScheduleUpdated = () => {
  fetchRepaymentSummary();
  notificationStore.showSuccess('Repayment schedule updated successfully');
};

// Lifecycle hooks
onMounted(() => {
  fetchRepaymentSummary();
});
</script>

<style scoped>
.application-repayments-tab {
  padding-bottom: 1rem;
}
</style>
