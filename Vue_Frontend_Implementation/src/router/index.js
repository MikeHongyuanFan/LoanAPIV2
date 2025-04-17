import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

// Auth views
import LoginView from '@/views/auth/LoginView.vue'
import ForgotPasswordView from '@/views/auth/ForgotPasswordView.vue'
import ResetPasswordView from '@/views/auth/ResetPasswordView.vue'

// Dashboard view
import DashboardView from '@/views/dashboard/DashboardView.vue'

// Application views
import ApplicationListView from '@/views/application/ApplicationListView.vue'
import ApplicationCreateView from '@/views/application/ApplicationCreateView.vue'
import ApplicationDetailView from '@/views/application/ApplicationDetailView.vue'

// Borrower views
import BorrowerListView from '@/views/borrower/BorrowerListView.vue'
import BorrowerCreateView from '@/views/borrower/BorrowerCreateView.vue'
import BorrowerDetailView from '@/views/borrower/BorrowerDetailView.vue'

// Broker views
import BrokerListView from '@/views/broker/BrokerListView.vue'
import BrokerCreateView from '@/views/broker/BrokerCreateView.vue'
import BrokerDetailView from '@/views/broker/BrokerDetailView.vue'

// Product views
import ProductListView from '@/views/product/ProductListView.vue'
import ProductDetailView from '@/views/product/ProductDetailView.vue'

// Document views
import DocumentListView from '@/views/document/DocumentListView.vue'

// Report views
import ReportView from '@/views/dashboard/ReportView.vue'

// Admin views
import AdminDashboardView from '@/views/dashboard/AdminDashboardView.vue'

// Profile view
import ProfileView from '@/views/auth/ProfileView.vue'

// Not found view
import NotFoundView from '@/views/NotFoundView.vue'

const routes = [
  // Public routes
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { layout: 'auth', requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordView,
    meta: { layout: 'auth', requiresAuth: false }
  },
  {
    path: '/reset-password/:token',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: { layout: 'auth', requiresAuth: false }
  },
  
  // Protected routes
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  
  // Application routes
  {
    path: '/applications',
    name: 'applications',
    component: ApplicationListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/applications/create',
    name: 'application-create',
    component: ApplicationCreateView,
    meta: { requiresAuth: true }
  },
  {
    path: '/applications/:id',
    name: 'application-detail',
    component: ApplicationDetailView,
    meta: { requiresAuth: true }
  },
  
  // Borrower routes
  {
    path: '/borrowers',
    name: 'borrowers',
    component: BorrowerListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/borrowers/create',
    name: 'borrower-create',
    component: BorrowerCreateView,
    meta: { requiresAuth: true }
  },
  {
    path: '/borrowers/:id',
    name: 'borrower-detail',
    component: BorrowerDetailView,
    meta: { requiresAuth: true }
  },
  
  // Broker routes
  {
    path: '/brokers',
    name: 'brokers',
    component: BrokerListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/brokers/create',
    name: 'broker-create',
    component: BrokerCreateView,
    meta: { requiresAuth: true }
  },
  {
    path: '/brokers/:id',
    name: 'broker-detail',
    component: BrokerDetailView,
    meta: { requiresAuth: true }
  },
  
  // Product routes
  {
    path: '/products',
    name: 'products',
    component: ProductListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/products/:id',
    name: 'product-detail',
    component: ProductDetailView,
    meta: { requiresAuth: true }
  },
  
  // Document routes
  {
    path: '/documents',
    name: 'documents',
    component: DocumentListView,
    meta: { requiresAuth: true }
  },
  
  // Report routes
  {
    path: '/reports',
    name: 'reports',
    component: ReportView,
    meta: { requiresAuth: true }
  },
  
  // Admin routes
  {
    path: '/admin',
    name: 'admin',
    component: AdminDashboardView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  
  // Not found route
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
  
  // Check if the route requires authentication
  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } 
  // Check if the route requires admin role
  else if (requiresAdmin && !authStore.hasRole('ADMIN')) {
    next({ name: 'dashboard' })
  } 
  // If the user is already authenticated and tries to access login page
  else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } 
  // Otherwise, proceed as normal
  else {
    next()
  }
})

export default router
