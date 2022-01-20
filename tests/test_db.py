"""Test cases for databse."""

import pytest
from sqlalchemy.exc import ProgrammingError

from common.db_utils import DBUtils


class TestDBUtils:
    """Test DBUtils."""

    def test_init(self):
        """Test __init__."""
        dbu = DBUtils("postgresql+psycopg2://postgres:postgres@localhost/zattoo")
        assert dbu.db_url_without_db == "postgresql+psycopg2://postgres:postgres@localhost"

    def test_create_db(self, mock_dsn):
        """Test create_db negative case."""
        dbu = DBUtils(mock_dsn)
        with pytest.raises(ProgrammingError):
            dbu.create_db(ignore_exists=False)
