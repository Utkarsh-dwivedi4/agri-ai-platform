from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# ✅ Handle declarative_base import for different SQLAlchemy versions
try:
    from sqlalchemy.orm import declarative_base  # for SQLAlchemy >= 1.4
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base  # fallback for older versions

from .config import DATABASE_URL

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,         # Set True if you want SQL logs
    future=True
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base class for models
Base = declarative_base()
