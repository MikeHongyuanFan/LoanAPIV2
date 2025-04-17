<template>
  <v-app-bar color="primary" app dark>
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    <v-app-bar-title>Loan Application System V2</v-app-bar-title>
    <v-spacer></v-spacer>
    <v-btn icon @click="showNotifications = !showNotifications">
      <v-badge :content="unreadNotificationsCount" :value="unreadNotificationsCount > 0" color="error">
        <v-icon>mdi-bell</v-icon>
      </v-badge>
    </v-btn>
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn icon v-bind="props">
          <v-avatar size="36">
            <v-img :src="userAvatar" alt="User Avatar"></v-img>
          </v-avatar>
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="navigateTo('/profile')">
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item>
        <v-list-item @click="logout">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" app>
    <v-list>
      <v-list-item to="/" :active="isActive('/')" color="primary">
        <template v-slot:prepend>
          <v-icon>mdi-view-dashboard</v-icon>
        </template>
        <v-list-item-title>Dashboard</v-list-item-title>
      </v-list-item>

      <v-list-group value="applications">
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" prepend-icon="mdi-file-document">
            <v-list-item-title>Applications</v-list-item-title>
          </v-list-item>
        </template>
        <v-list-item to="/applications" :active="isActive('/applications')">
          <template v-slot:prepend>
            <v-icon>mdi-format-list-bulleted</v-icon>
          </template>
          <v-list-item-title>All Applications</v-list-item-title>
        </v-list-item>
        <v-list-item to="/applications/create" :active="isActive('/applications/create')">
          <template v-slot:prepend>
            <v-icon>mdi-plus</v-icon>
          </template>
          <v-list-item-title>Create Application</v-list-item-title>
        </v-list-item>
      </v-list-group>

      <v-list-group value="borrowers">
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" prepend-icon="mdi-account">
            <v-list-item-title>Borrowers</v-list-item-title>
          </v-list-item>
        </template>
        <v-list-item to="/borrowers" :active="isActive('/borrowers')">
          <template v-slot:prepend>
            <v-icon>mdi-format-list-bulleted</v-icon>
          </template>
          <v-list-item-title>All Borrowers</v-list-item-title>
        </v-list-item>
        <v-list-item to="/borrowers/create" :active="isActive('/borrowers/create')">
          <template v-slot:prepend>
            <v-icon>mdi-plus</v-icon>
          </template>
          <v-list-item-title>Create Borrower</v-list-item-title>
        </v-list-item>
      </v-list-group>

      <v-list-group value="brokers">
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" prepend-icon="mdi-briefcase">
            <v-list-item-title>Brokers</v-list-item-title>
          </v-list-item>
        </template>
        <v-list-item to="/brokers" :active="isActive('/brokers')">
          <template v-slot:prepend>
            <v-icon>mdi-format-list-bulleted</v-icon>
          </template>
          <v-list-item-title>All Brokers</v-list-item-title>
        </v-list-item>
        <v-list-item to="/brokers/create" :active="isActive('/brokers/create')">
          <template v-slot:prepend>
            <v-icon>mdi-plus</v-icon>
          </template>
          <v-list-item-title>Create Broker</v-list-item-title>
        </v-list-item>
      </v-list-group>

      <v-list-item to="/products" :active="isActive('/products')" color="primary">
        <template v-slot:prepend>
          <v-icon>mdi-package-variant</v-icon>
        </template>
        <v-list-item-title>Products</v-list-item-title>
      </v-list-item>

      <v-list-item to="/documents" :active="isActive('/documents')" color="primary">
        <template v-slot:prepend>
          <v-icon>mdi-file-document-multiple</v-icon>
        </template>
        <v-list-item-title>Documents</v-list-item-title>
      </v-list-item>

      <v-list-item to="/reports" :active="isActive('/reports')" color="primary">
        <template v-slot:prepend>
          <v-icon>mdi-chart-bar</v-icon>
        </template>
        <v-list-item-title>Reports</v-list-item-title>
      </v-list-item>

      <v-list-item v-if="isAdmin" to="/admin" :active="isActive('/admin')" color="primary">
        <template v-slot:prepend>
          <v-icon>mdi-shield-account</v-icon>
        </template>
        <v-list-item-title>Admin</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>

  <v-main>
    <v-container fluid>
      <slot></slot>
    </v-container>
  </v-main>

  <v-navigation-drawer v-model="showNotifications" location="right" temporary width="400">
    <v-toolbar color="primary" dark>
      <v-toolbar-title>Notifications</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="showNotifications = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-list>
      <template v-if="notifications.length > 0">
        <v-list-item v-for="notification in notifications" :key="notification.id" :class="{ 'unread': !notification.read }">
          <v-list-item-title>{{ notification.title }}</v-list-item-title>
          <v-list-item-subtitle>{{ notification.message }}</v-list-item-subtitle>
          <v-list-item-subtitle class="text-caption">{{ formatDate(notification.created_at) }}</v-list-item-subtitle>
          <template v-slot:append>
            <v-btn icon size="small" @click="markAsRead(notification.id)" v-if="!notification.read">
              <v-icon>mdi-check</v-icon>
            </v-btn>
          </template>
        </v-list-item>
      </template>
      <v-list-item v-else>
        <v-list-item-title>No notifications</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>

  <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout">
    {{ snackbar.text }}
    <template v-slot:actions>
      <v-btn variant="text" @click="snackbar.show = false">Close</v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useNotificationStore } from '@/stores/notificationStore'
import { useSnackbarStore } from '@/stores/snackbarStore'
import { format } from 'date-fns'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()
const snackbarStore = useSnackbarStore()

const drawer = ref(true)
const showNotifications = ref(false)

// User information
const userAvatar = computed(() => {
  return authStore.user?.profile_picture || 'https://cdn.vuetifyjs.com/images/john.jpg'
})

const isAdmin = computed(() => {
  return authStore.hasRole('ADMIN')
})

// Notifications
const notifications = computed(() => {
  return notificationStore.notifications
})

const unreadNotificationsCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

// Snackbar
const snackbar = computed(() => {
  return snackbarStore.snackbar
})

// Methods
const isActive = (path) => {
  return route.path === path
}

const navigateTo = (path) => {
  router.push(path)
}

const logout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    snackbarStore.showError('Failed to logout. Please try again.')
  }
}

const markAsRead = async (id) => {
  try {
    await notificationStore.markAsRead(id)
  } catch (error) {
    snackbarStore.showError('Failed to mark notification as read.')
  }
}

const formatDate = (dateString) => {
  return format(new Date(dateString), 'MMM d, yyyy h:mm a')
}

// Fetch notifications on component mount
onMounted(async () => {
  try {
    await notificationStore.fetchNotifications()
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
  }
})
</script>

<style scoped>
.unread {
  background-color: rgba(25, 118, 210, 0.1);
  font-weight: bold;
}
</style>
