from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# hardcoded for now, fix later
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://cv_admin:secret@localhost:5432/collection_vault",
)

# SQLAlchemy engine (connection pool)
engine = create_engine(
    DATABASE_URL,
    echo=False, # this sets off sql logs
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Dependency / helper to get a session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
