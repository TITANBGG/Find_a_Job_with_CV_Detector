"""
Dosya saklama servisi
"""
import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import Tuple


class FileStorage:
    """Dosya kaydetme işlemleri"""
    
    @staticmethod
    def save_upload_file(upload_file: UploadFile, base_dir: Path) -> Tuple[str, str]:
        """
        Yüklenen dosyayı diske kaydet
        
        Args:
            upload_file: FastAPI UploadFile objesi
            base_dir: Kayıt dizini
            
        Returns:
            Tuple[file_path, original_filename]
            - file_path: Sunucudaki tam yol
            - original_filename: Orijinal dosya adı
        """
        # UUID üret
        file_uuid = str(uuid.uuid4())
        
        # Dosya uzantısını al
        original_filename = upload_file.filename or "unknown"
        file_extension = Path(original_filename).suffix.lower()
        
        # Yeni dosya adı
        new_filename = f"{file_uuid}{file_extension}"
        
        # Tam yol
        file_path = base_dir / new_filename
        
        # Dosyayı kaydet
        with open(file_path, "wb") as buffer:
            content = upload_file.file.read()
            buffer.write(content)
        
        return str(file_path), original_filename
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Dosya uzantısını döndür (nokta ile birlikte, küçük harf)
        
        Args:
            filename: Dosya adı
            
        Returns:
            Dosya uzantısı (.pdf, .docx vb.)
        """
        return Path(filename).suffix.lower()