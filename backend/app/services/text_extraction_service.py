"""
Text extraction ve OCR servisi
PDF, DOCX ve görsel dosyalardan metin çıkarır
"""
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from docx import Document
from PIL import Image
from pathlib import Path


class TextExtractionService:
    """Dosyalardan metin çıkarma servisi"""
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Dosyadan metin çıkar
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            Çıkarılan metin
        """
        file_path_obj = Path(file_path)
        extension = file_path_obj.suffix.lower()
        
        if extension == ".pdf":
            return TextExtractionService._extract_from_pdf(file_path)
        elif extension == ".docx":
            return TextExtractionService._extract_from_docx(file_path)
        elif extension in [".jpg", ".jpeg", ".png"]:
            return TextExtractionService._extract_from_image(file_path)
        else:
            raise ValueError(f"Desteklenmeyen dosya tipi: {extension}")
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """
        PDF'den metin çıkar
        Önce doğrudan text extraction, başarısız olursa OCR
        
        Args:
            file_path: PDF dosya yolu
            
        Returns:
            Çıkarılan metin
        """
        text = ""
        
        try:
            # Önce PyMuPDF ile doğrudan text extraction dene
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            doc.close()
            
            # Eğer metin çok az ise (taranmış PDF olabilir), OCR'a geç
            if len(text.strip()) < 100:
                text = TextExtractionService._extract_from_pdf_ocr(file_path)
        
        except Exception as e:
            print(f"PDF text extraction hatası: {e}")
            # Hata durumunda OCR dene
            text = TextExtractionService._extract_from_pdf_ocr(file_path)
        
        return text
    
    @staticmethod
    def _extract_from_pdf_ocr(file_path: str) -> str:
        """
        PDF'den OCR ile metin çıkar
        
        Args:
            file_path: PDF dosya yolu
            
        Returns:
            OCR ile çıkarılan metin
        """
        text = ""
        
        try:
            # PDF'i görsellere çevir
            images = convert_from_path(file_path)
            
            # Her sayfaya OCR uygula
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image, lang='tur+eng')
                text += f"\n--- Sayfa {i+1} ---\n{page_text}"
        
        except Exception as e:
            print(f"PDF OCR hatası: {e}")
        
        return text
    
    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """
        DOCX dosyasından metin çıkar
        
        Args:
            file_path: DOCX dosya yolu
            
        Returns:
            Çıkarılan metin
        """
        text = ""
        
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs]
            text = "\n".join(paragraphs)
        
        except Exception as e:
            print(f"DOCX extraction hatası: {e}")
        
        return text
    
    @staticmethod
    def _extract_from_image(file_path: str) -> str:
        """
        Görsel dosyasından OCR ile metin çıkar
        
        Args:
            file_path: Görsel dosya yolu
            
        Returns:
            OCR ile çıkarılan metin
        """
        text = ""
        
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='tur+eng')
        
        except Exception as e:
            print(f"Image OCR hatası: {e}")
        
        return text