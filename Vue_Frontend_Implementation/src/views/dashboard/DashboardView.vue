<template>
  <div class="dashboard">
    <h1 class="text-h4 mb-6">Dashboard</h1>

    <v-row>
      <!-- Summary Cards -->
      <v-col cols="12" md="3">
        <v-card class="mb-4">
          <v-card-item>
            <v-card-title>Total Applications</v-card-title>
            <div class="text-h3 mt-2">{{ dashboardData.totalApplications }}</div>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="mb-4">
          <v-card-item>
            <v-card-title>Pending Applications</v-card-title>
            <div class="text-h3 mt-2">{{ dashboardData.pendingApplications }}</div>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="mb-4">
          <v-card-item>
            <v-card-title>Approved Applications</v-card-title>
            <div class="text-h3 mt-2">{{ dashboardData.approvedApplications }}</div>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="mb-4">
          <v-card-item>
            <v-card-title>Total Loan Amount</v-card-title>
            <div class="text-h3 mt-2">${{ formatCurrency(dashboardData.totalLoanAmount) }}</div>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Charts -->
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-card-title>Applications by Status</v-card-title>
          <v-card-text>
            <div class="chart-container">
              <DoughnutChart :chartData="applicationsByStatusChart" :options="chartOptions" />
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-card-title>Monthly Applications</v-card-title>
          <v-card-text>
            <div class="chart-container">
              <LineChart :chartData="monthlyApplicationsChart" :options="chartOptions" />
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Recent Applications -->
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Recent Applications</v-card-title>
          <v-card-text>
            <v-table>
              <thead>
                <tr>
                  <th>Reference</th>
                  <th>Borrower</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in dashboardData.recentApplications" :key="app.id">
                  <td>{{ app.reference_number }}</td>
                  <td>{{ app.borrower_name }}</td>
                  <td>${{ formatCurrency(app.loan_amount) }}</td>
                  <td>
                    <v-chip :color="getStatusColor(app.status)">{{ app.status }}</v-chip>
                  </td>
                  <td>{{ formatDate(app.created_at) }}</td>
                  <td>
                    <v-btn icon size="small" :to="`/applications/${app.id}`">
                      <v-icon>mdi-eye</v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Reminders -->
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Reminders</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="reminder in dashboardData.reminders" :key="reminder.id">
                <v-list-item-title>{{ reminder.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(reminder.date) }}</v-list-item-subtitle>
                <template v-slot:append>
                  <v-btn icon size="small" @click="markReminderComplete(reminder.id)">
                    <v-icon>mdi-check</v-icon>
                  </v-btn>
                </template>
              </v-list-item>
              <v-list-item v-if="dashboardData.reminders.length === 0">
                <v-list-item-title>No reminders</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { format } from 'date-fns'
import { DoughnutChart, LineChart } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title } from 'chart.js'
import { useSnackbarStore } from '@/stores/snackbarStore'

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title)

const snackbarStore = useSnackbarStore()

// Dashboard data
const dashboardData = ref({
  totalApplications: 0,
  pendingApplications: 0,
  approvedApplications: 0,
  totalLoanAmount: 0,
  recentApplications: [],
  reminders: [],
  applicationsByStatus: {},
  monthlyApplications: {}
})

// Chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}

// Computed chart data
const applicationsByStatusChart = computed(() => {
  const statuses = Object.keys(dashboardData.value.applicationsByStatus || {})
  const counts = statuses.map(status => dashboardData.value.applicationsByStatus[status])
  
  return {
    labels: statuses,
    datasets: [
      {
        data: counts,
        backgroundColor: [
          '#4CAF50',
          '#2196F3',
          '#FFC107',
          '#FF5252',
          '#9C27B0',
          '#607D8B'
        ]
      }
    ]
  }
})

const monthlyApplicationsChart = computed(() => {
  const months = Object.keys(dashboardData.value.monthlyApplications || {})
  const counts = months.map(month => dashboardData.value.monthlyApplications[month])
  
  return {
    labels: months,
    datasets: [
      {
        label: 'Applications',
        data: counts,
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.2)',
        tension: 0.4
      }
    ]
  }
})

// Helper methods
const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US').format(value)
}

const formatDate = (dateString) => {
  return format(new Date(dateString), 'MMM d, yyyy')
}

const getStatusColor = (status) => {
  const statusColors = {
    'DRAFT': 'grey',
    'SUBMITTED': 'blue',
    'UNDER_REVIEW': 'amber',
    'APPROVED': 'green',
    'REJECTED': 'red',
    'FINALIZED': 'purple'
  }
  
  return statusColors[status] || 'grey'
}

const markReminderComplete = async (id) => {
  try {
    // Call API to mark reminder as complete
    // await reminderService.markComplete(id)
    
    // Update local state
    dashboardData.value.reminders = dashboardData.value.reminders.filter(r => r.id !== id)
    
    snackbarStore.showSuccess('Reminder marked as complete')
  } catch (error) {
    snackbarStore.showError('Failed to mark reminder as complete')
  }
}

// Fetch dashboard data
const fetchDashboardData = async () => {
  try {
    // In a real app, this would be an API call
    // const response = await dashboardService.getSummary()
    // dashboardData.value = response
    
    // Mock data for demonstration
    dashboardData.value = {
      totalApplications: 156,
      pendingApplications: 42,
      approvedApplications: 98,
      totalLoanAmount: 12450000,
      recentApplications: [
        { id: 1, reference_number: 'APP-2025-001', borrower_name: 'John Smith', loan_amount: 250000, status: 'APPROVED', created_at: '2025-04-15T10:30:00Z' },
        { id: 2, reference_number: 'APP-2025-002', borrower_name: 'Jane Doe', loan_amount: 175000, status: 'UNDER_REVIEW', created_at: '2025-04-14T14:45:00Z' },
        { id: 3, reference_number: 'APP-2025-003', borrower_name: 'Robert Johnson', loan_amount: 320000, status: 'SUBMITTED', created_at: '2025-04-13T09:15:00Z' },
        { id: 4, reference_number: 'APP-2025-004', borrower_name: 'Sarah Williams', loan_amount: 450000, status: 'DRAFT', created_at: '2025-04-12T16:20:00Z' },
        { id: 5, reference_number: 'APP-2025-005', borrower_name: 'Michael Brown', loan_amount: 195000, status: 'FINALIZED', created_at: '2025-04-11T11:10:00Z' }
      ],
      reminders: [
        { id: 1, title: 'Follow up on APP-2025-002', date: '2025-04-18T09:00:00Z' },
        { id: 2, title: 'Call John Smith about documents', date: '2025-04-19T14:00:00Z' },
        { id: 3, title: 'Review valuation report for APP-2025-003', date: '2025-04-20T10:30:00Z' }
      ],
      applicationsByStatus: {
        'DRAFT': 16,
        'SUBMITTED': 26,
        'UNDER_REVIEW': 42,
        'APPROVED': 98,
        'REJECTED': 12,
        'FINALIZED': 62
      },
      monthlyApplications: {
        'Jan': 12,
        'Feb': 19,
        'Mar': 24,
        'Apr': 31,
        'May': 0,
        'Jun': 0,
        'Jul': 0,
        'Aug': 0,
        'Sep': 0,
        'Oct': 0,
        'Nov': 0,
        'Dec': 0
      }
    }
  } catch (error) {
    snackbarStore.showError('Failed to load dashboard data')
  }
}

// Lifecycle hooks
onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.chart-container {
  height: 300px;
}
</style>
