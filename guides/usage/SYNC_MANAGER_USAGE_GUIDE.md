# 📘 Sync Manager - Complete Usage Guide

## 🎯 What is Sync Manager?

Sync Manager is a **multi-tenant property synchronization system** that helps you:
- Keep property data synchronized between multiple sources and destinations
- Track changes automatically
- Maintain historical snapshots
- Detect and flag manual changes
- Provide API access to your data

## 🏗️ Core Concepts

### 1. **Tenant**
- A workspace for your organization
- Isolated data (multi-tenant architecture)
- Has its own API key for authentication
- Example: "YM Properties", "My Real Estate Company"

### 2. **Source**
- Where property data comes FROM
- Types:
  - **JSON**: Import from JSON files
  - **Scraped**: Data from web scraping
  - **Manual**: Manually entered data
  - **API**: From external APIs

### 3. **Target**
- Where property data goes TO
- Examples:
  - Your website
  - Your database
  - Another API
  - CMS system

### 4. **Properties**
- Individual property records
- Stored in sources and targets
- Have unique `external_id`
- Automatically tracked with hash for change detection

### 5. **Snapshots**
- Historical versions of properties
- Created before updates
- Retained for 30 days (configurable)
- Useful for rollback and audit

## 📋 Basic Workflow

```
┌─────────────┐
│   SOURCES   │  (Where data comes FROM)
│             │
│ • YM Website│  Scrape properties
│ • JSON Files│  Import bulk data
│ • Manual    │  Direct entry
└──────┬──────┘
       │
       ↓
┌─────────────┐
│SYNC MANAGER │  (Orchestration & Intelligence)
│             │
│ • Detects   │  Compares hashes
│   changes   │  Creates snapshots
│ • Tracks    │  Flags conflicts
│   history   │  Logs operations
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   TARGETS   │  (Where data goes TO)
│             │
│ • Website   │  Update live site
│ • Database  │  Sync to DB
│ • API       │  Send to other systems
└─────────────┘
```

## 🚀 Getting Started

### Step 1: Initialize Database

```bash
cd sync_manager_project
python -m sync_manager.cli init
```

This creates all database tables.

### Step 2: Create Your Tenant

```bash
python -m sync_manager.cli create-tenant "My Company"
```

**Save the API key!** You'll need it for API access.

Output:
```
✓ Tenant created successfully!
  ID: 1
  Name: My Company
  API Key: xyzabc123...
  
⚠️  Save this API key securely - it won't be shown again!
```

### Step 3: Start the API Server

```bash
uvicorn sync_manager.api:app --reload
```

Access interactive docs at: http://localhost:8000/docs

## 💼 Common Use Cases

### Use Case 1: Import Properties from JSON

**Scenario:** You have property data in a JSON file that you want to import.

**Steps:**

1. **Create a source:**
```bash
curl -X POST http://localhost:8000/sources \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Property Listings",
    "type": "json",
    "config": {}
  }'
```

2. **Prepare your JSON file** (`properties.json`):
```json
[
  {
    "id": "PROP001",
    "title": "Beautiful Villa",
    "price": 500000,
    "bedrooms": 4,
    "location": "Madrid"
  },
  {
    "id": "PROP002",
    "title": "City Apartment",
    "price": 250000,
    "bedrooms": 2,
    "location": "Barcelona"
  }
]
```

3. **Import the data:**
```bash
python -m sync_manager.cli import 1 1 properties.json
```

Where:
- `1` = tenant_id
- `1` = source_id
- `properties.json` = your file

**Result:**
```
✓ Import completed!
  Status: success
  Stats: {'created': 2, 'updated': 0}
```

### Use Case 2: Sync from Source to Target

**Scenario:** You want to sync imported properties to your website.

**Steps:**

1. **Create a target:**
```bash
curl -X POST http://localhost:8000/targets \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Website",
    "type": "website",
    "config": {
      "url": "https://mywebsite.com"
    }
  }'
```

2. **Sync source to target:**
```bash
python -m sync_manager.cli sync 1 1 1
```

Where:
- `1` = tenant_id
- `1` = source_id
- `1` = target_id

**Result:**
```
✓ Sync completed!
  Status: success
  Stats: {'created': 2, 'updated': 0, 'skipped': 0, 'warnings': 0}
```

### Use Case 3: Detect Manual Changes

**Scenario:** Someone manually edited a property on your website. Sync Manager will detect this.

**What happens:**

1. Property is synced from source → target (hash: `abc123`)
2. Someone manually edits the property on target (hash changes to `xyz789`)
3. Next sync detects hash mismatch
4. Property is flagged with `has_manual_changes: true`
5. Automatic sync is **skipped** to prevent overwriting
6. Warning is added to the property

**Check for warnings:**
```bash
curl http://localhost:8000/targets/1/properties \
  -H "X-API-Key: YOUR_API_KEY"
```

Response shows:
```json
{
  "id": 1,
  "external_id": "PROP001",
  "data": {...},
  "has_manual_changes": true,
  "warning": "Source has changes but target has manual modifications..."
}
```

### Use Case 4: Update Properties (Re-import)

**Scenario:** Your source data changed, and you want to update.

**Steps:**

1. **Update your JSON file:**
```json
[
  {
    "id": "PROP001",
    "title": "Beautiful Villa - UPDATED",
    "price": 520000,  // Price increased
    "bedrooms": 4,
    "location": "Madrid"
  }
]
```

2. **Re-import:**
```bash
python -m sync_manager.cli import 1 1 properties.json
```

**Result:**
```
✓ Import completed!
  Status: success
  Stats: {'created': 0, 'updated': 1}
```

3. **Sync to target:**
```bash
python -m sync_manager.cli sync 1 1 1
```

Sync Manager:
- ✅ Creates snapshot of old version
- ✅ Updates property with new data
- ✅ Updates hash
- ✅ Keeps history for 30 days

### Use Case 5: Daily Automated Sync

**Scenario:** You want to automatically sync every day.

**Create a script** (`daily_sync.py`):
```python
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"
API_KEY = "your_api_key_here"

def daily_sync():
    print(f"Starting daily sync - {datetime.now()}")
    
    # 1. Import latest data
    with open("latest_properties.json") as f:
        properties = json.load(f)
    
    response = requests.post(
        f"{API_URL}/sources/1/import",
        headers={"X-API-Key": API_KEY},
        json={"data": properties}
    )
    
    import_result = response.json()
    print(f"Import: {import_result['stats']}")
    
    # 2. Sync to website
    response = requests.post(
        f"{API_URL}/sync/1/1",
        headers={"X-API-Key": API_KEY}
    )
    
    sync_result = response.json()
    print(f"Sync: {sync_result['stats']}")
    
    # 3. Check for warnings
    if sync_result['stats']['warnings'] > 0:
        print(f"⚠️  WARNING: {sync_result['stats']['warnings']} properties have manual changes!")

if __name__ == "__main__":
    daily_sync()
```

**Schedule with Windows Task Scheduler:**
- Create task to run `python daily_sync.py` every day at 2 AM

### Use Case 6: Cleanup Old Snapshots

**Scenario:** Remove snapshots older than 30 days to save space.

```bash
python -m sync_manager.cli cleanup 1 --days 30
```

Or via API:
```bash
curl -X POST http://localhost:8000/cleanup?days=30 \
  -H "X-API-Key: YOUR_API_KEY"
```

## 🔧 CLI Commands Reference

```bash
# Initialize database
python -m sync_manager.cli init

# Create tenant
python -m sync_manager.cli create-tenant "Company Name"

# Import JSON to source
python -m sync_manager.cli import TENANT_ID SOURCE_ID file.json

# Sync source to target
python -m sync_manager.cli sync TENANT_ID SOURCE_ID TARGET_ID

# Cleanup snapshots
python -m sync_manager.cli cleanup TENANT_ID --days 30
```

## 🌐 API Endpoints Reference

### Authentication
All endpoints (except `/health` and `POST /tenants`) require:
```
Header: X-API-Key: your_api_key_here
```

### Core Endpoints

**Health Check:**
```bash
GET /health
```

**Create Tenant:**
```bash
POST /tenants
Body: {"name": "Company", "api_key": "generated_key"}
```

**Create Source:**
```bash
POST /sources
Body: {"name": "Source Name", "type": "json", "config": {}}
```

**Create Target:**
```bash
POST /targets
Body: {"name": "Target Name", "type": "website", "config": {}}
```

**List Sources:**
```bash
GET /sources
```

**List Targets:**
```bash
GET /targets
```

**Import Data to Source:**
```bash
POST /sources/{source_id}/import
Body: {"data": [{"id": "1", ...}, ...]}
```

**Sync Source to Target:**
```bash
POST /sync/{source_id}/{target_id}
```

**List Source Properties:**
```bash
GET /sources/{source_id}/properties
```

**List Target Properties:**
```bash
GET /targets/{target_id}/properties
```

**Update Target Property (PATCH):**
```bash
PATCH /targets/{target_id}/properties/{property_id}
Body: {"data": {"price": 300000}}
```
*Note: This marks the property as manually changed*

**Delete Source:**
```bash
DELETE /sources/{source_id}
```

**Delete Target:**
```bash
DELETE /targets/{target_id}
```

**Cleanup Snapshots:**
```bash
POST /cleanup?days=30
```

## 📊 Real-World Example: Real Estate Agency

### Scenario
You're a real estate agency that:
1. Scrapes properties from YM website daily
2. Maintains your own website with properties
3. Sometimes manually edits property details
4. Needs to keep both sites in sync

### Setup

**1. Create tenant:**
```bash
python -m sync_manager.cli create-tenant "My Real Estate Agency"
# Save API key: abc123xyz...
```

**2. Create sources:**
```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "abc123xyz..."

# YM scraped source
requests.post(f"{API_URL}/sources", 
    headers={"X-API-Key": API_KEY},
    json={"name": "YM Website", "type": "scraped", "config": {}})

# Manual entries source
requests.post(f"{API_URL}/sources",
    headers={"X-API-Key": API_KEY},
    json={"name": "Manual Entries", "type": "manual", "config": {}})
```

**3. Create target:**
```python
# Your website
requests.post(f"{API_URL}/targets",
    headers={"X-API-Key": API_KEY},
    json={"name": "My Website", "type": "website", 
          "config": {"url": "https://myrealestate.com"}})
```

**4. Daily workflow script:**
```python
import requests
import json
from ym_scraper import scrape_ym_properties  # Your existing scraper

def daily_workflow():
    # 1. Scrape YM
    print("Scraping YM...")
    ym_properties = scrape_ym_properties()
    
    # 2. Import to Sync Manager
    print("Importing to Sync Manager...")
    requests.post(
        f"{API_URL}/sources/1/import",
        headers={"X-API-Key": API_KEY},
        json={"data": ym_properties}
    )
    
    # 3. Sync to your website
    print("Syncing to website...")
    result = requests.post(
        f"{API_URL}/sync/1/1",
        headers={"X-API-Key": API_KEY}
    ).json()
    
    # 4. Report
    print(f"Created: {result['stats']['created']}")
    print(f"Updated: {result['stats']['updated']}")
    print(f"Warnings: {result['stats']['warnings']}")
    
    # 5. Handle warnings
    if result['stats']['warnings'] > 0:
        send_email_alert("Manual changes detected!")

daily_workflow()
```

**5. Schedule it:**
- Windows Task Scheduler: Run `python daily_workflow.py` at 3 AM daily

## 🎨 Advanced Usage

### Multiple Sources → One Target

```python
# Sync from multiple sources to one target
requests.post(f"{API_URL}/sync/1/1")  # YM → Website
requests.post(f"{API_URL}/sync/2/1")  # Manual → Website
```

### One Source → Multiple Targets

```python
# Sync one source to multiple targets
requests.post(f"{API_URL}/sync/1/1")  # Source → Website
requests.post(f"{API_URL}/sync/1/2")  # Source → Database
requests.post(f"{API_URL}/sync/1/3")  # Source → API
```

### Conditional Sync

```python
def smart_sync():
    # Get source properties
    source_props = requests.get(
        f"{API_URL}/sources/1/properties",
        headers={"X-API-Key": API_KEY}
    ).json()
    
    # Only sync if more than 100 properties
    if len(source_props) > 100:
        requests.post(f"{API_URL}/sync/1/1",
            headers={"X-API-Key": API_KEY})
        print("Synced!")
    else:
        print("Not enough properties, skipped sync")
```

## 🔍 Monitoring & Debugging

### Check What's In Your System

```bash
# List all sources
curl http://localhost:8000/sources -H "X-API-Key: YOUR_KEY"

# List all targets
curl http://localhost:8000/targets -H "X-API-Key: YOUR_KEY"

# Check properties in source
curl http://localhost:8000/sources/1/properties -H "X-API-Key: YOUR_KEY"

# Check properties in target (with warnings)
curl http://localhost:8000/targets/1/properties -H "X-API-Key: YOUR_KEY"
```

### View API Docs

Go to: http://localhost:8000/docs

Interactive Swagger UI where you can:
- See all endpoints
- Test API calls
- View request/response schemas

## 🎯 Best Practices

1. **Always save API keys** - They're shown only once during tenant creation

2. **Use descriptive names** - Name sources and targets clearly:
   - ✅ "YM Website - Properties"
   - ❌ "Source 1"

3. **Handle manual changes** - Check for warnings regularly:
   ```python
   if sync_result['stats']['warnings'] > 0:
       # Alert someone to review manual changes
   ```

4. **Regular cleanup** - Run cleanup monthly:
   ```bash
   python -m sync_manager.cli cleanup 1 --days 30
   ```

5. **Use snapshots for rollback** - Keep 30+ days for safety

6. **Test sync on staging first** - Create separate tenant for testing

7. **Monitor sync logs** - Check stats after each sync

## 🆘 Troubleshooting

**Import returns 0 created/updated:**
- Check JSON format - must have `id` or `external_id` field
- Verify data is a list: `[{...}, {...}]` not just `{...}`

**Sync creates duplicates:**
- Ensure `external_id` is consistent between imports
- Use same ID format each time

**Manual changes not detected:**
- Verify property was synced at least once from source
- Check that `source_property_id` is set

**API returns 401:**
- Check API key is correct
- Verify `X-API-Key` header format

**Database connection errors:**
- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env` is correct

## 📚 Summary

Sync Manager is your **central hub** for property data synchronization:

1. **Import** data from various sources (JSON, scraping, manual)
2. **Sync** to multiple targets (website, database, APIs)
3. **Track** all changes automatically with snapshots
4. **Detect** manual modifications and prevent overwriting
5. **Access** everything via REST API or CLI

**Start simple:**
- Create tenant
- Create 1 source
- Create 1 target  
- Import data
- Sync

**Then expand:**
- Add more sources
- Add more targets
- Automate with scripts
- Monitor with API

Need help? Check:
- API docs: http://localhost:8000/docs
- IMPLEMENTATION.md for technical details
- QUICKSTART.md for quick reference
