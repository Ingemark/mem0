from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from openmemory.api.config.settings import get_settings
from openmemory.api.app.models import Base

settings = get_settings()

DATABASE_URL = settings.database_url
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment")

SCHEMA_NAME = settings.schema_name
if not SCHEMA_NAME:
    raise RuntimeError("SCHEMA_NAME is not set in environment")

if not settings.user_id:
    raise RuntimeError("USER_ID is not set in environment")

if not settings.app_id:
    raise RuntimeError("APP_ID is not set in environment")

# SQLAlchemy engine & session
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "options": f"-csearch_path={SCHEMA_NAME},public"
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
