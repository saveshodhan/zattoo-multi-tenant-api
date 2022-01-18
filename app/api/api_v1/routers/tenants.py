"""APIRouter to multiple tenants."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_tenants
from app.schemas import tenant_schemas


router = APIRouter()


@router.get("/tenants", response_model=List[str])
async def get_tenants(
    db: Session = Depends(deps.get_db)
):
    """Get all tenant ids.."""
    data = await crud_tenants.get_tenants(db)
    return [
        tenant_schemas.TenantSchema.from_orm(x).tenant_id
        for x in data   # this is required coz we need a flat list of tenant_ids
    ]


@router.get("/tenants/{tenant_id}", response_model=tenant_schemas.TenantDetailedSchema)
async def get_single_tenant(
    tenant_id: str,
    db: Session = Depends(deps.get_db)
):
    """Get a single tenant."""
    try:
        return await crud_tenants.get_single_tenant(db, tenant_id)
    except NoResultFound as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.post("/tenants", response_model=tenant_schemas.TenantDetailedSchema)
async def add_single_tenant(
    tenant_obj: tenant_schemas.TenantPostSchema,
    db: Session = Depends(deps.get_db)
):
    """Add a new tenant.."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/tenants/{tenant_id}", status_code=204)
async def update_single_tenant(
    tenant_obj: tenant_schemas.TenantPutSchema,
    db: Session = Depends(deps.get_db),
):
    """Update an existing tenant."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/tenants/{tenant_id}", status_code=204)
async def delete_single_tenant(
    tenant_id: str,
    db: Session = Depends(deps.get_db)
):
    """Delete a tenant."""
    raise HTTPException(status_code=501, detail="Not implemented")
