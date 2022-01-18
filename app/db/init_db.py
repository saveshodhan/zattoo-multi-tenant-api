"""Initialise the database."""

from urllib.parse import urlparse

from psycopg2.errors import DuplicateDatabase
from sqlalchemy.exc import ProgrammingError

from app.db.database import DB
from app.models.models import DeclarativeBase   # has to be imported from models


class DBUtils:
    """Create or drop databse."""

    def __init__(self, db_url):
        """Init."""
        self.db_url = db_url
        self.url_parsed = urlparse(db_url)
        self.db_url_without_db = f"{self.url_parsed.scheme}://{self.url_parsed.netloc}"

    def create_db(self, ignore_exists=True):
        """Create databse."""
        db = DB(self.db_url_without_db)
        engine = db._create_engine()
        try:
            with engine.connect() as conn:
                conn.execute("COMMIT")
                conn.execute(f"CREATE DATABASE {self.url_parsed.path.lstrip('/')}")
                conn.execute("COMMIT")
        except ProgrammingError as exc:
            if isinstance(exc.orig, DuplicateDatabase) and ignore_exists:
                pass
            else:
                raise
        return True

    def create_tables(self):
        """Create tables."""
        db = DB(self.db_url)
        engine = db._create_engine()
        DeclarativeBase.metadata.create_all(bind=engine)
        return db

    def kill_idling_connections(self, conn):
        """Kill `idle` and `idle in transaction` connections."""
        query = f"""
        SELECT pg_terminate_backend(pid) FROM pg_stat_activity
        WHERE datname = '{self.url_parsed.path.lstrip("/")}'
        AND pid <> pg_backend_pid()
        """
        conn.execute(query)
        conn.execute("COMMIT")
        return True

    # def drop_database(self):
    #     """Drop databse."""
    #     db = DB(self.db_url_without_db)
    #     engine = db._create_engine()
    #     with engine.connect() as conn:
    #         conn.execute("COMMIT")
    #         self.kill_idling_connections(conn)
    #         conn.execute(f"DROP DATABASE IF EXISTS {self.url_parsed.path.lstrip('/')}")
    #         conn.execute("COMMIT")
    #     return True
