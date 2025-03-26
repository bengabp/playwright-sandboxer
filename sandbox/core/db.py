# app/core/db.py
from sqlalchemy import create_engine # Changed import
from sqlalchemy.orm import sessionmaker, declarative_base, Session # Changed imports
from sandbox.core.config import settings
import logging

# --- Remove async logging config if you added it ---

# Create the SYNCHRONOUS engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False, # Set to True for debugging SQL
    pool_recycle=3600
)

# Create the SYNCHRONOUS session factory
# autocommit=False, autoflush=False are standard defaults for sessionmaker
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Base class for SQLAlchemy models (no change needed)
Base = declarative_base()

# Dependency to get DB session (SYNCHRONOUS version)
def get_db() -> Session: # Changed return type hint
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Ensure session is closed