"""Run the main application."""

import uvicorn

from app.api.api_v1.main import app     # noqa; F401
from config import current_config as CC


def web_config():
    """Make config required for web app.

    Also, putting it in a separate function helps in testing it.
    """
    return {
        "host": CC.HOST,
        "port": int(CC.PORT),
        "debug": CC.DEBUG,
        "reload": CC.DEBUG,
        "workers": 1,
        "log_level": "trace" if CC.DEBUG else "info",
    }


if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("run:app", **web_config())
