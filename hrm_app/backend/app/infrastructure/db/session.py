"""Database engine + session factory + table creation."""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..config import settings
from .models import Base

engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    """Create tables if they do not exist (core-phase; Alembic can replace later)."""
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return SessionLocal()
