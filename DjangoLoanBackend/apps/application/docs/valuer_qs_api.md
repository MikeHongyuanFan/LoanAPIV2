# Valuer and QS Information API Documentation

This document describes the API endpoints and data structures for working with Valuer and QS information in the Loan Application System.

## Overview

Valuer and QS information is stored directly in the Application model as JSON fields. This allows for flexible schema and easy querying. The API provides endpoints for updating this information and validation to ensure the data is complete and correct.

## Data Structures

### Valuer Information

The `valuer_info` field is a JSON object with the following structure:

```json
{
  "company_name": "Test Valuer Company",
  "contact_name": "John Valuer",
  "email": "valuer@example.com",
  "phone": "1122334455"
}
```

All fields are required when updating valuer information.

### QS Information

The `qs_info` field is a JSON object with the following structure:

```json
{
  "company_name": "Test QS Company",
  "contact_name": "Jane QS",
  "email": "qs@example.com",
  "phone": "5544332211"
}
```

All fields are required when updating QS information.

## API Endpoints

### Update Valuer Information

```
POST /api/applications/{id}/update-valuer-info/
```

Updates the valuer information for an application.

#### Request Body

```json
{
  "company_name": "Test Valuer Company",
  "contact_name": "John Valuer",
  "email": "valuer@example.com",
  "phone": "1122334455"
}
```

#### Response

```json
{
  "id": "uuid",
  "reference_number": "APP-2023-001",
  "stage": "VALUATION",
  "valuer_info": {
    "company_name": "Test Valuer Company",
    "contact_name": "John Valuer",
    "email": "valuer@example.com",
    "phone": "1122334455"
  },
  // ... other application fields
}
```

### Update QS Information

```
POST /api/applications/{id}/update-qs-info/
```

Updates the QS information for an application.

#### Request Body

```json
{
  "company_name": "Test QS Company",
  "contact_name": "Jane QS",
  "email": "qs@example.com",
  "phone": "5544332211"
}
```

#### Response

```json
{
  "id": "uuid",
  "reference_number": "APP-2023-001",
  "stage": "DUAL",
  "qs_info": {
    "company_name": "Test QS Company",
    "contact_name": "Jane QS",
    "email": "qs@example.com",
    "phone": "5544332211"
  },
  // ... other application fields
}
```

## Validation Rules

1. When an application is in the `VALUATION` stage, `valuer_info` is required.
2. When an application is in the `DUAL` stage, `qs_info` is required.
3. All fields in the `valuer_info` and `qs_info` objects are required.
4. The `email` field must be a valid email address.

## Example Usage

### JavaScript Example

```javascript
// Update valuer information
const updateValuerInfo = async (applicationId, valuerInfo) => {
  const response = await fetch(`/api/applications/${applicationId}/update-valuer-info/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(valuerInfo),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error);
  }
  
  return response.json();
};

// Update QS information
const updateQSInfo = async (applicationId, qsInfo) => {
  const response = await fetch(`/api/applications/${applicationId}/update-qs-info/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(qsInfo),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error);
  }
  
  return response.json();
};
```

### Python Example

```python
import requests

# Update valuer information
def update_valuer_info(application_id, valuer_info):
    response = requests.post(
        f'/api/applications/{application_id}/update-valuer-info/',
        json=valuer_info
    )
    response.raise_for_status()
    return response.json()

# Update QS information
def update_qs_info(application_id, qs_info):
    response = requests.post(
        f'/api/applications/{application_id}/update-qs-info/',
        json=qs_info
    )
    response.raise_for_status()
    return response.json()
```
