# API Integration Documentation

This document outlines the API integration strategy for the Vue.js frontend of the Loan Application System V2.

## API Client Architecture

The frontend uses a centralized API client built on Axios to communicate with the backend services. The architecture follows these principles:

1. **Centralized Configuration**: All API-related configuration is centralized in the `apiClient.js` file
2. **Service-Based Organization**: API calls are organized into service modules by domain
3. **Authentication Handling**: Token management and authentication is handled automatically
4. **Error Handling**: Consistent error handling across all API calls
5. **Response Transformation**: Standardized response transformation

## API Client Implementation

### Base API Client

The base API client (`apiClient.js`) provides:

- Base URL configuration
- Request/response interceptors
- Authentication token management
- Error handling
- Response transformation

```javascript
// src/services/apiClient.js
import axios from 'axios'
import router from '@/router'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor for handling common errors
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    const { response } = error
    
    // Handle authentication errors
    if (response && response.status === 401) {
      localStorage.removeItem('token')
      
      if (router.currentRoute.value.name !== 'login') {
        router.push({
          name: 'login',
          query: { redirect: router.currentRoute.value.fullPath }
        })
      }
    }
    
    return Promise.reject(error)
  }
)

export default apiClient
```

## Service Modules

Each API domain has its own service module that encapsulates all related API calls:

### Authentication Service

```javascript
// src/services/authService.js
import apiClient from './apiClient'

const authService = {
  login(credentials) {
    return apiClient.post('/auth/login/', credentials)
  },
  
  logout() {
    return apiClient.post('/auth/logout/')
  },
  
  // Other auth-related API calls...
}

export default authService
```

### Application Service

```javascript
// src/services/applicationService.js
import apiClient from './apiClient'

const applicationService = {
  getApplications(filters = {}) {
    return apiClient.get('/applications/', { params: filters })
  },
  
  getApplication(id) {
    return apiClient.get(`/applications/${id}/`)
  },
  
  // Other application-related API calls...
}

export default applicationService
```

## API Endpoints Mapping

The following table maps frontend features to their corresponding API endpoints:

### Authentication Endpoints

| Feature | Frontend Method | API Endpoint | HTTP Method |
|---------|----------------|-------------|------------|
| Login | `authService.login()` | `/auth/login/` | POST |
| Logout | `authService.logout()` | `/auth/logout/` | POST |
| Forgot Password | `authService.forgotPassword()` | `/auth/forgot-password/` | POST |
| Reset Password | `authService.resetPassword()` | `/auth/reset-password/` | POST |
| Change Password | `authService.changePassword()` | `/auth/change-password/` | POST |
| Get User Profile | `authService.getUserProfile()` | `/auth/profile/` | GET |
| Update User Profile | `authService.updateUserProfile()` | `/auth/profile/` | PATCH |

### Application Endpoints

| Feature | Frontend Method | API Endpoint | HTTP Method |
|---------|----------------|-------------|------------|
| List Applications | `applicationService.getApplications()` | `/applications/` | GET |
| Get Application | `applicationService.getApplication()` | `/applications/{id}/` | GET |
| Create Application | `applicationService.createApplication()` | `/applications/` | POST |
| Update Application | `applicationService.updateApplication()` | `/applications/{id}/` | PATCH |
| Delete Application | `applicationService.deleteApplication()` | `/applications/{id}/` | DELETE |
| Upload Documents | `applicationService.uploadDocuments()` | `/applications/{id}/documents/` | POST |
| Generate Documents | `applicationService.generateDocuments()` | `/applications/{id}/generate-documents/` | POST |
| Create Note | `applicationService.createNote()` | `/applications/{id}/notes/` | POST |
| Get Notes | `applicationService.getNotes()` | `/applications/{id}/notes/list/` | GET |
| Calculate Loan | `applicationService.calculateLoan()` | `/applications/{id}/calculator/` | POST |
| Create Repayment Schedule | `applicationService.createRepaymentSchedule()` | `/applications/{id}/repayments/` | POST |
| Get Repayment Schedule | `applicationService.getRepaymentSchedule()` | `/applications/{id}/repayments/` | GET |
| Create Extension | `applicationService.createExtension()` | `/applications/{id}/extension/` | POST |
| Get Extensions | `applicationService.getExtensions()` | `/applications/{id}/extension/` | GET |
| Duplicate Application | `applicationService.duplicateApplication()` | `/applications/{id}/duplicate/` | POST |
| Get Fees | `applicationService.getFees()` | `/applications/{id}/fees/` | GET |
| Create Fee | `applicationService.createFee()` | `/applications/{id}/fees/` | POST |
| Get Payments | `applicationService.getPayments()` | `/applications/{id}/payments/` | GET |
| Create Payment | `applicationService.createPayment()` | `/applications/{id}/payments/` | POST |
| Submit Application | `applicationService.submitApplication()` | `/applications/{id}/submit/` | POST |
| Review Application | `applicationService.reviewApplication()` | `/applications/{id}/review/` | POST |
| Finalize Application | `applicationService.finalizeApplication()` | `/applications/{id}/finalize/` | POST |

### Borrower Endpoints

| Feature | Frontend Method | API Endpoint | HTTP Method |
|---------|----------------|-------------|------------|
| List Borrowers | `borrowerService.getBorrowers()` | `/borrowers/` | GET |
| Get Borrower | `borrowerService.getBorrower()` | `/borrowers/{id}/` | GET |
| Create Borrower | `borrowerService.createBorrower()` | `/borrowers/` | POST |
| Update Borrower | `borrowerService.updateBorrower()` | `/borrowers/{id}/` | PATCH |
| Delete Borrower | `borrowerService.deleteBorrower()` | `/borrowers/{id}/` | DELETE |
| Search Borrowers | `borrowerService.searchBorrowers()` | `/borrowers/search/` | GET |
| Get Borrower Applications | `borrowerService.getBorrowerApplications()` | `/borrowers/{id}/applications/` | GET |
| Check Duplicates | `borrowerService.checkDuplicates()` | `/borrowers/check-duplicates/` | POST |
| Merge Borrowers | `borrowerService.mergeBorrowers()` | `/borrowers/merge/` | POST |
| Get Merge History | `borrowerService.getMergeHistory()` | `/borrowers/merge-history/` | GET |

### Broker Endpoints

| Feature | Frontend Method | API Endpoint | HTTP Method |
|---------|----------------|-------------|------------|
| List Brokers | `brokerService.getBrokers()` | `/brokers/` | GET |
| Get Broker | `brokerService.getBroker()` | `/brokers/{id}/` | GET |
| Create Broker | `brokerService.createBroker()` | `/brokers/` | POST |
| Update Broker | `brokerService.updateBroker()` | `/brokers/{id}/` | PATCH |
| Delete Broker | `brokerService.deleteBroker()` | `/brokers/{id}/` | DELETE |
| Get Broker Applications | `brokerService.getBrokerApplications()` | `/brokers/{id}/applications/` | GET |
| Get Broker Borrowers | `brokerService.getBrokerBorrowers()` | `/brokers/{id}/borrowers/` | GET |
| Get Broker Commissions | `brokerService.getBrokerCommissions()` | `/brokers/{id}/commissions/` | GET |
| Get Commission Summary | `brokerService.getBrokerCommissionSummary()` | `/brokers/{id}/commission-summary/` | GET |

### Document Endpoints

| Feature | Frontend Method | API Endpoint | HTTP Method |
|---------|----------------|-------------|------------|
| Generate Document | `documentService.generateDocument()` | `/documents/generate/` | POST |
| Get Document | `documentService.getDocument()` | `/documents/{id}/` | GET |
| Update Document | `documentService.updateDocument()` | `/documents/{id}/` | PATCH |
| Delete Document | `documentService.deleteDocument()` | `/documents/{id}/` | DELETE |
| Upload Document | `documentService.uploadDocument()` | `/documents/upload/` | POST |
| Get Document Templates | `documentService.getDocumentTemplates()` | `/documents/templates/` | GET |
| Get Document Template | `documentService.getDocumentTemplate()` | `/documents/templates/{id}/` | GET |
| Create Document Template | `documentService.createDocumentTemplate()` | `/documents/templates/` | POST |
| Update Document Template | `documentService.updateDocumentTemplate()` | `/documents/templates/{id}/` | PATCH |
| Delete Document Template | `documentService.deleteDocumentTemplate()` | `/documents/templates/{id}/` | DELETE |
| Send for Signing | `documentService.sendForSigning()` | `/documents/send-for-signing/` | POST |
| Get Signing Requests | `documentService.getSigningRequests()` | `/documents/signing-requests/` | GET |
| Get Signing Request | `documentService.getSigningRequest()` | `/documents/signing-requests/{id}/` | GET |
| Get Document Versions | `documentService.getDocumentVersions()` | `/documents/{id}/versions/` | GET |
| Create Document Version | `documentService.createDocumentVersion()` | `/documents/{id}/versions/` | POST |

### Notification Endpoints

| Feature | Frontend Method | API Endpoint | HTTP Method |
|---------|----------------|-------------|------------|
| List Notifications | `notificationService.getNotifications()` | `/notifications/` | GET |
| Get Notification | `notificationService.getNotification()` | `/notifications/{id}/` | GET |
| Create Notification | `notificationService.createNotification()` | `/notifications/` | POST |
| Update Notification | `notificationService.updateNotification()` | `/notifications/{id}/` | PATCH |
| Delete Notification | `notificationService.deleteNotification()` | `/notifications/{id}/` | DELETE |
| Send Notification | `notificationService.sendNotification()` | `/notifications/{id}/send/` | POST |
| Mark as Read | `notificationService.markAsRead()` | `/notifications/{id}/` | PATCH |
| Mark All as Read | `notificationService.markAllAsRead()` | `/notifications/mark-all-read/` | POST |
| Get Notification Settings | `notificationService.getNotificationSettings()` | `/notifications/settings/` | GET |
| Update Notification Settings | `notificationService.updateNotificationSettings()` | `/notifications/settings/` | POST |

## Error Handling Strategy

The frontend implements a multi-layered error handling strategy:

1. **API Client Level**: The API client intercepts common errors (401, 500, etc.) and handles them globally
2. **Service Level**: Each service method can handle specific errors related to that API call
3. **Component Level**: Components can handle specific errors related to their functionality
4. **Global Error Handler**: A global error handler catches unhandled errors

### Example Error Handling in a Component

```javascript
const fetchApplications = async () => {
  try {
    loading.value = true
    applications.value = await applicationService.getApplications(filters.value)
  } catch (error) {
    if (error.response?.status === 400) {
      // Handle validation errors
      validationErrors.value = error.response.data.errors
    } else {
      // Use global snackbar for other errors
      snackbarStore.showError('Failed to load applications')
    }
  } finally {
    loading.value = false
  }
}
```

## Authentication Flow

The authentication flow is handled by the `authStore` and `authService`:

1. User submits login credentials
2. `authService.login()` sends credentials to the API
3. On successful login, the API returns a token
4. `authStore` stores the token in localStorage
5. `apiClient` includes the token in subsequent requests
6. If a request returns a 401 error, the user is redirected to the login page

## Data Caching Strategy

The frontend implements a simple caching strategy using Pinia stores:

1. Data is fetched from the API and stored in Pinia stores
2. Components access data from the stores instead of making direct API calls
3. Stores implement methods to refresh data when needed
4. Cached data is invalidated when it's modified

## API Testing

API integration can be tested using:

1. **Unit Tests**: Mock API responses and test service methods
2. **Integration Tests**: Test the interaction between components and services
3. **End-to-End Tests**: Test the complete flow from UI to API and back

## Next Steps

1. Implement error handling for all API calls
2. Add loading states for all API calls
3. Implement data caching for frequently accessed data
4. Add retry logic for failed API calls
5. Implement offline support for critical features
