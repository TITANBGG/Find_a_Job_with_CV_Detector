"""
Veritabanı bağlantısı ve session yönetimi
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite için gerekli
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Database session dependency for FastAPI
    Her request için yeni bir session oluşturur ve sonunda kapatır
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Veritabanı tablolarını oluştur
    Uygulama başlangıcında çağrılmalı
    """
    from app.infra.models import Resume, Analysis  # Import models
    Base.metadata.create_all(bind=engine)