<div align="center">

<br/>

```
  ██████╗██╗   ██╗    ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗
 ██╔════╝██║   ██║    ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
 ██║     ██║   ██║    ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝
 ██║     ╚██╗ ██╔╝    ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
 ╚██████╗ ╚████╔╝     ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
  ╚═════╝  ╚═══╝      ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```

# Akıllı CV Analiz ve İş Öneri Platformu

**CV'ni yükle. Güçlü yönlerini keşfet. Doğru işe adım at.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/Lisans-MIT-green?style=flat-square)](LICENSE)
[![University](https://img.shields.io/badge/Fırat_Üniversitesi-Bilgisayar_Müh.-red?style=flat-square)](https://firat.edu.tr)
[![Status](https://img.shields.io/badge/Durum-Aktif_Geliştirme-orange?style=flat-square)](#)

<br/>

**[🎥 Demo Videosu](https://youtu.be/C6HcAOKBrYg)** · **[📋 Kurulum](#-kurulum)** · **[🏗️ Mimari](#️-sistem-mimarisi)** · **[🤝 Ekip](#-ekip)**

<br/>

</div>

---

## 🧠 Ne Yapar?

Geleneksel iş arama sürecinde adaylar iki temel soruyla boğuşur:

> *"CV'm bu ilana ne kadar uyuyor?"*
> *"Hangi teknolojileri öğrensem daha fazla iş fırsatı yakalarım?"*

Bu platform bu soruları veri ile yanıtlar. CV'ni PDF olarak yükle; sistem saniyeler içinde:

| Adım | İşlem |
|------|--------|
| 📄 **Metin Çıkarma** | CV'den ham metin ve yapısal bilgiler alınır |
| 🔍 **Yetenek Analizi** | NLP ile teknolojiler, araçlar ve alan etiketleri çıkarılır |
| 🧬 **Embedding** | CV ve iş ilanları vektör uzayına taşınır |
| 📐 **Eşleştirme** | Cosine similarity ile her ilan için uyum skoru hesaplanır |
| 📊 **Raporlama** | Eşleşen / eksik skill'ler ve sıralı iş önerileri sunulur |

---

## ✨ Özellikler

- 📁 **PDF & DOCX Desteği** — Çoklu format CV yükleme
- 🤖 **Yapay Zeka Destekli Analiz** — Sentence-Transformers tabanlı embedding
- 💼 **Vektör Tabanlı Eşleştirme** — Cosine similarity ile hassas skor hesaplama
- 📈 **Skill Gap Analizi** — "Eksiklerim neler?" sorusuna somut yanıt
- 🔒 **KVKK Uyumlu** — Güvenli dosya işleme ve veri yönetimi
- ⚡ **Modüler Mimari** — Bağımsız, test edilebilir servis katmanları

---

## 🏗️ Sistem Mimarisi

Sistem üç ana katmandan oluşur:

```
┌─────────────────────────────────────────────────────────────┐
│                     SUNUM KATMANI                           │
│         UserInterface  ·  ResultViewer  ·  ReportService    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  UYGULAMA KATMANI                           │
│                                                             │
│   ┌──────────────────┐      ┌────────────────────────────┐  │
│   │  CV ANALİZ SİSTEMİ│      │  İŞ EŞLEŞTİRME SİSTEMİ   │  │
│   │                  │      │                            │  │
│   │  UploadManager   │      │  JobRepository             │  │
│   │  TextExtraction  │─────▶│  JobEmbeddingService       │  │
│   │  AIAnalyzer      │      │  JobMatcher                │  │
│   └──────────────────┘      └────────────────────────────┘  │
│                                                             │
│              ProcessingEngine  ·  APIHandler                │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   VERİ & GÜVENLİK KATMANI                   │
│          DatabaseManager  ·  SecurityService  ·  Logger     │
└─────────────────────────────────────────────────────────────┘
```

### Veri Akışı

```
Kullanıcı CV yükler
        │
        ▼
UploadManager ──► Doğrulama + analysis_id üretimi
        │
        ▼
TextExtractionService ──► Ham metin çıkarma (PyMuPDF)
        │
        ▼
AIAnalyzer ──► Skill çıkarımı + Alan etiketleme + Profil özeti
        │
        ▼
JobEmbeddingService ──► CV & ilan vektörleri
        │
        ▼
JobMatcher ──► Cosine Similarity skorları
        │
        ▼
ResultViewer ──► Sıralı iş önerileri + Skill gap raporu
```

---

## 📦 Modüller

<details>
<summary><b>📄 CV Analiz Sistemi</b></summary>

| Modül | Sorumluluk |
|-------|------------|
| `UploadManager` | Dosya yükleme, MIME/boyut doğrulama, `analysis_id` üretimi |
| `TextExtractionService` | PyMuPDF ile PDF/DOCX'ten ham metin çıkarma |
| `AIAnalyzer` | NLP ön işleme, teknoloji tespiti, alan etiketleme, profil özeti |

</details>

<details>
<summary><b>💼 İş Eşleştirme Sistemi</b></summary>

| Modül | Sorumluluk |
|-------|------------|
| `JobRepository` | İlan veritabanı CRUD, filtreleme (seviye, lokasyon, tür) |
| `JobEmbeddingService` | İlan açıklamalarını vektöre dönüştürme |
| `JobMatcher` | Cosine similarity + kritik skill ağırlıklandırması |

</details>

<details>
<summary><b>🔒 Güvenlik & KVKK Sistemi</b></summary>

| Kontrol | Detay |
|---------|-------|
| Dosya doğrulama | Uzantı + MIME türü kontrolü |
| Boyut sınırı | Maksimum yükleme boyutu kısıtlaması |
| Veri politikası | Analiz tamamlandıktan sonra CV verisi temizlenir |
| Loglama | KVKK kapsamında maskelenmiş log kaydı |

</details>

---

## 🛠️ Teknoloji Yığını

```
Backend          │  Python 3.11+  ·  FastAPI  ·  Uvicorn  ·  Pydantic
NLP / AI         │  spaCy  ·  Sentence-Transformers (all-MiniLM-L6-v2)
Metin Çıkarma    │  PyMuPDF  ·  docx2txt
Veritabanı       │  SQLite (geliştirme)  ·  PostgreSQL (üretim)
Frontend         │  HTML5  ·  CSS3  ·  JavaScript
Araçlar          │  Git  ·  Docker (planlanan)
```

---

## 🚀 Kurulum

### Ön Koşullar

- Python 3.11+
- pip
- Git

### Adım 1 — Depoyu Klonla

```bash
git clone https://github.com/TITANBGG/Find_a_Job_with_CV_Detector.git
cd Find_a_Job_with_CV_Detector
```

### Adım 2 — Sanal Ortam

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### Adım 3 — Bağımlılıklar

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Adım 4 — Ortam Değişkenleri

Kök dizinde `.env` dosyası oluştur:

```env
DB_URL=sqlite:///./data/app.db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
SECRET_KEY=your-secret-key-here
```

### Adım 5 — Çalıştır

```bash
# Backend
uvicorn app.main:app --reload

# Frontend (ayrı terminal)
cd frontend
python -m http.server 5500
```

| Servis | Adres |
|--------|-------|
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Frontend | http://localhost:5500/upload.html |

---

## 📐 Veri Yapıları

<details>
<summary><b>CV Kaydı</b></summary>

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

</details>

<details>
<summary><b>İş İlanı Kaydı</b></summary>

```json
{
  "id": "job_001",
  "title": "Python Backend Developer",
  "company": "Örnek Teknoloji A.Ş.",
  "location": "İstanbul / Remote",
  "level": "Mid",
  "description": "REST API geliştirme, PostgreSQL, Docker...",
  "required_skills": ["python", "django", "postgresql", "docker"]
}
```

</details>

<details>
<summary><b>Analiz Sonucu</b></summary>

```json
{
  "analysis_id": "e3b0c442-98fc-1c1f-9f6e-7f7d5b0e1234",
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

</details>

---

## 🗺️ Yol Haritası

- [x] CV yükleme ve metin çıkarma
- [x] NLP tabanlı skill analizi
- [x] Vektör tabanlı iş eşleştirme
- [x] Temel web arayüzü
- [ ] Gerçek zamanlı iş ilanı API entegrasyonu (LinkedIn, Kariyer.net)
- [ ] Kullanıcı oturum sistemi ve analiz geçmişi
- [ ] İK paneli — çoklu CV karşılaştırma
- [ ] Kurs/eğitim öneri entegrasyonu (Udemy, Coursera)
- [ ] Docker ile tam konteynerleştirme
- [ ] PDF analiz raporu indirme

---

## 🎥 Demo

Platform çalışma mantığını ve arayüzü görmek için:

**▶️ [YouTube Demo Videosu](https://youtu.be/C6HcAOKBrYg)**

---

## 👥 Ekip

Bu proje **Fırat Üniversitesi Bilgisayar Mühendisliği — Mühendislik Tasarımı Projesi** kapsamında geliştirilmiştir.

| İsim | GitHub |
|------|--------|
| Ali Nebi Er | [@TITANBGG](https://github.com/TITANBGG) |
| Ahmet Dağıstanlı | — |
| İkra Şahin | — |

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında lisanslanmıştır.

---

<div align="center">

*Fırat Üniversitesi · Bilgisayar Mühendisliği · 2024–2025*

</div>
