# Branch API Documentation

This document describes the API endpoints and data structures for working with Branch entities in the Loan Application System.

## Overview

The Branch API provides endpoints for managing branch offices. Branches are physical locations where the company operates and are associated with Business Development (BD) staff members.

## Data Structures

### Branch

```json
{
  "id": "uuid",
  "name": "Sydney CBD Branch",
  "code": "SYD001",
  "address_line1": "123 George Street",
  "address_line2": "Level 10",
  "city": "Sydney",
  "state": "NSW",
  "postal_code": "2000",
  "country": "Australia",
  "phone": "0291234567",
  "email": "sydney@example.com",
  "is_active": true,
  "manager_name": "John Manager",
  "manager_email": "john.manager@example.com",
  "manager_phone": "0412345678",
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z",
  "bd_count": 5,
  "active_bd_count": 4,
  "full_address": "123 George Street\nLevel 10\nSydney, NSW 2000\nAustralia"
}
```

## API Endpoints

### List Branches

```
GET /api/branches/
```

Returns a list of all branches with simplified information.

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
    "manager_name": "John Manager"
  },
  {
    "id": "uuid",
    "name": "Melbourne CBD Branch",
    "code": "MEL001",
    "city": "Melbourne",
    "state": "VIC",
    "is_active": true,
    "manager_name": "Jane Manager"
  }
]
```

### Get Branch Details

```
GET /api/branches/{id}/
```

Returns detailed information about a specific branch.

#### Response

```json
{
  "id": "uuid",
  "name": "Sydney CBD Branch",
  "code": "SYD001",
  "address_line1": "123 George Street",
  "address_line2": "Level 10",
  "city": "Sydney",
  "state": "NSW",
  "postal_code": "2000",
  "country": "Australia",
  "phone": "0291234567",
  "email": "sydney@example.com",
  "is_active": true,
  "manager_name": "John Manager",
  "manager_email": "john.manager@example.com",
  "manager_phone": "0412345678",
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z",
  "bd_count": 5,
  "active_bd_count": 4,
  "full_address": "123 George Street\nLevel 10\nSydney, NSW 2000\nAustralia"
}
```

### Create Branch

```
POST /api/branches/
```

Creates a new branch.

#### Request Body

```json
{
  "name": "Brisbane CBD Branch",
  "code": "BRI001",
  "address_line1": "456 Queen Street",
  "address_line2": "Level 5",
  "city": "Brisbane",
  "state": "QLD",
  "postal_code": "4000",
  "country": "Australia",
  "phone": "0731234567",
  "email": "brisbane@example.com",
  "is_active": true,
  "manager_name": "Bob Manager",
  "manager_email": "bob.manager@example.com",
  "manager_phone": "0487654321"
}
```

#### Response

Returns the created branch with all fields, including the generated ID and timestamps.

### Update Branch

```
PUT /api/branches/{id}/
PATCH /api/branches/{id}/
```

Updates an existing branch. PUT requires all fields, while PATCH allows partial updates.

#### Request Body (PATCH example)

```json
{
  "manager_name": "New Manager",
  "manager_email": "new.manager@example.com",
  "is_active": false
}
```

#### Response

Returns the updated branch with all fields.

### Delete Branch

```
DELETE /api/branches/{id}/
```

Deletes a branch.

#### Response

Returns 204 No Content on success.

### Get Active Branches

```
GET /api/branches/active/
```

Returns a list of all active branches.

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
    "manager_name": "John Manager"
  },
  {
    "id": "uuid",
    "name": "Melbourne CBD Branch",
    "code": "MEL001",
    "city": "Melbourne",
    "state": "VIC",
    "is_active": true,
    "manager_name": "Jane Manager"
  }
]
```

### Get Branch BDs

```
GET /api/branches/{id}/bds/
```

Returns a list of all BDs associated with a specific branch.

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
    "branch_name": "Sydney CBD Branch",
    "is_active": true
  }
]
```

## Filtering and Searching

The Branch API supports filtering and searching:

- **Filter by fields**: `is_active`, `state`, `country`
  - Example: `/api/branches/?is_active=true&state=NSW`

- **Search**: `name`, `code`, `city`, `manager_name`
  - Example: `/api/branches/?search=Sydney`

- **Ordering**: `name`, `code`, `created_at`
  - Example: `/api/branches/?ordering=-created_at`

## Example Usage

### JavaScript Example

```javascript
// Get all branches
const getBranches = async () => {
  const response = await fetch('/api/branches/');
  return response.json();
};

// Get branch details
const getBranchDetails = async (branchId) => {
  const response = await fetch(`/api/branches/${branchId}/`);
  return response.json();
};

// Create a new branch
const createBranch = async (branchData) => {
  const response = await fetch('/api/branches/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(branchData),
  });
  return response.json();
};

// Update a branch
const updateBranch = async (branchId, branchData) => {
  const response = await fetch(`/api/branches/${branchId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(branchData),
  });
  return response.json();
};

// Delete a branch
const deleteBranch = async (branchId) => {
  await fetch(`/api/branches/${branchId}/`, {
    method: 'DELETE',
  });
};

// Get BDs for a branch
const getBranchBDs = async (branchId) => {
  const response = await fetch(`/api/branches/${branchId}/bds/`);
  return response.json();
};
```
