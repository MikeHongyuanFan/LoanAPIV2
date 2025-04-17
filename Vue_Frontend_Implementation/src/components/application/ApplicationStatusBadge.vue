<template>
  <v-chip
    :color="statusColor"
    :text-color="textColor"
    size="small"
    class="font-weight-medium"
  >
    {{ formattedStatus }}
  </v-chip>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (value) => {
      return [
        'DRAFT',
        'PENDING',
        'UNDER_REVIEW',
        'INFORMATION_REQUESTED',
        'APPROVED',
        'CONDITIONALLY_APPROVED',
        'REJECTED',
        'WITHDRAWN',
        'CANCELLED',
        'COMPLETED',
        'EXPIRED'
      ].includes(value);
    }
  },
  size: {
    type: String,
    default: 'small'
  }
});

const statusColor = computed(() => {
  const colorMap = {
    'DRAFT': 'grey',
    'PENDING': 'blue',
    'UNDER_REVIEW': 'indigo',
    'INFORMATION_REQUESTED': 'amber',
    'APPROVED': 'success',
    'CONDITIONALLY_APPROVED': 'light-green',
    'REJECTED': 'error',
    'WITHDRAWN': 'grey-darken-1',
    'CANCELLED': 'grey-darken-2',
    'COMPLETED': 'teal',
    'EXPIRED': 'deep-orange'
  };
  
  return colorMap[props.status] || 'grey';
});

const textColor = computed(() => {
  // For light background colors, use dark text
  const lightBackgrounds = ['amber', 'light-green', 'grey'];
  return lightBackgrounds.includes(statusColor.value) ? 'black' : 'white';
});

const formattedStatus = computed(() => {
  return props.status
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0) + word.slice(1).toLowerCase())
    .join(' ');
});
</script>

<style scoped>
/* Additional styling if needed */
</style>
