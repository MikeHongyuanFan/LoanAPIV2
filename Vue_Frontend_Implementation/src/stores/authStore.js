import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/authService'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  
  const hasRole = (roleName) => {
    if (!user.value || !user.value.roles) return false
    return user.value.roles.includes(roleName)
  }

  // Actions
  const login = async (credentials) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authService.login(credentials)
      token.value = response.token
      localStorage.setItem('token', response.token)
      
      // Decode token to get user info
      const decoded = jwtDecode(response.token)
      user.value = decoded.user
      
      return response
    } catch (err) {
      error.value = err.response?.data?.message || 'Login failed'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
    }
  }

  const forgotPassword = async (email) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authService.forgotPassword(email)
      return response
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to send password reset email'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const resetPassword = async (token, password) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authService.resetPassword(token, password)
      return response
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to reset password'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const changePassword = async (oldPassword, newPassword) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authService.changePassword(oldPassword, newPassword)
      return response
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to change password'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const fetchUserProfile = async () => {
    if (!token.value) return null
    
    loading.value = true
    error.value = null
    
    try {
      const response = await authService.getUserProfile()
      user.value = response
      return response
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch user profile'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const updateUserProfile = async (profileData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authService.updateUserProfile(profileData)
      user.value = response
      return response
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update user profile'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  // Initialize user if token exists
  const initialize = async () => {
    if (token.value) {
      try {
        await fetchUserProfile()
      } catch (err) {
        // If token is invalid, logout
        logout()
      }
    }
  }

  return {
    // State
    token,
    user,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    hasRole,
    
    // Actions
    login,
    logout,
    forgotPassword,
    resetPassword,
    changePassword,
    fetchUserProfile,
    updateUserProfile,
    initialize
  }
})
