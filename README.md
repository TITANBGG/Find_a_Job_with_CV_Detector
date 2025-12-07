Tamam, README’yi hem videoyu hem de tasarım dosyalarındaki sistemleri özellikle vurgulayacak şekilde baştan toparlayalım. Aşağıyı direkt `README.md` olarak koyabilirsin.

````markdown
# Akıllı CV Analiz ve İş Öneri Platformu

**Yapay zeka tabanlı CV analizi + iş ilanı eşleştirme ve iş öneri sistemi**

Bu proje, kullanıcının CV’sini alıp:

1. CV metnini otomatik işler,  
2. Teknik ve davranışsal yetenekleri çıkarır,  
3. Profili iş ilanlarıyla vektör tabanlı olarak karşılaştırır,  
4. Uygun iş/stajları **puanlanmış şekilde** önerir,  
5. Eksik / geliştirilmesi gereken alanlar için **geri bildirim** üretir.

Fırat Üniversitesi Bilgisayar Mühendisliği **Mühendislik Tasarımı Projesi** kapsamında, uçtan uca çalışan bir **karar destek sistemi** olarak tasarlanmıştır.

---

## 🎥 Demo Videosu

Platformun çalışma mantığını ve arayüzünü görmek için demo videosu:

➡️ **YouTube Video:** https://youtu.be/C6HcAOKBrYg  

---

## 📌 İçindekiler

1. [Proje Özeti](#-proje-özeti)  
2. [Problem ve Çözüm](#-problem-ve-çözüm)  
3. [Hedef Kitle ve Kullanım Senaryoları](#-hedef-kitle-ve-kullanım-senaryoları)  
4. [Ana Sistemler ve Alt Modüller](#-ana-sistemler-ve-alt-modüller)  
5. [Özellikler](#-özellikler)  
6. [Sistem Mimarisi ve Veri Akışı](#-sistem-mimarisi-ve-veri-akışı)  
7. [Kullanılan Teknolojiler](#-kullanılan-teknolojiler)  
8. [Kurulum ve Çalıştırma](#-kurulum-ve-çalıştırma)  
9. [Veri Yapıları Örneği](#-veri-yapıları-örneği)  
10. [Yol Haritası](#-yol-haritası)  
11. [Ekip](#-ekip)  
12. [Lisans](#-lisans)  

---

## 1. Proje Özeti

Geleneksel işe alım sürecinde:

- Adaylar, CV’lerinin bir ilana **gerçekten ne kadar uyduğunu** bilemiyor.  
- İK ekipleri yüzlerce CV’yi gözle taramak zorunda kalıyor.  
- “Hangi iş bana daha uygun?” sorusu veri yerine sezgiyle cevaplanıyor.

**Akıllı CV Analiz ve İş Öneri Platformu**, CV ve iş ilanlarını metin tabanlı olmaktan çıkarıp:

- Yetenek seti çıkarımı,  
- Vektör temsili (embedding),  
- Benzerlik skoru (cosine similarity)  

üzerinden **sayısal olarak kıyaslayabilen** bir sistem sunar. Kullanıcı tek bir CV yükleyerek:

- Profili hakkında özet rapor,
- Güçlü / zayıf yönler,
- Eşleşme yüzdeleriyle iş/staj önerileri

elde eder.

---

## 2. Problem ve Çözüm

### Problem

- CV’ler dağınık metin yapısında; içinden anlamlı, standart bir **yetenek profili** çıkarmak zor.  
- İş ilanlarının detayları da benzer şekilde dağınık; manuel eşleştirme hem yavaş hem subjektif.  
- Öğrenciler ve yeni mezunlar, piyasadaki ilanların kendilerinden ne istediğini ve kendi CV’lerinin buna ne kadar uyduğunu bilmiyor.

### Çözüm

Bu platform:

- CV’yi otomatik okuyup **yetenek envanterine** çevirir (diller, framework’ler, araçlar, alanlar).  
- İş ilanlarını da benzer şekilde normalize eder (gereken skill listeleri + açıklama metni).  
- CV vektörü ile ilan vektörlerini karşılaştırarak **eşleşme skorları** üretir.  
- Sonuç sayfasında:
  - En uygun ilanları sıralar,
  - Hangi skill’lerin eşleştiğini,
  - Hangi kritik skill’lerin eksik olduğunu gösterir.

---

## 3. Hedef Kitle ve Kullanım Senaryoları

### 3.1 Hedef Kitle

- **İş Arayan Bireyler**  
  Kariyerini ilerletmek isteyen, “Bu ilanda ne kadar güçlüyüm?” sorusuna net cevap arayanlar.

- **Öğrenciler & Yeni Mezunlar**  
  CV’sinde hangi alanlara ağırlık vermesi gerektiğini, hangi teknolojilerde geri kaldığını görmek isteyenler.

- **İK ve İnsan Kaynakları Ekipleri**  
  Yüzlerce CV arasında, belirli pozisyon için en uygun adayları hızlıca shortlist etmek isteyen ekipler.

- **Eğitim ve Kariyer Merkezleri**  
  Öğrencilerin iş piyasasına hazır oluşlarını, CV kalitelerini ve skill gap’lerini takip etmek isteyen kurumlar.

### 3.2 Örnek Senaryo

1. Kullanıcı sisteme girip CV’sini PDF olarak yükler.  
2. Sistem CV’yi otomatik işler, kullanılan teknolojileri ve alanları çıkarır.  
3. Veritabanındaki iş ilanları taranır, her ilan için eşleşme skoru hesaplanır.  
4. Kullanıcıya şu bilgiler sunulur:
   - En uyumlu ilanlar listesi (% matç ile),
   - Eşleşen teknolojiler listesi,
   - Eksik/geliştirilmesi gereken teknolojiler,
   - Genel profil özeti.

---

## 4. Ana Sistemler ve Alt Modüller

Mühendislik Tasarımı raporlarında ve CRC kartlarında tanımlanan yapıya uygun olarak sistem aşağıdaki **ana modüllerden** oluşur:

### 4.1 CV Analiz Sistemi

CV’nin sisteme alınması, metne dönüştürülmesi ve yetenek çıkarımı:

- **UploadManager**
  - Dosya yükleme (PDF/DOCX),
  - Boyut ve MIME türü kontrolü,
  - Dosyanın güvenli bir klasöre kaydedilmesi,
  - `analysis_id` üretimi.

- **TextExtractionService**
  - PyMuPDF / benzeri araçla CV’den ham metin çıkarma,
  - Bozuk dosya / okunamayan CV için hata üretme.

- **AIAnalyzer (Skill & Profil Analizcisi)**
  - NLP ön işleme (lowercase, stop-word temizliği, vs.),
  - Teknoloji ve araç isimlerinin çekilmesi (Python, React, Docker, vs.),
  - Alan etiketleri (Backend, Data Science, Computer Vision, vb.),
  - Kısa profil özeti üretimi (özet cümle).

### 4.2 İş İlanı Eşleştirme ve İş Öneri Sistemi

İş ilanlarının yönetimi ve eşleştirme mantığı:

- **JobRepository / JobDatabaseManager**
  - İş ilanı kayıtlarının saklanması,
  - `job_postings.json` ya da veritabanı tablosu üzerinden erişim,
  - Filtreler (aktif ilan, pozisyon türü, seviye, lokasyon).

- **JobEmbeddingService**
  - İş ilanı açıklamasını embedding vektörüne dönüştürme,
  - İlan skill set’lerini normalize etme.

- **JobMatcher**
  - CV embedding’i ile iş ilanı embedding’leri arasında cosine similarity hesaplama,
  - Skill tabanlı ekstra puanlama (kritik skill’ler için ağırlık),
  - En yüksek skorlu ilanları `top_matches` listesi olarak döndürme.

### 4.3 Kullanıcı ve Oturum Yönetim Sistemi (Planlanan)

- Kullanıcı kaydı / oturumu,  
- Geçmiş analizleri görme,  
- Favori ilanlar kaydetme,  
- İK tarafı için çoklu CV / ilan yönetimi.

### 4.4 Raporlama ve Sonuç Sunum Sistemi

Analiz sonuçlarının kullanıcıya sunulması:

- **ResultViewer / ReportService**
  - Profil özeti (summary),
  - Güçlü / zayıf yönler listesi,
  - İş eşleşmeleri tablosu,
  - Gelecekte PDF rapor indirme özelliği için altyapı.

### 4.5 Güvenlik ve KVKK Uyumu Sistemi

- **SecurityService**
  - Dosya uzantısı ve MIME kontrolü,
  - Maksimum dosya boyutu sınırlaması,
  - Gerekirse virüs tarama entegrasyon noktası,
  - KVKK / GDPR kapsamında loglama, maskeleme ve veri saklama politikalarının uygulanacağı katman.

---

## 5. Özellikler

Kısaca sistemin sunduğu başlıca özellikler:

- CV yükleme (PDF/DOCX)  
- Otomatik metin çıkarma  
- Yetenek ve teknoloji çıkarımı (skills)  
- Profil özeti ve alan etiketleme  
- İş ilanı analizi ve vektör tabanlı eşleştirme  
- Eşleşme skoru (%), eşleşen / eksik skill listeleri  
- Kullanıcı dostu web arayüzü  
- Ölçeklenebilir, modüler mimari

---

## 6. Sistem Mimarisi ve Veri Akışı

Sistem 3 temel katmanda ele alınır:

1. **Sunum Katmanı**
   - `UserInterface`, `ResultViewer`
   - Kullanıcının CV’yi yüklediği ve sonuçları gördüğü katman.

2. **Uygulama / İş Mantığı Katmanı**
   - `UploadManager`, `TextExtractionService`, `AIAnalyzer`
   - `JobRepository`, `JobEmbeddingService`, `JobMatcher`
   - `ProcessingEngine`, `APIHandler`
   - Analiz sürecini orkestre eden mantığın bulunduğu katman.

3. **Veri & Güvenlik Katmanı**
   - `DatabaseManager`, `JobDatabaseManager`
   - `SecurityService`
   - Tüm kalıcı veri, loglar ve güvenlik kontrolleri burada.

### 6.1 Tipik Veri Akışı

1. Kullanıcı `upload.html` üzerinden CV dosyasını seçer ve yükler.  
2. `UploadManager` dosyayı doğrular ve kaydeder, `analysis_id` üretir.  
3. `ProcessingEngine` bu `analysis_id` ile:
   - Metin çıkarma,
   - Yetenek analizi,
   - İş eşleştirme adımlarını sırayla çalıştırır.  
4. `JobMatcher` en uygun ilanları ve skorlarını hesaplar.  
5. Sonuçlar `DatabaseManager` üzerinden saklanır.  
6. `ResultViewer`, `GET /api/analysis/{analysis_id}` ile sonuçları çekerek kullanıcıya sunar.

---

## 7. Kullanılan Teknolojiler

> Buradaki isimleri, projede gerçekten kullandığın kütüphane/model adlarına göre güncelleyebilirsin.

- **Dil**
  - Python 3.11+

- **Backend**
  - FastAPI veya Flask (REST API)
  - Uvicorn / Gunicorn (ASGI sunucusu)
  - Pydantic (veri şemaları, validation)
  - PyMuPDF / pdfminer / docx2txt (CV’den metin çıkarma)

- **NLP / Yapay Zeka**
  - spaCy (temel NLP pipeline)
  - Sentence-Transformers / BERT tabanlı embedding modelleri
  - Gerekirse LLM API entegrasyonu (örn. GPT-4o-mini)

- **Frontend**
  - HTML5, CSS3, JavaScript
  - (İleride React / Vue gibi bir framework’e taşınabilir)

- **Veritabanı**
  - Geliştirme için: SQLite
  - Üretim senaryosunda: PostgreSQL önerilir

- **Araçlar**
  - Git & GitHub (sürüm kontrolü)
  - (Opsiyonel) Docker ile konteynerleştirme

---

## 8. Kurulum ve Çalıştırma

> Aşağıdaki adımlar genel bir Python backend + statik frontend yapısı içindir.  
> Kendi proje klasör yapılarına göre uyarlaman gerekebilir.

### 8.1 Depoyu Klonla

```bash
git clone https://github.com/<kullanici-adi>/<repo-adi>.git
cd <repo-adi>
````

### 8.2 Sanal Ortam ve Bağımlılıklar

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
```

Gerekiyorsa spaCy modelini indir:

```bash
python -m spacy download en_core_web_sm
```

### 8.3 Ortam Değişkenleri (.env)

Kök dizinde bir `.env` dosyası oluştur:

```env
DB_URL=sqlite:///./data/app.db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
OPENAI_API_KEY=...
```

### 8.4 Veritabanı

Basit senaryoda ilk çalıştırmada tablolar otomatik oluşturulur.
Migration kullanıyorsan:

```bash
alembic upgrade head
```

### 8.5 Backend’i Çalıştır

```bash
uvicorn app.main:app --reload
# veya
python main.py
```

Varsayılan adres: `http://localhost:8000`

### 8.6 Frontend’i Çalıştır

Statik HTML için:

```bash
cd frontend
python -m http.server 5500
```

Tarayıcıda: `http://localhost:5500/upload.html`

---

## 9. Veri Yapıları Örneği

### 9.1 CV Kaydı

```json
{
  "id": "cv_001",
  "raw_text": "PDF'den çıkarılmış ham metin...",
  "clean_text": "ön işlenmiş metin...",
  "skills": ["python", "pandas", "django"],
  "domains": ["backend", "data"],
  "summary": "Python backend ağırlıklı geliştirici profili"
}
```

### 9.2 İş İlanı Kaydı

```json
[
  {
    "id": "job_001",
    "title": "Python Backend Developer",
    "company": "Örnek Teknoloji A.Ş.",
    "location": "İstanbul / Remote",
    "level": "Mid",
    "description": "REST API geliştirme, PostgreSQL, Docker...",
    "required_skills": ["python", "django", "postgresql", "docker"]
  }
]
```

### 9.3 Analiz Sonucu

```json
{
  "analysis_id": "e3b0c442-98fc-1fcf-9f6e-7f7d5b0e1234",
  "status": "COMPLETED",
  "profile": {
    "summary": "Python + Data ağırlıklı profil",
    "skills": ["python", "pandas", "numpy", "sql"],
    "domains": ["data", "backend"],
    "strengths": ["python", "pandas"],
    "improvements": ["docker", "cloud", "ci_cd"]
  },
  "matches": [
    {
      "job_id": "job_001",
      "title": "Python Backend Developer",
      "company": "Örnek Teknoloji A.Ş.",
      "match_score": 0.87,
      "matched_skills": ["python", "django"],
      "missing_skills": ["docker"]
    }
  ]
}
```

---

## 10. Yol Haritası

* [x] Tek CV yükleme ve temel analiz
* [x] Örnek iş ilanları üzerinden temel eşleştirme
* [ ] Gerçek zamanlı iş ilanı API entegrasyonu
* [ ] Kullanıcı oturum sistemi ve geçmiş analizler
* [ ] İK için çoklu aday / ilan yönetim paneli
* [ ] Gelişim önerileri için kurs / eğitim öneri entegrasyonu
* [ ] Docker ile tam konteynerleştirme ve deploy dökümanı

---

## 11. Ekip

Bu proje, **Fırat Üniversitesi Bilgisayar Mühendisliği**
**Mühendislik Tasarımı Projesi** kapsamında geliştirilmiştir.

* **Ali Nebi Er**
* **Ahmet Dağıstanlı**
* **İkra Şahin**

---

## 12. Lisans

Bu depo için kullanılacak lisans henüz belirlenmediyse, GitHub’ın “Add a license” özelliği kullanılarak bir lisans (MIT, Apache-2.0, GPL-3.0, vb.) eklenebilir.

```

```

