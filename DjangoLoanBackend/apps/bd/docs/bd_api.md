# BD API Documentation

This document describes the API endpoints and data structures for working with Business Development (BD) entities in the Loan Application System.

## Overview

The BD API provides endpoints for managing Business Development staff members. BDs are associated with branches and are responsible for business development activities.

## Data Structures

### BD

```json
{
  "id": "uuid",
  "first_name": "John",
  "last_name": "Smith",
  "full_name": "John Smith",
  "email": "john.smith@example.com",
  "phone": "0412345678",
  "branch": "uuid",
  "branch_name": "Sydney CBD Branch",
  "branch_details": {
    "id": "uuid",
    "name": "Sydney CBD Branch",
    "code": "SYD001",
    "city": "Sydney",
    "state": "NSW",
    "is_active": true,
    "manager_name": "John Manager"
  },
  "employee_id": "EMP001",
  "position": "Business Development Manager",
  "hire_date": "2020-01-15",
  "is_active": true,
  "bio": "John has over 10 years of experience in business development.",
  "linkedin_profile": "https://www.linkedin.com/in/johnsmith",
  "profile_image": "/media/bd_profiles/john_smith.jpg",
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z",
  "experience_years": 3
}
```

## API Endpoints

### List BDs

```
GET /api/bds/
```

Returns a list of all BDs with simplified information.

#### Response

```json
[
  {
    "id": "uuid",
    "full_name": "John Smith",
    "email": "john.smith@example.com",
    "position": "Business Development Manager",
    "branch_name": "Sydney CBD Branch",
    "is_active": true
  },
  {
    "id": "uuid",
    "full_name": "Jane Doe",
    "email": "jane.doe@example.com",
    "position": "Senior Business Developer",
    "branch_name": "Melbourne CBD Branch",
    "is_active": true
  }
]
```

### Get BD Details

```
GET /api/bds/{id}/
```

Returns detailed information about a specific BD.

#### Response

```json
{
  "id": "uuid",
  "first_name": "John",
  "last_name": "Smith",
  "full_name": "John Smith",
  "email": "john.smith@example.com",
  "phone": "0412345678",
  "branch": "uuid",
  "branch_name": "Sydney CBD Branch",
  "branch_details": {
    "id": "uuid",
    "name": "Sydney CBD Branch",
    "code": "SYD001",
    "city": "Sydney",
    "state": "NSW",
    "is_active": true,
    "manager_name": "John Manager"
  },
  "employee_id": "EMP001",
  "position": "Business Development Manager",
  "hire_date": "2020-01-15",
  "is_active": true,
  "bio": "John has over 10 years of experience in business development.",
  "linkedin_profile": "https://www.linkedin.com/in/johnsmith",
  "profile_image": "/media/bd_profiles/john_smith.jpg",
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z",
  "experience_years": 3
}
```

### Create BD

```
POST /api/bds/
```

Creates a new BD.

#### Request Body

```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com",
  "phone": "0487654321",
  "branch": "uuid",
  "employee_id": "EMP002",
  "position": "Senior Business Developer",
  "hire_date": "2021-02-15",
  "is_active": true,
  "bio": "Jane has over 8 years of experience in business development.",
  "linkedin_profile": "https://www.linkedin.com/in/janedoe"
}
```

#### Response

Returns the created BD with all fields, including the generated ID and timestamps.

### Update BD

```
PUT /api/bds/{id}/
PATCH /api/bds/{id}/
```

Updates an existing BD. PUT requires all fields, while PATCH allows partial updates.

#### Request Body (PATCH example)

```json
{
  "position": "Senior Business Development Manager",
  "is_active": false
}
```

#### Response

Returns the updated BD with all fields.

### Delete BD

```
DELETE /api/bds/{id}/
```

Deletes a BD.

#### Response

Returns 204 No Content on success.

### Get Active BDs

```
GET /api/bds/active/
```

Returns a list of all active BDs.

#### Response

```json
[
  {
    "id": "uuid",
    "full_name": "John Smith",
    "email": "john.smith@example.com",
    "position": "Business Development Manager",
    "branch_name": "Sydney CBD Branch",
    "is_active": true
  },
  {
    "id": "uuid",
    "full_name": "Jane Doe",
    "email": "jane.doe@example.com",
    "position": "Senior Business Developer",
    "branch_name": "Melbourne CBD Branch",
    "is_active": true
  }
]
```

### Get BDs by Branch

```
GET /api/bds/by-branch/
```

Returns BDs grouped by branch.

#### Response

```json
[
  {
    "id": "uuid",
    "name": "Sydney CBD Branch",
    "code": "SYD001",
    "city": "Sydney",
    "state": "NSW",
    "is_active": true,
    "manager_name": "John Manager",
    "bds": [
      {
        "id": "uuid",
        "full_name": "John Smith",
        "email": "john.smith@example.com",
        "position": "Business Development Manager",
        "branch_name": "Sydney CBD Branch",
        "is_active": true
      },
      {
        "id": "uuid",
        "full_name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "position": "Business Developer",
        "branch_name": "Sydney CBD Branch",
        "is_active": true
      }
    ]
  },
  {
    "id": "uuid",
    "name": "Melbourne CBD Branch",
    "code": "MEL001",
    "city": "Melbourne",
    "state": "VIC",
    "is_active": true,
    "manager_name": "Jane Manager",
    "bds": [
      {
        "id": "uuid",
        "full_name": "Jane Doe",
        "email": "jane.doe@example.com",
        "position": "Senior Business Developer",
        "branch_name": "Melbourne CBD Branch",
        "is_active": true
      }
    ]
  }
]
```

## Filtering and Searching

The BD API supports filtering and searching:

- **Filter by fields**: `is_active`, `branch`, `position`
  - Example: `/api/bds/?is_active=true&branch=uuid`

- **Search**: `first_name`, `last_name`, `email`, `employee_id`
  - Example: `/api/bds/?search=John`

- **Ordering**: `last_name`, `first_name`, `hire_date`, `created_at`
  - Example: `/api/bds/?ordering=last_name,first_name`

## Example Usage

### JavaScript Example

```javascript
// Get all BDs
const getBDs = async () => {
  const response = await fetch('/api/bds/');
  return response.json();
};

// Get BD details
const getBDDetails = async (bdId) => {
  const response = await fetch(`/api/bds/${bdId}/`);
  return response.json();
};

// Create a new BD
const createBD = async (bdData) => {
  const response = await fetch('/api/bds/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bdData),
  });
  return response.json();
};

// Update a BD
const updateBD = async (bdId, bdData) => {
  const response = await fetch(`/api/bds/${bdId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bdData),
  });
  return response.json();
};

// Delete a BD
const deleteBD = async (bdId) => {
  await fetch(`/api/bds/${bdId}/`, {
    method: 'DELETE',
  });
};

// Get BDs by branch
const getBDsByBranch = async () => {
  const response = await fetch('/api/bds/by-branch/');
  return response.json();
};
```
