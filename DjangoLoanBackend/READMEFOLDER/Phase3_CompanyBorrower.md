# Phase 3: Company Borrower Implementation

## Overview

Phase 3 focuses on extending the loan application system to support company borrowers in addition to individual borrowers. This phase will implement models and APIs for company borrowers, including company details, directors, shareholders, and financial information.

## Milestones

### Milestone 3.1: Company Borrower Model

**Status:** Not Started  
**Target Start Date:** 2023-04-20  
**Target Completion Date:** 2023-04-25

#### Tasks:

1. **Create Company Model**
   - Implement base Company model with company details
   - Add company type classification (Pty Ltd, Ltd, Trust, Partnership, etc.)
   - Add company registration and tax information fields
   - Add company contact information

2. **Create Company Director Model**
   - Implement Director model with personal details
   - Add relationship to Company model
   - Add director role and appointment information
   - Add director identification fields

3. **Create Company Shareholder Model**
   - Implement Shareholder model with ownership details
   - Support both individual and corporate shareholders
   - Add relationship to Company model
   - Add shareholding percentage and class information

4. **Create Company Financial Information Model**
   - Implement Financial Information model for company financials
   - Add annual revenue, profit, assets, and liabilities fields
   - Add relationship to Company model
   - Support multiple financial years

5. **Update Application Model**
   - Extend Application model to support company borrowers
   - Add relationship between Application and Company
   - Ensure backward compatibility with individual borrowers

6. **Create Database Migrations**
   - Create migration files for all new models
   - Ensure data integrity with appropriate constraints
   - Add indexes for performance optimization

### Milestone 3.2: Company Borrower API

**Status:** Not Started  
**Target Start Date:** 2023-04-26  
**Target Completion Date:** 2023-05-02

#### Tasks:

1. **Implement Company API**
   - Create CRUD endpoints for company management
   - Implement serializers for company data
   - Add validation for company registration information
   - Add filtering and search capabilities

2. **Implement Director API**
   - Create CRUD endpoints for director management
   - Implement serializers for director data
   - Add validation for director identification
   - Support listing directors by company

3. **Implement Shareholder API**
   - Create CRUD endpoints for shareholder management
   - Implement serializers for shareholder data
   - Add validation for shareholding percentages
   - Support listing shareholders by company

4. **Implement Financial Information API**
   - Create CRUD endpoints for financial information
   - Implement serializers for financial data
   - Add validation for financial figures
   - Support listing financial information by company and year

5. **Update Application API**
   - Extend application endpoints to support company borrowers
   - Update application serializers for company data
   - Add validation for company applications
   - Ensure backward compatibility with individual applications

6. **Add Documentation and Tests**
   - Create API documentation for all new endpoints
   - Add unit tests for models and serializers
   - Add integration tests for API endpoints
   - Update existing documentation to reflect company borrower support

## Implementation Details

### Company Model

The Company model will store information about company borrowers, including:

- Company name and trading name
- Company type (Pty Ltd, Ltd, Trust, Partnership, etc.)
- ACN, ABN, and other registration numbers
- Registration date and jurisdiction
- Registered address and business address
- Contact information (phone, email, website)
- Industry and business description
- Number of employees and years in business

### Director Model

The Director model will store information about company directors, including:

- Personal details (name, date of birth, etc.)
- Relationship to the company
- Director ID and appointment date
- Residential address and contact information
- Identification documents
- Role in the company (Managing Director, Executive Director, etc.)

### Shareholder Model

The Shareholder model will store information about company shareholders, including:

- Shareholder type (Individual or Corporate)
- For individual shareholders: personal details
- For corporate shareholders: company details
- Shareholding percentage and share class
- Date of acquisition
- Relationship to directors (if any)

### Financial Information Model

The Financial Information model will store financial data for companies, including:

- Financial year
- Annual revenue and profit
- Total assets and liabilities
- Current ratio and debt-to-equity ratio
- EBITDA and other financial metrics
- Source of financial information (Audited, Management Accounts, etc.)

### Application Model Extensions

The Application model will be extended to support company borrowers:

- Add relationship to Company model
- Add borrower type field (Individual or Company)
- Add company-specific application fields
- Ensure backward compatibility with individual applications

## API Endpoints

### Company API

- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create a new company
- `GET /api/companies/{id}/` - Get company details
- `PUT /api/companies/{id}/` - Update company details
- `DELETE /api/companies/{id}/` - Delete a company
- `GET /api/companies/{id}/directors/` - List company directors
- `GET /api/companies/{id}/shareholders/` - List company shareholders
- `GET /api/companies/{id}/financials/` - List company financial information

### Director API

- `GET /api/directors/` - List all directors
- `POST /api/directors/` - Create a new director
- `GET /api/directors/{id}/` - Get director details
- `PUT /api/directors/{id}/` - Update director details
- `DELETE /api/directors/{id}/` - Delete a director

### Shareholder API

- `GET /api/shareholders/` - List all shareholders
- `POST /api/shareholders/` - Create a new shareholder
- `GET /api/shareholders/{id}/` - Get shareholder details
- `PUT /api/shareholders/{id}/` - Update shareholder details
- `DELETE /api/shareholders/{id}/` - Delete a shareholder

### Financial Information API

- `GET /api/financials/` - List all financial information
- `POST /api/financials/` - Create new financial information
- `GET /api/financials/{id}/` - Get financial information details
- `PUT /api/financials/{id}/` - Update financial information
- `DELETE /api/financials/{id}/` - Delete financial information

### Application API Extensions

- `POST /api/applications/company/` - Create a new company application
- `GET /api/applications/company/{id}/` - Get company application details
- `PUT /api/applications/company/{id}/` - Update company application
- `GET /api/applications/company/{id}/directors/` - List application directors
- `GET /api/applications/company/{id}/shareholders/` - List application shareholders
- `GET /api/applications/company/{id}/financials/` - List application financial information

## Data Models

### Company

```
{
  "id": "uuid",
  "name": "ABC Company Pty Ltd",
  "trading_name": "ABC Solutions",
  "company_type": "PTY_LTD",
  "acn": "123456789",
  "abn": "12345678901",
  "registration_date": "2010-01-01",
  "registration_jurisdiction": "NSW",
  "registered_address": {
    "line1": "123 Business St",
    "line2": "Suite 100",
    "city": "Sydney",
    "state": "NSW",
    "postal_code": "2000",
    "country": "Australia"
  },
  "business_address": {
    "line1": "456 Office Ave",
    "line2": "",
    "city": "Sydney",
    "state": "NSW",
    "postal_code": "2000",
    "country": "Australia"
  },
  "phone": "0298765432",
  "email": "info@abccompany.com.au",
  "website": "https://www.abccompany.com.au",
  "industry": "Technology",
  "business_description": "Software development and IT consulting",
  "employees_count": 25,
  "years_in_business": 13,
  "created_at": "2023-04-20T10:00:00Z",
  "updated_at": "2023-04-20T10:00:00Z"
}
```

### Director

```
{
  "id": "uuid",
  "company": "uuid",
  "first_name": "John",
  "last_name": "Smith",
  "date_of_birth": "1975-05-15",
  "director_id": "DIR123456",
  "appointment_date": "2010-01-01",
  "role": "MANAGING_DIRECTOR",
  "residential_address": {
    "line1": "789 Home St",
    "line2": "",
    "city": "Sydney",
    "state": "NSW",
    "postal_code": "2000",
    "country": "Australia"
  },
  "phone": "0412345678",
  "email": "john.smith@abccompany.com.au",
  "identification_type": "DRIVERS_LICENSE",
  "identification_number": "DL123456",
  "created_at": "2023-04-20T10:00:00Z",
  "updated_at": "2023-04-20T10:00:00Z"
}
```

### Shareholder

```
{
  "id": "uuid",
  "company": "uuid",
  "shareholder_type": "INDIVIDUAL",
  "individual": {
    "first_name": "Jane",
    "last_name": "Smith",
    "date_of_birth": "1978-08-20"
  },
  "corporate": null,
  "shareholding_percentage": 60.0,
  "share_class": "ORDINARY",
  "acquisition_date": "2010-01-01",
  "is_director": true,
  "director": "uuid",
  "created_at": "2023-04-20T10:00:00Z",
  "updated_at": "2023-04-20T10:00:00Z"
}
```

### Financial Information

```
{
  "id": "uuid",
  "company": "uuid",
  "financial_year": "2022",
  "financial_year_end_date": "2022-06-30",
  "annual_revenue": 5000000.00,
  "annual_profit": 750000.00,
  "total_assets": 3000000.00,
  "total_liabilities": 1500000.00,
  "current_assets": 1200000.00,
  "current_liabilities": 800000.00,
  "equity": 1500000.00,
  "ebitda": 900000.00,
  "source": "AUDITED",
  "notes": "Financial statements audited by XYZ Accountants",
  "created_at": "2023-04-20T10:00:00Z",
  "updated_at": "2023-04-20T10:00:00Z"
}
```

### Application (Extended)

```
{
  "id": "uuid",
  "reference_number": "APP12345",
  "borrower_type": "COMPANY",
  "individual_borrower": null,
  "company_borrower": "uuid",
  "loan_amount": 1000000.00,
  "loan_purpose": "Business expansion",
  "loan_term": 60,
  "status": "IN_PROGRESS",
  "stage": "DOCUMENTATION",
  "created_at": "2023-04-20T10:00:00Z",
  "updated_at": "2023-04-20T10:00:00Z"
}
```
