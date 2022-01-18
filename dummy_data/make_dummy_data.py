"""Populate dummy data into db."""

import json
from pathlib import Path

from app.db.init_db import DBUtils
from app.models.models import Tenant
from config import current_config as CC


# MOCK_DATA_URL = "https://61e6d457ce3a2d00173594a3.mockapi.io/tenant"


def make_data():
    """Make data to be inserted into db."""
    data_file = Path(__file__).parent / "dummy_data.json"
    data = json.load(open(data_file))
    for each in data:
        each.pop("id")
        each["tenant_info"] = {
            "email": each.pop("email").lower(),
            "address": ", ".join(each.pop("address")),
            "description": each.pop("desc"),
        }
    return data


def insert_tenants(session, data):
    """Populate tenant table."""
    for each in data:
        t = Tenant(**each)
        session.add(t)
    session.commit()


def update_tenants(session):
    """Update tenant_id by adding tenant_number in the beginning."""
    tenants = session.query(Tenant).all()
    for tenant in tenants:
        tenant.tenant_id = f"{tenant.tenant_number}_{tenant.tenant_id}"
    session.commit()


def main():
    """Run main func."""
    dummy_data = make_data()
    db_utils = DBUtils(CC.POSTGRES_ZATTOO_READ_WRITE)
    db_utils.create_db()
    db = db_utils.create_tables()
    session = db.get_session()
    insert_tenants(session, dummy_data)
    update_tenants(session)


if __name__ == "__main__":
    main()
