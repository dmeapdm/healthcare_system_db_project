"""
Sesión de base de datos vía SQLAlchemy, usando el driver pymysql (el mismo
que ya usa 16_import_elomed_data.py) para hablar con healthcare_system_db.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset=utf8mb4"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency de FastAPI: entrega una sesión por request y la cierra
    siempre al terminar, haya error o no."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
