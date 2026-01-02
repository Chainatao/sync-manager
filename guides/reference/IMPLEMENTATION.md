# Sync Manager Implementation

## Overview
This is a complete implementation of the Sync Manager system as specified. The system provides property synchronization management with multi-tenancy support, source/target management, and change tracking.

## What Has Been Implemented

### ✅ Core Architecture
- **Multi-tenant system** with `tenant_id` filtering on all entities
- **PostgreSQL database** using SQLAlchemy ORM
- **Source and Target management** for flexible data flows
- **Property tracking** with hash-based change detection
- **Snapshot system** for historical versions with configurable retention

### ✅ Database Models (`models.py`)
1. **Tenant** - Workspace isolation with API keys
2. **Source** - Data sources (JSON, scraped, manual)
3. **Target** - Destination systems (websites, APIs)
4. **SourceProperty** - Individual items in sources
5. **TargetProperty** - Individual items in targets (with manual change tracking)
6. **SourceSnapshot** - Historical versions of source properties
7. **TargetSnapshot** - Historical versions of target properties
8. **SyncLog** - Audit trail of synchronization operations

All tables include:
- Proper indexes for performance
- Foreign key relationships with cascade rules
- Timestamps (created_at, updated_at)

### ✅ Sync Service (`sync_service.py`)
- **`sync_source_to_target()`** - Synchronous property synchronization
- **`import_json_to_source()`** - Auto-import JSON files
- **`cleanup_old_snapshots()`** - Retention policy enforcement
- **`mark_manual_changes()`** - Manual change tracking
- **Manual change warnings** - Flags conflicts between source and manual edits

### ✅ RESTful API (`api.py`)
Full FastAPI implementation with:
- API key authentication via headers
- Tenant isolation on all endpoints
- CRUD operations for sources and targets
- Property listing and management
- PATCH support for target properties
- Batch import via JSON
- Sync triggers
- Snapshot cleanup

Endpoints:
```
GET    /health
POST   /tenants
POST   /sources
POST   /targets
GET    /sources
GET    /targets
POST   /sources/{id}/import
POST   /sync/{source_id}/{target_id}
GET    /sources/{id}/properties
GET    /targets/{id}/properties
PATCH  /targets/{id}/properties/{prop_id}
DELETE /sources/{id}
DELETE /targets/{id}
POST   /cleanup
```

### ✅ CLI Tool (`cli.py`)
Command-line interface for:
- Database initialization
- Tenant creation with API key generation
- JSON import
- Manual sync triggers
- Snapshot cleanup
- Batch operations support

Commands:
```bash
python -m website_tools.sync_manager.cli init
python -m website_tools.sync_manager.cli create-tenant "Name"
python -m website_tools.sync_manager.cli import <tenant_id> <source_id> file.json
python -m website_tools.sync_manager.cli sync <tenant_id> <source_id> <target_id>
python -m website_tools.sync_manager.cli cleanup <tenant_id> --days 30
```

### ✅ Configuration (`config.py`)
Environment-based configuration:
- `DATABASE_URL` - PostgreSQL connection string
- `RETENTION_DAYS` - Snapshot retention period (default: 30)
- `API_KEY` - Authentication

### ✅ Utilities (`utils.py`)
- Hash computation (SHA-256)
- Deep diff for comparing property changes

### ✅ Database Layer (`database.py`)
- SQLAlchemy engine configuration
- Session management with context manager
- Database initialization

## Features Implemented

### ✅ Multi-Tenancy
- Each tenant has isolated data
- API key authentication per tenant
- `tenant_id` filtering on all queries
- Environment-based `DATABASE_URL` for separate instances

### ✅ Synchronous Operations
- Synchronous sync from source to target
- Real-time change detection via hashing
- Stats tracking (created, updated, skipped, warnings)

### ✅ Manual Change Handling
- Detects when target differs from source
- Sets `has_manual_changes` flag
- Adds warning message
- Skips automatic sync to prevent overwrites
- Requires manual resolution

### ✅ Auto-Import JSON
- Import existing JSON files on initial migration
- Supports lists of property objects
- Creates/updates properties based on hash
- Returns import statistics

### ✅ Snapshot Retention
- Snapshots created before every update
- Configurable retention period (default 30 days)
- Cleanup via CLI or API
- Can be scheduled as nightly job

### ✅ API Keys
- Secure token generation
- Per-tenant authentication
- Header-based verification (`X-API-Key`)

### ✅ PATCH Support
- Partial updates to target properties
- Automatically marks as manually changed
- Creates snapshot before update

### ✅ Batch Operations
- Import multiple properties via JSON array
- Sync all properties from source to target
- Batch delete via cascade relationships

## Setup Instructions

### 1. Run Setup Script
```bash
# Windows
run_setup.bat

# Or directly with Python
python setup_sync_manager.py
```

This creates:
- `website_tools/sync_manager/` directory
- All Python modules
- Configuration templates
- Documentation

### 2. Install Dependencies
```bash
uv sync
```

The following dependencies were added to `pyproject.toml`:
- `sqlalchemy>=2.0.0`
- `psycopg2-binary>=2.9.9`
- `fastapi>=0.115.0`
- `uvicorn>=0.32.0`
- `pydantic>=2.12.5` (already present)

### 3. Configure Database
```bash
cd website_tools/sync_manager
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/sync_manager
RETENTION_DAYS=30
```

### 4. Initialize Database
```bash
python -m website_tools.sync_manager.cli init
```

### 5. Create First Tenant
```bash
python -m website_tools.sync_manager.cli create-tenant "My Company"
```

Save the generated API key!

### 6. Start API Server
```bash
uvicorn website_tools.sync_manager.api:app --reload --host 0.0.0.0 --port 8000
```

## Usage Examples

### Creating Sources and Targets via API

```bash
# Create a source
curl -X POST http://localhost:8000/sources \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Scraped Properties", "type": "scraped"}'

# Create a target
curl -X POST http://localhost:8000/targets \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Website", "type": "website"}'
```

### Importing JSON Data

```bash
# Via CLI
python -m website_tools.sync_manager.cli import 1 1 properties.json

# Via API
curl -X POST http://localhost:8000/sources/1/import \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": [{"id": "prop1", "title": "Property 1", "price": 100000}]}'
```

### Synchronizing Properties

```bash
# Via CLI
python -m website_tools.sync_manager.cli sync 1 1 2

# Via API
curl -X POST http://localhost:8000/sync/1/2 \
  -H "X-API-Key: YOUR_API_KEY"
```

### Patching Target Properties

```bash
curl -X PATCH http://localhost:8000/targets/1/properties/1 \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"price": 95000}}'
```

### Cleanup Old Snapshots

```bash
# Via CLI (nightly cron job)
python -m website_tools.sync_manager.cli cleanup 1 --days 30

# Via API
curl -X POST http://localhost:8000/cleanup?days=30 \
  -H "X-API-Key: YOUR_API_KEY"
```

## Integration with Existing System

The sync manager can be integrated with your existing scrapers:

```python
from website_tools.sync_manager.sync_service import SyncService
from website_tools.sync_manager.database import get_db
from website_tools.sync_manager.models import Source

# After scraping
scraped_data = [...]  # Your scraped properties

# Import to source
sync_service = SyncService(tenant_id=1)
result = sync_service.import_json_to_source(source_id=1, data=scraped_data)

# Auto-sync to target
sync_result = sync_service.sync_source_to_target(source_id=1, target_id=1)
```

## Scheduled Jobs

### Nightly Cleanup (Example Cron)
```cron
# Run cleanup every night at 2 AM
0 2 * * * cd /path/to/project && python -m website_tools.sync_manager.cli cleanup 1 --days 30
```

### Automated Scraping and Sync
```python
# In your scraper
from website_tools.sync_manager.sync_service import SyncService

def scrape_and_sync():
    # 1. Scrape data
    properties = scrape_properties()
    
    # 2. Import to source
    sync_service = SyncService(tenant_id=1)
    sync_service.import_json_to_source(source_id=1, data=properties)
    
    # 3. Sync to target
    sync_service.sync_source_to_target(source_id=1, target_id=1)
```

## What Was NOT Implemented (As Requested)

- ❌ Backup functionality (explicitly excluded)
- ❌ Web interface (to be added later)
- ❌ Async operations (requested synchronous only)
- ❌ Automatic scraping triggers (can be added via cron/scheduler)

## Next Steps

1. **Run the setup**: `python setup_sync_manager.py`
2. **Install dependencies**: `uv sync`
3. **Configure database**: Edit `.env` file
4. **Initialize**: `python -m website_tools.sync_manager.cli init`
5. **Create tenant**: Get your API key
6. **Test the API**: Start server and test endpoints
7. **Integrate scrapers**: Connect existing data sources
8. **Schedule cleanup**: Set up nightly job

## Architecture Decisions

### Why PostgreSQL?
- Robust JSON support for flexible property data
- Strong consistency for multi-tenant isolation
- Excellent indexing for fast queries
- ACID compliance for data integrity

### Why Snapshots?
- Track historical changes
- Enable rollback if needed
- Audit trail for compliance
- Debugging manual changes

### Why Hash-Based Detection?
- Fast comparison without deep inspection
- Deterministic change detection
- Efficient storage
- Works with any JSON structure

### Why Multi-Tenancy?
- Scalable for multiple clients
- Data isolation and security
- Shared infrastructure
- Flexible deployment

## Security Considerations

1. **API Keys**: Store securely, never commit to git
2. **Database**: Use strong passwords, restrict access
3. **Environment**: Use `.env` file, never hardcode credentials
4. **Tenant Isolation**: All queries filtered by `tenant_id`
5. **Input Validation**: Pydantic models validate all API inputs

## Performance Notes

- Indexes on all foreign keys and search fields
- Hash comparison avoids expensive JSON comparisons
- Batch operations for efficiency
- Connection pooling via SQLAlchemy
- Configurable cleanup to manage storage

## File Structure
```
website_tools/sync_manager/
├── __init__.py          # Package initialization
├── config.py            # Environment configuration
├── models.py            # SQLAlchemy models
├── database.py          # Database connection and session management
├── utils.py             # Helper functions (hashing, diff)
├── sync_service.py      # Core synchronization logic
├── api.py               # FastAPI REST API
├── cli.py               # Command-line interface
├── .env.example         # Environment template
└── README.md            # User documentation
```

## Support

For issues or questions:
1. Check the README.md in sync_manager/
2. Review the API documentation at `/docs` when server is running
3. Examine sync_logs table for operation history
4. Check manual_changes_warning field for conflict details
