# Dilolog — Google Ads Trafik Kampanyası

Hedef: **dilolog.com'a nitelikli trafik** (Türkiye, Türkçe, ~300 TL/gün).

## Dosyalar
| Dosya | Ne işe yarar |
|---|---|
| `dilolog_google_ads_editor.csv` | Google Ads Editor'e tek seferde içe aktarılır (kampanya, reklam grupları, anahtar kelimeler, RSA reklamları, negatifler, site bağlantıları, açıklama metinleri). |
| `build.py` | CSV'yi üretir ve karakter sınırlarını kontrol eder. Metinleri burada düzenleyip `python3 build.py` çalıştır. |

## Kampanya yapısı
- **Tür:** Arama (yalnızca Google Arama; Arama Ağı iş ortakları ve Görüntülü Reklam Ağı kapalı)
- **Bütçe:** 300 TL/gün (~9.000 TL/ay)
- **Teklif:** Tıklamaları en üst düzeye çıkar, maks. TBM sınırı 6 TL → hedef ~50+ tıklama/gün
- **Konum:** Türkiye (konum seçeneği: "Varlık" — hedef konumda bulunan kişiler)
- **Dil:** Türkçe
- **Durum:** **Duraklatılmış** olarak içe aktarılır; kontrol edip sen yayına alırsın.

| Reklam grubu | Örnek anahtar kelimeler |
|---|---|
| Marka | dilolog, dilolog uygulama |
| İngilizce Öğren | ingilizce öğren, online ingilizce öğren |
| Konuşma Pratiği | ingilizce konuşma pratiği, speaking pratiği |
| Online Dil Kursu | online dil kursu, online ingilizce kursu |
| Dil Öğrenme Uygulaması | dil öğrenme uygulaması, ingilizce öğrenme sitesi |

Her grupta 12 başlık + 4 açıklamalı 1 duyarlı arama reklamı (RSA) var. 23 kampanya düzeyi negatif kelime (iş ilanı, pdf, çeviri, sözlük, kpss…) alakasız tıklamaları keser.

## Yayına alma adımları
1. [Google Ads Editor](https://ads.google.com/intl/tr_tr/home/tools/ads-editor/)'ı aç → hesabı indir.
2. **Hesap → İçe aktar → Dosyadan** → `dilolog_google_ads_editor.csv` → değişiklikleri incele → **Değişiklikleri koru**.
3. Editor'de kontrol et: Ağlar (yalnızca Google Arama), konum seçeneği ("Varlık"), reklam zamanlaması.
4. **Site bağlantısı URL'lerini** gerçek sayfalarla değiştir (şu an hepsi ana sayfaya gidiyor; Google farklı URL isteyebilir).
5. **Metinleri siteye göre doğrula:** Sadece İngilizce değil başka diller de varsa (Almanca, İspanyolca…) her dil için "İngilizce Öğren" grubunu kopyalayıp uyarlayın. Ücretsiz deneme / fiyat avantajı gerçekse başlıklara ekleyin — en güçlü tıklama tetikleyicisi budur.
6. **Dönüşüm takibi:** Google Ads → Hedefler → Dönüşümler → GA4'ü bağla; "kayıt" veya "uygulama indirme" olayını dönüşüm olarak işaretle. Trafik hedefi için şart değil ama ileride optimizasyon için gerekli.
7. Kampanyayı **Etkin** yap → **Yayınla**.

## İlk 2 haftalık optimizasyon
- **3. gün:** Arama terimleri raporunu incele, alakasızları negatif ekle.
- **7. gün:** TBM ortalaması 3 TL altındaysa maks. TBM'yi düşürme; tıklama hacmi düşükse sınırı 8 TL'ye çıkar.
- **14. gün:** Düşük performanslı RSA öğelerini ("Düşük" etiketli) değiştir. Dönüşüm verisi 30+ olduysa teklif stratejisini "Dönüşümleri en üst düzeye çıkar"a geçirmeyi değerlendir — salt trafik yerine kayıt getiren trafik.
- İsteğe bağlı: bütçenin %20–30'u ile **Demand Gen** / YouTube kampanyası (dil öğrenme ilgi alanları) ucuz tıklama sağlar ama kalite daha düşüktür.

> Not: dilolog.com bu çalışma ortamından erişilemediği için metinler genel tutuldu; doğrulanamayan iddialar (ücretsiz, fiyat, garanti) bilerek eklenmedi.
