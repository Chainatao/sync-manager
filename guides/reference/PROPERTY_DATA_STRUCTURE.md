# 🏠 Property Data Structure for Sync Manager

## 📋 Quick Answer

**Sync Manager is structure-agnostic!** It accepts **any JSON structure** you want.

The only requirement: **Each property must have a unique identifier** called `id` or `external_id`.

## 🎯 Required Fields

```json
{
  "id": "UNIQUE_IDENTIFIER"     // REQUIRED: String or number
  // ... any other fields you want ...
}
```

OR

```json
{
  "external_id": "UNIQUE_IDENTIFIER"   // Alternative field name
  // ... any other fields you want ...
}
```

## 📊 How It Works

### Data Storage Model

```
┌──────────────────────────────────────────────┐
│ Property Record in Sync Manager              │
├──────────────────────────────────────────────┤
│                                              │
│  id: 123                   (Database PK)     │
│  external_id: "PROP001"    (Your unique ID)  │
│  data: { ... }             (JSON BLOB)       │
│  hash: "abc123..."         (Auto-computed)   │
│  created_at: 2024-01-01                      │
│  updated_at: 2024-01-02                      │
│                                              │
└──────────────────────────────────────────────┘
```

**The `data` field stores your ENTIRE property as JSON!**

Everything goes in `data` - Sync Manager doesn't care about the structure.

## 🏗️ Real Estate Property Examples

### Example 1: Minimal Structure

```json
[
  {
    "id": "PROP001",
    "title": "Beautiful Villa",
    "price": 500000
  },
  {
    "id": "PROP002",
    "title": "City Apartment",
    "price": 250000
  }
]
```

### Example 2: Basic Real Estate

```json
[
  {
    "id": "PROP001",
    "title": "Luxury Villa in Madrid",
    "description": "Beautiful villa with pool and garden",
    "price": 850000,
    "currency": "EUR",
    "bedrooms": 5,
    "bathrooms": 3,
    "area": 350,
    "area_unit": "sqm",
    "location": {
      "city": "Madrid",
      "district": "Salamanca",
      "address": "Calle Serrano 123"
    },
    "type": "villa",
    "status": "available"
  },
  {
    "id": "PROP002",
    "title": "Modern Apartment in Barcelona",
    "description": "City center apartment with sea views",
    "price": 450000,
    "currency": "EUR",
    "bedrooms": 2,
    "bathrooms": 2,
    "area": 95,
    "area_unit": "sqm",
    "location": {
      "city": "Barcelona",
      "district": "Eixample",
      "address": "Passeig de Gracia 45"
    },
    "type": "apartment",
    "status": "available"
  }
]
```

### Example 3: Comprehensive Structure (Recommended)

```json
[
  {
    "id": "PROP001",
    "external_ref": "YM-12345",
    "listing_info": {
      "title": "Luxury Villa with Private Pool",
      "description": "Stunning 5-bedroom villa located in prime Madrid location...",
      "short_description": "5 bed villa with pool",
      "status": "available",
      "listing_type": "sale",
      "featured": true,
      "published": true,
      "published_date": "2024-01-15"
    },
    "pricing": {
      "price": 850000,
      "currency": "EUR",
      "price_per_sqm": 2428,
      "negotiable": true,
      "reduced": false,
      "previous_price": null
    },
    "property_details": {
      "type": "villa",
      "subtype": "detached",
      "bedrooms": 5,
      "bathrooms": 3,
      "half_bathrooms": 1,
      "living_rooms": 2,
      "kitchens": 1,
      "parking_spaces": 2,
      "garage": true,
      "floors": 2,
      "year_built": 2018,
      "condition": "excellent"
    },
    "area": {
      "total": 350,
      "built": 320,
      "plot": 500,
      "unit": "sqm",
      "interior": 280,
      "terrace": 40
    },
    "location": {
      "country": "Spain",
      "region": "Madrid",
      "city": "Madrid",
      "district": "Salamanca",
      "neighborhood": "Recoletos",
      "address": "Calle Serrano 123",
      "postal_code": "28006",
      "latitude": 40.4168,
      "longitude": -3.7038,
      "zone": "A"
    },
    "features": {
      "amenities": [
        "swimming_pool",
        "garden",
        "terrace",
        "balcony",
        "elevator",
        "storage_room",
        "air_conditioning",
        "heating",
        "fireplace",
        "alarm",
        "video_intercom"
      ],
      "orientation": "south",
      "views": ["garden", "mountains"],
      "natural_light": "excellent",
      "accessibility": false,
      "pets_allowed": true,
      "furnished": false
    },
    "energy": {
      "rating": "B",
      "consumption": 45.2,
      "emissions": 12.3,
      "certificate_number": "ENG-123456"
    },
    "media": {
      "images": [
        {
          "url": "https://example.com/images/prop001_01.jpg",
          "title": "Main view",
          "order": 1
        },
        {
          "url": "https://example.com/images/prop001_02.jpg",
          "title": "Living room",
          "order": 2
        }
      ],
      "videos": [
        {
          "url": "https://youtube.com/watch?v=abc123",
          "type": "youtube",
          "title": "Property tour"
        }
      ],
      "virtual_tour": "https://matterport.com/show/?m=abc123",
      "floor_plan": "https://example.com/floorplans/prop001.pdf"
    },
    "contact": {
      "agent_name": "María García",
      "agent_phone": "+34 600 123 456",
      "agent_email": "maria@agency.com",
      "agency": "Premium Real Estate",
      "agency_id": "AGC001"
    },
    "dates": {
      "created": "2024-01-15T10:00:00Z",
      "updated": "2024-01-20T15:30:00Z",
      "available_from": "2024-02-01"
    },
    "metadata": {
      "source": "ym_website",
      "internal_notes": "Client prefers viewings on weekends",
      "tags": ["luxury", "new", "pool"],
      "custom_fields": {
        "ibi_tax": 1200,
        "community_fees": 150
      }
    }
  }
]
```

### Example 4: Rental Property

```json
{
  "id": "RENT001",
  "title": "3 Bedroom Apartment for Rent",
  "type": "apartment",
  "listing_type": "rent",
  "bedrooms": 3,
  "bathrooms": 2,
  "area": 120,
  "location": {
    "city": "Valencia",
    "district": "Ruzafa"
  },
  "rental_info": {
    "monthly_rent": 1200,
    "currency": "EUR",
    "deposit": 2400,
    "agency_fee": 1200,
    "utilities_included": false,
    "min_rental_period": 12,
    "max_rental_period": null,
    "available_from": "2024-03-01"
  },
  "requirements": {
    "min_income": 3600,
    "guarantor_required": true,
    "pets_allowed": false,
    "smoking_allowed": false
  }
}
```

### Example 5: Commercial Property

```json
{
  "id": "COM001",
  "title": "Commercial Space in Shopping Center",
  "type": "commercial",
  "subtype": "retail",
  "area": 85,
  "location": {
    "city": "Madrid",
    "shopping_center": "Centro Comercial ABC"
  },
  "commercial_info": {
    "business_type": "retail_shop",
    "transfer_fee": 25000,
    "monthly_rent": 2500,
    "smoke_outlet": false,
    "display_window": true,
    "corner_location": false,
    "foot_traffic": "high"
  },
  "licenses": ["retail", "food_service"],
  "opening_hours": {
    "monday_friday": "10:00-21:00",
    "saturday": "10:00-22:00",
    "sunday": "Closed"
  }
}
```

## 🔧 How Sync Manager Processes Your Data

### Step 1: Import

When you import this JSON:
```json
{
  "id": "PROP001",
  "title": "Villa",
  "price": 500000,
  "bedrooms": 4
}
```

Sync Manager stores it as:
```python
SourceProperty(
    external_id="PROP001",
    data={
        "id": "PROP001",
        "title": "Villa",
        "price": 500000,
        "bedrooms": 4
    },
    hash="computed_hash_of_entire_data"
)
```

### Step 2: Sync

When syncing, Sync Manager:
1. Gets source property data
2. Computes hash of the entire JSON
3. Compares with target property hash
4. If different → updates target with new data

### Step 3: Retrieval

When you query the API:
```bash
GET /targets/1/properties
```

You get back:
```json
[
  {
    "id": 1,
    "external_id": "PROP001",
    "data": {
      "id": "PROP001",
      "title": "Villa",
      "price": 500000,
      "bedrooms": 4
    },
    "has_manual_changes": false,
    "warning": null
  }
]
```

The `data` field contains your original structure!

## 📝 Recommended Structure for YM Properties

Based on typical real estate websites, here's what I recommend:

```json
{
  "id": "string",                    // REQUIRED - Your unique ID
  
  // Basic Info (Recommended)
  "title": "string",
  "description": "string",
  "type": "villa|apartment|house|commercial",
  "status": "available|reserved|sold|rented",
  "listing_type": "sale|rent|transfer",
  
  // Pricing (Recommended)
  "price": number,
  "currency": "EUR|USD",
  
  // Property Details (Recommended)
  "bedrooms": number,
  "bathrooms": number,
  "area": number,
  "area_unit": "sqm|sqft",
  
  // Location (Recommended)
  "location": {
    "city": "string",
    "district": "string",
    "address": "string"
  },
  
  // Optional but Useful
  "images": ["url1", "url2"],
  "features": ["pool", "garden", "parking"],
  "contact": {
    "agent": "string",
    "phone": "string",
    "email": "string"
  },
  
  // Metadata (Optional)
  "source": "ym_website",
  "scraped_at": "2024-01-15T10:00:00Z",
  "url": "https://ym.com/property/123"
}
```

## 🎨 Import Examples

### Import from Python Script

```python
import requests
import json

properties = [
    {
        "id": "PROP001",
        "title": "Beautiful Villa",
        "price": 850000,
        "bedrooms": 5,
        "location": {"city": "Madrid"}
    },
    {
        "id": "PROP002",
        "title": "Modern Apartment",
        "price": 450000,
        "bedrooms": 2,
        "location": {"city": "Barcelona"}
    }
]

response = requests.post(
    "http://localhost:8000/sources/1/import",
    headers={"X-API-Key": "YOUR_KEY"},
    json={"data": properties}
)

print(response.json())
# Output: {"status": "success", "stats": {"created": 2, "updated": 0}}
```

### Import from JSON File

```bash
# properties.json
[
  {
    "id": "PROP001",
    "title": "Villa",
    "price": 850000
  }
]

# Import via CLI
python -m sync_manager.cli import 1 1 properties.json
```

### Import from YM Scraper

```python
# ym_scraper.py
from bs4 import BeautifulSoup
import requests

def scrape_ym_properties():
    properties = []
    
    # Scrape YM website
    response = requests.get("https://ym-website.com/properties")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for prop_div in soup.find_all('div', class_='property'):
        property_data = {
            "id": prop_div.get('data-id'),
            "title": prop_div.find('h2').text,
            "price": int(prop_div.find('span', class_='price').text.replace('€', '').replace(',', '')),
            "bedrooms": int(prop_div.find('span', class_='beds').text),
            "location": {
                "city": prop_div.find('span', class_='city').text
            },
            "url": prop_div.find('a')['href'],
            "scraped_at": datetime.now().isoformat()
        }
        properties.append(property_data)
    
    return properties

# Use with Sync Manager
properties = scrape_ym_properties()

requests.post(
    "http://localhost:8000/sources/1/import",
    headers={"X-API-Key": "YOUR_KEY"},
    json={"data": properties}
)
```

## ⚠️ Important Notes

### 1. ID Field is Critical

```python
# ✅ CORRECT - Has unique ID
{"id": "PROP001", "title": "Villa"}

# ✅ CORRECT - Alternative field name
{"external_id": "PROP001", "title": "Villa"}

# ❌ WRONG - No ID field
{"title": "Villa", "price": 500000}

# ❌ WRONG - Null ID
{"id": null, "title": "Villa"}
```

### 2. IDs Must Be Consistent

```python
# First import
{"id": "PROP001", "title": "Villa", "price": 500000}

# Update (same ID)
{"id": "PROP001", "title": "Villa", "price": 520000}  # ✅ Updates existing

# Different ID format
{"id": "001", "title": "Villa", "price": 520000}  # ❌ Creates new property!
```

### 3. Entire Object is Hashed

When you update ANY field, Sync Manager detects it:

```python
# Original
{"id": "PROP001", "title": "Villa", "price": 500000}

# Change price
{"id": "PROP001", "title": "Villa", "price": 520000}
# Hash changes → Sync Manager creates snapshot and updates

# Change anything
{"id": "PROP001", "title": "Luxury Villa", "price": 500000}
# Hash changes → Detected as update
```

### 4. Nested Structures Work

```python
# Completely fine
{
  "id": "PROP001",
  "location": {
    "coordinates": {
      "lat": 40.4168,
      "lng": -3.7038,
      "precision": "exact"
    },
    "nearby": {
      "metro": ["Sol", "Gran Via"],
      "schools": [
        {"name": "School A", "distance": 200},
        {"name": "School B", "distance": 500}
      ]
    }
  }
}
```

## 🚀 Best Practices

### 1. Always Include Core Fields

```json
{
  "id": "required",
  "title": "recommended",
  "type": "recommended",
  "price": "recommended",
  "location": "recommended"
}
```

### 2. Keep Structure Consistent

Don't change field names between imports:
```python
# Import 1
{"id": "PROP001", "bedrooms": 5}

# Import 2 - Different field name
{"id": "PROP001", "bedroom_count": 5}  # ❌ Treated as different data
```

### 3. Store Source Information

```json
{
  "id": "PROP001",
  "title": "Villa",
  "metadata": {
    "source": "ym_website",
    "source_url": "https://ym.com/property/123",
    "scraped_at": "2024-01-15T10:00:00Z",
    "scraper_version": "1.0"
  }
}
```

### 4. Use ISO Dates

```json
{
  "created_at": "2024-01-15T10:00:00Z",     // ✅ ISO format
  "updated_at": "2024-01-15 10:00:00"       // ⚠️ Works but not ideal
}
```

## 📚 Summary

**Key Points:**
1. ✅ Sync Manager accepts **any JSON structure**
2. ✅ Only requirement: unique `id` or `external_id` field
3. ✅ Everything goes in the `data` field (JSON blob)
4. ✅ Hash computed from entire JSON for change detection
5. ✅ Nested structures fully supported
6. ✅ Keep field names consistent between imports

**Your Structure = Your Choice!**

Just ensure each property has a unique identifier, and Sync Manager handles the rest.
