<template>
  <div class="not-found">
    <v-container class="text-center">
      <v-row justify="center">
        <v-col cols="12" md="8">
          <h1 class="text-h1 font-weight-bold mb-4">404</h1>
          <h2 class="text-h4 mb-6">Page Not Found</h2>
          <p class="text-body-1 mb-8">
            The page you are looking for doesn't exist or has been moved.
          </p>
          <v-btn color="primary" size="large" to="/">
            Return to Dashboard
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
// No script needed for this simple view
</script>

<style scoped>
.not-found {
  padding: 100px 0;
}
</style>
