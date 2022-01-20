"""Models for database."""

from datetime import datetime as dt

from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase = declarative_base()


class Tenant(DeclarativeBase):
    """Tenant table."""

    __tablename__ = "tenant"

    tenant_number = Column(Integer, primary_key=True)
    tenant_id = Column(String, nullable=False)
    tenant_info = Column(JSONB, default={})
    created_at = Column(DateTime, default=dt.now())
    updated_at = Column(DateTime, default=dt.now())

    __table_args__ = (
        UniqueConstraint("tenant_id", name="uix__tenant_id"),
    )
