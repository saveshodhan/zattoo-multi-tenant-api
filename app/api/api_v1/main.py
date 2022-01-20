"""Main web app file."""

from functools import partial

from fastapi import Depends, FastAPI

from app.api import deps
from app.api.api_v1.routers import probes, tenants

APP_VERSION = "v1"
ROUTE_PREFIX = f"/api/{APP_VERSION}"

app = FastAPI(
    title="Zattoo multi-tenant API",
    description="Zattoo multi-tenant API.",
    version=APP_VERSION,
)

route_include = partial(
    app.include_router,
    prefix=ROUTE_PREFIX,
    dependencies=[Depends(deps.authorize_http_bearer_token)],
)

route_include(probes.router, tags=["probes"])
route_include(tenants.router, tags=["tenants"])
