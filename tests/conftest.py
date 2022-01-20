"""Pytest fixtures for app."""

from fastapi.testclient import TestClient
import pytest
from testing.postgresql import Postgresql as TestPostgresql

from app.api.api_v1.main import app, ROUTE_PREFIX
from app.api.deps import get_db
from common.db_utils import DBUtils
from config import current_config as CC


@pytest.fixture(scope="session")
def _data():
    """Create a fixture to store data to be moved across tests."""
    yield {
        "test_data": [
            {
                "tenant_id": "1_Jacklyn91",
                "tenant_info": {
                    "email": "keaton_schuster33@hotmail.com",
                    "address": "30261 Tania Track, Kossside, 24443, Angola",
                    "description": "Velit delectus non."
                }
            },
            {
                "tenant_id": "2_Jasmin.Mann34",
                "tenant_info": {
                    "email": "audra.parisian@hotmail.com",
                    "address": "418 Kellen Corners, North Harrymouth, 25205-3294, Liechtenstein",
                    "description": "Itaque eaque et illum."
                }
            },
        ]
    }


@pytest.fixture(scope="session")
def mock_dsn():
    """Mock Postgres db dsn."""
    with TestPostgresql() as test_psql:
        yield test_psql.url()


@pytest.fixture(scope="session")
def mock_db(mock_dsn):
    """Mock the callable from deps for db."""
    db_utils = DBUtils(mock_dsn)
    db = db_utils.create_tables()

    def get_test_db():
        try:
            yield db.get_session()
        finally:
            db.close_session()
    yield get_test_db


@pytest.fixture(scope="session")
def mock_auth_token():
    """Mock HTTP Bearer token."""
    CC.ZATTOO_HTTP_BEARER_TOKEN = "youcantseeme"
    return CC.ZATTOO_HTTP_BEARER_TOKEN


@pytest.fixture(scope="session")
def test_app(mock_db, mock_auth_token):
    """Create a test FastAPI app with mocked postgres db."""
    app.dependency_overrides[get_db] = mock_db
    test_app = TestClient(app)
    test_app.headers["Authorization"] = f"Bearer {mock_auth_token}"
    test_app.base_url += ROUTE_PREFIX
    test_app.base_url = test_app.base_url.rstrip("/") + "/"     # making sure base_url has 1 and only 1 "/"
    # "/" is required coz TestClient performs a `urljoin` on base_url and url, and to make the ROUTE_PREFIX included in
    # the base_url we need "/" in the end else it wont consider it as part of the path.
    # also, to have the route appended to this extended base_url, we need to remove the "/" from the beginning of the
    # route in the test cases ahead.
    # https://stackoverflow.com/a/10893427/4260095
    yield test_app
