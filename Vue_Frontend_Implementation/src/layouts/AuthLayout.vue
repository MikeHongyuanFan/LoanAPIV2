<template>
  <v-container fluid class="auth-container fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="auth-card">
          <v-card-title class="text-center pt-6">
            <h1 class="text-h4 font-weight-bold primary--text">Loan Application System V2</h1>
          </v-card-title>
          <slot></slot>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
// Auth layout is simple, just a container for auth-related views
</script>

<style scoped>
.auth-container {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.auth-card {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
