# API Implementation Milestones

This document outlines the implementation plan for the new API requirements in the Loan Application System V2. The milestones are organized from basic to advanced implementation, prioritized by importance.

## Phase 1: Core Entity Updates (High Priority)

### Milestone 1.1: Application Stage Implementation
**Estimated Time: 3-5 days**

1. **Update Application Model**
   - Add `stage` field as Enum with values: 
     - "enquiry"
     - "indicative offer"
     - "valuation"
     - "dual"
     - "formal approval"
     - "loan documents issued"
     - "loan documents return"
     - "settlement"
     - "reject"
     - "withdrawal"
   - Create migration for the model update

2. **Implement Stage Change Notifications**
   - Create a signal handler for stage changes
   - Implement email notification to broker and borrowers when stage changes
   - Add unit tests for stage change notifications

3. **Implement Stage Timer Logic**
   - Create a configurable setting for stage duration thresholds
   - Implement a background task to check for stagnant applications
   - Create notification system for BD alerts when applications remain in the same stage
   - Add unit tests for timer logic

### Milestone 1.2: Valuer and QS Integration
**Estimated Time: 2-4 days**

1. **Update Application Model**
   - Add embedded fields for valuer information:
     - `valuer_info.company_name`
     - `valuer_info.contact_name`
     - `valuer_info.email`
     - `valuer_info.phone`
   - Add embedded fields for QS information:
     - `qs_info.company_name`
     - `qs_info.contact_name`
     - `qs_info.email`
     - `qs_info.phone`
   - Create migration for the model update

2. **Update Application API**
   - Modify serializers to include valuer and QS information
   - Update API documentation
   - Add validation for valuer and QS fields
   - Add unit tests for valuer and QS fields

## Phase 2: New Entity Services (High Priority)

### Milestone 2.1: Branch Service Implementation
**Estimated Time: 3-4 days**

1. **Create Branch Model**
   - Implement Branch model with fields:
     - `id`
     - `name`
     - `address`
     - Created/updated timestamps
   - Create migration for the new model

2. **Implement Branch API Endpoints**
   - `GET /branches/`: List branches
   - `POST /branches/`: Create new branch
   - `GET /branches/{id}/`: Get branch detail
   - `DELETE /branches/{id}/`: Delete branch
   - `PATCH /branches/{id}/`: Update branch info

3. **Create Branch Serializers**
   - Implement serializers for Branch model
   - Add validation for branch fields
   - Add unit tests for branch serializers

4. **Add Branch API Documentation**
   - Update API documentation with branch endpoints
   - Add example requests and responses

### Milestone 2.2: BD (Business Development) Service Implementation
**Estimated Time: 4-5 days**

1. **Create BD Model**
   - Implement BD model with fields:
     - `id`
     - `name`
     - `email`
     - `phone`
     - `branch_id` (ForeignKey to Branch)
     - Created/updated timestamps
   - Create migration for the new model

2. **Implement BD API Endpoints**
   - `GET /bds/`: List all BDs (with optional filters)
   - `POST /bds/`: Create a new BD
   - `GET /bds/{id}/`: Get BD detail
   - `DELETE /bds/{id}/`: Delete BD
   - `PATCH /bds/{id}/`: Update BD

3. **Create BD Serializers**
   - Implement serializers for BD model
   - Add validation for BD fields
   - Add unit tests for BD serializers

4. **Add BD API Documentation**
   - Update API documentation with BD endpoints
   - Add example requests and responses

### Milestone 2.3: Update Broker Model and API
**Estimated Time: 2-3 days**

1. **Update Broker Model**
   - Add `branch_id` field (ForeignKey to Branch)
   - Add `bd_ids` field (ManyToMany relationship with BD)
   - Create migration for the model update

2. **Update Broker API**
   - Modify serializers to include branch and BD information
   - Update API documentation
   - Add validation for branch and BD fields
   - Add unit tests for updated broker model

## Phase 3: Company Borrower Implementation (Medium Priority)

### Milestone 3.1: Company Borrower Model
**Estimated Time: 3-4 days**

1. **Create Company Borrower Model**
   - Implement Company Borrower model with fields:
     - `company_name`
     - `abn` / `acn`
     - `director_id` (ForeignKey to Borrower)
     - `contact_number`
     - `industry_type`
     - `registered_address` (structured address)
     - `trustee_flags` (is_trustee, is_smsf)
     - `trustee_name`
     - `annual_income`
     - Created/updated timestamps
   - Create migration for the new model

2. **Update Application Model**
   - Add relationship to Company Borrower
   - Create migration for the model update

3. **Create Company Borrower Serializers**
   - Implement serializers for Company Borrower model
   - Add validation for company borrower fields
   - Add unit tests for company borrower serializers

### Milestone 3.2: Company Borrower API
**Estimated Time: 2-3 days**

1. **Implement Company Borrower API Endpoints**
   - `GET /company-borrowers/`: List company borrowers
   - `POST /company-borrowers/`: Create company borrower
   - `GET /company-borrowers/{id}/`: Get company borrower detail
   - `PATCH /company-borrowers/{id}/`: Update company borrower
   - `DELETE /company-borrowers/{id}/`: Delete company borrower

2. **Update Application API**
   - Modify application serializers to include company borrower information
   - Update API documentation
   - Add unit tests for company borrower API

## Phase 4: Enhanced Loan Details (Medium Priority)

### Milestone 4.1: Loan Details Enhancement
**Estimated Time: 3-4 days**

1. **Update Application Model**
   - Add `purpose` field as multi-select (purchase, refinance, cash out, etc.)
   - Add `use_of_funds` field (structured with description & amount per row)
   - Add `exit_strategy` field (sale, refinance, cashflow, other)
   - Create migration for the model update

2. **Update Security/Property Information**
   - Enhance security model with additional fields:
     - `property_type` (enum)
     - `purchase_price`
     - `current_debt` (1st mortgage, 2nd mortgage)
     - `valuation_type` (single/double/garage/etc.)
     - `bedrooms`, `bathrooms`, `car_spaces`
     - `building_size`, `land_size`
     - `owner_occupied` (boolean)
   - Create migration for the model update

3. **Update Application API**
   - Modify serializers to include enhanced loan details
   - Update API documentation
   - Add validation for new fields
   - Add unit tests for enhanced loan details

## Phase 5: Integration and Workflow Enhancements (Medium Priority)

### Milestone 5.1: Form Signature and Document Upload
**Estimated Time: 2-3 days**

1. **Update Application Model**
   - Add `form_signature_date` field
   - Add `form_signed_by` field (borrowers/guarantors)
   - Add `uploaded_pdf_path` field
   - Create migration for the model update

2. **Enhance Document Service**
   - Update document upload functionality to link with application
   - Add signature verification for uploaded documents
   - Add unit tests for document upload and signature verification

### Milestone 5.2: Application Creation Flow Enhancement
**Estimated Time: 3-4 days**

1. **Update Application Creation API**
   - Enhance application creation to handle all new fields
   - Implement validation for the complete application flow
   - Add support for creating borrowers, guarantors, and company borrowers in a single request
   - Add unit tests for the enhanced application creation flow

2. **Implement PDF Data Extraction**
   - Add functionality to extract data from uploaded PDF applications
   - Map extracted data to application fields
   - Add validation for extracted data
   - Add unit tests for PDF data extraction

## Phase 6: Notification and Reporting Enhancements (Lower Priority)

### Milestone 6.1: Enhanced Notification System
**Estimated Time: 3-4 days**

1. **Update Notification Model**
   - Add support for BD notifications
   - Add support for branch-level notifications
   - Create migration for the model update

2. **Implement Notification Templates**
   - Create templates for stage change notifications
   - Create templates for stagnant application notifications
   - Add unit tests for notification templates

### Milestone 6.2: Reporting and Analytics
**Estimated Time: 4-5 days**

1. **Implement BD Performance Reports**
   - Create API endpoints for BD performance metrics
   - Implement filters for date ranges, branches, and application stages
   - Add unit tests for BD performance reports

2. **Implement Branch Performance Reports**
   - Create API endpoints for branch performance metrics
   - Implement filters for date ranges and application stages
   - Add unit tests for branch performance reports

3. **Implement Application Stage Analytics**
   - Create API endpoints for application stage metrics
   - Implement filters for date ranges, BDs, and branches
   - Add unit tests for application stage analytics

## Phase 7: API Security and Performance Optimization (Lower Priority)

### Milestone 7.1: API Security Enhancements
**Estimated Time: 2-3 days**

1. **Implement Role-Based Access Control**
   - Add BD and branch manager roles
   - Configure permissions for BD and branch manager roles
   - Add unit tests for role-based access control

2. **Enhance API Authentication**
   - Add support for API keys
   - Implement rate limiting for API endpoints
   - Add unit tests for API authentication

### Milestone 7.2: Performance Optimization
**Estimated Time: 3-4 days**

1. **Optimize Database Queries**
   - Add indexes for frequently queried fields
   - Implement query optimization for complex queries
   - Add performance tests for API endpoints

2. **Implement Caching**
   - Add caching for frequently accessed data
   - Configure cache invalidation
   - Add unit tests for caching

## Implementation Timeline

| Phase | Milestone | Priority | Estimated Time |
|-------|-----------|----------|----------------|
| 1 | 1.1: Application Stage Implementation | High | 3-5 days |
| 1 | 1.2: Valuer and QS Integration | High | 2-4 days |
| 2 | 2.1: Branch Service Implementation | High | 3-4 days |
| 2 | 2.2: BD Service Implementation | High | 4-5 days |
| 2 | 2.3: Update Broker Model and API | High | 2-3 days |
| 3 | 3.1: Company Borrower Model | Medium | 3-4 days |
| 3 | 3.2: Company Borrower API | Medium | 2-3 days |
| 4 | 4.1: Loan Details Enhancement | Medium | 3-4 days |
| 5 | 5.1: Form Signature and Document Upload | Medium | 2-3 days |
| 5 | 5.2: Application Creation Flow Enhancement | Medium | 3-4 days |
| 6 | 6.1: Enhanced Notification System | Lower | 3-4 days |
| 6 | 6.2: Reporting and Analytics | Lower | 4-5 days |
| 7 | 7.1: API Security Enhancements | Lower | 2-3 days |
| 7 | 7.2: Performance Optimization | Lower | 3-4 days |

**Total Estimated Time: 39-55 days**

## Dependencies and Risks

### Dependencies
1. **Branch and BD Services**: The Broker model update depends on the implementation of Branch and BD services.
2. **Application Stage Implementation**: The notification system for stage changes depends on the implementation of the application stage field.
3. **Company Borrower Model**: The application creation flow enhancement depends on the implementation of the company borrower model.

### Risks
1. **Data Migration**: Updating existing applications with new fields may require complex data migration.
2. **Integration Complexity**: The integration of multiple new services may introduce unexpected complexity.
3. **Performance Impact**: The addition of new fields and relationships may impact API performance.
4. **Testing Coverage**: Ensuring comprehensive test coverage for all new features may be challenging.

## Success Criteria

1. **API Completeness**: All required API endpoints are implemented and documented.
2. **Data Integrity**: All data relationships are properly maintained.
3. **Performance**: API response times remain within acceptable limits.
4. **Test Coverage**: All new features have adequate test coverage.
5. **Documentation**: API documentation is complete and up-to-date.
