# Vue Frontend Implementation for Loan Application System V2

This directory contains the Vue.js frontend implementation for the Loan Application System V2.

## Project Structure

The frontend is built using Vue 3 with the Composition API, Pinia for state management, and Vue Router for routing. The project follows a modular structure organized by features.

```
Vue_Frontend_Implementation/
├── public/                  # Static assets
├── src/
│   ├── assets/              # Images, fonts, etc.
│   ├── components/          # Reusable components
│   │   ├── common/          # Common UI components
│   │   ├── application/     # Application-specific components
│   │   ├── borrower/        # Borrower-specific components
│   │   ├── broker/          # Broker-specific components
│   │   └── ...              # Other feature-specific components
│   ├── composables/         # Reusable composition functions
│   ├── layouts/             # Layout components
│   ├── router/              # Vue Router configuration
│   ├── services/            # API services
│   ├── stores/              # Pinia stores
│   ├── utils/               # Utility functions
│   ├── views/               # Page components
│   │   ├── application/     # Application-related views
│   │   ├── borrower/        # Borrower-related views
│   │   ├── broker/          # Broker-related views
│   │   └── ...              # Other feature-specific views
│   ├── App.vue              # Root component
│   └── main.js              # Entry point
├── .env                     # Environment variables
├── .eslintrc.js             # ESLint configuration
├── package.json             # Dependencies and scripts
└── vite.config.js           # Vite configuration
```

## Setup Instructions

### Prerequisites

- Node.js 16+ and npm 8+
- Access to the backend API server

### Installation

1. Navigate to the Vue_Frontend_Implementation directory:
   ```
   cd /Users/hongyuanfan/Desktop/LoanApplicationV2/Vue_Frontend_Implementation
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file with the backend API URL:
   ```
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

4. Start the development server:
   ```
   npm run dev
   ```

5. Build for production:
   ```
   npm run build
   ```

## Features

The frontend implementation includes the following features:

### Authentication
- Login/logout functionality
- Password reset
- User profile management
- Role-based access control

### Dashboard
- Overview of loan applications
- Key metrics and statistics
- Task lists and reminders
- Role-specific dashboards

### Application Management
- Application listing with filtering and sorting
- Application creation and editing
- Stage tracking and updates
- Document generation and management
- Notes and reminders
- Fee management
- Repayment tracking
- Loan extension handling

### Borrower Management
- Borrower listing with filtering and search
- Borrower creation and editing
- Duplicate detection and merging
- Application history

### Broker Management
- Broker listing with filtering and search
- Broker creation and editing
- Commission tracking
- Application history

### Document Management
- Document upload and download
- Template-based document generation
- E-signature integration
- Version control

### Notification System
- Notification center
- Email template management
- SMS notifications
- Scheduled reminders

## API Integration

The frontend communicates with the backend API using the services defined in the `src/services` directory. Each service corresponds to a specific API endpoint group:

- `applicationService.js` - Handles application-related API calls
- `borrowerService.js` - Handles borrower-related API calls
- `brokerService.js` - Handles broker-related API calls
- `authService.js` - Handles authentication-related API calls
- etc.

## State Management

Pinia stores are used for state management, with separate stores for different features:

- `authStore.js` - Manages authentication state
- `applicationStore.js` - Manages application data
- `borrowerStore.js` - Manages borrower data
- etc.

## Routing

Vue Router is used for routing, with routes defined in the `src/router` directory. The routes are organized by feature and include:

- Public routes (login, forgot password, etc.)
- Protected routes that require authentication
- Role-based routes that require specific permissions

## UI Components

The UI is built using a combination of custom components and a UI library (Vuetify). Components are organized by feature and include:

- Form components for data entry
- Table components for data display
- Modal components for dialogs
- Card components for information display
- etc.

## Development Guidelines

- Follow the Vue Style Guide for code organization and naming conventions
- Use the Composition API for component logic
- Use Pinia for state management
- Use Vue Router for routing
- Use Axios for API calls
- Write unit tests for components and services
- Use ESLint for code linting
