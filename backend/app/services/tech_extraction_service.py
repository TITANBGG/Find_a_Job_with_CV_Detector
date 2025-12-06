"""
Teknoloji çıkarma servisi
CV metninden teknolojileri (Python, Java, CSS vb.) tespit eder
"""
import re
import json
from typing import Dict, List
from pathlib import Path


class TechExtractionService:
    """Teknoloji tespiti servisi"""
    
    @staticmethod
    def load_tech_dictionary(dict_path: Path) -> Dict:
        """
        Teknoloji sözlüğünü yükle
        
        Args:
            dict_path: Sözlük dosya yolu
            
        Returns:
            Teknoloji sözlüğü dict
        """
        with open(dict_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Metni normalize et (küçük harf, temizleme)
        Nokta ve tire karakterlerini koru (vue.js, next.js, asp.net, vb. için)
        
        Args:
            text: Ham metin
            
        Returns:
            Normalize edilmiş metin
        """
        # Küçük harfe çevir
        text = text.lower()
        
        # Noktalama işaretlerini temizle ama nokta, tire, +, # karakterlerini koru
        # vue.js, next.js, node.js, asp.net gibi teknolojiler için
        text = re.sub(r'[^\w\s+#\.\-]', ' ', text)
        
        return text
    
    @staticmethod
    def extract_technologies(text: str, tech_dict: Dict) -> Dict[str, List[Dict]]:
        """
        Metinden teknolojileri çıkar
        
        Args:
            text: CV metni
            tech_dict: Teknoloji sözlüğü
            
        Returns:
            Dict: Her kategori için teknoloji listesi
            {
                "languages": [{"name": "python", "count": 5}, ...],
                "frontend": [...],
                ...
            }
        """
        normalized_text = TechExtractionService.normalize_text(text)
        
        result = {}
        
        # Her kategori için teknolojileri ara
        for category, technologies in tech_dict.items():
            category_results = []
            
            for tech in technologies:
                # Kelime sınırlarını gözetmek için pattern oluştur
                tech_lower = tech.lower()
                
                # Özel durumlar için uyarlanmış pattern'ler
                if tech_lower == "c#":
                    pattern = r'\bc#\b'
                elif tech_lower == "c++":
                    pattern = r'\bc\+\+\b'
                elif tech_lower == "c":
                    # "c" kelimesinin tek başına geçmesini ara (c++, c# ile karışmasın)
                    pattern = r'\bc\b(?!\+\+|#)'
                elif "." in tech_lower:
                    # vue.js, next.js, node.js, asp.net gibi noktalı teknolojiler
                    # Noktayı escape et ve kelime sınırlarını kullan
                    tech_escaped = re.escape(tech_lower)
                    pattern = rf'\b{tech_escaped}\b'
                else:
                    # Normal teknolojiler için escape ve kelime sınırları
                    tech_escaped = re.escape(tech_lower)
                    pattern = rf'\b{tech_escaped}\b'
                
                # Kaç kez geçtiğini say
                matches = re.findall(pattern, normalized_text)
                count = len(matches)
                
                if count > 0:
                    category_results.append({
                        "name": tech_lower,
                        "count": count
                    })
            
            # Sayıya göre sırala (en çok geçenden aza)
            category_results.sort(key=lambda x: x["count"], reverse=True)
            result[category] = category_results
        
        return result