"""
Analiz sonuçları endpoint'i
GET /api/results/{analysis_id}
"""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any

from app.infra.db import get_db
from app.infra.repositories import AnalysisRepository
from app.services.job_matching_service import JobMatchingService
from app.config.settings import settings


router = APIRouter()


class TechnologyItem(BaseModel):
    """Teknoloji item modeli"""
    name: str
    count: int


class TechnologiesResult(BaseModel):
    """Teknolojiler sonuç modeli"""
    languages: List[TechnologyItem]
    frontend: List[TechnologyItem]
    backend: List[TechnologyItem]
    databases: List[TechnologyItem]
    devops: List[TechnologyItem]


class MatchedJob(BaseModel):
    """Eşleşen iş ilanı modeli"""
    job_id: int
    title: str
    company: str
    location: str
    match_score: float
    matched_technologies: List[str]


class AnalysisResultResponse(BaseModel):
    """Analiz sonuç response modeli"""
    analysis_id: str
    status: str
    emails: List[str] = []
    phones: List[str] = []
    technologies: TechnologiesResult | None = None
    matched_jobs: List[MatchedJob] = []  # YENİ ALAN


@router.get("/results/{analysis_id}", response_model=AnalysisResultResponse)
def get_analysis_results(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """
    Analiz sonuçlarını getir ve iş ilanlarıyla eşleştir
    
    Args:
        analysis_id: Analiz UUID
        db: Database session
        
    Returns:
        AnalysisResultResponse: Analiz sonuçları + iş önerileri
    """
    # 1. Analizi bul
    analysis = AnalysisRepository.get_by_analysis_id(
        session=db,
        analysis_id=analysis_id
    )
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analiz bulunamadı"
        )
    
    # 2. Status kontrolü
    if analysis.status in ["PENDING", "PROCESSING"]:
        # Henüz tamamlanmamış
        return AnalysisResultResponse(
            analysis_id=analysis_id,
            status=analysis.status.lower()
        )
    
    if analysis.status == "FAILED":
        # Başarısız
        return AnalysisResultResponse(
            analysis_id=analysis_id,
            status="failed",
            emails=[],
            phones=[],
            technologies=None,
            matched_jobs=[]
        )
    
    # 3. Sonuçları parse et (status == "DONE")
    try:
        emails = json.loads(analysis.emails_json) if analysis.emails_json else []
        phones = json.loads(analysis.phones_json) if analysis.phones_json else []
        tech_data = json.loads(analysis.tech_json) if analysis.tech_json else {}
        
        # TechnologiesResult'a dönüştür
        technologies = TechnologiesResult(
            languages=[TechnologyItem(**item) for item in tech_data.get("languages", [])],
            frontend=[TechnologyItem(**item) for item in tech_data.get("frontend", [])],
            backend=[TechnologyItem(**item) for item in tech_data.get("backend", [])],
            databases=[TechnologyItem(**item) for item in tech_data.get("databases", [])],
            devops=[TechnologyItem(**item) for item in tech_data.get("devops", [])]
        )
        
        # 4. CV'den çıkan tüm teknolojileri tek bir liste haline getir
        cv_technologies = []
        for category_name in ["languages", "frontend", "backend", "databases", "devops"]:
            category_items = tech_data.get(category_name, [])
            for item in category_items:
                cv_technologies.append(item["name"])
        
        # 5. İş ilanlarını yükle ve eşleştir
        matched_jobs = []
        try:
            # job_postings.json yolu
            job_postings_path = settings.BASE_DIR / "storage" / "job_postings.json"
            
            if job_postings_path.exists():
                job_postings = JobMatchingService.load_job_postings(job_postings_path)
                matched_jobs_data = JobMatchingService.match_jobs(
                    cv_technologies=cv_technologies,
                    job_postings=job_postings,
                    top_k=5
                )
                
                # MatchedJob modeline dönüştür
                matched_jobs = [MatchedJob(**job) for job in matched_jobs_data]
            else:
                print(f"[WARNING] job_postings.json bulunamadı: {job_postings_path}")
        
        except Exception as e:
            print(f"[ERROR] İş eşleştirme hatası: {e}")
            # Hata olsa bile devam et, sadece matched_jobs boş kalır
        
        # 6. Response döndür
        return AnalysisResultResponse(
            analysis_id=analysis_id,
            status="done",
            emails=emails,
            phones=phones,
            technologies=technologies,
            matched_jobs=matched_jobs
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sonuçlar parse edilemedi: {str(e)}"
        )