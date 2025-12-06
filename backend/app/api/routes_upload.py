"""
CV yükleme endpoint'i
POST /api/upload
"""
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.infra.db import get_db
from app.infra.file_storage import FileStorage
from app.infra.repositories import ResumeRepository, AnalysisRepository
from app.services.processing_service import ProcessingService
from app.config.settings import settings


router = APIRouter()


class UploadResponse(BaseModel):
    """Upload response modeli"""
    analysis_id: str
    status: str


@router.post("/upload", response_model=UploadResponse)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    CV dosyası yükle ve işle
    
    Args:
        file: Yüklenen dosya (PDF, DOCX, JPG, PNG)
        db: Database session
        
    Returns:
        UploadResponse: analysis_id ve status
    """
    # 1. Dosya validasyonu
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dosya adı boş olamaz"
        )
    
    # Dosya uzantısı kontrolü
    file_ext = FileStorage.get_file_extension(file.filename)
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Desteklenmeyen dosya tipi. İzin verilenler: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Dosya boyutu kontrolü (basit)
    file.file.seek(0, 2)  # Dosya sonuna git
    file_size = file.file.tell()  # Boyutu al
    file.file.seek(0)  # Başa dön
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dosya boyutu çok büyük. Maksimum: {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB"
        )
    
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dosya boş olamaz"
        )
    
    # 2. Dosyayı diske kaydet
    try:
        file_path, original_filename = FileStorage.save_upload_file(
            upload_file=file,
            base_dir=settings.STORAGE_DIR
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Dosya kaydedilemedi: {str(e)}"
        )
    
    # 3. Resume kaydı oluştur
    resume = ResumeRepository.create(
        session=db,
        file_path=file_path,
        original_filename=original_filename
    )
    
    # 4. Analysis kaydı oluştur
    analysis_id = str(uuid.uuid4())
    analysis = AnalysisRepository.create(
        session=db,
        resume_id=resume.id,
        analysis_id=analysis_id,
        status="PROCESSING"
    )
    
    # 5. CV'yi işle (senkron)
    try:
        ProcessingService.process_resume(
            resume_id=resume.id,
            file_path=file_path,
            analysis_id=analysis_id,
            db_session=db
        )
    except Exception as e:
        # İşlem hatası durumunda hata fırlat
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CV işlenirken hata oluştu: {str(e)}"
        )
    
    # 6. Response döndür
    return UploadResponse(
        analysis_id=analysis_id,
        status="done"
    )