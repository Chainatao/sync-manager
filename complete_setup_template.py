"""
Complete setup script for independent Sync Manager project
This file will be copied into the sync_manager_project directory
"""
import sys
from pathlib import Path

# Get the project root
project_root = Path(__file__).parent
sync_manager_dir = project_root / "sync_manager"

print("🚀 Completing Sync Manager Setup...")
print("="*60)

# Create sync_service.py
sync_service_content = '''from datetime import datetime, timedelta
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
'''

(sync_manager_dir / "sync_service.py").write_text(sync_service_content)
print("✅ Created: sync_manager/sync_service.py")

# Create api.py
api_content = '''from fastapi import FastAPI, Depends, HTTPException, Header
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .models import Tenant, Source, Target, SourceProperty, TargetProperty
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


def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key and return tenant"""
    with get_db() as db:
        tenant = db.query(Tenant).filter(Tenant.api_key == x_api_key).first()
        if not tenant:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return tenant


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
async def create_source(source: SourceCreate, tenant: Tenant = Depends(verify_api_key)):
    """Create a new source"""
    with get_db() as db:
        new_source = Source(
            tenant_id=tenant.id,
            name=source.name,
            type=source.type,
            config=source.config
        )
        db.add(new_source)
        db.flush()
        
        return {"id": new_source.id, "name": new_source.name, "type": new_source.type}


@app.post("/targets")
async def create_target(target: TargetCreate, tenant: Tenant = Depends(verify_api_key)):
    """Create a new target"""
    with get_db() as db:
        new_target = Target(
            tenant_id=tenant.id,
            name=target.name,
            type=target.type,
            config=target.config
        )
        db.add(new_target)
        db.flush()
        
        return {"id": new_target.id, "name": new_target.name, "type": new_target.type}


@app.get("/sources")
async def list_sources(tenant: Tenant = Depends(verify_api_key)):
    """List all sources for tenant"""
    with get_db() as db:
        sources = db.query(Source).filter(Source.tenant_id == tenant.id).all()
        return [{"id": s.id, "name": s.name, "type": s.type, "is_active": s.is_active} for s in sources]


@app.get("/targets")
async def list_targets(tenant: Tenant = Depends(verify_api_key)):
    """List all targets for tenant"""
    with get_db() as db:
        targets = db.query(Target).filter(Target.tenant_id == tenant.id).all()
        return [{"id": t.id, "name": t.name, "type": t.type, "is_active": t.is_active} for t in targets]


@app.post("/sources/{source_id}/import")
async def import_to_source(
    source_id: int,
    import_data: PropertyImport,
    tenant: Tenant = Depends(verify_api_key)
):
    """Import JSON data to a source"""
    sync_service = SyncService(tenant.id)
    result = sync_service.import_json_to_source(source_id, import_data.data)
    return result


@app.post("/sync/{source_id}/{target_id}")
async def sync_properties(
    source_id: int,
    target_id: int,
    tenant: Tenant = Depends(verify_api_key)
):
    """Sync properties from source to target"""
    sync_service = SyncService(tenant.id)
    result = sync_service.sync_source_to_target(source_id, target_id)
    return result


@app.get("/sources/{source_id}/properties")
async def list_source_properties(
    source_id: int,
    tenant: Tenant = Depends(verify_api_key)
):
    """List properties in a source"""
    with get_db() as db:
        properties = db.query(SourceProperty).join(Source).filter(
            Source.id == source_id,
            Source.tenant_id == tenant.id
        ).all()
        return [{"id": p.id, "external_id": p.external_id, "data": p.data} for p in properties]


@app.get("/targets/{target_id}/properties")
async def list_target_properties(
    target_id: int,
    tenant: Tenant = Depends(verify_api_key)
):
    """List properties in a target"""
    with get_db() as db:
        properties = db.query(TargetProperty).join(Target).filter(
            Target.id == target_id,
            Target.tenant_id == tenant.id
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
    tenant: Tenant = Depends(verify_api_key)
):
    """Patch a target property (marks it as manually changed)"""
    sync_service = SyncService(tenant.id)
    
    with get_db() as db:
        prop = db.query(TargetProperty).join(Target).filter(
            TargetProperty.id == property_id,
            TargetProperty.target_id == target_id,
            Target.tenant_id == tenant.id
        ).first()
        
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        
        prop.data.update(patch.data)
        sync_service.mark_manual_changes(property_id)
        
        return {"status": "updated", "id": prop.id}


@app.delete("/sources/{source_id}")
async def delete_source(source_id: int, tenant: Tenant = Depends(verify_api_key)):
    """Delete a source"""
    with get_db() as db:
        source = db.query(Source).filter(
            Source.id == source_id,
            Source.tenant_id == tenant.id
        ).first()
        
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        
        db.delete(source)
        return {"status": "deleted"}


@app.delete("/targets/{target_id}")
async def delete_target(target_id: int, tenant: Tenant = Depends(verify_api_key)):
    """Delete a target"""
    with get_db() as db:
        target = db.query(Target).filter(
            Target.id == target_id,
            Target.tenant_id == tenant.id
        ).first()
        
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
'''

(sync_manager_dir / "api.py").write_text(api_content)
print("✅ Created: sync_manager/api.py")

print("\nRun complete_modules_setup.py to finish...")
