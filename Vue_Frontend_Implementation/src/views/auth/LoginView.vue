<template>
  <v-card-text>
    <v-form @submit.prevent="login" ref="form">
      <v-alert v-if="error" type="error" class="mb-4">
        {{ error }}
      </v-alert>

      <v-text-field
        v-model="email"
        label="Email"
        type="email"
        :rules="emailRules"
        required
        prepend-inner-icon="mdi-email"
        variant="outlined"
      ></v-text-field>

      <v-text-field
        v-model="password"
        label="Password"
        :type="showPassword ? 'text' : 'password'"
        :rules="passwordRules"
        required
        prepend-inner-icon="mdi-lock"
        :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append-inner="showPassword = !showPassword"
        variant="outlined"
      ></v-text-field>

      <div class="d-flex justify-space-between align-center mb-4">
        <v-checkbox v-model="rememberMe" label="Remember me" hide-details></v-checkbox>
        <router-link to="/forgot-password" class="text-decoration-none">
          Forgot password?
        </router-link>
      </div>

      <v-btn
        type="submit"
        color="primary"
        block
        size="large"
        :loading="loading"
        :disabled="loading"
      >
        Login
      </v-btn>
    </v-form>
  </v-card-text>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Form data
const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')
const form = ref(null)

// Form validation rules
const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'Email must be valid'
]

const passwordRules = [
  v => !!v || 'Password is required'
]

// Login method
const login = async () => {
  const { valid } = await form.value.validate()
  
  if (!valid) return
  
  loading.value = true
  error.value = ''
  
  try {
    await authStore.login({
      email: email.value,
      password: password.value
    })
    
    // Redirect to the requested page or dashboard
    const redirectPath = route.query.redirect || '/'
    router.push(redirectPath)
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed. Please check your credentials and try again.'
  } finally {
    loading.value = false
  }
}
</script>
