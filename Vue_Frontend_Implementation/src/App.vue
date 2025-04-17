<template>
  <v-app>
    <component :is="layout">
      <router-view />
    </component>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

const route = useRoute()

// Determine which layout to use based on the route's meta.layout property
const layout = computed(() => {
  const layoutName = route.meta.layout || 'default'
  return layoutName === 'auth' ? AuthLayout : DefaultLayout
})
</script>

<style>
/* Global styles */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Roboto', sans-serif;
}

#app {
  height: 100%;
}

.page-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
}

.card-container {
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.required-field::after {
  content: " *";
  color: red;
}

.error-text {
  color: #FF5252;
  font-size: 12px;
  margin-top: 4px;
}
</style>
