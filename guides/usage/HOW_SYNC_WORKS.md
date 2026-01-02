# 🔄 How Sync Manager Synchronization Works

## ❓ The Key Question: How Does It Know Where to Sync?

### Current Implementation (Out of the Box)

**The truth:** Sync Manager currently **manages sync logic internally** - it doesn't automatically push to external systems like your website or database.

## 📊 What Actually Happens

### When You Run: `sync 1 1 1` (tenant_id, source_id, target_id)

```
┌─────────────────────────────────────────────────────────────────┐
│ WHAT SYNC MANAGER DOES:                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Gets properties from SOURCE                                 │
│     └─> Reads from source_properties table                     │
│                                                                 │
│  2. Compares with TARGET                                        │
│     └─> Reads from target_properties table                     │
│                                                                 │
│  3. Detects changes via hash comparison                         │
│     └─> Compare property.hash values                           │
│                                                                 │
│  4. Updates TARGET_PROPERTIES table in Sync Manager database    │
│     └─> Creates/updates records in target_properties           │
│                                                                 │
│  5. Creates snapshots for audit trail                           │
│     └─> Saves to target_snapshots table                        │
│                                                                 │
│  ❌ DOES NOT: Actually push to your website/external system    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🏗️ The Database Structure

```
PostgreSQL Database: sync_manager
│
├── tenants                    (Your organizations)
│
├── sources                    (Data origins)
│   └── source_properties      (Properties IN sources)
│
├── targets                    (Data destinations)
│   └── target_properties      (Properties IN targets - INTERNAL!)
│
├── source_snapshots           (History)
├── target_snapshots           (History)
└── sync_logs                  (Audit trail)
```

### Key Point:
**`target_properties` is just a table in Sync Manager's database!**

It's not connected to your actual website or external system.

## 🎯 Two Ways to Use Sync Manager

### Option A: Central State Manager (Current Design)

Sync Manager as your **single source of truth**:

```
Your Scraper → Import to Source → Sync to Target (internal) → Your App Reads from Sync Manager
```

**Your application queries Sync Manager's API:**

```python
# Your website/app reads from Sync Manager
import requests

response = requests.get(
    "http://localhost:8000/targets/1/properties",
    headers={"X-API-Key": "YOUR_KEY"}
)

properties = response.json()

# Display properties on your website
for prop in properties:
    display_property(prop['data'])
```

**Advantages:**
- ✅ Sync Manager handles all change detection
- ✅ Automatic history tracking
- ✅ Manual change warnings
- ✅ Single API to query

**Disadvantages:**
- ❌ Your app must query Sync Manager
- ❌ Extra dependency
- ❌ Not standalone

---

### Option B: Active Push System (Requires Custom Code)

Extend Sync Manager to **actively push** to external systems:

```
Source → Sync Manager detects changes → Pushes to Your Website/DB
```

**You need to implement "Target Adapters":**

```python
# custom_target_adapters.py

class TargetAdapter:
    """Base adapter for pushing to external systems"""
    def push_properties(self, properties):
        raise NotImplementedError


class WebsiteAdapter(TargetAdapter):
    """Pushes to your website API"""
    def __init__(self, config):
        self.api_url = config.get('url')
        self.api_key = config.get('api_key')
    
    def push_properties(self, properties):
        for prop in properties:
            response = requests.post(
                f"{self.api_url}/api/properties",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=prop['data']
            )
            print(f"Pushed {prop['external_id']}: {response.status_code}")


class DatabaseAdapter(TargetAdapter):
    """Pushes directly to your database"""
    def __init__(self, config):
        self.conn_string = config.get('connection')
        self.engine = create_engine(self.conn_string)
    
    def push_properties(self, properties):
        with self.engine.connect() as conn:
            for prop in properties:
                conn.execute(
                    text("INSERT INTO properties VALUES (:id, :data) ON CONFLICT (id) DO UPDATE SET data = :data"),
                    {"id": prop['external_id'], "data": json.dumps(prop['data'])}
                )


class FTPAdapter(TargetAdapter):
    """Pushes files via FTP"""
    def __init__(self, config):
        self.host = config.get('host')
        self.username = config.get('username')
        self.password = config.get('password')
    
    def push_properties(self, properties):
        with FTP(self.host) as ftp:
            ftp.login(self.username, self.password)
            # Upload JSON file
            data = json.dumps(properties)
            ftp.storbinary('STOR properties.json', io.BytesIO(data.encode()))


# Adapter factory
ADAPTERS = {
    'website': WebsiteAdapter,
    'database': DatabaseAdapter,
    'ftp': FTPAdapter,
}

def get_adapter(target):
    """Get adapter based on target type"""
    adapter_class = ADAPTERS.get(target.type)
    if not adapter_class:
        raise ValueError(f"No adapter for target type: {target.type}")
    return adapter_class(target.config)
```

**Then modify sync_service.py:**

```python
# Modified sync_source_to_target method

def sync_source_to_target(self, source_id: int, target_id: int) -> Dict[str, Any]:
    """Synchronize properties from source to target"""
    with get_db() as db:
        source = db.query(Source).filter(...).first()
        target = db.query(Target).filter(...).first()
        
        # ... existing sync logic ...
        
        # NEW: Get properties that changed
        changed_properties = []
        
        for src_prop in source_properties:
            target_prop = db.query(TargetProperty).filter(...).first()
            
            if target_prop:
                if target_prop.hash != src_prop.hash:
                    # Update
                    target_prop.data = src_prop.data
                    changed_properties.append(target_prop)
                    stats["updated"] += 1
            else:
                # Create
                new_target_prop = TargetProperty(...)
                db.add(new_target_prop)
                changed_properties.append(new_target_prop)
                stats["created"] += 1
        
        # NEW: Push to external system
        from custom_target_adapters import get_adapter
        
        try:
            adapter = get_adapter(target)
            adapter.push_properties([
                {
                    'external_id': p.external_id,
                    'data': p.data
                }
                for p in changed_properties
            ])
            print(f"✓ Pushed {len(changed_properties)} properties to {target.name}")
        except Exception as e:
            print(f"✗ Failed to push to {target.name}: {e}")
            # Continue anyway - data is still synced in Sync Manager
        
        return {"status": "success", "stats": stats}
```

## 📝 Practical Examples

### Example 1: Query Sync Manager from Your Website

**Your Flask/FastAPI website:**

```python
from flask import Flask, render_template
import requests

app = Flask(__name__)

SYNC_MANAGER_API = "http://localhost:8000"
API_KEY = "your_api_key"

@app.route('/properties')
def list_properties():
    # Get properties from Sync Manager
    response = requests.get(
        f"{SYNC_MANAGER_API}/targets/1/properties",
        headers={"X-API-Key": API_KEY}
    )
    
    properties = response.json()
    return render_template('properties.html', properties=properties)

@app.route('/property/<property_id>')
def show_property(property_id):
    # Get single property
    response = requests.get(
        f"{SYNC_MANAGER_API}/targets/1/properties",
        headers={"X-API-Key": API_KEY}
    )
    
    properties = response.json()
    property = next(p for p in properties if p['external_id'] == property_id)
    return render_template('property.html', property=property)
```

### Example 2: Push to Your Website After Sync

**Custom sync script:**

```python
import requests

SYNC_MANAGER = "http://localhost:8000"
YOUR_WEBSITE = "https://your-website.com"
SYNC_API_KEY = "sync_manager_key"
WEBSITE_API_KEY = "your_website_key"

def sync_and_push():
    # 1. Sync in Sync Manager
    response = requests.post(
        f"{SYNC_MANAGER}/sync/1/1",
        headers={"X-API-Key": SYNC_API_KEY}
    )
    
    result = response.json()
    print(f"Synced: {result['stats']}")
    
    # 2. Get updated properties
    response = requests.get(
        f"{SYNC_MANAGER}/targets/1/properties",
        headers={"X-API-Key": SYNC_API_KEY}
    )
    
    properties = response.json()
    
    # 3. Push to your website
    for prop in properties:
        response = requests.post(
            f"{YOUR_WEBSITE}/api/properties",
            headers={"Authorization": f"Bearer {WEBSITE_API_KEY}"},
            json={
                "id": prop['external_id'],
                **prop['data']
            }
        )
        
        if response.status_code == 200:
            print(f"✓ Pushed {prop['external_id']}")
        else:
            print(f"✗ Failed to push {prop['external_id']}: {response.text}")

sync_and_push()
```

### Example 3: Export to File System

**Export properties to files:**

```python
import json
import requests
from pathlib import Path

def export_to_files():
    # Get properties from Sync Manager
    response = requests.get(
        "http://localhost:8000/targets/1/properties",
        headers={"X-API-Key": "YOUR_KEY"}
    )
    
    properties = response.json()
    
    # Export to individual JSON files
    output_dir = Path("exported_properties")
    output_dir.mkdir(exist_ok=True)
    
    for prop in properties:
        file_path = output_dir / f"{prop['external_id']}.json"
        file_path.write_text(json.dumps(prop['data'], indent=2))
        print(f"✓ Exported {prop['external_id']}")
    
    # Also create a combined file
    (output_dir / "all_properties.json").write_text(
        json.dumps([p['data'] for p in properties], indent=2)
    )
    
    print(f"\n✓ Exported {len(properties)} properties to {output_dir}")

export_to_files()
```

## 🎨 Which Approach Should You Use?

### Use Option A (Query Sync Manager) If:
- ✅ Building a new application
- ✅ Want Sync Manager as single source of truth
- ✅ Need built-in history and tracking
- ✅ Comfortable with API dependency

### Use Option B (Custom Push) If:
- ✅ Have existing website/system
- ✅ Can't change how your website works
- ✅ Need to push to multiple systems
- ✅ Want traditional "push" behavior

### Hybrid Approach:
- Use Sync Manager for tracking and history
- Query it for read operations
- Implement custom push for critical updates

## 🔧 Recommendation for Your YM Workflow

Based on your situation, I recommend:

**Phase 1: Start Simple (Query Mode)**
```python
# daily_workflow.py

# 1. Scrape YM
ym_properties = scrape_ym()

# 2. Import to Sync Manager
requests.post(f"{SYNC_API}/sources/1/import",
    headers={"X-API-Key": KEY},
    json={"data": ym_properties})

# 3. Sync internally
requests.post(f"{SYNC_API}/sync/1/1",
    headers={"X-API-Key": KEY})

# 4. Get synced data
properties = requests.get(f"{SYNC_API}/targets/1/properties",
    headers={"X-API-Key": KEY}).json()

# 5. Update your website
for prop in properties:
    update_website(prop)
```

**Phase 2: Add Custom Adapter (Later)**

Once comfortable, implement target adapters to push automatically.

## 📚 Summary

**Current State:**
- Target is just a database table in Sync Manager
- You query Sync Manager to get synced data
- Your app/scripts handle the actual "push"

**To Make It Push:**
- Implement target adapters
- Modify sync_service.py
- Configure target with connection details

**Best Practice:**
- Start with Option A (query mode)
- Add custom push logic as needed
- Keep Sync Manager as your tracking system

The key insight: **Sync Manager is a state management and tracking system**, not a data replication tool out of the box. You control how data flows to external systems.
