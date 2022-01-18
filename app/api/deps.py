"""FastAPI deepndencies."""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBearer

from app.db.database import DB
from common.security_utils import validate_http_bearer_token
from config import current_config as CC


def get_db():
    """Get db session obj."""
    db = DB(CC.POSTGRES_ZATTOO_READ_WRITE)
    try:
        yield db.get_session()
    finally:
        db.close_session()


def authorize_http_bearer_token(token: HTTPBasicCredentials = Depends(HTTPBearer())):
    """Validate the token."""
    if validate_http_bearer_token(token.credentials):
        return True
    raise HTTPException(status_code=401, detail="Not authenticated")
