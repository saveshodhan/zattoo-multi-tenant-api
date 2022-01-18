"""Test cases for Zattoo web app."""

from run import web_config


class TestProbesRoutes:
    """Test routes in `probes`."""

    def test_ping(self, test_app):
        """Test ping response."""
        response = test_app.get("ping")
        assert response.json() == {"status": True, "message": "pong"}


class TestAuth:
    """Test auth."""

    def test_bad_auth_token(self, test_app):
        """Test authorization by passing bad token."""
        response = test_app.get("tenants/1", headers={"Authorization": "Bearer youcanseeme"})
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_no_auth_token(self, test_app):
        """Test authorization by passing no token."""
        response = test_app.get("tenants/1", headers={"Authorization": "Bearer"})
        assert response.status_code == 403
        assert response.json() == {"detail": "Not authenticated"}


def test_web_config():
    """Test web_config."""
    from config import current_config as CC
    CC.HOST = "somehost"
    CC.PORT = "3142"
    CC.DEBUG = True
    old_env = CC.ENV
    CC.ENV = "local"

    expected_config = {
        "host": "somehost",
        "port": 3142,
        "debug": True,
        "reload": True,
        "workers": 1,
        "log_level": "trace",
    }
    config = web_config()
    assert config == expected_config

    CC.ENV = old_env
