<template>
  <div class="application-timeline-tab">
    <div class="d-flex justify-space-between align-center mb-4">
      <h3 class="text-h6">Application Timeline</h3>
      <v-btn-group>
        <v-btn
          :color="timelineFilter === 'all' ? 'primary' : ''"
          variant="text"
          @click="timelineFilter = 'all'"
        >
          All
        </v-btn>
        <v-btn
          :color="timelineFilter === 'status' ? 'primary' : ''"
          variant="text"
          @click="timelineFilter = 'status'"
        >
          Status Changes
        </v-btn>
        <v-btn
          :color="timelineFilter === 'documents' ? 'primary' : ''"
          variant="text"
          @click="timelineFilter = 'documents'"
        >
          Documents
        </v-btn>
        <v-btn
          :color="timelineFilter === 'notes' ? 'primary' : ''"
          variant="text"
          @click="timelineFilter = 'notes'"
        >
          Notes
        </v-btn>
      </v-btn-group>
    </div>

    <!-- Integrate the existing ApplicationTimeline component -->
    <application-timeline
      :application-id="application.id"
      :filter="timelineFilter"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ApplicationTimeline from '@/components/application/timeline/ApplicationTimeline.vue';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

// State
const timelineFilter = ref('all');
</script>

<style scoped>
.application-timeline-tab {
  padding-bottom: 1rem;
}
</style>
