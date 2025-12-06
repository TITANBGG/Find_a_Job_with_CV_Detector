"""
Veritabanı repository katmanı - CRUD işlemleri
"""
from sqlalchemy.orm import Session
from app.infra.models import Resume, Analysis
from typing import Optional


class ResumeRepository:
    """Resume CRUD işlemleri"""
    
    @staticmethod
    def create(session: Session, file_path: str, original_filename: str) -> Resume:
        """
        Yeni bir CV kaydı oluştur
        
        Args:
            session: DB session
            file_path: Sunucudaki dosya yolu
            original_filename: Orijinal dosya adı
            
        Returns:
            Oluşturulan Resume objesi
        """
        resume = Resume(
            file_path=file_path,
            original_filename=original_filename
        )
        session.add(resume)
        session.commit()
        session.refresh(resume)
        return resume
    
    @staticmethod
    def get_by_id(session: Session, resume_id: int) -> Optional[Resume]:
        """
        ID'ye göre CV kaydını getir
        
        Args:
            session: DB session
            resume_id: Resume ID
            
        Returns:
            Resume objesi veya None
        """
        return session.query(Resume).filter(Resume.id == resume_id).first()


class AnalysisRepository:
    """Analysis CRUD işlemleri"""
    
    @staticmethod
    def create(session: Session, resume_id: int, analysis_id: str, status: str = "PENDING") -> Analysis:
        """
        Yeni bir analiz kaydı oluştur
        
        Args:
            session: DB session
            resume_id: İlgili Resume ID
            analysis_id: Benzersiz analiz ID (UUID)
            status: Başlangıç durumu
            
        Returns:
            Oluşturulan Analysis objesi
        """
        analysis = Analysis(
            analysis_id=analysis_id,
            resume_id=resume_id,
            status=status
        )
        session.add(analysis)
        session.commit()
        session.refresh(analysis)
        return analysis
    
    @staticmethod
    def update_with_results(
        session: Session,
        analysis_id: str,
        status: str,
        tech_json: str,
        emails_json: str,
        phones_json: str
    ) -> Optional[Analysis]:
        """
        Analiz sonuçlarını güncelle
        
        Args:
            session: DB session
            analysis_id: Analiz ID
            status: Yeni durum
            tech_json: Teknolojiler JSON string
            emails_json: Emailler JSON string
            phones_json: Telefonlar JSON string
            
        Returns:
            Güncellenen Analysis objesi veya None
        """
        analysis = session.query(Analysis).filter(
            Analysis.analysis_id == analysis_id
        ).first()
        
        if analysis:
            analysis.status = status
            analysis.tech_json = tech_json
            analysis.emails_json = emails_json
            analysis.phones_json = phones_json
            session.commit()
            session.refresh(analysis)
        
        return analysis
    
    @staticmethod
    def get_by_analysis_id(session: Session, analysis_id: str) -> Optional[Analysis]:
        """
        Analysis ID'ye göre kaydı getir
        
        Args:
            session: DB session
            analysis_id: Analiz ID
            
        Returns:
            Analysis objesi veya None
        """
        return session.query(Analysis).filter(
            Analysis.analysis_id == analysis_id
        ).first()