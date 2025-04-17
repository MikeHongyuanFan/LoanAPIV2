# API Service Relationship Document

This document outlines the API relationships and dependencies between services for the Loan Application System V2. Each service section describes its endpoints, dependencies, and relationship with other services.

---

## 1. Application Service

### Core Endpoints:
- `GET /applications/`: List all applications with optional filters
- `GET /applications/{id}/`: Retrieve specific application details
- `POST /applications/`: Create application
- `PATCH /applications/{id}/`: Update application info, status, etc.
- `DELETE /applications/{id}/`: Delete application

### Related Endpoints:
- `POST /applications/{id}/documents/`: Upload documents to an application
- `POST /applications/{id}/generate-documents/`: Generate PDF documents
- `POST /applications/{id}/notes/`: Create application notes
- `GET /applications/{id}/notes/list/`: Get all notes for an application
- `POST /applications/{id}/calculator/`: Calculate loan amounts and repayments
- `POST /applications/{id}/repayments/`: Create repayment schedule
- `GET /applications/{id}/repayments/`: Get repayment schedule
- `POST /applications/{id}/extension/`: Create loan extension
- `GET /applications/{id}/extension/`: Get loan extensions
- `POST /applications/{id}/duplicate/`: Duplicate an application
- `GET /applications/{id}/fees/`: Get fees for an application
- `POST /applications/{id}/fees/`: Create a fee for an application
- `GET /applications/{id}/payments/`: Get payments for an application
- `POST /applications/{id}/payments/`: Create a payment for an application
- `POST /applications/{id}/submit/`: Submit an application for review
- `POST /applications/{id}/review/`: Review an application
- `POST /applications/{id}/finalize/`: Finalize an application
- `GET /search/advanced/`: Advanced search for applications

### Dependencies:
- **Borrower Service**: Application links to one or more borrowers
- **Broker Service**: Links brokers to application
- **Product Service**: Links products to application
- **Document Service**: Used to generate and manage files
- **Notification Service**: Triggers email alerts on status changes and repayment reminders

---

## 2. Borrower Service

### Core Endpoints:
- `GET /borrowers/`: List borrowers with optional filters
- `GET /borrowers/{id}/`: Get borrower details
- `POST /borrowers/`: Create borrower
- `PATCH /borrowers/{id}/`: Update borrower
- `DELETE /borrowers/{id}/`: Delete borrower

### Related Endpoints:
- `GET /borrowers/search/`: Search borrowers by name, email, phone, etc.
- `GET /borrowers/{id}/applications/`: Get applications linked to borrower
- `POST /borrowers/check-duplicates/`: Check for duplicate borrowers
- `POST /borrowers/merge/`: Merge duplicate borrowers
- `GET /borrowers/merge-history/`: Get history of borrower merges

### Dependencies:
- **Application Service**: Borrowers are linked to applications
- **Guarantor Service**: Borrowers can have guarantors
- **Document Service**: Borrowers can have documents

---

## 3. Guarantor Service

### Core Endpoints:
- `GET /guarantors/`: List guarantors
- `GET /guarantors/{id}/`: Get guarantor details
- `POST /guarantors/`: Create guarantor
- `PATCH /guarantors/{id}/`: Update guarantor
- `DELETE /guarantors/{id}/`: Delete guarantor

### Dependencies:
- **Borrower Service**: Guarantors are linked to borrowers
- **Application Service**: Guarantors can be linked to specific applications

---

## 4. Broker Service

### Core Endpoints:
- `GET /brokers/`: List all brokers
- `GET /brokers/{id}/`: Get broker details
- `POST /brokers/`: Create broker
- `PATCH /brokers/{id}/`: Update broker
- `DELETE /brokers/{id}/`: Delete broker

### Related Endpoints:
- `GET /brokers/{id}/applications/`: Get applications linked to broker
- `GET /brokers/{id}/borrowers/`: Get borrowers linked to broker
- `GET /brokers/{id}/commissions/`: Get broker commissions
- `GET /brokers/{id}/commission-summary/`: Get commission summary for broker

### Dependencies:
- **Application Service**: Brokers are linked to applications
- **Borrower Service**: Brokers can be linked to borrowers

---

## 5. Document Service

### Core Endpoints:
- `GET /documents/`: List documents with optional filters
- `GET /documents/{id}/`: Get document details
- `PATCH /documents/{id}/`: Update document
- `DELETE /documents/{id}/`: Delete document
- `POST /documents/upload/`: Upload a document
- `POST /documents/generate/`: Generate a document

### Related Endpoints:
- `GET /documents/templates/`: Get all document templates
- `GET /documents/templates/{id}/`: Get document template details
- `POST /documents/templates/`: Create document template
- `PATCH /documents/templates/{id}/`: Update document template
- `DELETE /documents/templates/{id}/`: Delete document template
- `POST /documents/send-for-signing/`: Send document for signing
- `GET /documents/signing-requests/`: Get signing requests
- `GET /documents/signing-requests/{id}/`: Get signing request details
- `GET /documents/{id}/versions/`: Get document versions
- `POST /documents/{id}/versions/`: Create document version

### Dependencies:
- **Application Service**: Documents can be linked to applications
- **Borrower Service**: Documents can be linked to borrowers
- **Notification Service**: Notifications are sent when documents require action

---

## 6. Note Service

### Core Endpoints:
- `GET /notes/`: List notes with optional filters
- `GET /notes/{id}/`: Get note details
- `POST /notes/`: Create note
- `PATCH /notes/{id}/`: Update note
- `DELETE /notes/{id}/`: Delete note

### Dependencies:
- **Application Service**: Notes can be linked to applications
- **Borrower Service**: Notes can be linked to borrowers
- **User Service**: Notes are created by users

---

## 7. Product Service

### Core Endpoints:
- `GET /products/`: List products
- `GET /products/{id}/`: Get product details
- `POST /products/`: Create product
- `PATCH /products/{id}/`: Update product
- `DELETE /products/{id}/`: Delete product

### Dependencies:
- **Application Service**: Products are linked to applications

---

## 8. Authentication & User Service

### Core Endpoints:
- `POST /auth/login/`: Login
- `POST /auth/logout/`: Logout
- `POST /auth/forgot-password/`: Reset password link
- `POST /auth/reset-password/`: Reset password
- `POST /auth/change-password/`: Change password
- `GET /auth/profile/`: Get user profile
- `PATCH /auth/profile/`: Update user profile
- `GET /users/`: List users
- `GET /users/{id}/`: Get user details
- `POST /users/`: Create user
- `PATCH /users/{id}/`: Update user
- `DELETE /users/{id}/`: Delete user

### Dependencies:
- **Notification Service**: Sends notifications for password resets and account changes

---

## 9. Notification Service

### Core Endpoints:
- `GET /notifications/`: List notifications
- `GET /notifications/{id}/`: Get notification details
- `POST /notifications/`: Create notification
- `PATCH /notifications/{id}/`: Update notification (e.g., mark as read)
- `DELETE /notifications/{id}/`: Delete notification
- `POST /notifications/{id}/send/`: Send notification
- `POST /notifications/mark-all-read/`: Mark all notifications as read
- `GET /notifications/settings/`: Get notification settings
- `POST /notifications/settings/`: Update notification settings

### Triggers & Behaviors:
- Application status changes: Notifications sent to relevant users
- Repayment reminder: Triggered before repayment due date
- Document upload/generation: Notifications sent to relevant users
- User actions: Notifications for assignments and mentions

### Dependencies:
- **User Service**: Notifications are sent to users
- **Application Service**: Notifications are triggered by application events
- **Document Service**: Notifications are triggered by document events

---

## 10. Fee & Payment Service

### Core Endpoints:
- `GET /fees/`: List fees
- `GET /fees/{id}/`: Get fee details
- `POST /fees/`: Create fee
- `PATCH /fees/{id}/`: Update fee
- `DELETE /fees/{id}/`: Delete fee
- `GET /payments/`: List payments
- `GET /payments/{id}/`: Get payment details
- `POST /payments/`: Create payment
- `PATCH /payments/{id}/`: Update payment
- `DELETE /payments/{id}/`: Delete payment

### Dependencies:
- **Application Service**: Fees and payments are linked to applications
- **Notification Service**: Notifications are sent for payment confirmations and reminders

---

## 11. Repayment Service

### Core Endpoints:
- `GET /repayments/`: List repayments
- `GET /repayments/{id}/`: Get repayment details
- `POST /repayments/`: Create repayment
- `PATCH /repayments/{id}/`: Update repayment
- `DELETE /repayments/{id}/`: Delete repayment
- `GET /repayment-schedules/`: List repayment schedules
- `GET /repayment-schedules/{id}/`: Get repayment schedule details
- `POST /repayment-schedules/`: Create repayment schedule
- `PATCH /repayment-schedules/{id}/`: Update repayment schedule
- `DELETE /repayment-schedules/{id}/`: Delete repayment schedule

### Dependencies:
- **Application Service**: Repayments are linked to applications
- **Notification Service**: Notifications are sent for repayment reminders and confirmations

---

## 12. Extension Service

### Core Endpoints:
- `GET /extensions/`: List extensions
- `GET /extensions/{id}/`: Get extension details
- `POST /extensions/`: Create extension
- `PATCH /extensions/{id}/`: Update extension
- `DELETE /extensions/{id}/`: Delete extension
- `POST /extensions/{id}/approve/`: Approve extension
- `POST /extensions/{id}/reject/`: Reject extension

### Dependencies:
- **Application Service**: Extensions are linked to applications
- **User Service**: Extensions are approved by users
- **Notification Service**: Notifications are sent for extension approvals and rejections

---

## API Security and Access Control

All API endpoints are protected by authentication and authorization mechanisms:

1. **Authentication**: JWT-based authentication is used for all API requests
2. **Authorization**: Role-based access control determines what actions users can perform
3. **Rate Limiting**: API rate limiting prevents abuse
4. **Audit Logging**: All API requests are logged for audit purposes

## API Versioning

The API uses URL-based versioning:

- Current version: `/api/v1/`
- Future versions will be `/api/v2/`, etc.

## Error Handling

All API endpoints return standardized error responses:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field_name": ["Error details"]
    }
  }
}
```

## Pagination

List endpoints support pagination with the following query parameters:

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `sort`: Field to sort by (default varies by endpoint)
- `order`: Sort order (`asc` or `desc`, default: `asc`)

Response format for paginated endpoints:

```json
{
  "items": [...],
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 10,
    "pages": 10
  }
}
```
