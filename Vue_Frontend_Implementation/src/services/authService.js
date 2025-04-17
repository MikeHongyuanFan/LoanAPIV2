import apiClient from './apiClient'

const authService = {
  /**
   * Login with email and password
   * @param {Object} credentials - User credentials
   * @param {string} credentials.email - User email
   * @param {string} credentials.password - User password
   * @returns {Promise} - Promise with user data and token
   */
  login(credentials) {
    return apiClient.post('/auth/login/', credentials)
  },

  /**
   * Logout the current user
   * @returns {Promise} - Promise with logout status
   */
  logout() {
    return apiClient.post('/auth/logout/')
  },

  /**
   * Request password reset email
   * @param {string} email - User email
   * @returns {Promise} - Promise with reset status
   */
  forgotPassword(email) {
    return apiClient.post('/auth/forgot-password/', { email })
  },

  /**
   * Reset password with token
   * @param {string} token - Reset token
   * @param {string} password - New password
   * @returns {Promise} - Promise with reset status
   */
  resetPassword(token, password) {
    return apiClient.post('/auth/reset-password/', { token, password })
  },

  /**
   * Change user password
   * @param {string} oldPassword - Current password
   * @param {string} newPassword - New password
   * @returns {Promise} - Promise with change status
   */
  changePassword(oldPassword, newPassword) {
    return apiClient.post('/auth/change-password/', { 
      old_password: oldPassword, 
      new_password: newPassword 
    })
  },

  /**
   * Get current user profile
   * @returns {Promise} - Promise with user profile data
   */
  getUserProfile() {
    return apiClient.get('/auth/profile/')
  },

  /**
   * Update user profile
   * @param {Object} profileData - User profile data
   * @returns {Promise} - Promise with updated profile data
   */
  updateUserProfile(profileData) {
    return apiClient.patch('/auth/profile/', profileData)
  },

  /**
   * Create a new user account
   * @param {Object} userData - User data
   * @returns {Promise} - Promise with created user data
   */
  createAccount(userData) {
    return apiClient.post('/auth/create-account/', userData)
  }
}

export default authService
