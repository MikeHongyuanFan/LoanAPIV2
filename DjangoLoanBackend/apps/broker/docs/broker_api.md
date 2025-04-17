# Broker API Documentation

This document describes the API endpoints and data structures for working with Broker entities in the Loan Application System.

## Overview

The Broker API provides endpoints for managing brokers, broker tiers, broker specializations, broker commissions, and commission payments. Brokers are now associated with branches and BDs (Business Development staff).

## Data Structures

### Broker

```json
{
  "id": "uuid",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "phone": "0412345678",
  "company": "ABC Brokers",
  "address": "123 Broker Street, Sydney NSW 2000",
  "license_number": "BRK12345",
  "commission_rate": 5.0,
  "active": true,
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z",
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
  "bd": "uuid",
  "bd_name": "Jane Doe",
  "bd_details": {
    "id": "uuid",
    "full_name": "Jane Doe",
    "email": "jane.doe@example.com",
    "position": "Business Development Manager",
    "branch_name": "Sydney CBD Branch",
    "is_active": true
  },
  "tier": "uuid",
  "tier_name": "Gold",
  "tier_details": {
    "id": "uuid",
    "name": "Gold",
    "description": "Gold tier brokers",
    "commission_multiplier": 1.5,
    "created_at": "2023-04-17T10:00:00Z",
    "updated_at": "2023-04-17T10:00:00Z"
  },
  "specializations": ["uuid1", "uuid2"],
  "specialization_names": ["Residential", "Commercial"],
  "specialization_details": [
    {
      "id": "uuid1",
      "name": "Residential",
      "description": "Residential property loans",
      "created_at": "2023-04-17T10:00:00Z",
      "updated_at": "2023-04-17T10:00:00Z"
    },
    {
      "id": "uuid2",
      "name": "Commercial",
      "description": "Commercial property loans",
      "created_at": "2023-04-17T10:00:00Z",
      "updated_at": "2023-04-17T10:00:00Z"
    }
  ],
  "years_of_experience": 5,
  "accreditation_number": "ACC12345",
  "accreditation_expiry": "2025-01-01",
  "profile_image": "/media/broker_profiles/john_smith.jpg",
  "bio": "John has over 5 years of experience in mortgage broking.",
  "website": "https://www.abcbrokers.com",
  "linkedin_profile": "https://www.linkedin.com/in/johnsmith",
  "accreditation_valid": true
}
```

### Broker Tier

```json
{
  "id": "uuid",
  "name": "Gold",
  "description": "Gold tier brokers",
  "commission_multiplier": 1.5,
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z"
}
```

### Broker Specialization

```json
{
  "id": "uuid",
  "name": "Residential",
  "description": "Residential property loans",
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z"
}
```

### Broker Commission

```json
{
  "id": "uuid",
  "broker": "uuid",
  "broker_name": "John Smith",
  "application": "uuid",
  "application_reference": "APP12345",
  "amount": 5000.00,
  "status": "PENDING",
  "description": "Commission for loan approval",
  "payment_date": null,
  "payment_reference": null,
  "notes": null,
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z"
}
```

### Commission Payment

```json
{
  "id": "uuid",
  "broker": "uuid",
  "broker_name": "John Smith",
  "payment_date": "2023-04-17",
  "total_amount": 10000.00,
  "payment_method": "BANK_TRANSFER",
  "reference_number": "PAY12345",
  "notes": "Monthly commission payment",
  "items": [
    {
      "id": "uuid",
      "commission": "uuid",
      "commission_details": {
        "id": "uuid",
        "broker": "uuid",
        "broker_name": "John Smith",
        "application": "uuid",
        "application_reference": "APP12345",
        "amount": 5000.00,
        "status": "PAID",
        "description": "Commission for loan approval",
        "payment_date": "2023-04-17",
        "payment_reference": "PAY12345",
        "notes": null,
        "created_at": "2023-04-17T10:00:00Z",
        "updated_at": "2023-04-17T10:00:00Z"
      },
      "amount_paid": 5000.00
    }
  ],
  "created_at": "2023-04-17T10:00:00Z",
  "updated_at": "2023-04-17T10:00:00Z"
}
```

## API Endpoints

### Broker Endpoints

#### List Brokers

```
GET /api/brokers/
```

Returns a list of all brokers with simplified information.

#### Get Broker Details

```
GET /api/brokers/{id}/
```

Returns detailed information about a specific broker.

#### Create Broker

```
POST /api/brokers/
```

Creates a new broker.

#### Update Broker

```
PUT /api/brokers/{id}/
PATCH /api/brokers/{id}/
```

Updates an existing broker. PUT requires all fields, while PATCH allows partial updates.

#### Delete Broker

```
DELETE /api/brokers/{id}/
```

Deletes a broker.

#### Get Active Brokers

```
GET /api/brokers/active/
```

Returns a list of all active brokers.

#### Get Brokers by Branch

```
GET /api/brokers/by-branch/
```

Returns brokers grouped by branch.

#### Get Brokers by BD

```
GET /api/brokers/by-bd/
```

Returns brokers grouped by BD.

#### Get Brokers by Tier

```
GET /api/brokers/by-tier/
```

Returns brokers grouped by tier.

#### Get Broker Commissions

```
GET /api/brokers/{id}/commissions/
```

Returns all commissions for a specific broker.

### Broker Tier Endpoints

#### List Broker Tiers

```
GET /api/broker-tiers/
```

Returns a list of all broker tiers.

#### Get Broker Tier Details

```
GET /api/broker-tiers/{id}/
```

Returns detailed information about a specific broker tier.

#### Create Broker Tier

```
POST /api/broker-tiers/
```

Creates a new broker tier.

#### Update Broker Tier

```
PUT /api/broker-tiers/{id}/
PATCH /api/broker-tiers/{id}/
```

Updates an existing broker tier.

#### Delete Broker Tier

```
DELETE /api/broker-tiers/{id}/
```

Deletes a broker tier.

### Broker Specialization Endpoints

#### List Broker Specializations

```
GET /api/broker-specializations/
```

Returns a list of all broker specializations.

#### Get Broker Specialization Details

```
GET /api/broker-specializations/{id}/
```

Returns detailed information about a specific broker specialization.

#### Create Broker Specialization

```
POST /api/broker-specializations/
```

Creates a new broker specialization.

#### Update Broker Specialization

```
PUT /api/broker-specializations/{id}/
PATCH /api/broker-specializations/{id}/
```

Updates an existing broker specialization.

#### Delete Broker Specialization

```
DELETE /api/broker-specializations/{id}/
```

Deletes a broker specialization.

### Broker Commission Endpoints

#### List Broker Commissions

```
GET /api/broker-commissions/
```

Returns a list of all broker commissions.

#### Get Broker Commission Details

```
GET /api/broker-commissions/{id}/
```

Returns detailed information about a specific broker commission.

#### Create Broker Commission

```
POST /api/broker-commissions/
```

Creates a new broker commission.

#### Update Broker Commission

```
PUT /api/broker-commissions/{id}/
PATCH /api/broker-commissions/{id}/
```

Updates an existing broker commission.

#### Delete Broker Commission

```
DELETE /api/broker-commissions/{id}/
```

Deletes a broker commission.

### Commission Payment Endpoints

#### List Commission Payments

```
GET /api/commission-payments/
```

Returns a list of all commission payments.

#### Get Commission Payment Details

```
GET /api/commission-payments/{id}/
```

Returns detailed information about a specific commission payment.

#### Create Commission Payment

```
POST /api/commission-payments/
```

Creates a new commission payment.

#### Update Commission Payment

```
PUT /api/commission-payments/{id}/
PATCH /api/commission-payments/{id}/
```

Updates an existing commission payment.

#### Delete Commission Payment

```
DELETE /api/commission-payments/{id}/
```

Deletes a commission payment.

## Filtering and Searching

### Broker Filtering

The Broker API supports filtering and searching:

- **Filter by fields**: `active`, `branch`, `bd`, `tier`, `specializations`
  - Example: `/api/brokers/?active=true&branch=uuid`

- **Search**: `name`, `email`, `company`, `license_number`
  - Example: `/api/brokers/?search=John`

- **Ordering**: `name`, `company`, `created_at`
  - Example: `/api/brokers/?ordering=-created_at`

### Broker Commission Filtering

- **Filter by fields**: `broker`, `status`, `payment_date`
  - Example: `/api/broker-commissions/?broker=uuid&status=PENDING`

- **Search**: `broker__name`, `application__reference_number`
  - Example: `/api/broker-commissions/?search=APP12345`

- **Ordering**: `created_at`, `amount`, `payment_date`
  - Example: `/api/broker-commissions/?ordering=-amount`

### Commission Payment Filtering

- **Filter by fields**: `broker`, `payment_date`, `payment_method`
  - Example: `/api/commission-payments/?broker=uuid&payment_method=BANK_TRANSFER`

- **Search**: `broker__name`, `reference_number`
  - Example: `/api/commission-payments/?search=PAY12345`

- **Ordering**: `payment_date`, `total_amount`
  - Example: `/api/commission-payments/?ordering=-payment_date`

## Example Usage

### JavaScript Example

```javascript
// Get all brokers
const getBrokers = async () => {
  const response = await fetch('/api/brokers/');
  return response.json();
};

// Get broker details
const getBrokerDetails = async (brokerId) => {
  const response = await fetch(`/api/brokers/${brokerId}/`);
  return response.json();
};

// Create a new broker
const createBroker = async (brokerData) => {
  const response = await fetch('/api/brokers/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(brokerData),
  });
  return response.json();
};

// Update a broker
const updateBroker = async (brokerId, brokerData) => {
  const response = await fetch(`/api/brokers/${brokerId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(brokerData),
  });
  return response.json();
};

// Delete a broker
const deleteBroker = async (brokerId) => {
  await fetch(`/api/brokers/${brokerId}/`, {
    method: 'DELETE',
  });
};

// Get brokers by branch
const getBrokersByBranch = async () => {
  const response = await fetch('/api/brokers/by-branch/');
  return response.json();
};

// Get brokers by BD
const getBrokersByBD = async () => {
  const response = await fetch('/api/brokers/by-bd/');
  return response.json();
};

// Get brokers by tier
const getBrokersByTier = async () => {
  const response = await fetch('/api/brokers/by-tier/');
  return response.json();
};
```
