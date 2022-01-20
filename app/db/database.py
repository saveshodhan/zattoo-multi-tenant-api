"""Database related."""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DB:
    """Main class for db and connection management."""

    def __init__(self, db_url, autocommit=False, autoflush=False):
        """Initialise."""
        self.db_url = db_url
        self.autocommit = autocommit
        self.autoflush = autoflush

    def _create_engine(self):
        self.engine = create_engine(
            self.db_url,
            echo=False,
            max_overflow=5,
            pool_size=20,
            pool_timeout=10,
            pool_recycle=3600
        )
        return self.engine

    def _create_session(self):
        self._create_engine()
        self.scoped_session = scoped_session(sessionmaker(
            autocommit=self.autocommit,
            autoflush=self.autoflush,
            expire_on_commit=False,
            bind=self.engine
        ))
        return self.scoped_session

    def get_session(self):
        """Return a session obj if created, or create one and return."""
        if hasattr(self, "scoped_session"):
            return self.scoped_session
        return self._create_session()

    def close_session(self):
        """Close db session."""
        self.scoped_session.close()
        delattr(self, "scoped_session")
