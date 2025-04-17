import { defineStore } from 'pinia'
import { ref } from 'vue'
import notificationService from '@/services/notificationService'

export const useNotificationStore = defineStore('notification', () => {
  // State
  const notifications = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Actions
  const fetchNotifications = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await notificationService.getNotifications()
      notifications.value = response
      return response
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch notifications'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const markAsRead = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      await notificationService.markAsRead(id)
      
      // Update local state
      const index = notifications.value.findIndex(n => n.id === id)
      if (index !== -1) {
        notifications.value[index].read = true
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to mark notification as read'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const markAllAsRead = async () => {
    loading.value = true
    error.value = null
    
    try {
      await notificationService.markAllAsRead()
      
      // Update local state
      notifications.value = notifications.value.map(n => ({ ...n, read: true }))
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to mark all notifications as read'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const deleteNotification = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      await notificationService.deleteNotification(id)
      
      // Update local state
      notifications.value = notifications.value.filter(n => n.id !== id)
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete notification'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    notifications,
    loading,
    error,
    
    // Actions
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification
  }
})
