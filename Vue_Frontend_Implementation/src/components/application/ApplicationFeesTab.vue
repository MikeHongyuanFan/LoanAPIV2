<template>
  <div class="application-fees-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Fees & Charges</h3>
      <div class="d-flex">
        <v-btn
          v-if="canAddFees"
          color="primary"
          prepend-icon="mdi-cash-plus"
          @click="showAddFeeDialog = true"
        >
          Add Fee
        </v-btn>
      </div>
    </div>

    <!-- Integrate the existing ApplicationFees component -->
    <application-fees
      :application-id="application.id"
      @fee-added="handleFeeAdded"
      @fee-updated="handleFeeUpdated"
      @fee-deleted="handleFeeDeleted"
      @payment-recorded="handlePaymentRecorded"
    />

    <!-- Add Fee Dialog -->
    <v-dialog v-model="showAddFeeDialog" max-width="600px">
      <v-card>
        <v-card-title class="bg-grey-lighten-4 py-3">
          <v-icon start class="mr-2">mdi-cash-plus</v-icon>
          Add Fee
        </v-card-title>
        <v-card-text class="pa-4">
          <v-form ref="feeForm" @submit.prevent="addFee">
            <v-select
              v-model="feeType"
              :items="feeTypes"
              label="Fee Type"
              required
              :rules="[v => !!v || 'Fee type is required']"
            ></v-select>

            <v-text-field
              v-model="feeDescription"
              label="Description"
              class="mt-4"
            ></v-text-field>

            <v-text-field
              v-model.number="feeAmount"
              label="Amount"
              type="number"
              prefix="$"
              required
              :rules="[
                v => !!v || 'Amount is required',
                v => v > 0 || 'Amount must be greater than 0'
              ]"
              class="mt-4"
            ></v-text-field>

            <v-checkbox
              v-model="feeIsTaxable"
              label="Taxable"
              hint="Apply GST to this fee"
              persistent-hint
              class="mt-2"
            ></v-checkbox>

            <v-select
              v-model="feePaymentMethod"
              :items="paymentMethods"
              label="Payment Method"
              class="mt-4"
            ></v-select>

            <v-checkbox
              v-model="feeIsPaid"
              label="Mark as Paid"
              class="mt-2"
            ></v-checkbox>

            <v-text-field
              v-if="feeIsPaid"
              v-model="feeReceiptNumber"
              label="Receipt Number"
              class="mt-4"
            ></v-text-field>

            <v-text-field
              v-if="feeIsPaid"
              v-model="feePaidDate"
              label="Payment Date"
              type="date"
              class="mt-4"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showAddFeeDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="addFee" :loading="adding">
            Add Fee
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { useApplicationStore } from '@/stores/application';
import ApplicationFees from '@/components/application/ApplicationFees.vue';

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

// State for adding fees
const showAddFeeDialog = ref(false);
const feeType = ref(null);
const feeDescription = ref('');
const feeAmount = ref(0);
const feeIsTaxable = ref(true);
const feePaymentMethod = ref(null);
const feeIsPaid = ref(false);
const feeReceiptNumber = ref('');
const feePaidDate = ref(new Date().toISOString().substr(0, 10));
const adding = ref(false);

// Form ref
const feeForm = ref(null);

// Fee types
const feeTypes = [
  { title: 'Application Fee', value: 'APPLICATION_FEE' },
  { title: 'Establishment Fee', value: 'ESTABLISHMENT_FEE' },
  { title: 'Valuation Fee', value: 'VALUATION_FEE' },
  { title: 'Legal Fee', value: 'LEGAL_FEE' },
  { title: 'Broker Commission', value: 'BROKER_COMMISSION' },
  { title: 'Late Payment Fee', value: 'LATE_PAYMENT_FEE' },
  { title: 'Early Repayment Fee', value: 'EARLY_REPAYMENT_FEE' },
  { title: 'Other Fee', value: 'OTHER_FEE' }
];

// Payment methods
const paymentMethods = [
  { title: 'Credit Card', value: 'CREDIT_CARD' },
  { title: 'Direct Debit', value: 'DIRECT_DEBIT' },
  { title: 'Bank Transfer', value: 'BANK_TRANSFER' },
  { title: 'Cash', value: 'CASH' },
  { title: 'Cheque', value: 'CHEQUE' },
  { title: 'Loan Proceeds', value: 'LOAN_PROCEEDS' },
  { title: 'Other', value: 'OTHER' }
];

// Computed properties
const canAddFees = computed(() => {
  return authStore.hasPermission('application:edit') || 
         authStore.hasPermission('fee:create');
});

// Methods
const addFee = async () => {
  if (!feeForm.value) return;
  
  const { valid } = await feeForm.value.validate();
  if (!valid) return;
  
  adding.value = true;
  
  try {
    const feeData = {
      fee_type: feeType.value,
      description: feeDescription.value,
      amount: parseFloat(feeAmount.value),
      is_taxable: feeIsTaxable.value,
      payment_method: feePaymentMethod.value
    };
    
    if (feeIsPaid) {
      feeData.is_paid = true;
      feeData.receipt_number = feeReceiptNumber.value;
      feeData.paid_date = feePaidDate.value;
    }
    
    await applicationStore.createFee(props.application.id, feeData);
    
    notificationStore.showSuccess('Fee added successfully');
    showAddFeeDialog.value = false;
    
    // Reset form
    feeType.value = null;
    feeDescription.value = '';
    feeAmount.value = 0;
    feeIsTaxable.value = true;
    feePaymentMethod.value = null;
    feeIsPaid.value = false;
    feeReceiptNumber.value = '';
    feePaidDate.value = new Date().toISOString().substr(0, 10);
  } catch (error) {
    notificationStore.showError('Failed to add fee');
    console.error('Error adding fee:', error);
  } finally {
    adding.value = false;
  }
};

// Event handlers
const handleFeeAdded = () => {
  notificationStore.showSuccess('Fee added successfully');
};

const handleFeeUpdated = () => {
  notificationStore.showSuccess('Fee updated successfully');
};

const handleFeeDeleted = () => {
  notificationStore.showSuccess('Fee deleted successfully');
};

const handlePaymentRecorded = () => {
  notificationStore.showSuccess('Payment recorded successfully');
};
</script>

<style scoped>
.application-fees-tab {
  padding-bottom: 1rem;
}
</style>
