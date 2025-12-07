"""
İş ilanı eşleştirme servisi
CV'den çıkarılan teknolojilere göre en uygun iş ilanlarını bulur
"""
import json
from pathlib import Path
from typing import List, Dict


class JobMatchingService:
    """İş ilanı eşleştirme servisi"""
    
    @staticmethod
    def load_job_postings(json_path: Path) -> List[Dict]:
        """
        İş ilanları JSON dosyasını yükle
        
        Args:
            json_path: job_postings.json dosya yolu
            
        Returns:
            İş ilanları listesi
        """
        try:
            if not json_path.exists():
                print(f"[JobMatching] HATA: Dosya bulunamadı: {json_path}")
                return []
            
            with open(json_path, 'r', encoding='utf-8') as f:
                postings = json.load(f)
                print(f"[JobMatching] {len(postings)} iş ilanı yüklendi")
                return postings
        except Exception as e:
            print(f"[JobMatching] JSON yükleme hatası: {e}")
            return []
    
    @staticmethod
    def match_jobs(
        cv_technologies: List[str], 
        job_postings: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:
        """
        CV teknolojilerine göre iş ilanlarını eşleştir ve skorla
        
        Args:
            cv_technologies: CV'den çıkarılan teknoloji listesi (küçük harf)
            job_postings: İş ilanları listesi
            top_k: Döndürülecek maksimum ilan sayısı
            
        Returns:
            Eşleşen iş ilanları listesi (skora göre sıralı)
            Her eleman:
            {
                "job_id": int,
                "title": str,
                "company": str,
                "location": str,
                "match_score": float,  # 0-1 arası
                "matched_technologies": list[str]
            }
        """
        if not cv_technologies:
            print("[JobMatching] CV'de teknoloji bulunamadı")
            return []
        
        if not job_postings:
            print("[JobMatching] İş ilanı yok")
            return []
        
        # CV teknolojilerini set'e çevir (hızlı lookup + küçük harf)
        cv_tech_set = set(tech.lower().strip() for tech in cv_technologies)
        print(f"[JobMatching] CV teknolojileri: {cv_tech_set}")
        
        matched_jobs = []
        
        for job in job_postings:
            # İlanın gerektirdiği teknolojiler
            required_techs = [tech.lower().strip() for tech in job.get("required_technologies", [])]
            
            if not required_techs:
                continue
            
            # Eşleşen teknolojileri bul
            matched_techs = list(cv_tech_set.intersection(set(required_techs)))
            
            # Eşleşme yoksa bu ilanı atlayalım
            if not matched_techs:
                continue
            
            # Skor hesapla: eşleşen teknoloji sayısı / gereken teknoloji sayısı
            match_score = len(matched_techs) / len(required_techs)
            
            matched_jobs.append({
                "job_id": job["id"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "match_score": round(match_score, 2),  # 2 ondalık basamak
                "matched_technologies": sorted(matched_techs)  # Alfabetik sırala
            })
        
        # Skora göre azalan sırada sırala
        matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
        
        print(f"[JobMatching] {len(matched_jobs)} eşleşme bulundu, top {top_k} döndürülüyor")
        
        # Top K kadarını döndür
        return matched_jobs[:top_k]