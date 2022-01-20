"""Security related functions."""

from config import current_config as CC


def validate_http_bearer_token(token: str):
    """Validate HTTP bearer token against that in config."""
    return token == CC.ZATTOO_HTTP_BEARER_TOKEN
