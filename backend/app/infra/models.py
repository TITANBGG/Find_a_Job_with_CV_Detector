"""
SQLAlchemy veritabanı modelleri
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.infra.db import Base


class Resume(Base):
    """CV dosyası modeli"""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    analyses = relationship("Analysis", back_populates="resume")
    
    def __repr__(self):
        return f"<Resume(id={self.id}, filename={self.original_filename})>"


class Analysis(Base):
    """CV analiz sonuçları modeli"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String(36), unique=True, nullable=False, index=True)  # UUID
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    
    # Status: PENDING, PROCESSING, DONE, FAILED
    status = Column(String(20), default="PENDING", nullable=False)
    
    # JSON stringler - SQLite için text olarak saklanıyor
    tech_json = Column(Text, nullable=True)  # Teknolojiler
    emails_json = Column(Text, nullable=True)  # Email listesi
    phones_json = Column(Text, nullable=True)  # Telefon listesi
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    resume = relationship("Resume", back_populates="analyses")
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, analysis_id={self.analysis_id}, status={self.status})>"