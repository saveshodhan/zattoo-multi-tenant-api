"""Crud functions related to tenants."""

from app.models.models import Tenant


async def get_single_tenant(db, tenant_number):
    """Return a single tenant."""
    return db.query(Tenant).\
        filter(Tenant.tenant_number == tenant_number).\
        one()


async def get_tenants(db):
    """Get all tenants."""
    return db.query(Tenant).all()


# async def add_single_tenant(db, tenant_obj):
#     """Add new tenant to the db."""
#     tenant = Tenant(**tenant_obj)
#     db.add(tenant)
#     db.commit()
#     return tenant


# async def update_single_tenant(db, tenant_number, tenant_update_dict):
#     """Update a given tenant's fields as allowed in TenantPutSchema."""
#     tenant = db.query(Tenant).filter(Tenant.tenant_number == tenant_number).one()
#     for key, val in tenant_update_dict.items():
#         # the update obj should have `exclude_unset=True` by caller, to avoid null values updated in db
#         setattr(tenant, key, val)
#     db.commit()
#     return True


# async def delete_single_tenant(db, tenant_number):
#     """Delete single tenant from the db."""
#     db.delete(
#         db.query(Tenant).filter(Tenant.tenant_number == tenant_number).one()
#     )
#     db.commit()
#     return True
