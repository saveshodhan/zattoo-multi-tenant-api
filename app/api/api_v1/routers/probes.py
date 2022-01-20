"""APIRouter to manage different probe routes for liveness, health-check, etc.."""

from fastapi import APIRouter


router = APIRouter()


@router.get("/ping")
async def ping_check():
    """Ping check (liveness).

    Returns:
        {dict}
    """
    return {"status": True, "message": "pong"}
