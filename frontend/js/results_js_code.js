// results.html için JavaScript kodu
// Bu kodu <script> tagı içine veya ayrı bir JS dosyasına koyun

// API base URL - backend'in çalıştığı adres
const API_BASE_URL = 'http://127.0.0.1:5000/api';

// DOM yüklendiğinde çalışacak
document.addEventListener('DOMContentLoaded', function() {
    console.log('[Results] Sayfa yüklendi');
    
    // URL'den analysis_id parametresini al
    const urlParams = new URLSearchParams(window.location.search);
    const analysisId = urlParams.get('analysis_id');
    
    console.log('[Results] Analysis ID:', analysisId);
    
    if (!analysisId) {
        // analysis_id yoksa kullanıcıyı bilgilendir
        displayError('Analysis ID bulunamadı. Lütfen önce bir CV yükleyin.');
        return;
    }
    
    // Sonuçları yükle
    loadResults(analysisId);
});

/**
 * Backend'den analiz sonuçlarını yükle ve göster
 */
async function loadResults(analysisId) {
    const resultsContainer = document.getElementById('results-container');
    
    if (!resultsContainer) {
        console.error('[Results] results-container elementi bulunamadı!');
        return;
    }
    
    // Loading mesajı göster
    resultsContainer.innerHTML = '<p>⏳ Sonuçlar yükleniyor...</p>';
    
    try {
        console.log('[Results] Backend\'e istek gönderiliyor:', API_BASE_URL + '/results/' + analysisId);
        
        // Backend'den sonuçları çek
        const response = await fetch(API_BASE_URL + '/results/' + analysisId);
        
        console.log('[Results] Response alındı. Status:', response.status);
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Analiz bulunamadı. ID yanlış olabilir.');
            } else {
                throw new Error('Sonuçlar alınırken bir hata oluştu. (HTTP ' + response.status + ')');
            }
        }
        
        const data = await response.json();
        console.log('[Results] Response data:', data);
        
        // Sonuçları ekranda göster
        displayResults(data);
        
    } catch (error) {
        console.error('[Results] ❌ Hata:', error);
        
        if (error.message.includes('Failed to fetch')) {
            displayError('Sunucuya bağlanılamadı. Backend çalışıyor mu?<br>Detay: ' + error.message);
        } else {
            displayError(error.message);
        }
    }
}

/**
 * Sonuçları HTML olarak göster
 */
function displayResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    let html = '';
    
    // 1. Status bilgisi
    html += `<div class="status-section">`;
    html += `<h3>📊 Analiz Durumu</h3>`;
    html += `<p>Durum: <strong>${getStatusText(data.status)}</strong></p>`;
    html += `</div>`;
    
    // Eğer status done değilse, sadece durumu göster
    if (data.status !== 'done') {
        if (data.status === 'processing' || data.status === 'pending') {
            html += `<p class="info-message">Analiz henüz tamamlanmadı. Lütfen birkaç saniye sonra sayfayı yenileyin.</p>`;
        }
        resultsContainer.innerHTML = html;
        return;
    }
    
    // 2. CV'den çıkan teknolojiler
    html += `<div class="technologies-section">`;
    html += `<h3>💻 CV'nizden Çıkarılan Teknolojiler</h3>`;
    
    if (data.technologies) {
        const techs = data.technologies;
        
        // Her kategori için
        const categories = [
            { key: 'languages', title: 'Programlama Dilleri' },
            { key: 'frontend', title: 'Frontend' },
            { key: 'backend', title: 'Backend' },
            { key: 'databases', title: 'Veritabanları' },
            { key: 'devops', title: 'DevOps & Araçlar' }
        ];
        
        categories.forEach(category => {
            const items = techs[category.key];
            if (items && items.length > 0) {
                html += `<h4>${category.title}</h4>`;
                html += `<ul>`;
                items.forEach(tech => {
                    html += `<li><strong>${tech.name}</strong> (${tech.count} kez)</li>`;
                });
                html += `</ul>`;
            }
        });
    } else {
        html += `<p>Teknoloji bulunamadı.</p>`;
    }
    
    html += `</div>`;
    
    // 3. İletişim bilgileri (opsiyonel)
    if ((data.emails && data.emails.length > 0) || (data.phones && data.phones.length > 0)) {
        html += `<div class="contact-section">`;
        html += `<h3>📧 İletişim Bilgileri</h3>`;
        
        if (data.emails && data.emails.length > 0) {
            html += `<h4>E-posta:</h4>`;
            html += `<ul>`;
            data.emails.forEach(email => {
                html += `<li>${email}</li>`;
            });
            html += `</ul>`;
        }
        
        if (data.phones && data.phones.length > 0) {
            html += `<h4>Telefon:</h4>`;
            html += `<ul>`;
            data.phones.forEach(phone => {
                html += `<li>${phone}</li>`;
            });
            html += `</ul>`;
        }
        
        html += `</div>`;
    }
    
    // 4. İŞ ÖNERİLERİ - YENİ BÖLÜM
    html += `<div class="job-recommendations-section">`;
    html += `<h3>🎯 Size Uygun İş İlanları</h3>`;
    
    if (data.matched_jobs && data.matched_jobs.length > 0) {
        html += `<p class="info-text">CV'nizdeki teknolojilere göre ${data.matched_jobs.length} iş ilanı bulundu:</p>`;
        
        // Her iş ilanı için bir kart
        data.matched_jobs.forEach(job => {
            const matchPercent = Math.round(job.match_score * 100);
            
            html += `<div class="job-card">`;
            html += `<div class="job-header">`;
            html += `<h4>${job.title}</h4>`;
            html += `<span class="match-badge">${matchPercent}% Uyum</span>`;
            html += `</div>`;
            html += `<p><strong>Şirket:</strong> ${job.company}</p>`;
            html += `<p><strong>Lokasyon:</strong> ${job.location}</p>`;
            html += `<p><strong>Eşleşen Teknolojiler:</strong> ${job.matched_technologies.join(', ')}</p>`;
            html += `</div>`;
        });
    } else {
        html += `<p class="no-jobs-message">Maalesef CV'nizdeki teknolojilerle eşleşen bir iş ilanı bulunamadı.</p>`;
        html += `<p class="info-text">Daha fazla teknoloji öğrenerek şansınızı artırabilirsiniz!</p>`;
    }
    
    html += `</div>`;
    
    // HTML'i container'a yerleştir
    resultsContainer.innerHTML = html;
}

/**
 * Hata mesajı göster
 */
function displayError(message) {
    const resultsContainer = document.getElementById('results-container');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="error-message">
                <h3>❌ Hata</h3>
                <p>${message}</p>
                <p><a href="upload.html">Yeni CV Yükle</a></p>
            </div>
        `;
    }
}

/**
 * Status'u Türkçe metne çevir
 */
function getStatusText(status) {
    const statusMap = {
        'done': '✅ Tamamlandı',
        'processing': '⏳ İşleniyor...',
        'pending': '⏳ Sırada Bekliyor...',
        'failed': '❌ Başarısız'
    };
    return statusMap[status] || status;
}