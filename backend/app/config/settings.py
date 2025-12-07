"""
Uygulama ayarları ve yapılandırma
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Proje kök dizini
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Uygulama ayarları"""
    
    # Base directory (job_postings.json için gerekli)
    BASE_DIR: Path = BASE_DIR
    
    # Veritabanı
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/app.db"
    
    # Dosya yükleme
    STORAGE_DIR: Path = BASE_DIR / "storage" / "resumes"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}
    
    # Teknoloji sözlüğü
    TECH_DICT_PATH: Path = BASE_DIR / "app" / "config" / "tech_dictionary.json"
    
    # API
    API_PREFIX: str = "/api"
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()

# Storage dizinini oluştur
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)