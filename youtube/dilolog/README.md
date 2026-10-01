# Dilolog Taktik videoları – YouTube günlük planlama

`youtube_planla.py`, masaüstündeki **Dilolog Taktik videoları** klasöründeki videoları
YouTube'a yükler ve her güne 1 video düşecek şekilde **18:00 (Türkiye saati)** için
herkese açık yayın planlar. Başlık ve açıklama aynı klasördeki metin dosyalarından alınır.
Adında "bağlaç" geçen video (zaten yüklenmiş olan YDS bağlaç sorusu) atlanır.

## Bir kerelik kurulum
1. Python 3.9+ kurulu olsun. Sonra:
   `pip install google-api-python-client google-auth-oauthlib`
2. https://console.cloud.google.com → yeni proje → **YouTube Data API v3**'ü etkinleştirin.
3. **OAuth izin ekranı**: "Harici", kendi Gmail adresinizi *test kullanıcısı* olarak ekleyin.
4. **Kimlik bilgileri → OAuth istemci kimliği → Masaüstü uygulaması** → JSON'u indirip
   `client_secret.json` adıyla bu betiğin yanına koyun.

## Kullanım
Önce planı kontrol edin (hiçbir şey yüklenmez):

    python youtube_planla.py ~/Desktop/"Dilolog Taktik videoları" --deneme

Her videonun yanında doğru başlığın ve metin kaynağının yazdığını görün, sonra:

    python youtube_planla.py ~/Desktop/"Dilolog Taktik videoları"

İlk çalıştırmada tarayıcı açılır, YouTube kanalınızın hesabıyla izin verin.

Windows'ta klasör yolu genelde `%USERPROFILE%\Desktop\Dilolog Taktik videoları`
(OneDrive kullanıyorsanız `%USERPROFILE%\OneDrive\Masaüstü\...`) olur.

## Bilmeniz gerekenler
- **Kota:** Ücretsiz API kotası günde yaklaşık 6 yüklemeye yeter. Betik durursa ertesi gün
  aynı komutu tekrar çalıştırın; `youtube_planla_durum.json` sayesinde kaldığı yerden devam eder
  ve yayın tarihleri kaymaz.
- **Doğrulanmamış Google projesi:** API ile yüklenen videolar, proje Google denetiminden geçene
  kadar YouTube tarafından "özel"de kilitlenebilir. Böyle olursa videolar Studio'da durur;
  her birini Studio'dan elle "Planla"ya almanız yeterli.
- Sıralama dosya adına göredir (1, 2, …, 10). Farklı sıra istiyorsanız dosya adlarının başına numara verin.
- Seçenekler: `--saat 19:30`, `--baslangic 2026-10-05`, `--atla bağlaç başka_kelime`.
