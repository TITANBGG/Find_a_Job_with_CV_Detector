"""
Text extraction ve OCR servisi
PDF, DOCX ve görsel dosyalardan metin çıkarır
Geliştirilmiş hata yönetimi ile
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
        
        try:
            if extension == ".pdf":
                return TextExtractionService._extract_from_pdf(file_path)
            elif extension == ".docx":
                return TextExtractionService._extract_from_docx(file_path)
            elif extension in [".jpg", ".jpeg", ".png"]:
                return TextExtractionService._extract_from_image(file_path)
            else:
                print(f"[TextExtraction] Desteklenmeyen dosya tipi: {extension}")
                return ""
        except Exception as e:
            print(f"[TextExtraction] GENEL HATA: {e}")
            return ""
    
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
            
            print(f"[TextExtraction] PDF'den {len(text)} karakter çıkarıldı")
            
            # Eğer metin çok az ise (taranmış PDF olabilir), OCR'a geç
            if len(text.strip()) < 100:
                print("[TextExtraction] Yetersiz metin, OCR deneniyor...")
                ocr_text = TextExtractionService._extract_from_pdf_ocr(file_path)
                if len(ocr_text) > len(text):
                    text = ocr_text
        
        except Exception as e:
            print(f"[TextExtraction] PDF text extraction hatası: {e}")
            # Hata durumunda OCR dene
            try:
                text = TextExtractionService._extract_from_pdf_ocr(file_path)
            except Exception as ocr_error:
                print(f"[TextExtraction] OCR da başarısız: {ocr_error}")
        
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
            print("[TextExtraction] PDF -> Image dönüşümü başlıyor...")
            images = convert_from_path(file_path)
            
            # Her sayfaya OCR uygula
            for i, image in enumerate(images):
                try:
                    page_text = pytesseract.image_to_string(image, lang='tur+eng')
                    text += f"\n--- Sayfa {i+1} ---\n{page_text}"
                except Exception as page_error:
                    print(f"[TextExtraction] Sayfa {i+1} OCR hatası: {page_error}")
            
            print(f"[TextExtraction] OCR'dan {len(text)} karakter çıkarıldı")
        
        except Exception as e:
            print(f"[TextExtraction] PDF OCR hatası: {e}")
            print("[TextExtraction] Poppler veya Tesseract kurulu değil olabilir")
        
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
            print(f"[TextExtraction] DOCX'ten {len(text)} karakter çıkarıldı")
        
        except Exception as e:
            print(f"[TextExtraction] DOCX extraction hatası: {e}")
        
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
            print(f"[TextExtraction] Image'dan {len(text)} karakter çıkarıldı")
        
        except Exception as e:
            print(f"[TextExtraction] Image OCR hatası: {e}")
            print("[TextExtraction] Tesseract kurulu değil olabilir")
        
        return text