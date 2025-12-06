"""
API Test Script
Backend'i test etmek için basit bir script
"""
import requests
import sys
import time
from pathlib import Path


API_BASE_URL = "http://localhost:8000/api"


def test_health():
    """Health check testi"""
    print("🏥 Health check test ediliyor...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check başarılı:", response.json())
            return True
        else:
            print("❌ Health check başarısız:", response.status_code)
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        print("   Server çalışıyor mu? (uvicorn app.main:app --reload)")
        return False


def test_upload(file_path):
    """CV upload testi"""
    print(f"\n📤 CV yükleniyor: {file_path}")
    
    if not Path(file_path).exists():
        print(f"❌ Dosya bulunamadı: {file_path}")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload başarılı!")
            print(f"   Analysis ID: {result['analysis_id']}")
            print(f"   Status: {result['status']}")
            return result['analysis_id']
        else:
            print(f"❌ Upload başarısız: {response.status_code}")
            print(f"   Hata: {response.text}")
            return None
    
    except Exception as e:
        print(f"❌ Upload hatası: {e}")
        return None


def test_results(analysis_id):
    """Analiz sonuçlarını test et"""
    print(f"\n📊 Sonuçlar getiriliyor: {analysis_id}")
    
    try:
        response = requests.get(f"{API_BASE_URL}/results/{analysis_id}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sonuçlar başarıyla alındı!")
            print(f"\n📝 Analiz Sonuçları:")
            print(f"   Status: {result['status']}")
            print(f"   Emails: {result.get('emails', [])}")
            print(f"   Phones: {result.get('phones', [])}")
            
            if result.get('technologies'):
                print(f"\n🔧 Teknolojiler:")
                techs = result['technologies']
                
                for category in ['languages', 'frontend', 'backend', 'databases', 'devops']:
                    items = techs.get(category, [])
                    if items:
                        print(f"\n   {category.upper()}:")
                        for item in items:
                            print(f"     - {item['name']}: {item['count']} kez")
            
            return True
        
        elif response.status_code == 404:
            print("❌ Analiz bulunamadı")
            return False
        else:
            print(f"❌ Sonuç alınamadı: {response.status_code}")
            print(f"   Hata: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Sonuç alma hatası: {e}")
        return False


def main():
    """Ana test fonksiyonu"""
    print("=" * 60)
    print("CV Detector Backend API Test")
    print("=" * 60)
    
    # Health check
    if not test_health():
        print("\n❌ Server çalışmıyor. Test iptal edildi.")
        sys.exit(1)
    
    # CV dosyası kontrolü
    if len(sys.argv) < 2:
        print("\n⚠️  Kullanım: python test_api.py <cv_dosya_yolu>")
        print("   Örnek: python test_api.py sample_cv.pdf")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Upload testi
    analysis_id = test_upload(file_path)
    if not analysis_id:
        print("\n❌ Upload başarısız. Test iptal edildi.")
        sys.exit(1)
    
    # Biraz bekle (senkron işlem olsa da)
    print("\n⏳ İşleniyor...")
    time.sleep(1)
    
    # Sonuçları al
    if test_results(analysis_id):
        print("\n" + "=" * 60)
        print("✅ Tüm testler başarılı!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Test başarısız!")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()