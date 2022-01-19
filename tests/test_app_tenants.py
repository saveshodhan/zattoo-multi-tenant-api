"""Test cases for tenants."""

from app.schemas import tenant_schemas
from app.crud.crud_tenants import add_single_tenant
from app.models.models import Tenant
from app.schemas.tenant_schemas import TenantDetailedSchema


def get_all_tenants(test_app):
    """Get all tenant."""
    return test_app.get("tenants")


class TestTenantRoutes:
    """Test routes in `tenants`."""

    def test_add_tenants_for_tests(self, _data, mock_db, test_app):
        """Add new tenants to db for further tests.

        This is required as the POST route is not yet implemented.
        """
        db = next(mock_db())
        for each in _data["test_data"]:
            t = Tenant(**each)
            db.add(t)
        db.commit()

        response = test_app.post("tenants", json=_data["test_data"][0])
        assert response.status_code == 501, response.text
        assert response.json() == {"detail":"Not implemented"}

    def test_get_all_tenants(self, test_app, mock_db):
        """Test all tenants response."""
        response = get_all_tenants(test_app)
        assert response.status_code == 200, response.text
        assert response.json() == ["1_Jacklyn91", "2_Jasmin.Mann34"]

    def test_get_single_tenant(self, _data, test_app):
        """Get a single tenant."""
        response = test_app.get("tenants/1")
        assert TenantDetailedSchema.validate(response.json())

    def test_get_tenant_bad(self, test_app):
        """Get a bad tenant."""
        response = test_app.get("tenants/-1")
        assert response.status_code == 404, response.text

    def test_update_tenant(self, test_app):
        """Update an tenant."""
        response = test_app.put("tenants/1", json={"tenant_info": {"foo": "bar"}})
        assert response.status_code == 501, response.text
        assert response.json() == {"detail":"Not implemented"}

    def test_delete_tenant(self, test_app):
        """Delete an tenant."""
        response = test_app.delete(f"tenants/1")
        assert response.status_code == 501, response.text
        assert response.json() == {"detail":"Not implemented"}

