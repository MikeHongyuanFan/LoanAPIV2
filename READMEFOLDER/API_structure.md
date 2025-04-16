# API Service Relationship Document

This document outlines the API relationships and dependencies between services for the CRM Loan Management System. Each service section describes its endpoints, dependencies, and relationship with other services.

---

## 1. Application Service

### Core Endpoints:
- `GET /applications/`: List all applications
- `GET /applications/{id}/`: Retrieve specific application details
- `POST /applications/`: Create application
- `DELETE /applications/{id}/`: Delete application
- `PATCH /applications/{id}/`: Update application info, stage, fees, etc.

### Related Endpoints:
- `POST /applications/{id}/documents/`: Upload documents
- `POST /applications/{id}/generate-documents/`: Generate PDF documents
- `POST /applications/{id}/notes/`: Create application notes
- `POST /applications/{id}/calculator/`: Loan calculator tool
- `POST /applications/{id}/repayments/`: Add repayment schedule
- `POST /applications/{id}/extension/`: Loan extension info

### Dependencies:
- **Borrower Service**: Application creation auto-links borrowers
- **Broker Service**: Links brokers/referrals to application
- **Valuer/QS Service**: Links valuers and QS to application
- **Notification Service**: Triggers email alerts on stage changes and repayment reminders
- **Document Service**: Used to generate and manage files

---

## 2. Borrower Service

### Core Endpoints:
- `GET /borrowers/`: List borrowers
- `GET /borrowers/{id}/`: Borrower detail page
- `POST /borrowers/`: Add borrower

### Related Endpoints:
- `GET /borrowers/search/`: Search borrower by name, phone, etc.
- `GET /borrowers/{id}/applications/`: Applications linked to borrower

### Dependencies:
- **Application Service**: Automatically creates or links borrower on application creation
- **Broker Service**: Links borrower to broker or referral

---

## 3. Guarantor Service

### Core Endpoints:
- `POST /guarantors/`: Create guarantor (company/individual)
- `GET /guarantors/{id}/`: Retrieve guarantor details

### Dependencies:
- **Application Service**: Pulls input fields from application form

---

## 4. Broker Service

### Core Endpoints:
- `GET /brokers/`: List all brokers
- `GET /brokers/{id}/`: Broker detail page
- `POST /brokers/`: Add broker
- `DELETE /brokers/{id}/`: Delete broker

### Related Endpoints:
- `GET /brokers/{id}/applications/`: Applications linked to broker
- `GET /brokers/{id}/borrowers/`: Borrowers linked to broker

### Dependencies:
- **Application Service**: Links broker to application
- **Borrower Service**: Broker links with borrower

---

## 5. Valuer Service

### Core Endpoints:
- `GET /valuers/`: List valuers
- `POST /valuers/`: Add valuer
- `DELETE /valuers/{id}/`: Delete valuer
- `GET /valuers/{id}/applications/`: Applications associated with valuer

---

## 6. QS Service

### Core Endpoints:
- `GET /qs/`: List QS
- `POST /qs/`: Add QS
- `DELETE /qs/{id}/`: Delete QS
- `GET /qs/{id}/applications/`: Applications associated with QS

---

## 7. Product Service

### Core Endpoints:
- `GET /products/`: Product list
- `GET /products/{id}/`: Product details
- `GET /products/{id}/documents/`: Product document list

---

## 8. Account & Authentication Service

### Core Endpoints:
- `POST /auth/login/`: Login
- `POST /auth/forgot-password/`: Reset password link
- `POST /auth/change-password/`: Change password
- `POST /auth/create-account/`: Create user account
- `DELETE /auth/delete-account/`: Delete account

---

## 9. Notification Service

### Triggers & Behaviors:
- Repayment reminder: Triggered X days before repayment due date
- Expiration reminder: Triggered X days before loan expiration
- Late repayment: Triggers at 3, 7, 10 days post-due
- Stage stagnation: Triggers after X days in same stage

### Dependencies:
- **Application Service**: Sends notification on stage changes
- **Repayment Schedule**: Uses due date data to schedule reminders

---

## 10. Document Service

### Core Endpoints:
- `POST /documents/generate/`: Generate documents from application data
- `GET /documents/{id}/`: Retrieve document
- `POST /documents/upload/`: Upload additional documents

### Dependencies:
- **Application Service**: Main source of document data and triggers
- **Product Service**: Document templates

---
