"""Tenant schemas."""

from datetime import datetime as dt

from pydantic import BaseModel


class TenantBaseSchema(BaseModel):
    """Base schema for Tenant."""

    class Config:
        """Config."""

        orm_mode = True


class TenantSchema(TenantBaseSchema):
    """Schema to GET Tenant.

    Mostly used to get all tenants, with minimum data.
    """

    tenant_id: str


class TenantDetailedSchema(TenantSchema):
    """Schema to GET details of Tenant.

    Mostly to get details of a single tenant, hence has most of the info.
    """

    tenant_number: int
    tenant_info: dict
    created_at: dt
    updated_at: dt


class TenantPostSchema(TenantBaseSchema):
    """Schema for adding a new Tenant (POST)."""

    tenant_info: dict


class TenantPutSchema(TenantBaseSchema):
    """Schema for updating an existing Tenant (PUT)."""

    tenant_info: dict
