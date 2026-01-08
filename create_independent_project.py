"""
Setup script to create an independent Sync Manager project
This will create a standalone directory structure separate from the main project
"""
import os
import sys
from pathlib import Path
import shutil

# Set UTF-8 encoding for console output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("Creating Independent Sync Manager Project...")
print("="*60)

# Create independent project directory
project_root = Path(__file__).parent / "sync_manager_project"
project_root.mkdir(exist_ok=True)
print(f"[OK] Created project root: {project_root}")

# Create directory structure
directories = [
    "sync_manager",
    "sync_manager/data",
    "docs",
    "tests",
]

for dir_path in directories:
    (project_root / dir_path).mkdir(parents=True, exist_ok=True)
    print(f"[OK] Created: {dir_path}/")

# Create __init__.py files
init_files = [
    "sync_manager/__init__.py",
]

for init_file in init_files:
    (project_root / init_file).write_text('"""Sync Manager - Multi-tenant Property Synchronization System"""', encoding='utf-8')
    print(f"[OK] Created: {init_file}")

# Create pyproject.toml
pyproject_content = '''[project]
name = "sync-manager"
version = "1.0.0"
description = "Multi-tenant property synchronization management system"
readme = "README.md"
requires-python = ">=3.12"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
dependencies = [
    "fastapi>=0.115.0",
    "sqlalchemy>=2.0.0",
    "psycopg2-binary>=2.9.9",
    "uvicorn>=0.32.0",
    "pydantic>=2.12.5",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "black>=24.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 100
target-version = ["py312"]

[tool.ruff]
line-length = 100
target-version = "py312"

[project.scripts]
sync-manager = "sync_manager.cli:main"
'''
(project_root / "pyproject.toml").write_text(pyproject_content, encoding='utf-8')
print("[OK] Created: pyproject.toml")

# Create .gitignore
gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Database
*.db
*.sqlite3

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Data
sync_manager/data/*.json
!sync_manager/data/.gitkeep

# Tests
.pytest_cache/
.coverage
htmlcov/
'''
(project_root / ".gitignore").write_text(gitignore_content, encoding='utf-8')
print("[OK] Created: .gitignore")

# Create config.py
config_content = '''import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/sync_manager")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "30"))

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
'''
(project_root / "sync_manager" / "config.py").write_text(config_content, encoding='utf-8')
print("[OK] Created: sync_manager/config.py")

# Create models.py
models_content = '''from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    api_key = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    sources = relationship("Source", back_populates="tenant", cascade="all, delete-orphan")
    targets = relationship("Target", back_populates="tenant", cascade="all, delete-orphan")


class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    config = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    tenant = relationship("Tenant", back_populates="sources")
    properties = relationship("SourceProperty", back_populates="source", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_sources_tenant_id", "tenant_id"),
        Index("idx_sources_type", "type"),
    )


class Target(Base):
    __tablename__ = "targets"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    config = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    tenant = relationship("Tenant", back_populates="targets")
    properties = relationship("TargetProperty", back_populates="target", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_targets_tenant_id", "tenant_id"),
        Index("idx_targets_type", "type"),
    )


class SourceProperty(Base):
    __tablename__ = "source_properties"
    
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    external_id = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)
    hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    source = relationship("Source", back_populates="properties")
    snapshots = relationship("SourceSnapshot", back_populates="property", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_source_properties_source_id", "source_id"),
        Index("idx_source_properties_external_id", "external_id"),
        Index("idx_source_properties_hash", "hash"),
    )


class TargetProperty(Base):
    __tablename__ = "target_properties"
    
    id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("targets.id", ondelete="CASCADE"), nullable=False)
    source_property_id = Column(Integer, ForeignKey("source_properties.id", ondelete="SET NULL"), nullable=True)
    external_id = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)
    hash = Column(String(64), nullable=False)
    has_manual_changes = Column(Boolean, default=False, nullable=False)
    manual_changes_warning = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    target = relationship("Target", back_populates="properties")
    snapshots = relationship("TargetSnapshot", back_populates="property", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_target_properties_target_id", "target_id"),
        Index("idx_target_properties_source_property_id", "source_property_id"),
        Index("idx_target_properties_external_id", "external_id"),
        Index("idx_target_properties_hash", "hash"),
        Index("idx_target_properties_has_manual_changes", "has_manual_changes"),
    )


class SourceSnapshot(Base):
    __tablename__ = "source_snapshots"
    
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("source_properties.id", ondelete="CASCADE"), nullable=False)
    data = Column(JSON, nullable=False)
    hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    property = relationship("SourceProperty", back_populates="snapshots")
    
    __table_args__ = (
        Index("idx_source_snapshots_property_id", "property_id"),
        Index("idx_source_snapshots_created_at", "created_at"),
    )


class TargetSnapshot(Base):
    __tablename__ = "target_snapshots"
    
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("target_properties.id", ondelete="CASCADE"), nullable=False)
    data = Column(JSON, nullable=False)
    hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    property = relationship("TargetProperty", back_populates="snapshots")
    
    __table_args__ = (
        Index("idx_target_snapshots_property_id", "property_id"),
        Index("idx_target_snapshots_created_at", "created_at"),
    )


class SyncLog(Base):
    __tablename__ = "sync_logs"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    target_id = Column(Integer, ForeignKey("targets.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(50), nullable=False)
    message = Column(Text, nullable=True)
    stats = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index("idx_sync_logs_tenant_id", "tenant_id"),
        Index("idx_sync_logs_created_at", "created_at"),
        Index("idx_sync_logs_status", "status"),
    )


class Developer(Base):
    __tablename__ = "developers"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String(512), nullable=True)
    logo_url = Column(String(512), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    developments = relationship("Development", back_populates="developer", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_developers_tenant_id", "tenant_id"),
        Index("idx_developers_name", "name"),
    )


class Development(Base):
    __tablename__ = "developments"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    developer_id = Column(Integer, ForeignKey("developers.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    total_units = Column(Integer, nullable=True)
    available_units = Column(Integer, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    images = Column(JSON, nullable=True)
    website = Column(String(512), nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    developer = relationship("Developer", back_populates="developments")
    
    __table_args__ = (
        Index("idx_developments_tenant_id", "tenant_id"),
        Index("idx_developments_developer_id", "developer_id"),
        Index("idx_developments_name", "name"),
    )
'''
(project_root / "sync_manager" / "models.py").write_text(models_content, encoding='utf-8')
print("[OK] Created: sync_manager/models.py")

print("\n" + "="*60)
print("Copying remaining modules...")
print("="*60)

# Copy all module files from setup script content
modules = {
    "database.py": '''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from .config import DATABASE_URL
from .models import Base

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    """Database session context manager"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
''',
    "utils.py": '''import hashlib
import json
from typing import Any, Dict


def compute_hash(data: Dict[str, Any]) -> str:
    """Compute SHA-256 hash of data dictionary"""
    json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(json_str.encode()).hexdigest()


def deep_diff(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two dictionaries and return differences"""
    differences = {}
    all_keys = set(dict1.keys()) | set(dict2.keys())
    
    for key in all_keys:
        if key not in dict1:
            differences[key] = {"status": "added", "new": dict2[key]}
        elif key not in dict2:
            differences[key] = {"status": "removed", "old": dict1[key]}
        elif dict1[key] != dict2[key]:
            differences[key] = {"status": "changed", "old": dict1[key], "new": dict2[key]}
    
    return differences
''',
    "sync_service.py": '''from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from .models import (
    Source, Target, SourceProperty, TargetProperty,
    SourceSnapshot, TargetSnapshot, SyncLog, Tenant
)
from .utils import compute_hash, deep_diff
from .database import get_db
from .config import RETENTION_DAYS


class SyncService:
    """Service for synchronizing properties between sources and targets"""
    
    def __init__(self, tenant_id: int):
        self.tenant_id = tenant_id
    
    def sync_source_to_target(self, source_id: int, target_id: int) -> Dict[str, Any]:
        """Synchronize properties from source to target"""
        with get_db() as db:
            source = db.query(Source).filter(
                Source.id == source_id,
                Source.tenant_id == self.tenant_id
            ).first()
            
            target = db.query(Target).filter(
                Target.id == target_id,
                Target.tenant_id == self.tenant_id
            ).first()
            
            if not source or not target:
                return {"status": "failed", "message": "Source or target not found"}
            
            stats = {
                "created": 0,
                "updated": 0,
                "skipped": 0,
                "warnings": 0
            }
            
            source_properties = db.query(SourceProperty).filter(
                SourceProperty.source_id == source_id
            ).all()
            
            for src_prop in source_properties:
                target_prop = db.query(TargetProperty).filter(
                    TargetProperty.target_id == target_id,
                    TargetProperty.external_id == src_prop.external_id
                ).first()
                
                if target_prop:
                    if target_prop.hash != src_prop.hash:
                        if target_prop.has_manual_changes:
                            target_prop.manual_changes_warning = (
                                f"Source has changes but target has manual modifications. "
                                f"Last sync: {target_prop.updated_at}"
                            )
                            stats["warnings"] += 1
                            stats["skipped"] += 1
                        else:
                            self._create_snapshot(db, target_prop)
                            target_prop.data = src_prop.data
                            target_prop.hash = src_prop.hash
                            target_prop.source_property_id = src_prop.id
                            target_prop.updated_at = datetime.utcnow()
                            stats["updated"] += 1
                    else:
                        stats["skipped"] += 1
                else:
                    new_target_prop = TargetProperty(
                        target_id=target_id,
                        source_property_id=src_prop.id,
                        external_id=src_prop.external_id,
                        data=src_prop.data,
                        hash=src_prop.hash
                    )
                    db.add(new_target_prop)
                    stats["created"] += 1
            
            log = SyncLog(
                tenant_id=self.tenant_id,
                source_id=source_id,
                target_id=target_id,
                status="success" if stats["warnings"] == 0 else "partial",
                stats=stats
            )
            db.add(log)
            
            return {"status": "success", "stats": stats}
    
    def import_json_to_source(self, source_id: int, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Import JSON data into a source"""
        with get_db() as db:
            source = db.query(Source).filter(
                Source.id == source_id,
                Source.tenant_id == self.tenant_id
            ).first()
            
            if not source:
                return {"status": "failed", "message": "Source not found"}
            
            stats = {"created": 0, "updated": 0}
            
            for item in data:
                external_id = str(item.get("id") or item.get("external_id", ""))
                if not external_id:
                    continue
                
                item_hash = compute_hash(item)
                
                existing = db.query(SourceProperty).filter(
                    SourceProperty.source_id == source_id,
                    SourceProperty.external_id == external_id
                ).first()
                
                if existing:
                    if existing.hash != item_hash:
                        self._create_source_snapshot(db, existing)
                        existing.data = item
                        existing.hash = item_hash
                        existing.updated_at = datetime.utcnow()
                        stats["updated"] += 1
                else:
                    new_prop = SourceProperty(
                        source_id=source_id,
                        external_id=external_id,
                        data=item,
                        hash=item_hash
                    )
                    db.add(new_prop)
                    stats["created"] += 1
            
            return {"status": "success", "stats": stats}
    
    def _create_snapshot(self, db: Session, prop: TargetProperty):
        """Create a snapshot of target property before update"""
        snapshot = TargetSnapshot(
            property_id=prop.id,
            data=prop.data,
            hash=prop.hash
        )
        db.add(snapshot)
    
    def _create_source_snapshot(self, db: Session, prop: SourceProperty):
        """Create a snapshot of source property before update"""
        snapshot = SourceSnapshot(
            property_id=prop.id,
            data=prop.data,
            hash=prop.hash
        )
        db.add(snapshot)
    
    def cleanup_old_snapshots(self, days: Optional[int] = None):
        """Clean up snapshots older than specified days"""
        days = days or RETENTION_DAYS
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        with get_db() as db:
            db.query(SourceSnapshot).filter(
                SourceSnapshot.created_at < cutoff_date
            ).delete()
            
            db.query(TargetSnapshot).filter(
                TargetSnapshot.created_at < cutoff_date
            ).delete()
    
    def mark_manual_changes(self, target_property_id: int):
        """Mark a target property as having manual changes"""
        with get_db() as db:
            prop = db.query(TargetProperty).filter(
                TargetProperty.id == target_property_id
            ).first()
            
            if prop:
                if prop.source_property_id:
                    source_prop = db.query(SourceProperty).filter(
                        SourceProperty.id == prop.source_property_id
                    ).first()
                    
                    if source_prop and prop.hash != source_prop.hash:
                        self._create_snapshot(db, prop)
                        prop.has_manual_changes = True
                        prop.manual_changes_warning = (
                            f"Manual changes detected. Automatic sync disabled. "
                            f"Detected at: {datetime.utcnow()}"
                        )
''',
    "api.py": '''from fastapi import FastAPI, Depends, HTTPException, Header
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from .models import Tenant, Source, Target, SourceProperty, TargetProperty, Developer, Development
from .database import get_db, init_db
from .sync_service import SyncService


app = FastAPI(title="Sync Manager API", version="1.0.0")


class TenantCreate(BaseModel):
    name: str
    api_key: str


class SourceCreate(BaseModel):
    name: str
    type: str
    config: Optional[Dict[str, Any]] = None


class TargetCreate(BaseModel):
    name: str
    type: str
    config: Optional[Dict[str, Any]] = None


class PropertyImport(BaseModel):
    data: List[Dict[str, Any]]


class PropertyPatch(BaseModel):
    data: Dict[str, Any]


def verify_api_key(x_api_key: str = Header(...)) -> int:
    """Verify API key and return tenant ID"""
    with get_db() as db:
        tenant = db.query(Tenant).filter(Tenant.api_key == x_api_key).first()
        if not tenant:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return tenant.id


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/tenants")
async def create_tenant(tenant: TenantCreate):
    """Create a new tenant"""
    with get_db() as db:
        existing = db.query(Tenant).filter(Tenant.name == tenant.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Tenant already exists")
        
        new_tenant = Tenant(name=tenant.name, api_key=tenant.api_key)
        db.add(new_tenant)
        db.flush()
        
        return {"id": new_tenant.id, "name": new_tenant.name}


@app.post("/sources")
async def create_source(source: SourceCreate, tenant_id: int = Depends(verify_api_key)):
    """Create a new source"""
    with get_db() as db:
        new_source = Source(
            tenant_id=tenant_id,
            name=source.name,
            type=source.type,
            config=source.config
        )
        db.add(new_source)
        db.flush()
        
        return {"id": new_source.id, "name": new_source.name, "type": new_source.type}


@app.post("/targets")
async def create_target(target: TargetCreate, tenant_id: int = Depends(verify_api_key)):
    """Create a new target"""
    with get_db() as db:
        new_target = Target(
            tenant_id=tenant_id,
            name=target.name,
            type=target.type,
            config=target.config
        )
        db.add(new_target)
        db.flush()
        
        return {"id": new_target.id, "name": new_target.name, "type": new_target.type}


@app.get("/sources")
async def list_sources(tenant_id: int = Depends(verify_api_key)):
    """List all sources for tenant"""
    with get_db() as db:
        sources = db.query(Source).filter(Source.tenant_id == tenant_id).all()
        return [{"id": s.id, "name": s.name, "type": s.type, "is_active": s.is_active} for s in sources]


@app.get("/targets")
async def list_targets(tenant_id: int = Depends(verify_api_key)):
    """List all targets for tenant"""
    with get_db() as db:
        targets = db.query(Target).filter(Target.tenant_id == tenant_id).all()
        return [{"id": t.id, "name": t.name, "type": t.type, "is_active": t.is_active} for t in targets]


@app.post("/sources/{source_id}/import")
async def import_to_source(
    source_id: int,
    import_data: PropertyImport,
    tenant_id: int = Depends(verify_api_key)
):
    """Import JSON data to a source"""
    sync_service = SyncService(tenant_id)
    result = sync_service.import_json_to_source(source_id, import_data.data)
    return result


@app.post("/sync/{source_id}/{target_id}")
async def sync_properties(
    source_id: int,
    target_id: int,
    tenant_id: int = Depends(verify_api_key)
):
    """Sync properties from source to target"""
    sync_service = SyncService(tenant_id)
    result = sync_service.sync_source_to_target(source_id, target_id)
    return result


@app.get("/sources/{source_id}/properties")
async def list_source_properties(
    source_id: int,
    tenant_id: int = Depends(verify_api_key)
):
    """List properties in a source"""
    with get_db() as db:
        properties = db.query(SourceProperty).join(Source).filter(
            Source.id == source_id,
            Source.tenant_id == tenant_id
        ).all()
        return [{"id": p.id, "external_id": p.external_id, "data": p.data} for p in properties]


@app.get("/targets/{target_id}/properties")
async def list_target_properties(
    target_id: int,
    tenant_id: int = Depends(verify_api_key)
):
    """List properties in a target"""
    with get_db() as db:
        properties = db.query(TargetProperty).join(Target).filter(
            Target.id == target_id,
            Target.tenant_id == tenant_id
        ).all()
        return [{
            "id": p.id,
            "external_id": p.external_id,
            "data": p.data,
            "has_manual_changes": p.has_manual_changes,
            "warning": p.manual_changes_warning
        } for p in properties]


@app.patch("/targets/{target_id}/properties/{property_id}")
async def patch_target_property(
    target_id: int,
    property_id: int,
    patch: PropertyPatch,
    tenant_id: int = Depends(verify_api_key)
):
    """Patch a target property (marks it as manually changed)"""
    sync_service = SyncService(tenant_id)
    
    with get_db() as db:
        prop = db.query(TargetProperty).join(Target).filter(
            TargetProperty.id == property_id,
            TargetProperty.target_id == target_id,
            Target.tenant_id == tenant_id
        ).first()
        
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        
        prop.data.update(patch.data)
        sync_service.mark_manual_changes(property_id)
        
        return {"status": "updated", "id": prop.id}


@app.delete("/sources/{source_id}")
async def delete_source(source_id: int, tenant_id: int = Depends(verify_api_key)):
    """Delete a source"""
    with get_db() as db:
        source = db.query(Source).filter(
            Source.id == source_id,
            Source.tenant_id == tenant_id
        ).first()
        
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        
        db.delete(source)
        return {"status": "deleted"}


@app.delete("/targets/{target_id}")
async def delete_target(target_id: int, tenant_id: int = Depends(verify_api_key)):
    """Delete a target"""
    with get_db() as db:
        target = db.query(Target).filter(
            Target.id == target_id,
            Target.tenant_id == tenant_id
        ).first()
        
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")
        
        db.delete(target)
        return {"status": "deleted"}


# ========================================
# DEVELOPER ENDPOINTS
# ========================================

class DeveloperCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DeveloperUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@app.post("/developers")
async def create_developer(developer: DeveloperCreate, tenant_id: int = Depends(verify_api_key)):
    """Create a new developer"""
    with get_db() as db:
        new_developer = Developer(
            tenant_id=tenant_id,
            name=developer.name,
            description=developer.description,
            website=developer.website,
            logo_url=developer.logo_url,
            contact_email=developer.contact_email,
            contact_phone=developer.contact_phone,
            meta_data=developer.metadata
        )
        db.add(new_developer)
        db.flush()
        
        return {"id": new_developer.id, "name": new_developer.name}


@app.get("/developers")
async def list_developers(tenant_id: int = Depends(verify_api_key)):
    """List all developers for tenant"""
    with get_db() as db:
        developers = db.query(Developer).filter(Developer.tenant_id == tenant_id).all()
        return [{
            "id": d.id,
            "name": d.name,
            "description": d.description,
            "website": d.website,
            "logo_url": d.logo_url,
            "contact_email": d.contact_email,
            "contact_phone": d.contact_phone
        } for d in developers]


@app.get("/developers/{developer_id}")
async def get_developer(developer_id: int, tenant_id: int = Depends(verify_api_key)):
    """Get developer details"""
    with get_db() as db:
        developer = db.query(Developer).filter(
            Developer.id == developer_id,
            Developer.tenant_id == tenant_id
        ).first()
        
        if not developer:
            raise HTTPException(status_code=404, detail="Developer not found")
        
        return {
            "id": developer.id,
            "name": developer.name,
            "description": developer.description,
            "website": developer.website,
            "logo_url": developer.logo_url,
            "contact_email": developer.contact_email,
            "contact_phone": developer.contact_phone,
            "metadata": developer.meta_data
        }


@app.patch("/developers/{developer_id}")
async def update_developer(
    developer_id: int,
    developer_update: DeveloperUpdate,
    tenant_id: int = Depends(verify_api_key)
):
    """Update developer"""
    with get_db() as db:
        developer = db.query(Developer).filter(
            Developer.id == developer_id,
            Developer.tenant_id == tenant_id
        ).first()
        
        if not developer:
            raise HTTPException(status_code=404, detail="Developer not found")
        
        update_data = developer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(developer, field, value)
        
        return {"status": "updated", "id": developer.id}


@app.delete("/developers/{developer_id}")
async def delete_developer(developer_id: int, tenant_id: int = Depends(verify_api_key)):
    """Delete a developer"""
    with get_db() as db:
        developer = db.query(Developer).filter(
            Developer.id == developer_id,
            Developer.tenant_id == tenant_id
        ).first()
        
        if not developer:
            raise HTTPException(status_code=404, detail="Developer not found")
        
        db.delete(developer)
        return {"status": "deleted"}


# ========================================
# DEVELOPMENT ENDPOINTS
# ========================================

class DevelopmentCreate(BaseModel):
    name: str
    developer_id: Optional[int] = None
    description: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    total_units: Optional[int] = None
    available_units: Optional[int] = None
    completion_date: Optional[datetime] = None
    images: Optional[List[str]] = None
    website: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DevelopmentUpdate(BaseModel):
    name: Optional[str] = None
    developer_id: Optional[int] = None
    description: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    total_units: Optional[int] = None
    available_units: Optional[int] = None
    completion_date: Optional[datetime] = None
    images: Optional[List[str]] = None
    website: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@app.post("/developments")
async def create_development(development: DevelopmentCreate, tenant_id: int = Depends(verify_api_key)):
    """Create a new development"""
    with get_db() as db:
        new_development = Development(
            tenant_id=tenant_id,
            developer_id=development.developer_id,
            name=development.name,
            description=development.description,
            location=development.location,
            city=development.city,
            state=development.state,
            country=development.country,
            total_units=development.total_units,
            available_units=development.available_units,
            completion_date=development.completion_date,
            images=development.images,
            website=development.website,
            meta_data=development.metadata
        )
        db.add(new_development)
        db.flush()
        
        return {"id": new_development.id, "name": new_development.name}


@app.get("/developments")
async def list_developments(
    developer_id: Optional[int] = None,
    tenant_id: int = Depends(verify_api_key)
):
    """List all developments for tenant, optionally filtered by developer"""
    with get_db() as db:
        query = db.query(Development).filter(Development.tenant_id == tenant_id)
        
        if developer_id:
            query = query.filter(Development.developer_id == developer_id)
        
        developments = query.all()
        return [{
            "id": d.id,
            "name": d.name,
            "developer_id": d.developer_id,
            "description": d.description,
            "location": d.location,
            "city": d.city,
            "state": d.state,
            "country": d.country,
            "total_units": d.total_units,
            "available_units": d.available_units,
            "completion_date": d.completion_date.isoformat() if d.completion_date else None,
            "website": d.website
        } for d in developments]


@app.get("/developments/{development_id}")
async def get_development(development_id: int, tenant_id: int = Depends(verify_api_key)):
    """Get development details"""
    with get_db() as db:
        development = db.query(Development).filter(
            Development.id == development_id,
            Development.tenant_id == tenant_id
        ).first()
        
        if not development:
            raise HTTPException(status_code=404, detail="Development not found")
        
        return {
            "id": development.id,
            "name": development.name,
            "developer_id": development.developer_id,
            "description": development.description,
            "location": development.location,
            "city": development.city,
            "state": development.state,
            "country": development.country,
            "total_units": development.total_units,
            "available_units": development.available_units,
            "completion_date": development.completion_date.isoformat() if development.completion_date else None,
            "images": development.images,
            "website": development.website,
            "metadata": development.meta_data
        }


@app.patch("/developments/{development_id}")
async def update_development(
    development_id: int,
    development_update: DevelopmentUpdate,
    tenant_id: int = Depends(verify_api_key)
):
    """Update development"""
    with get_db() as db:
        development = db.query(Development).filter(
            Development.id == development_id,
            Development.tenant_id == tenant_id
        ).first()
        
        if not development:
            raise HTTPException(status_code=404, detail="Development not found")
        
        update_data = development_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(development, field, value)
        
        return {"status": "updated", "id": development.id}


@app.delete("/developments/{development_id}")
async def delete_development(development_id: int, tenant_id: int = Depends(verify_api_key)):
    """Delete a development"""
    with get_db() as db:
        development = db.query(Development).filter(
            Development.id == development_id,
            Development.tenant_id == tenant_id
        ).first()
        
        if not development:
            raise HTTPException(status_code=404, detail="Development not found")
        
        db.delete(development)
        return {"status": "deleted"}
        
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")
        
        db.delete(target)
        return {"status": "deleted"}


@app.post("/cleanup")
async def cleanup_snapshots(
    days: Optional[int] = None,
    tenant: Tenant = Depends(verify_api_key)
):
    """Clean up old snapshots"""
    sync_service = SyncService(tenant.id)
    sync_service.cleanup_old_snapshots(days)
    return {"status": "cleanup completed"}
''',
    "test_api.py": '''"""
Test script for Sync Manager API
Run this script while the API server is running (uvicorn sync_manager.api:app --reload)
"""

import requests
import json
from datetime import datetime


BASE_URL = "http://127.0.0.1:8000"
API_KEY = "test-api-key-12345"

# Track created resources for cleanup
CREATED_RESOURCES = {
    "tenant_id": None,
    "sources": [],
    "targets": [],
    "developers": [],
    "developments": [],
}


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_response(response, title="Response"):
    """Print formatted response"""
    print(f"\n{title}:")
    print(f"Status: {response.status_code}")
    try:
        print(f"Data: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Data: {response.text}")


def cleanup_resources():
    """Delete all created resources"""
    print_section("CLEANUP - Deleting created resources")
    headers = {"X-API-Key": API_KEY}
    
    # Delete developments first (depends on nothing)
    for dev_id in CREATED_RESOURCES["developments"]:
        response = requests.delete(f"{BASE_URL}/developments/{dev_id}", headers=headers)
        if response.status_code == 200:
            print(f"✓ Deleted development {dev_id}")
        else:
            print(f"✗ Failed to delete development {dev_id}")
    
    # Delete developers
    for dev_id in CREATED_RESOURCES["developers"]:
        response = requests.delete(f"{BASE_URL}/developers/{dev_id}", headers=headers)
        if response.status_code == 200:
            print(f"✓ Deleted developer {dev_id}")
        else:
            print(f"✗ Failed to delete developer {dev_id}")
    
    # Delete targets
    for target_id in CREATED_RESOURCES["targets"]:
        response = requests.delete(f"{BASE_URL}/targets/{target_id}", headers=headers)
        if response.status_code == 200:
            print(f"✓ Deleted target {target_id}")
        else:
            print(f"✗ Failed to delete target {target_id}")
    
    # Delete sources
    for source_id in CREATED_RESOURCES["sources"]:
        response = requests.delete(f"{BASE_URL}/sources/{source_id}", headers=headers)
        if response.status_code == 200:
            print(f"✓ Deleted source {source_id}")
        else:
            print(f"✗ Failed to delete source {source_id}")
    
    print("\n✓ Cleanup completed")


def test_health():
    """Test health check endpoint"""
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    return response.status_code == 200


def test_create_tenant():
    """Test creating a tenant"""
    print_section("2. Create Tenant")
    data = {
        "name": "Test Company",
        "api_key": API_KEY
    }
    response = requests.post(f"{BASE_URL}/tenants", json=data)
    print_response(response)
    
    if response.status_code == 200:
        CREATED_RESOURCES["tenant_id"] = response.json().get("id")
    
    return response.status_code in [200, 400]  # 400 if already exists


def test_create_source():
    """Test creating a source"""
    print_section("3. Create Source")
    data = {
        "name": "MLS Data Feed",
        "type": "mls",
        "config": {
            "feed_url": "https://api.example.com/mls",
            "refresh_interval": 3600
        }
    }
    headers = {"X-API-Key": API_KEY}
    response = requests.post(f"{BASE_URL}/sources", json=data, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        source_id = response.json().get("id")
        CREATED_RESOURCES["sources"].append(source_id)
        return source_id
    return None


def test_create_target():
    """Test creating a target"""
    print_section("4. Create Target")
    data = {
        "name": "Website Properties",
        "type": "website",
        "config": {
            "api_endpoint": "https://mywebsite.com/api/properties",
            "auth_token": "token123"
        }
    }
    headers = {"X-API-Key": API_KEY}
    response = requests.post(f"{BASE_URL}/targets", json=data, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        target_id = response.json().get("id")
        CREATED_RESOURCES["targets"].append(target_id)
        return target_id
    return None


def test_list_sources():
    """Test listing sources"""
    print_section("5. List Sources")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/sources", headers=headers)
    print_response(response)
    return response.status_code == 200


def test_list_targets():
    """Test listing targets"""
    print_section("6. List Targets")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/targets", headers=headers)
    print_response(response)
    return response.status_code == 200


def test_import_properties(source_id):
    """Test importing properties to a source"""
    print_section("7. Import Properties to Source")
    data = {
        "data": [
            {
                "external_id": "PROP-001",
                "address": "123 Main St",
                "city": "New York",
                "state": "NY",
                "price": 500000,
                "bedrooms": 3,
                "bathrooms": 2
            },
            {
                "external_id": "PROP-002",
                "address": "456 Oak Ave",
                "city": "Los Angeles",
                "state": "CA",
                "price": 750000,
                "bedrooms": 4,
                "bathrooms": 3
            }
        ]
    }
    headers = {"X-API-Key": API_KEY}
    response = requests.post(f"{BASE_URL}/sources/{source_id}/import", json=data, headers=headers)
    print_response(response)
    return response.status_code == 200


def test_sync_properties(source_id, target_id):
    """Test syncing properties from source to target"""
    print_section("8. Sync Properties")
    headers = {"X-API-Key": API_KEY}
    response = requests.post(f"{BASE_URL}/sync/{source_id}/{target_id}", headers=headers)
    print_response(response)
    return response.status_code == 200


def test_get_source_properties(source_id):
    """Test getting source properties"""
    print_section("9. Get Source Properties")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/sources/{source_id}/properties", headers=headers)
    print_response(response)
    return response.status_code == 200


def test_get_target_properties(target_id):
    """Test getting target properties"""
    print_section("10. Get Target Properties")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/targets/{target_id}/properties", headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        properties = response.json()
        if properties and isinstance(properties, list):
            return properties[0].get("id")
    return None


def test_create_developer():
    """Test creating a developer"""
    print_section("11. Create Developer")
    data = {
        "name": "Premium Developers Inc",
        "description": "Leading real estate developer",
        "website": "https://premiumdev.com",
        "contact_email": "info@premiumdev.com",
        "contact_phone": "+1-555-0123"
    }
    headers = {"X-API-Key": API_KEY}
    response = requests.post(f"{BASE_URL}/developers", json=data, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        developer_id = response.json().get("id")
        CREATED_RESOURCES["developers"].append(developer_id)
        return developer_id
    return None


def test_list_developers():
    """Test listing developers"""
    print_section("12. List Developers")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/developers", headers=headers)
    print_response(response)
    return response.status_code == 200


def test_create_development(developer_id):
    """Test creating a development"""
    print_section("13. Create Development")
    data = {
        "developer_id": developer_id,
        "name": "Sunset Towers",
        "description": "Luxury high-rise apartments",
        "location": "Downtown",
        "city": "Miami",
        "state": "FL",
        "country": "USA",
        "total_units": 150,
        "available_units": 45,
        "website": "https://sunsettowers.com"
    }
    headers = {"X-API-Key": API_KEY}
    response = requests.post(f"{BASE_URL}/developments", json=data, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        development_id = response.json().get("id")
        CREATED_RESOURCES["developments"].append(development_id)
        return development_id
    return None


def test_list_developments():
    """Test listing developments"""
    print_section("14. List Developments")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/developments", headers=headers)
    print_response(response)
    return response.status_code == 200


def main():
    """Run all tests"""
    print("\n" + "█" * 60)
    print("  SYNC MANAGER API TEST SUITE")
    print("█" * 60)
    print(f"\nTesting API at: {BASE_URL}")
    print(f"Using API Key: {API_KEY}")
    
    results = []
    
    try:
        # Run tests
        results.append(("Health Check", test_health()))
        results.append(("Create Tenant", test_create_tenant()))
        
        source_id = test_create_source()
        results.append(("Create Source", source_id is not None))
        
        target_id = test_create_target()
        results.append(("Create Target", target_id is not None))
        
        results.append(("List Sources", test_list_sources()))
        results.append(("List Targets", test_list_targets()))
        
        if source_id:
            results.append(("Import Properties", test_import_properties(source_id)))
            
            if target_id:
                results.append(("Sync Properties", test_sync_properties(source_id, target_id)))
            
            results.append(("Get Source Properties", test_get_source_properties(source_id)))
        
        target_property_id = None
        if target_id:
            target_property_id = test_get_target_properties(target_id)
            results.append(("Get Target Properties", target_property_id is not None))
        
        developer_id = test_create_developer()
        results.append(("Create Developer", developer_id is not None))
        
        results.append(("List Developers", test_list_developers()))
        
        if developer_id:
            development_id = test_create_development(developer_id)
            results.append(("Create Development", development_id is not None))
        
        results.append(("List Developments", test_list_developments()))
        
        # Print summary
        print_section("TEST SUMMARY")
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{status:12} - {test_name}")
        
        print(f"\n{'='*60}")
        print(f"  Results: {passed}/{total} tests passed")
        print(f"{'='*60}\n")
        
        return passed == total
        
    finally:
        # Always run cleanup, even if tests fail
        cleanup_resources()


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server")
        print("   Make sure the server is running:")
        print("   uvicorn sync_manager.api:app --reload")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        exit(1)
''',
}

# Write each module
for filename, content in modules.items():
    # test_api.py goes to project root, other modules go to sync_manager/
    if filename == "test_api.py":
        (project_root / filename).write_text(content, encoding='utf-8')
        print(f"[OK] Created: {filename}")
    else:
        (project_root / "sync_manager" / filename).write_text(content, encoding='utf-8')
        print(f"[OK] Created: sync_manager/{filename}")

# Continue with CLI and other files...
cli_content = '''import argparse
import json
from pathlib import Path
from .database import init_db
from .models import Tenant
from .database import get_db
from .sync_service import SyncService
import secrets


def generate_api_key():
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)


def init_command():
    """Initialize the database"""
    print("Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")


def create_tenant_command(name: str):
    """Create a new tenant"""
    api_key = generate_api_key()
    
    with get_db() as db:
        tenant = Tenant(name=name, api_key=api_key)
        db.add(tenant)
        db.flush()
        
        print(f"✅ Tenant created successfully!")
        print(f"   ID: {tenant.id}")
        print(f"   Name: {tenant.name}")
        print(f"   API Key: {api_key}")
        print(f"\\n⚠️  Save this API key securely - it won't be shown again!")


def import_json_command(tenant_id: int, source_id: int, json_file: str):
    """Import JSON file to source"""
    data = json.loads(Path(json_file).read_text())
    
    sync_service = SyncService(tenant_id)
    result = sync_service.import_json_to_source(source_id, data)
    
    print(f"✅ Import completed!")
    print(f"   Status: {result['status']}")
    print(f"   Stats: {result.get('stats', {})}")


def sync_command(tenant_id: int, source_id: int, target_id: int):
    """Sync source to target"""
    sync_service = SyncService(tenant_id)
    result = sync_service.sync_source_to_target(source_id, target_id)
    
    print(f"✅ Sync completed!")
    print(f"   Status: {result['status']}")
    print(f"   Stats: {result.get('stats', {})}")


def cleanup_command(tenant_id: int, days: int = None):
    """Cleanup old snapshots"""
    sync_service = SyncService(tenant_id)
    sync_service.cleanup_old_snapshots(days)
    print(f"✅ Cleanup completed!")


def main():
    parser = argparse.ArgumentParser(description="Sync Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    subparsers.add_parser("init", help="Initialize database")
    
    tenant_parser = subparsers.add_parser("create-tenant", help="Create a new tenant")
    tenant_parser.add_argument("name", help="Tenant name")
    
    import_parser = subparsers.add_parser("import", help="Import JSON to source")
    import_parser.add_argument("tenant_id", type=int, help="Tenant ID")
    import_parser.add_argument("source_id", type=int, help="Source ID")
    import_parser.add_argument("json_file", help="Path to JSON file")
    
    sync_parser = subparsers.add_parser("sync", help="Sync source to target")
    sync_parser.add_argument("tenant_id", type=int, help="Tenant ID")
    sync_parser.add_argument("source_id", type=int, help="Source ID")
    sync_parser.add_argument("target_id", type=int, help="Target ID")
    
    cleanup_parser = subparsers.add_parser("cleanup", help="Cleanup old snapshots")
    cleanup_parser.add_argument("tenant_id", type=int, help="Tenant ID")
    cleanup_parser.add_argument("--days", type=int, help="Days to keep (default from config)")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_command()
    elif args.command == "create-tenant":
        create_tenant_command(args.name)
    elif args.command == "import":
        import_json_command(args.tenant_id, args.source_id, args.json_file)
    elif args.command == "sync":
        sync_command(args.tenant_id, args.source_id, args.target_id)
    elif args.command == "cleanup":
        cleanup_command(args.tenant_id, args.days)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
'''
(project_root / "sync_manager" / "cli.py").write_text(cli_content, encoding='utf-8')
print("[OK] Created: sync_manager/cli.py")

# Create .env.example
env_example = '''# Database connection URL
DATABASE_URL=postgresql://username:password@localhost:5432/sync_manager

# Snapshot retention period in days
RETENTION_DAYS=30
'''
(project_root / ".env.example").write_text(env_example, encoding='utf-8')
print("[OK] Created: .env.example")

# Create README.md
readme_content = '''# Sync Manager

Multi-tenant property synchronization management system with PostgreSQL backend.

## Features

- ✅ Multi-tenant architecture with API key authentication
- ✅ Source and Target management
- ✅ Property synchronization with change detection
- ✅ Manual change tracking and warnings
- ✅ Snapshot retention with configurable cleanup
- ✅ JSON import support
- ✅ PATCH support for target properties
- ✅ Batch operations
- ✅ RESTful API with FastAPI
- ✅ CLI for management operations

## Quick Start

### 1. Install Dependencies

Using pip:
```bash
pip install -e .
```

Using uv:
```bash
uv sync
```

### 2. Configure Database

```bash
cp .env.example .env
# Edit .env with your PostgreSQL DATABASE_URL
```

### 3. Initialize

```bash
python -m sync_manager.cli init
python -m sync_manager.cli create-tenant "My Company"
```

Save the API key displayed!

### 4. Start API Server

```bash
uvicorn sync_manager.api:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

## CLI Commands

```bash
# Initialize database
python -m sync_manager.cli init

# Create tenant
python -m sync_manager.cli create-tenant "Company Name"

# Import JSON
python -m sync_manager.cli import <tenant_id> <source_id> data.json

# Sync properties
python -m sync_manager.cli sync <tenant_id> <source_id> <target_id>

# Cleanup snapshots
python -m sync_manager.cli cleanup <tenant_id> --days 30
```

## API Endpoints

All endpoints (except `/health` and `POST /tenants`) require `X-API-Key` header.

- `GET /health` - Health check
- `POST /tenants` - Create tenant
- `POST /sources` - Create source
- `POST /targets` - Create target
- `GET /sources` - List sources
- `GET /targets` - List targets
- `POST /sources/{id}/import` - Import JSON data
- `POST /sync/{source_id}/{target_id}` - Sync properties
- `GET /sources/{id}/properties` - List source properties
- `GET /targets/{id}/properties` - List target properties
- `PATCH /targets/{id}/properties/{prop_id}` - Update property
- `DELETE /sources/{id}` - Delete source
- `DELETE /targets/{id}` - Delete target
- `POST /cleanup` - Cleanup snapshots

## Architecture

### Database Tables

- **tenants** - Tenant workspaces
- **sources** - Data sources (JSON, scraped, manual)
- **targets** - Destination systems (websites, APIs)
- **source_properties** - Properties in sources
- **target_properties** - Properties in targets (with manual change tracking)
- **source_snapshots** - Historical source versions
- **target_snapshots** - Historical target versions
- **sync_logs** - Synchronization audit logs

### Multi-Tenancy

- Each tenant has isolated data via `tenant_id`
- API key authentication per tenant
- All queries filtered by tenant context
- Cascade deletes maintain referential integrity

### Manual Changes

When a target property is modified manually:
1. System detects hash difference
2. Sets `has_manual_changes` flag
3. Adds warning message
4. Skips automatic synchronization
5. Requires manual resolution

### Snapshot Retention

- Snapshots created before updates
- Configurable retention period (default 30 days)
- Cleanup via CLI or API
- Can schedule with cron/nightly job

## Development

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

## License

MIT License
'''
(project_root / "README.md").write_text(readme_content, encoding='utf-8')
print("[OK] Created: README.md")

print("\n" + "="*60)
print("Independent Sync Manager project created!")
print("="*60)
print(f"\nProject location: {project_root.absolute()}")
print("\nNext steps:")
print(f"1. cd {project_root.name}")
print("2. pip install -e . (or: uv sync)")
print("3. cp .env.example .env")
print("4. python -m sync_manager.cli init")
print("5. python -m sync_manager.cli create-tenant 'My Company'")
print("6. uvicorn sync_manager.api:app --reload")
print("="*60)
