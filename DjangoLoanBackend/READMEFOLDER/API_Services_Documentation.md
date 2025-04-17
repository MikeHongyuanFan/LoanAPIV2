# API Services Documentation

This document provides a comprehensive overview of all API services in the Loan Application System V2, including their endpoints, functions, and relationships.

## Table of Contents

1. [Application Service](#1-application-service)
2. [Borrower Service](#2-borrower-service)
3. [Guarantor Service](#3-guarantor-service)
4. [Broker Service](#4-broker-service)
5. [Valuer Service](#5-valuer-service)
6. [QS Service](#6-qs-service)
7. [Product Service](#7-product-service)
8. [Document Service](#8-document-service)
9. [Notification Service](#9-notification-service)
10. [Authentication Service](#10-authentication-service)
11. [Dashboard Service](#11-dashboard-service)

---

## 1. Application Service

The Application Service manages loan applications throughout their lifecycle, from creation to settlement.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/applications/` | GET | List all applications with filtering options | Returns applications that may include references to Borrower, Broker, Valuer, QS entities |
| `/applications/` | POST | Create a new application | Creates relationships with Borrower, Broker, Valuer, QS entities |
| `/applications/{id}/` | GET | Retrieve a specific application | Returns application with references to related entities |
| `/applications/{id}/` | PATCH | Update a specific application | May update relationships with other entities |
| `/applications/{id}/` | DELETE | Delete a specific application | Removes application and potentially orphans related entities |

### Related Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/applications/{id}/documents/` | POST | Upload documents to an application | Creates Document entities linked to the Application |
| `/applications/{id}/generate-documents/` | POST | Generate documents based on application data | Creates Document entities linked to the Application |
| `/applications/{id}/notes/` | POST | Create a note for an application | Creates Note entity linked to the Application |
| `/applications/{id}/notes/list/` | GET | List all notes for an application | Returns Notes linked to the Application |
| `/applications/{id}/notes/{note_id}/` | GET/PUT/DELETE | Manage a specific note | Operates on Note entity linked to the Application |
| `/applications/{id}/notes/{note_id}/reminder/` | POST/DELETE | Set or remove reminder for a note | Updates Note entity and potentially creates Notification |
| `/applications/{id}/calculator/` | POST | Calculate loan amounts and repayments | Uses Application data for calculations |
| `/applications/{id}/repayments/` | POST | Create repayment schedule | Creates Repayment entities linked to the Application |
| `/applications/{id}/extension/` | POST | Create loan extension | Creates Extension entity linked to the Application |
| `/applications/{id}/duplicate/` | POST | Duplicate an application | Creates new Application based on existing one |
| `/applications/{id}/fees/` | GET/POST | List or create fees | Manages Fee entities linked to the Application |
| `/applications/{id}/fees/{fee_id}/` | GET/PUT/DELETE | Manage a specific fee | Operates on Fee entity linked to the Application |
| `/applications/{id}/payments/` | GET/POST | List or create payments | Manages Payment entities linked to the Application |
| `/applications/{id}/payments/{payment_id}/` | GET/PUT/DELETE | Manage a specific payment | Operates on Payment entity linked to the Application |

### Reporting Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/reports/statistics/` | GET | Get application statistics | Aggregates data from Applications |
| `/reports/performance/` | GET | Get application processing performance metrics | Analyzes Application processing times |
| `/reports/repayments/` | GET | Get repayment reports | Aggregates data from Repayments linked to Applications |

### Search Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/search/advanced/` | GET | Advanced search across applications | Searches across Applications and related entities |
| `/search/global/` | GET | Global search across all entity types | Searches across all entity types in the system |

### Bulk Operations

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/bulk-update/` | POST | Update multiple applications at once | Updates multiple Application entities |

### Note Management

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/notes/reminders/` | GET | Get pending note reminders | Retrieves Notes with pending reminders |
| `/notes/process-reminders/` | POST | Process pending note reminders | Updates Notes and creates Notifications |

---

## 2. Borrower Service

The Borrower Service manages borrower information and relationships.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/borrowers/` | GET | List all borrowers with filtering options | Returns borrowers that may be linked to Applications |
| `/borrowers/` | POST | Create a new borrower | Creates a Borrower entity that can be linked to Applications |
| `/borrowers/{id}/` | GET | Retrieve a specific borrower | Returns borrower with references to related entities |
| `/borrowers/{id}/` | PATCH | Update a specific borrower | Updates Borrower entity |
| `/borrowers/{id}/` | DELETE | Delete a specific borrower | Removes Borrower entity and potentially affects linked Applications |

### Related Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/borrowers/search/` | GET | Search borrowers by various criteria | Searches across Borrower entities |
| `/borrowers/{id}/applications/` | GET | List applications linked to a borrower | Returns Applications linked to the Borrower |
| `/borrowers/check-duplicates/` | POST | Check for potential duplicate borrowers | Analyzes Borrower entities for duplicates |
| `/borrowers/merge/` | POST | Merge duplicate borrower records | Combines multiple Borrower entities and updates relationships |
| `/borrowers/merge-history/` | GET | View history of borrower merges | Returns BorrowerMergeRecord entities |

---

## 3. Guarantor Service

The Guarantor Service manages guarantor information for loan applications.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/guarantors/` | POST | Create a new guarantor | Creates Guarantor entity linked to an Application |
| `/guarantors/{id}/` | GET | Retrieve a specific guarantor | Returns guarantor with references to related entities |
| `/guarantors/{id}/` | PATCH | Update a specific guarantor | Updates Guarantor entity |
| `/guarantors/{id}/` | DELETE | Delete a specific guarantor | Removes Guarantor entity |

---

## 4. Broker Service

The Broker Service manages broker information, relationships, and commissions.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/brokers/` | GET | List all brokers with filtering options | Returns brokers that may be linked to Applications |
| `/brokers/` | POST | Create a new broker | Creates a Broker entity that can be linked to Applications |
| `/brokers/{id}/` | GET | Retrieve a specific broker | Returns broker with references to related entities |
| `/brokers/{id}/` | PATCH | Update a specific broker | Updates Broker entity |
| `/brokers/{id}/` | DELETE | Delete a specific broker | Removes Broker entity and potentially affects linked Applications |

### Related Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/brokers/{id}/applications/` | GET | List applications linked to a broker | Returns Applications linked to the Broker |
| `/brokers/{id}/borrowers/` | GET | List borrowers linked to a broker | Returns Borrowers linked to the Broker via Applications |
| `/brokers/{id}/commissions/` | GET | List commissions for a broker | Returns BrokerCommission entities linked to the Broker |
| `/brokers/{id}/commission-summary/` | GET | Get commission summary for a broker | Aggregates data from BrokerCommission entities |

### Commission Management

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/commissions/` | GET | List all commissions | Returns BrokerCommission entities |
| `/commissions/{id}/` | GET | Retrieve a specific commission | Returns BrokerCommission entity |
| `/commission-payments/` | GET | List all commission payments | Returns CommissionPayment entities |
| `/commission-payments/` | POST | Create a commission payment | Creates CommissionPayment entity linked to BrokerCommission |
| `/commission-payments/{id}/` | GET | Retrieve a specific commission payment | Returns CommissionPayment entity |

---

## 5. Valuer Service

The Valuer Service manages property valuers and their relationships with applications.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/valuers/` | GET | List all valuers with filtering options | Returns valuers that may be linked to Applications |
| `/valuers/` | POST | Create a new valuer | Creates a Valuer entity that can be linked to Applications |
| `/valuers/{id}/` | GET | Retrieve a specific valuer | Returns valuer with references to related entities |
| `/valuers/{id}/` | PATCH | Update a specific valuer | Updates Valuer entity |
| `/valuers/{id}/` | DELETE | Delete a specific valuer | Removes Valuer entity and potentially affects linked Applications |

### Related Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/valuers/{id}/applications/` | GET | List applications linked to a valuer | Returns Applications linked to the Valuer |

---

## 6. QS Service

The QS (Quantity Surveyor) Service manages quantity surveyors and their relationships with applications.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/qs/` | GET | List all quantity surveyors with filtering options | Returns QS entities that may be linked to Applications |
| `/qs/` | POST | Create a new quantity surveyor | Creates a QS entity that can be linked to Applications |
| `/qs/{id}/` | GET | Retrieve a specific quantity surveyor | Returns QS with references to related entities |
| `/qs/{id}/` | PATCH | Update a specific quantity surveyor | Updates QS entity |
| `/qs/{id}/` | DELETE | Delete a specific quantity surveyor | Removes QS entity and potentially affects linked Applications |

### Related Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/qs/{id}/applications/` | GET | List applications linked to a quantity surveyor | Returns Applications linked to the QS |

---

## 7. Product Service

The Product Service manages loan products that can be offered to borrowers.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/products/` | GET | List all products with filtering options | Returns products that may be linked to Applications |
| `/products/` | POST | Create a new product | Creates a Product entity that can be linked to Applications |
| `/products/{id}/` | GET | Retrieve a specific product | Returns product with references to related entities |
| `/products/{id}/` | PATCH | Update a specific product | Updates Product entity |
| `/products/{id}/` | DELETE | Delete a specific product | Removes Product entity and potentially affects linked Applications |

### Related Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/products/{id}/documents/` | GET | List document requirements for a product | Returns document requirements for the Product |

---

## 8. Document Service

The Document Service manages document generation, storage, and e-signing workflows.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/documents/generate/` | POST | Generate a document from a template | Creates Document entity potentially linked to an Application |
| `/documents/{id}/` | GET | Retrieve a specific document | Returns document with references to related entities |
| `/documents/{id}/` | PATCH | Update a specific document | Updates Document entity |
| `/documents/{id}/` | DELETE | Delete a specific document | Removes Document entity |
| `/documents/upload/` | POST | Upload a document | Creates Document entity potentially linked to an Application |

### Template Management

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/documents/templates/` | GET | List all document templates | Returns DocumentTemplate entities |
| `/documents/templates/` | POST | Create a document template | Creates DocumentTemplate entity |
| `/documents/templates/{id}/` | GET | Retrieve a specific document template | Returns DocumentTemplate entity |
| `/documents/templates/{id}/` | PATCH | Update a specific document template | Updates DocumentTemplate entity |
| `/documents/templates/{id}/` | DELETE | Delete a specific document template | Removes DocumentTemplate entity |

### E-Signing

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/documents/send-for-signing/` | POST | Send a document for e-signing | Creates DocumentSigningRequest entity linked to Document |
| `/documents/signing-requests/` | GET | List all signing requests | Returns DocumentSigningRequest entities |
| `/documents/signing-requests/{id}/` | GET | Retrieve a specific signing request | Returns DocumentSigningRequest entity |
| `/documents/docusign-callback/` | POST | Webhook endpoint for DocuSign callbacks | Updates DocumentSigningRequest and Document entities |

### Version Control

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/documents/{id}/versions/` | GET | List all versions of a document | Returns Document entities related to the original document |
| `/documents/{id}/versions/` | POST | Create a new version of a document | Creates Document entity linked to the original document |

---

## 9. Notification Service

The Notification Service manages notifications, templates, and scheduled reminders.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/notifications/` | GET | List all notifications with filtering options | Returns Notification entities |
| `/notifications/` | POST | Create a new notification | Creates Notification entity |
| `/notifications/{id}/` | GET | Retrieve a specific notification | Returns Notification entity |
| `/notifications/{id}/` | PATCH | Update a specific notification | Updates Notification entity |
| `/notifications/{id}/` | DELETE | Delete a specific notification | Removes Notification entity |
| `/notifications/{id}/send/` | POST | Send a specific notification | Updates Notification entity and sends the notification |

### Settings Management

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/notifications/settings/` | GET | Get notification settings | Returns NotificationSetting entities |
| `/notifications/settings/` | POST | Update notification settings | Updates NotificationSetting entities |

### Template Management

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/notifications/templates/` | GET | List all notification templates | Returns NotificationTemplate entities |
| `/notifications/templates/` | POST | Create a notification template | Creates NotificationTemplate entity |
| `/notifications/templates/{id}/` | GET | Retrieve a specific notification template | Returns NotificationTemplate entity |
| `/notifications/templates/{id}/` | PATCH | Update a specific notification template | Updates NotificationTemplate entity |
| `/notifications/templates/{id}/` | DELETE | Delete a specific notification template | Removes NotificationTemplate entity |
| `/notifications/templates/{id}/preview/` | GET | Preview a notification template | Renders NotificationTemplate with sample data |
| `/notifications/templates/{id}/send-test/` | POST | Send a test notification using a template | Creates and sends a test Notification using NotificationTemplate |

### Processing

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/notifications/process-pending/` | POST | Process pending notifications | Updates and sends pending Notification entities |
| `/notifications/send-sms/` | POST | Send an SMS notification | Creates and sends SMS Notification |

### Scheduled Notifications

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/notifications/repayment-reminders/` | POST | Send repayment reminders | Creates Notification entities for upcoming repayments |
| `/notifications/late-repayment-reminders/` | POST | Send late repayment reminders | Creates Notification entities for overdue repayments |
| `/notifications/loan-expiration-reminders/` | POST | Send loan expiration reminders | Creates Notification entities for expiring loans |
| `/notifications/stagnant-stage-reminders/` | POST | Send stagnant stage reminders | Creates Notification entities for applications stuck in a stage |

---

## 10. Authentication Service

The Authentication Service manages user authentication, authorization, and permissions.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/auth/login/` | POST | Authenticate a user and return tokens | Validates User credentials |
| `/auth/forgot-password/` | POST | Initiate password reset process | Creates password reset token for User |
| `/auth/change-password/` | POST | Change user password | Updates User password |
| `/auth/create-account/` | POST | Create a new user account | Creates User and UserProfile entities |
| `/auth/delete-account/` | DELETE | Delete a user account | Removes User and UserProfile entities |

### User Management

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/users/` | GET | List all users | Returns User entities |
| `/users/{id}/` | GET | Retrieve a specific user | Returns User entity with UserProfile |

### Permission Management

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/permissions/` | GET | List all permissions | Returns Permission entities |
| `/permissions/` | POST | Create a new permission | Creates Permission entity |
| `/permissions/{id}/` | GET | Retrieve a specific permission | Returns Permission entity |
| `/roles/` | GET | List all roles | Returns Role entities |
| `/roles/` | POST | Create a new role | Creates Role entity |
| `/roles/{id}/` | GET | Retrieve a specific role | Returns Role entity |
| `/user-permissions/` | GET | List all user permissions | Returns UserPermission entities |
| `/user-permissions/` | POST | Assign permission to a user | Creates UserPermission entity |
| `/user-permissions/{id}/` | GET | Retrieve a specific user permission | Returns UserPermission entity |

### Audit Logging

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/audit-logs/` | GET | List audit logs | Returns AuditLog entities |

---

## 11. Dashboard Service

The Dashboard Service provides aggregated data and insights for different user roles.

### Core Endpoints

| Endpoint | Method | Function | Relationships |
|----------|--------|----------|--------------|
| `/dashboard/summary/` | GET | Get general dashboard summary | Aggregates data from multiple entities |
| `/dashboard/user/` | GET | Get user-specific dashboard data | Aggregates data relevant to the current user |
| `/dashboard/manager/` | GET | Get manager-specific dashboard data | Aggregates data for management insights |

---

## Entity Relationships

### Primary Relationships

- **Application** is the central entity with relationships to:
  - Borrower (many-to-one)
  - Broker (many-to-one)
  - Valuer (many-to-one)
  - QS (many-to-one)
  - Product (many-to-one)
  - UserProfile (assigned_to, many-to-one)
  - UserProfile (created_by, many-to-one)

- **Application** has child entities:
  - Note (one-to-many)
  - Repayment (one-to-many)
  - Extension (one-to-many)
  - Fee (one-to-many)
  - Payment (one-to-many)
  - Document (one-to-many)

- **Broker** has relationships to:
  - Application (one-to-many)
  - BrokerCommission (one-to-many)

- **BrokerCommission** has relationships to:
  - CommissionPayment (many-to-many through CommissionPaymentItem)

- **Document** has relationships to:
  - Application (many-to-one)
  - DocumentTemplate (many-to-one)
  - DocumentSigningRequest (one-to-many)
  - Document (original_document_id, self-referential for versioning)

- **Notification** has relationships to:
  - NotificationTemplate (many-to-one)
  - UserProfile (created_by, many-to-one)

- **User** has relationships to:
  - UserProfile (one-to-one)
  - UserPermission (one-to-many)
  - Role (many-to-many through UserRole)

### Relationship Diagram

```
Application
├── Borrower
├── Broker
│   └── BrokerCommission
│       └── CommissionPayment
├── Valuer
├── QS
├── Product
├── UserProfile (assigned_to)
├── UserProfile (created_by)
├── Note
├── Repayment
├── Extension
├── Fee
│   └── Payment
└── Document
    ├── DocumentTemplate
    ├── DocumentSigningRequest
    └── Document (version)

User
├── UserProfile
├── UserPermission
│   └── Permission
└── Role

Notification
├── NotificationTemplate
└── UserProfile (created_by)
```

This diagram shows the hierarchical relationships between the main entities in the system.
