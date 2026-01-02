# Projects - Property Management & Sync Manager

This repository contains property management tools and the new **Sync Manager** system.

## 🆕 Sync Manager

A multi-tenant property synchronization management system with PostgreSQL backend, RESTful API, and CLI tools.

### Quick Start

1. **Setup** (creates all files and directories):
   ```bash
   python setup_sync_manager.py
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Test installation**:
   ```bash
   python test_installation.py
   ```

4. **Configure & Initialize**:
   ```bash
   cd website_tools\sync_manager
   copy .env.example .env
   # Edit .env with your PostgreSQL DATABASE_URL
   
   python -m website_tools.sync_manager.cli init
   python -m website_tools.sync_manager.cli create-tenant "My Company"
   ```

5. **Start API**:
   ```bash
   uvicorn website_tools.sync_manager.api:app --reload
   ```
   
   Visit http://localhost:8000/docs for interactive API documentation.

### Documentation

- **SETUP_COMPLETE.md** - Overview and getting started
- **QUICKSTART.md** - 5-minute quick start guide  
- **IMPLEMENTATION.md** - Complete technical documentation
- **website_tools/sync_manager/README.md** - User guide (created by setup)

### Key Features

- ✅ Multi-tenant architecture with API key authentication
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Source & Target management
- ✅ Property synchronization with change detection
- ✅ Manual change tracking and warnings
- ✅ Snapshot retention (configurable, default 30 days)
- ✅ JSON auto-import
- ✅ RESTful API (FastAPI)
- ✅ CLI tools
- ✅ PATCH support for partial updates
- ✅ Batch operations

### Tools Included

- `setup_sync_manager.py` - Create all files and directories
- `test_installation.py` - Verify installation
- `migrate_json.py` - Auto-import existing JSON files
- `run_setup.bat` - Windows batch runner

## Existing Tools

Various property management utilities and scrapers in:
- `website_tools/` - Web scraping and management tools
- `utils/` - General utilities
- `xml/` - XML processing tools
- `availability/` - Availability management

## Requirements

- Python >= 3.12
- PostgreSQL (for Sync Manager)
- Dependencies managed by `uv` or `pip`
