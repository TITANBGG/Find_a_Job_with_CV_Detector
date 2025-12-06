"""
Temel bilgi çıkarma servisi
Email ve telefon numarası gibi bilgileri regex ile çıkarır
"""
import re
from typing import List, Dict


class InfoExtractionService:
    """Email, telefon gibi temel bilgileri çıkarma"""
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Metinden email adreslerini çıkar
        
        Args:
            text: Metin içeriği
            
        Returns:
            Email listesi
        """
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Benzersiz emailler
        return list(set(emails))
    
    @staticmethod
    def extract_phones(text: str) -> List[str]:
        """
        Metinden telefon numaralarını çıkar
        Türkiye formatlarını destekler: +90, 0, 5xx
        
        Args:
            text: Metin içeriği
            
        Returns:
            Telefon listesi
        """
        phones = []
        
        # Türkiye telefon formatları
        patterns = [
            r'\+90\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}',  # +90 555 123 45 67
            r'\+90\d{10}',  # +905551234567
            r'0\d{3}\s?\d{3}\s?\d{2}\s?\d{2}',  # 0555 123 45 67
            r'0\d{10}',  # 05551234567
            r'\b5\d{2}\s?\d{3}\s?\d{2}\s?\d{2}\b',  # 555 123 45 67
            r'\b5\d{9}\b',  # 5551234567
        ]
        
        for pattern in patterns:
            found = re.findall(pattern, text)
            phones.extend(found)
        
        # Temizle ve benzersiz yap
        phones = [p.replace(" ", "") for p in phones]
        return list(set(phones))
    
    @staticmethod
    def extract_basic_info(text: str) -> Dict[str, List[str]]:
        """
        Metinden temel bilgileri çıkar
        
        Args:
            text: Metin içeriği
            
        Returns:
            Dict: {"emails": [...], "phones": [...]}
        """
        return {
            "emails": InfoExtractionService.extract_emails(text),
            "phones": InfoExtractionService.extract_phones(text)
        }