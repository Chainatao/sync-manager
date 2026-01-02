<div align="center">

![Sync Manager Banner](https://via.placeholder.com/1200x300/4A90E2/FFFFFF?text=Property+Sync+Manager)

# 🏠 Property Sync Manager

**A powerful, standardized real estate property synchronization system**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-316192.svg)](https://www.postgresql.org/)

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Documentation](#documentation)

</div>

---

## 🌟 Overview

Property Sync Manager is a robust real estate data synchronization platform designed to streamline property management across multiple sources and targets. It provides a **standardized schema** for property data, ensuring consistency and reliability when syncing between different real estate platforms, websites, and databases.

### Why Sync Manager?

- 📊 **Standardized Schema**: Unified property data model supporting multilingual content
- 🔄 **Multi-Source Sync**: Import from JSON files, APIs, web scraping, and custom sources
- 🎯 **Multi-Target Push**: Deploy properties to multiple platforms with custom adapters
- 🏢 **Developers & Developments**: Built-in support for property developers and development projects
- 🌍 **Multilingual Support**: Native support for EN, ES, PL, UK, RU translations
- 🔍 **Smart Conflict Detection**: Automatic warning flags for manual changes
- 📈 **Snapshot History**: Track property changes over time with retention policies
- 🚀 **RESTful API**: Complete CRUD operations with FastAPI

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Property Management** | Complete CRUD operations for real estate properties |
| **Source Management** | Track and manage multiple data sources (JSON, API, Scraped) |
| **Target Management** | Configure and sync to multiple destination platforms |
| **Developer Registry** | Manage property developers with contact information |
| **Development Projects** | Track development projects with delivery dates |
| **Snapshot System** | Historical tracking with configurable retention |
| **Conflict Detection** | Identify manual changes vs source updates |
| **Multi-tenant Ready** | Built-in tenant_id filtering for isolation |

### Property Schema Highlights

```python
- Multilingual titles & descriptions (EN, ES, PL, UK, RU)
- Comprehensive property details (bedrooms, bathrooms, areas)
- Location data with geocoding support
- Rich feature enumeration (70+ property features)
- Multiple image and floor plan URLs
- Developer and development associations
- Energy and emission certificates
- Orientation and pool type specifications
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 13 or higher
- Git

### Installation

#### Option 1: Integrated Installation (within existing project)

```bash
# Run the setup script
python complete_setup_template.py

# Follow the prompts to choose integrated installation
```

#### Option 2: Independent Installation (standalone project)

```bash
# Create a new independent project
python create_independent_project.py

# Navigate to the new project
cd sync_manager_project

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

1. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE sync_manager;
   CREATE USER sync_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE sync_manager TO sync_user;
   ```

2. **Set environment variable:**
   ```bash
   # Windows
   set DATABASE_URL=postgresql://sync_user:your_password@localhost:5432/sync_manager
   
   # Linux/Mac
   export DATABASE_URL=postgresql://sync_user:your_password@localhost:5432/sync_manager
   ```

3. **Initialize database:**
   ```bash
   python -m sync_manager.cli init-db
   ```

### Running the Application

```bash
# Start the API server
python -m sync_manager.cli run

# API will be available at http://localhost:8000
# Interactive API docs at http://localhost:8000/docs
```

---

## 🏗️ Architecture

<div align="center">

![Architecture Diagram](https://via.placeholder.com/800x400/34495E/FFFFFF?text=Architecture+Diagram+-+Coming+Soon)

</div>

### Database Schema

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Developers    │      │  Developments    │      │   Properties    │
├─────────────────┤      ├──────────────────┤      ├─────────────────┤
│ id (PK)         │◄─────│ developer_id(FK) │◄─────│ development_id  │
│ name            │      │ id (PK)          │      │ id (PK)         │
│ contact_info    │      │ name             │      │ title (JSON)    │
│ created_at      │      │ location         │      │ description     │
│ updated_at      │      │ delivery_date    │      │ property_type   │
└─────────────────┘      │ created_at       │      │ price           │
                         │ updated_at       │      │ bedrooms        │
                         └──────────────────┘      │ bathrooms       │
                                                    │ ... (50+ fields)│
                                                    └─────────────────┘

┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│     Sources     │      │     Targets      │      │    Snapshots    │
├─────────────────┤      ├──────────────────┤      ├─────────────────┤
│ id (PK)         │      │ id (PK)          │      │ id (PK)         │
│ name            │      │ name             │      │ property_id(FK) │
│ type            │      │ url              │      │ snapshot_data   │
│ config (JSON)   │      │ api_key          │      │ created_at      │
│ created_at      │      │ created_at       │      └─────────────────┘
│ updated_at      │      │ updated_at       │
└─────────────────┘      └──────────────────┘
```

### Synchronization Flow

1. **Import Phase**: Properties are imported from sources (JSON, API, scraper)
2. **Normalization**: Data is transformed to standardized schema
3. **Storage**: Properties stored in PostgreSQL with snapshot creation
4. **Conflict Detection**: System identifies manual changes vs source updates
5. **Export Phase**: Adapters transform standardized data to target format
6. **Push**: Properties deployed to target platforms

---

## 📚 Documentation

Comprehensive guides are available in the `/guides` folder:

- **[01-QUICK_START.md](guides/01-QUICK_START.md)** - Get up and running in minutes
- **[02-DATABASE_SETUP.md](guides/02-DATABASE_SETUP.md)** - Database installation and configuration
- **[03-API_REFERENCE.md](guides/03-API_REFERENCE.md)** - Complete API endpoint documentation
- **[04-PROPERTY_SCHEMA.md](guides/04-PROPERTY_SCHEMA.md)** - Standardized property schema details
- **[05-SYNC_WORKFLOW.md](guides/05-SYNC_WORKFLOW.md)** - Understanding the sync process
- **[06-ADAPTERS.md](guides/06-ADAPTERS.md)** - Creating custom source/target adapters
- **[07-MIGRATION_GUIDE.md](guides/07-MIGRATION_GUIDE.md)** - Migrating from existing systems

---

## 🔌 API Endpoints

### Properties
- `GET /properties` - List all properties with filtering
- `POST /properties` - Create new property
- `GET /properties/{id}` - Get property details
- `PATCH /properties/{id}` - Update property
- `DELETE /properties/{id}` - Delete property

### Sources & Targets
- `GET /sources` - List all sources
- `POST /sources` - Register new source
- `GET /targets` - List all targets
- `POST /targets` - Register new target

### Sync Operations
- `POST /sync/import/{source_id}` - Import from source
- `POST /sync/export/{target_id}` - Push to target
- `GET /sync/status/{job_id}` - Check sync status

### Developers & Developments
- `GET /developers` - List all developers
- `POST /developers` - Create developer
- `GET /developments` - List all developments
- `POST /developments` - Create development

> 📘 **Full API documentation available at `/docs` when running the server**

---

## 🎯 Example: Basic Usage

### Import Properties from JSON

```python
from sync_manager.sync_service import SyncService
from sync_manager.database import get_db

# Initialize
db = next(get_db())
sync_service = SyncService(db)

# Import from JSON source
result = sync_service.import_from_source(
    source_id="json_source_001",
    tenant_id="agency_ym"
)

print(f"Imported {result['imported']} properties")
```

### Export Properties to Target

```python
# Push to target website
result = sync_service.export_to_target(
    target_id="target_website_001",
    tenant_id="agency_ym"
)

print(f"Exported {result['exported']} properties")
```

---

## 🛠️ Custom Adapters

Create custom source/target adapters by extending base classes:

```python
from sync_manager.adapters import BaseSourceAdapter

class MyCustomSourceAdapter(BaseSourceAdapter):
    def fetch_properties(self):
        # Your custom logic here
        return properties
    
    def transform_to_standard(self, raw_data):
        # Transform to StandardProperty schema
        return StandardProperty(**transformed_data)
```

See [06-ADAPTERS.md](guides/06-ADAPTERS.md) for detailed guide.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Project Maintainer**: Chainatao

- GitHub: [@Chainatao](https://github.com/Chainatao)
- Email: inform@acion.es

---

<div align="center">

**[⬆ back to top](#-property-sync-manager)**

Made with ❤️ for real estate professionals

![Footer](https://via.placeholder.com/1200x100/2C3E50/FFFFFF?text=Property+Sync+Manager+%7C+Streamline+Your+Real+Estate+Data)

</div>
