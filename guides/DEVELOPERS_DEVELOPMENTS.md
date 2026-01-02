# Developer & Development Management

## Overview

The Sync Manager now includes dedicated database tables and API endpoints for managing **Developers** and **Developments** (real estate projects). These entities are optional but provide structured relationship management for properties.

## Database Schema

### Developer Table
Stores information about real estate developers/companies:

- `id` - Primary key
- `tenant_id` - Foreign key to tenant
- `name` - Developer company name (required)
- `description` - Developer description
- `website` - Developer website URL
- `logo_url` - Developer logo URL
- `contact_email` - Contact email
- `contact_phone` - Contact phone
- `metadata` - Additional JSON data
- `created_at` - Timestamp
- `updated_at` - Timestamp

### Development Table
Stores information about real estate developments/projects:

- `id` - Primary key
- `tenant_id` - Foreign key to tenant
- `developer_id` - Foreign key to developer (optional)
- `name` - Development/project name (required)
- `description` - Development description
- `location` - Full location string
- `city` - City
- `state` - State/Province
- `country` - Country
- `total_units` - Total number of units
- `available_units` - Available units
- `completion_date` - Expected completion date
- `images` - Array of image URLs (JSON)
- `website` - Development website URL
- `metadata` - Additional JSON data
- `created_at` - Timestamp
- `updated_at` - Timestamp

## Relationship with Properties

In the `StandardProperty` schema, you can now reference developers and developments:

### Using Foreign Keys (Recommended)
```python
{
  "external_id": "prop-001",
  "developer_id": 5,        # FK to developers table
  "development_id": 12,     # FK to developments table
  ...
}
```

### Using Legacy Fields (Backward Compatible)
```python
{
  "external_id": "prop-001",
  "developer_name": "Acme Development Corp",
  "development_name": "Sunset Villas Phase 2",
  ...
}
```

**Note**: The system supports both approaches. Use foreign keys when you have developers/developments in the database, or use name fields for simple string references.

## API Endpoints

All endpoints require authentication via `X-API-Key` header.

### Developer Endpoints

#### Create Developer
```http
POST /developers
Content-Type: application/json
X-API-Key: your-api-key

{
  "name": "Acme Development Corp",
  "description": "Leading real estate developer in Spain",
  "website": "https://acmedev.com",
  "logo_url": "https://acmedev.com/logo.png",
  "contact_email": "info@acmedev.com",
  "contact_phone": "+34 123 456 789",
  "metadata": {
    "founded": 2005,
    "employees": 150
  }
}
```

**Response:**
```json
{
  "id": 5,
  "name": "Acme Development Corp"
}
```

#### List Developers
```http
GET /developers
X-API-Key: your-api-key
```

**Response:**
```json
[
  {
    "id": 5,
    "name": "Acme Development Corp",
    "description": "Leading real estate developer in Spain",
    "website": "https://acmedev.com",
    "logo_url": "https://acmedev.com/logo.png",
    "contact_email": "info@acmedev.com",
    "contact_phone": "+34 123 456 789"
  }
]
```

#### Get Developer
```http
GET /developers/5
X-API-Key: your-api-key
```

**Response:**
```json
{
  "id": 5,
  "name": "Acme Development Corp",
  "description": "Leading real estate developer in Spain",
  "website": "https://acmedev.com",
  "logo_url": "https://acmedev.com/logo.png",
  "contact_email": "info@acmedev.com",
  "contact_phone": "+34 123 456 789",
  "metadata": {
    "founded": 2005,
    "employees": 150
  }
}
```

#### Update Developer
```http
PATCH /developers/5
Content-Type: application/json
X-API-Key: your-api-key

{
  "description": "Updated description",
  "contact_phone": "+34 987 654 321"
}
```

**Response:**
```json
{
  "status": "updated",
  "id": 5
}
```

#### Delete Developer
```http
DELETE /developers/5
X-API-Key: your-api-key
```

**Response:**
```json
{
  "status": "deleted"
}
```

### Development Endpoints

#### Create Development
```http
POST /developments
Content-Type: application/json
X-API-Key: your-api-key

{
  "name": "Sunset Villas Phase 2",
  "developer_id": 5,
  "description": "Luxury villas with sea views",
  "location": "Marbella, Málaga, Spain",
  "city": "Marbella",
  "state": "Málaga",
  "country": "Spain",
  "total_units": 50,
  "available_units": 12,
  "completion_date": "2025-06-30T00:00:00Z",
  "images": [
    "https://example.com/development1.jpg",
    "https://example.com/development2.jpg"
  ],
  "website": "https://sunsetvillas.com",
  "metadata": {
    "amenities": ["pool", "gym", "spa"],
    "phase": 2
  }
}
```

**Response:**
```json
{
  "id": 12,
  "name": "Sunset Villas Phase 2"
}
```

#### List Developments
```http
GET /developments
X-API-Key: your-api-key
```

**Optional query parameter:**
- `developer_id` - Filter by developer

**Response:**
```json
[
  {
    "id": 12,
    "name": "Sunset Villas Phase 2",
    "developer_id": 5,
    "description": "Luxury villas with sea views",
    "location": "Marbella, Málaga, Spain",
    "city": "Marbella",
    "state": "Málaga",
    "country": "Spain",
    "total_units": 50,
    "available_units": 12,
    "completion_date": "2025-06-30T00:00:00",
    "website": "https://sunsetvillas.com"
  }
]
```

#### Get Development
```http
GET /developments/12
X-API-Key: your-api-key
```

**Response:**
```json
{
  "id": 12,
  "name": "Sunset Villas Phase 2",
  "developer_id": 5,
  "description": "Luxury villas with sea views",
  "location": "Marbella, Málaga, Spain",
  "city": "Marbella",
  "state": "Málaga",
  "country": "Spain",
  "total_units": 50,
  "available_units": 12,
  "completion_date": "2025-06-30T00:00:00",
  "images": [
    "https://example.com/development1.jpg",
    "https://example.com/development2.jpg"
  ],
  "website": "https://sunsetvillas.com",
  "metadata": {
    "amenities": ["pool", "gym", "spa"],
    "phase": 2
  }
}
```

#### Update Development
```http
PATCH /developments/12
Content-Type: application/json
X-API-Key: your-api-key

{
  "available_units": 8,
  "description": "Updated description"
}
```

**Response:**
```json
{
  "status": "updated",
  "id": 12
}
```

#### Delete Development
```http
DELETE /developments/12
X-API-Key: your-api-key
```

**Response:**
```json
{
  "status": "deleted"
}
```

## Workflow Examples

### Example 1: Creating a Complete Development Project

1. **Create the developer:**
```bash
curl -X POST http://localhost:8000/developers \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Premium Estates Ltd",
    "website": "https://premiumestates.com",
    "contact_email": "info@premiumestates.com"
  }'
```

2. **Create the development:**
```bash
curl -X POST http://localhost:8000/developments \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ocean View Residences",
    "developer_id": 5,
    "city": "Alicante",
    "total_units": 30,
    "available_units": 30,
    "completion_date": "2026-12-31T00:00:00Z"
  }'
```

3. **Import properties with development reference:**
```bash
curl -X POST http://localhost:8000/sources/1/import \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "external_id": "unit-001",
        "development_id": 12,
        "title": {"en": "3BR Villa", "es": "Villa de 3 dormitorios"},
        "price": 450000,
        "currency": "EUR",
        "bedrooms": 3,
        "bathrooms": 2
      }
    ]
  }'
```

### Example 2: Querying Developments by Developer

```bash
curl -X GET "http://localhost:8000/developments?developer_id=5" \
  -H "X-API-Key: your-key"
```

This returns all developments created by developer ID 5.

## Benefits

1. **Structured Data**: Store developer and development information in dedicated tables with proper relationships
2. **Reusability**: Reference the same developer/development across multiple properties
3. **Consistency**: Maintain consistent developer/development data across all properties
4. **Flexibility**: Still supports legacy name-based fields for backward compatibility
5. **Queryability**: Easy to filter and query properties by developer or development

## Migration Notes

If you have existing properties with `developer_name` and `development_name`:

1. Create Developer and Development records via API
2. Note their IDs
3. Update properties to use `developer_id` and `development_id`
4. Optionally keep legacy name fields for reference

The system supports both approaches simultaneously, so you can migrate gradually.
