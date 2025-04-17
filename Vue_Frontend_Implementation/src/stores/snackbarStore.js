import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useSnackbarStore = defineStore('snackbar', () => {
  // State
  const snackbar = ref({
    show: false,
    text: '',
    color: 'success',
    timeout: 3000
  })

  // Actions
  const showSnackbar = (text, color = 'success', timeout = 3000) => {
    snackbar.value = {
      show: true,
      text,
      color,
      timeout
    }
  }

  const showSuccess = (text, timeout = 3000) => {
    showSnackbar(text, 'success', timeout)
  }

  const showError = (text, timeout = 5000) => {
    showSnackbar(text, 'error', timeout)
  }

  const showWarning = (text, timeout = 4000) => {
    showSnackbar(text, 'warning', timeout)
  }

  const showInfo = (text, timeout = 3000) => {
    showSnackbar(text, 'info', timeout)
  }

  const hideSnackbar = () => {
    snackbar.value.show = false
  }

  return {
    // State
    snackbar,
    
    // Actions
    showSnackbar,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    hideSnackbar
  }
})
