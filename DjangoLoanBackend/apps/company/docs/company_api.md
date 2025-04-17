# Company API Documentation

This document describes the API endpoints and data structures for working with Company entities in the Loan Application System.

## Overview

The Company API provides endpoints for managing company borrowers, including company details, directors, shareholders, and financial information.

## Data Structures

### Company

```json
{
  "id": "uuid",
  "name": "ABC Company Pty Ltd",
  "trading_name": "ABC Solutions",
  "company_type": "PTY_LTD",
  "acn": "123456789",
  "abn": "12345678901",
  "registration_date": "2010-01-01",
  "registration_jurisdiction": "NSW",
  "registered_address_line1": "123 Business St",
  "registered_address_line2": "Suite 100",
  "registered_city": "Sydney",
  "registered_state": "NSW",
  "registered_postal_code": "2000",
  "registered_country": "Australia",
  "registered_address": {
    "line1": "123 Business St",
    "line2": "Suite 100",
    "city": "Sydney",
    "state": "NSW",
    "postal_code": "2000",
    "country": "Australia"
  },
  "business_address_line1": "456 Office Ave",
  "business_address_line2": "",
  "business_city": "Sydney",
  "business_state": "NSW",
  "business_postal_code": "2000",
  "business_country": "Australia",
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
  "directors": [
    {
      "id": "uuid",
      "full_name": "John Smith",
      "role": "MANAGING_DIRECTOR",
      "appointment_date": "2010-01-01",
      "phone": "0412345678",
      "email": "john.smith@abccompany.com.au"
    }
  ],
  "shareholders": [
    {
      "id": "uuid",
      "shareholder_name": "John Smith",
      "shareholder_type": "INDIVIDUAL",
      "shareholding_percentage": "60.00",
      "share_class": "ORDINARY",
      "is_director": true
    }
  ],
  "latest_financial": {
    "id": "uuid",
    "financial_year": "2022",
    "annual_revenue": "5000000.00",
    "annual_profit": "750000.00",
    "current_ratio": 1.5,
    "debt_to_equity_ratio": 1.0,
    "profit_margin": 0.15,
    "source": "AUDITED"
  },
  "financials": [
    {
      "id": "uuid",
      "financial_year": "2022",
      "annual_revenue": "5000000.00",
      "annual_profit": "750000.00",
      "current_ratio": 1.5,
      "debt_to_equity_ratio": 1.0,
      "profit_margin": 0.15,
      "source": "AUDITED"
    }
  ],
  "directors_count": 1,
  "shareholders_count": 1,
  "created_at": "2023-04-18T10:00:00Z",
  "updated_at": "2023-04-18T10:00:00Z"
}
```

### Director

```json
{
  "id": "uuid",
  "company": "uuid",
  "company_name": "ABC Company Pty Ltd",
  "first_name": "John",
  "middle_name": null,
  "last_name": "Smith",
  "full_name": "John Smith",
  "date_of_birth": "1975-05-15",
  "director_id": "DIR123456",
  "appointment_date": "2010-01-01",
  "role": "MANAGING_DIRECTOR",
  "residential_address_line1": "789 Home St",
  "residential_address_line2": null,
  "residential_city": "Sydney",
  "residential_state": "NSW",
  "residential_postal_code": "2000",
  "residential_country": "Australia",
  "residential_address": {
    "line1": "789 Home St",
    "line2": null,
    "city": "Sydney",
    "state": "NSW",
    "postal_code": "2000",
    "country": "Australia"
  },
  "phone": "0412345678",
  "email": "john.smith@abccompany.com.au",
  "identification_type": "DRIVERS_LICENSE",
  "identification_number": "DL123456",
  "identification_expiry": null,
  "is_shareholder": true,
  "created_at": "2023-04-18T10:00:00Z",
  "updated_at": "2023-04-18T10:00:00Z"
}
```

### Shareholder

```json
{
  "id": "uuid",
  "company": "uuid",
  "company_name": "ABC Company Pty Ltd",
  "shareholder_type": "INDIVIDUAL",
  "shareholder_name": "John Smith",
  "individual_first_name": "John",
  "individual_last_name": "Smith",
  "individual_date_of_birth": "1975-05-15",
  "corporate_name": null,
  "corporate_acn": null,
  "corporate_abn": null,
  "trust_name": null,
  "trust_abn": null,
  "trust_type": null,
  "shareholding_percentage": "60.00",
  "share_class": "ORDINARY",
  "acquisition_date": "2010-01-01",
  "is_director": true,
  "director": "uuid",
  "director_name": "John Smith",
  "created_at": "2023-04-18T10:00:00Z",
  "updated_at": "2023-04-18T10:00:00Z"
}
```

### Financial Information

```json
{
  "id": "uuid",
  "company": "uuid",
  "company_name": "ABC Company Pty Ltd",
  "financial_year": "2022",
  "financial_year_end_date": "2022-06-30",
  "annual_revenue": "5000000.00",
  "annual_profit": "750000.00",
  "total_assets": "3000000.00",
  "total_liabilities": "1500000.00",
  "current_assets": "1200000.00",
  "current_liabilities": "800000.00",
  "equity": "1500000.00",
  "ebitda": "900000.00",
  "current_ratio": 1.5,
  "debt_to_equity_ratio": 1.0,
  "profit_margin": 0.15,
  "source": "AUDITED",
  "notes": "Financial statements audited by XYZ Accountants",
  "created_at": "2023-04-18T10:00:00Z",
  "updated_at": "2023-04-18T10:00:00Z"
}
```

## API Endpoints

### Company Endpoints

#### List Companies

```
GET /api/companies/
```

Returns a list of all companies with simplified information.

#### Get Company Details

```
GET /api/companies/{id}/
```

Returns detailed information about a specific company, including directors, shareholders, and financial information.

#### Create Company

```
POST /api/companies/
```

Creates a new company.

#### Update Company

```
PUT /api/companies/{id}/
PATCH /api/companies/{id}/
```

Updates an existing company. PUT requires all fields, while PATCH allows partial updates.

#### Delete Company

```
DELETE /api/companies/{id}/
```

Deletes a company.

#### Get Company Directors

```
GET /api/companies/{id}/directors/
```

Returns all directors for a specific company.

#### Get Company Shareholders

```
GET /api/companies/{id}/shareholders/
```

Returns all shareholders for a specific company.

#### Get Company Financial Information

```
GET /api/companies/{id}/financials/
```

Returns all financial information for a specific company.

#### Get Latest Financial Information

```
GET /api/companies/{id}/latest_financial/
```

Returns the latest financial information for a specific company.

### Director Endpoints

#### List Directors

```
GET /api/directors/
```

Returns a list of all directors with simplified information.

#### Get Director Details

```
GET /api/directors/{id}/
```

Returns detailed information about a specific director.

#### Create Director

```
POST /api/directors/
```

Creates a new director.

#### Update Director

```
PUT /api/directors/{id}/
PATCH /api/directors/{id}/
```

Updates an existing director. PUT requires all fields, while PATCH allows partial updates.

#### Delete Director

```
DELETE /api/directors/{id}/
```

Deletes a director.

#### Get Directors by Company

```
GET /api/directors/by_company/
```

Returns directors grouped by company.

### Shareholder Endpoints

#### List Shareholders

```
GET /api/shareholders/
```

Returns a list of all shareholders with simplified information.

#### Get Shareholder Details

```
GET /api/shareholders/{id}/
```

Returns detailed information about a specific shareholder.

#### Create Shareholder

```
POST /api/shareholders/
```

Creates a new shareholder.

#### Update Shareholder

```
PUT /api/shareholders/{id}/
PATCH /api/shareholders/{id}/
```

Updates an existing shareholder. PUT requires all fields, while PATCH allows partial updates.

#### Delete Shareholder

```
DELETE /api/shareholders/{id}/
```

Deletes a shareholder.

#### Get Shareholders by Company

```
GET /api/shareholders/by_company/
```

Returns shareholders grouped by company.

#### Get Shareholders by Type

```
GET /api/shareholders/by_type/
```

Returns shareholders grouped by type (Individual, Corporate, Trust).

### Financial Information Endpoints

#### List Financial Information

```
GET /api/financials/
```

Returns a list of all financial information with simplified information.

#### Get Financial Information Details

```
GET /api/financials/{id}/
```

Returns detailed information about specific financial information.

#### Create Financial Information

```
POST /api/financials/
```

Creates new financial information.

#### Update Financial Information

```
PUT /api/financials/{id}/
PATCH /api/financials/{id}/
```

Updates existing financial information. PUT requires all fields, while PATCH allows partial updates.

#### Delete Financial Information

```
DELETE /api/financials/{id}/
```

Deletes financial information.

#### Get Financial Information by Company

```
GET /api/financials/by_company/
```

Returns financial information grouped by company.

#### Get Financial Information by Year

```
GET /api/financials/by_year/
```

Returns financial information grouped by year.

## Filtering and Searching

### Company Filtering

The Company API supports filtering and searching:

- **Filter by fields**: `company_type`, `registration_jurisdiction`
  - Example: `/api/companies/?company_type=PTY_LTD`

- **Search**: `name`, `trading_name`, `acn`, `abn`, `email`, `industry`
  - Example: `/api/companies/?search=ABC`

- **Ordering**: `name`, `registration_date`, `employees_count`, `years_in_business`
  - Example: `/api/companies/?ordering=-registration_date`

### Director Filtering

- **Filter by fields**: `company`, `role`, `is_shareholder`
  - Example: `/api/directors/?role=MANAGING_DIRECTOR`

- **Search**: `first_name`, `last_name`, `email`, `company__name`
  - Example: `/api/directors/?search=Smith`

- **Ordering**: `last_name`, `first_name`, `appointment_date`
  - Example: `/api/directors/?ordering=last_name`

### Shareholder Filtering

- **Filter by fields**: `company`, `shareholder_type`, `share_class`, `is_director`
  - Example: `/api/shareholders/?shareholder_type=INDIVIDUAL`

- **Search**: `individual_first_name`, `individual_last_name`, `corporate_name`, `trust_name`, `company__name`
  - Example: `/api/shareholders/?search=Smith`

- **Ordering**: `shareholding_percentage`, `acquisition_date`
  - Example: `/api/shareholders/?ordering=-shareholding_percentage`

### Financial Information Filtering

- **Filter by fields**: `company`, `financial_year`, `source`
  - Example: `/api/financials/?financial_year=2022`

- **Search**: `company__name`, `financial_year`
  - Example: `/api/financials/?search=ABC`

- **Ordering**: `financial_year`, `financial_year_end_date`, `annual_revenue`, `annual_profit`
  - Example: `/api/financials/?ordering=-financial_year`

## Example Usage

### JavaScript Example

```javascript
// Get all companies
const getCompanies = async () => {
  const response = await fetch('/api/companies/');
  return response.json();
};

// Get company details
const getCompanyDetails = async (companyId) => {
  const response = await fetch(`/api/companies/${companyId}/`);
  return response.json();
};

// Create a new company
const createCompany = async (companyData) => {
  const response = await fetch('/api/companies/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(companyData),
  });
  return response.json();
};

// Update a company
const updateCompany = async (companyId, companyData) => {
  const response = await fetch(`/api/companies/${companyId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(companyData),
  });
  return response.json();
};

// Delete a company
const deleteCompany = async (companyId) => {
  await fetch(`/api/companies/${companyId}/`, {
    method: 'DELETE',
  });
};

// Get company directors
const getCompanyDirectors = async (companyId) => {
  const response = await fetch(`/api/companies/${companyId}/directors/`);
  return response.json();
};

// Get company shareholders
const getCompanyShareholders = async (companyId) => {
  const response = await fetch(`/api/companies/${companyId}/shareholders/`);
  return response.json();
};

// Get company financial information
const getCompanyFinancials = async (companyId) => {
  const response = await fetch(`/api/companies/${companyId}/financials/`);
  return response.json();
};

// Get latest financial information
const getLatestFinancial = async (companyId) => {
  const response = await fetch(`/api/companies/${companyId}/latest_financial/`);
  return response.json();
};
```
