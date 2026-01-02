# Creating an Independent Sync Manager Project

This script creates a completely standalone Sync Manager project that is independent from your main project folder.

## What It Creates

A new directory `sync_manager_project/` with:

```
sync_manager_project/
├── pyproject.toml          # Independent dependencies
├── .gitignore              # Git configuration
├── .env.example            # Environment template
├── README.md               # Project documentation
├── sync_manager/           # Main package
│   ├── __init__.py
│   ├── config.py           # Configuration
│   ├── models.py           # Database models (8 tables)
│   ├── database.py         # Database connection
│   ├── utils.py            # Utilities
│   ├── sync_service.py     # Core sync logic
│   ├── api.py              # FastAPI REST API
│   ├── cli.py              # Command-line interface
│   └── data/               # Data directory
├── docs/                   # Documentation folder
└── tests/                  # Tests folder
```

## Features

- ✅ **Completely Independent** - No dependencies on parent project
- ✅ **Own Dependencies** - Separate pyproject.toml with only what's needed
- ✅ **Standalone Package** - Can be installed with pip/uv
- ✅ **CLI Command** - Installs `sync-manager` command globally
- ✅ **Clean Structure** - Professional project layout
- ✅ **Git Ready** - Includes .gitignore
- ✅ **Dev Tools** - Optional pytest, black, ruff

## Usage

### Step 1: Create the Independent Project

```bash
python create_independent_project.py
```

This creates `sync_manager_project/` directory with all files.

### Step 2: Navigate to the New Project

```bash
cd sync_manager_project
```

### Step 3: Install Dependencies

Using pip:
```bash
pip install -e .
```

Using uv:
```bash
uv sync
```

### Step 4: Configure

```bash
cp .env.example .env
# Edit .env with your PostgreSQL connection
```

### Step 5: Initialize

```bash
python -m sync_manager.cli init
python -m sync_manager.cli create-tenant "My Company"
```

### Step 6: Run

```bash
uvicorn sync_manager.api:app --reload
```

Visit: http://localhost:8000/docs

## Key Differences from Original

| Aspect | Original | Independent |
|--------|----------|-------------|
| Location | `website_tools/sync_manager/` | `sync_manager_project/` |
| Dependencies | Shared with main project | Own pyproject.toml |
| Installation | Part of main project | Standalone pip/uv install |
| CLI | `python -m website_tools.sync_manager.cli` | `python -m sync_manager.cli` or `sync-manager` |
| Import Path | `from website_tools.sync_manager import ...` | `from sync_manager import ...` |
| Repository | Same as main project | Can have its own git repo |

## Benefits

1. **Clean Separation** - No mixing with other project code
2. **Easy Distribution** - Can share as standalone package
3. **Independent Versioning** - Own version number
4. **Simpler Dependencies** - Only what you need
5. **Portable** - Move anywhere, works the same
6. **Team Friendly** - Others can use without your main project

## Moving Forward

After creating the independent project, you can:

1. **Initialize its own git repository:**
   ```bash
   cd sync_manager_project
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Publish to PyPI** (optional):
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

3. **Create Docker image** (optional):
   ```dockerfile
   FROM python:3.12
   WORKDIR /app
   COPY . .
   RUN pip install -e .
   CMD ["uvicorn", "sync_manager.api:app", "--host", "0.0.0.0"]
   ```

4. **Deploy independently** - To any server, cloud platform, or container

## CLI Usage (After Installation)

The independent project can be used two ways:

### Method 1: As Python Module
```bash
python -m sync_manager.cli init
python -m sync_manager.cli create-tenant "Company"
```

### Method 2: As Installed Command (if installed with pip)
```bash
sync-manager init
sync-manager create-tenant "Company"
```

## Development

### Install with Dev Dependencies

```bash
pip install -e ".[dev]"
```

This installs:
- pytest (testing)
- pytest-asyncio (async testing)
- black (code formatting)
- ruff (linting)

### Run Tests

```bash
pytest
```

### Format Code

```bash
black sync_manager/
```

### Lint Code

```bash
ruff check sync_manager/
```

## Maintenance

The independent project includes everything needed:
- All Python modules
- Database models
- API endpoints
- CLI commands
- Documentation
- Configuration templates

No connection to the main project folder is required after creation.

## Summary

Run `python create_independent_project.py` and you'll have a completely standalone, production-ready Sync Manager project that can be:
- Installed independently
- Distributed as a package
- Deployed anywhere
- Maintained separately
- Shared with others

Perfect for when you want Sync Manager as its own project! 🎉
