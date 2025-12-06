"""
CV işleme pipeline'ını orkestre eden ana servis
"""
import json
from sqlalchemy.orm import Session
from app.services.text_extraction_service import TextExtractionService
from app.services.info_extraction_service import InfoExtractionService
from app.services.tech_extraction_service import TechExtractionService
from app.infra.repositories import AnalysisRepository
from app.config.settings import settings


class ProcessingService:
    """CV işleme ana servisi"""
    
    @staticmethod
    def process_resume(
        resume_id: int,
        file_path: str,
        analysis_id: str,
        db_session: Session
    ) -> None:
        """
        CV'yi işle: text extraction, bilgi çıkarma, teknoloji tespiti
        
        Args:
            resume_id: Resume DB ID
            file_path: CV dosya yolu
            analysis_id: Analiz UUID
            db_session: DB session
        """
        try:
            # 1. Text extraction
            print(f"[ProcessingService] Text extraction başlıyor: {file_path}")
            text = TextExtractionService.extract_text(file_path)
            
            if not text or len(text.strip()) < 50:
                # Yetersiz metin
                AnalysisRepository.update_with_results(
                    session=db_session,
                    analysis_id=analysis_id,
                    status="FAILED",
                    tech_json=json.dumps({}),
                    emails_json=json.dumps([]),
                    phones_json=json.dumps([])
                )
                print(f"[ProcessingService] Yetersiz metin çıkarıldı")
                return
            
            print(f"[ProcessingService] {len(text)} karakter metin çıkarıldı")
            
            # 2. Temel bilgi çıkarma (email, telefon)
            basic_info = InfoExtractionService.extract_basic_info(text)
            print(f"[ProcessingService] Temel bilgiler: {len(basic_info['emails'])} email, {len(basic_info['phones'])} telefon")
            
            # 3. Teknoloji çıkarma
            tech_dict = TechExtractionService.load_tech_dictionary(settings.TECH_DICT_PATH)
            technologies = TechExtractionService.extract_technologies(text, tech_dict)
            
            # Toplam teknoloji sayısı
            total_techs = sum(len(techs) for techs in technologies.values())
            print(f"[ProcessingService] {total_techs} teknoloji tespit edildi")
            
            # 4. Sonuçları veritabanına kaydet
            AnalysisRepository.update_with_results(
                session=db_session,
                analysis_id=analysis_id,
                status="DONE",
                tech_json=json.dumps(technologies, ensure_ascii=False),
                emails_json=json.dumps(basic_info["emails"], ensure_ascii=False),
                phones_json=json.dumps(basic_info["phones"], ensure_ascii=False)
            )
            
            print(f"[ProcessingService] İşlem tamamlandı: {analysis_id}")
        
        except Exception as e:
            # Hata durumunda FAILED olarak işaretle
            print(f"[ProcessingService] HATA: {e}")
            AnalysisRepository.update_with_results(
                session=db_session,
                analysis_id=analysis_id,
                status="FAILED",
                tech_json=json.dumps({}),
                emails_json=json.dumps([]),
                phones_json=json.dumps([])
            )
            raise