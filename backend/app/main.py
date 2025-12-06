"""
FastAPI ana uygulama dosyası
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infra.db import init_db
from app.api import routes_upload, routes_results
from app.config.settings import settings


# FastAPI app instance
app = FastAPI(
    title="CV Detector API",
    description="CV dosyalarından teknoloji ve bilgi çıkarma API'si",
    version="1.0.0"
)

# CORS middleware - frontend ile iletişim için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik domain'ler eklenebilir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event - DB tablolarını oluştur
@app.on_event("startup")
def startup_event():
    """Uygulama başlangıcında çalışır"""
    print("🚀 CV Detector API başlatılıyor...")
    init_db()
    print("✅ Veritabanı hazır")


# Health check endpoint
@app.get("/api/health")
def health_check():
    """
    Health check endpoint
    
    Returns:
        Dict: {"status": "ok"}
    """
    return {"status": "ok"}


# API router'larını ekle
app.include_router(
    routes_upload.router,
    prefix=settings.API_PREFIX,
    tags=["upload"]
)

app.include_router(
    routes_results.router,
    prefix=settings.API_PREFIX,
    tags=["results"]
)


# Root endpoint
@app.get("/")
def root():
    """
    Root endpoint
    
    Returns:
        Dict: API bilgisi
    """
    return {
        "message": "CV Detector API",
        "version": "1.0.0",
        "docs": "/docs"
    }