# Quick Start Guide - Sync Manager

## 🚀 Get Started in 5 Minutes

### Step 1: Run Setup (30 seconds)
```bash
python setup_sync_manager.py
```

### Step 2: Install Dependencies (2 minutes)
```bash
uv sync
```

### Step 3: Configure Database (1 minute)
```bash
cd website_tools\sync_manager
copy .env.example .env
```

Edit `.env` and set your PostgreSQL URL:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/sync_manager
RETENTION_DAYS=30
```

### Step 4: Initialize Database (10 seconds)
```bash
python -m website_tools.sync_manager.cli init
```

### Step 5: Create Your Tenant (10 seconds)
```bash
python -m website_tools.sync_manager.cli create-tenant "My Company"
```

**IMPORTANT**: Save the API key that is displayed!

### Step 6: Start API Server (10 seconds)
```bash
uvicorn website_tools.sync_manager.api:app --reload
```

Visit: http://localhost:8000/docs for interactive API documentation

## 🎯 First Data Flow

### 1. Create a Source
```bash
curl -X POST http://localhost:8000/sources \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Scraped Data\", \"type\": \"scraped\"}"
```

### 2. Create a Target
```bash
curl -X POST http://localhost:8000/targets \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Website\", \"type\": \"website\"}"
```

### 3. Import JSON Data
Create a file `sample_properties.json`:
```json
[
  {
    "id": "prop001",
    "title": "Beautiful Villa",
    "price": 250000,
    "location": "Costa Blanca"
  },
  {
    "id": "prop002",
    "title": "Modern Apartment",
    "price": 150000,
    "location": "Alicante"
  }
]
```

Import it:
```bash
python -m website_tools.sync_manager.cli import 1 1 sample_properties.json
```

### 4. Sync to Target
```bash
python -m website_tools.sync_manager.cli sync 1 1 2
```

### 5. View Results
```bash
# List source properties
curl http://localhost:8000/sources/1/properties \
  -H "X-API-Key: YOUR_API_KEY_HERE"

# List target properties
curl http://localhost:8000/targets/2/properties \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

## 📊 Dashboard Preview

Once running, visit these URLs:

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Alternative Docs**: http://localhost:8000/redoc

## 🔧 Common Operations

### Import New Data
```bash
python -m website_tools.sync_manager.cli import <tenant_id> <source_id> data.json
```

### Sync Changes
```bash
python -m website_tools.sync_manager.cli sync <tenant_id> <source_id> <target_id>
```

### Cleanup Old Snapshots
```bash
python -m website_tools.sync_manager.cli cleanup <tenant_id> --days 30
```

### Update a Target Property Manually
```bash
curl -X PATCH http://localhost:8000/targets/2/properties/1 \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {\"price\": 240000}}"
```

## 🔄 Integration Example

```python
from website_tools.sync_manager.sync_service import SyncService

# Initialize service
sync_service = SyncService(tenant_id=1)

# Import scraped data
properties = [
    {"id": "p1", "title": "Property 1", "price": 100000},
    {"id": "p2", "title": "Property 2", "price": 200000}
]
result = sync_service.import_json_to_source(source_id=1, data=properties)
print(f"Imported: {result['stats']}")

# Sync to target
sync_result = sync_service.sync_source_to_target(source_id=1, target_id=2)
print(f"Synced: {sync_result['stats']}")
```

## 🕐 Schedule Automated Tasks

### Windows Task Scheduler
Create a batch file `sync_daily.bat`:
```batch
@echo off
cd C:\path\to\project
python -m website_tools.sync_manager.cli sync 1 1 2
python -m website_tools.sync_manager.cli cleanup 1 --days 30
```

Schedule it to run daily.

### Linux Cron
```cron
# Daily sync at 2 AM
0 2 * * * cd /path/to/project && python -m website_tools.sync_manager.cli sync 1 1 2

# Weekly cleanup on Sunday at 3 AM
0 3 * * 0 cd /path/to/project && python -m website_tools.sync_manager.cli cleanup 1 --days 30
```

## ❓ Troubleshooting

### Database Connection Error
- Check `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running
- Verify credentials

### API Key Invalid
- Check `X-API-Key` header spelling
- Use the exact key from tenant creation
- Keys are case-sensitive

### Import Not Working
- Verify JSON format (array of objects)
- Each object needs `id` or `external_id` field
- Check source_id exists

### Manual Changes Warning
- Target property was modified manually
- Source has new changes but sync is blocked
- Either accept source changes or keep manual changes

## 📚 Full Documentation

See `IMPLEMENTATION.md` for complete documentation.

## 🎉 You're Ready!

Your Sync Manager is now set up and running. Start integrating your data sources!
