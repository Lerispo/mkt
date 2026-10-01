#!/usr/bin/env python3
"""Dilolog Taktik videolarını YouTube'a yükleyip her güne 1 tane planlar.

Klasördeki her video için başlık/açıklama aynı klasördeki metinden alınır:
  1. Videoyla aynı adlı .txt dosyası varsa (ör. "ders2.mp4" + "ders2.txt"):
     ilk dolu satır = başlık, kalan satırlar = açıklama.
  2. Yoksa klasördeki diğer .txt dosyalarında video adının geçtiği satır
     aranır; o satırdan sonraki satırlar (bir sonraki boş satıra kadar
     başlık, ardından gelen paragraf açıklama) kullanılır.
  3. Hiçbiri bulunamazsa başlık dosya adından üretilir.

Videolar "özel" yüklenir ve publishAt ile planlanır; o saatte YouTube
onları otomatik olarak herkese açık yapar.

Önce mutlaka --deneme ile planı kontrol edin.
"""
import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from pathlib import Path
from zoneinfo import ZoneInfo

VIDEO_UZANTILARI = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".webm"}
SAAT_DILIMI = ZoneInfo("Europe/Istanbul")
DURUM_DOSYASI = "youtube_planla_durum.json"


def sade(metin):
    """Türkçe karakterleri ve büyük/küçük harfi eşitleyerek karşılaştırma için sadeleştirir."""
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = metin.translate(str.maketrans("çğıöşü", "cgiosu"))
    metin = unicodedata.normalize("NFKD", metin)
    return re.sub(r"[^a-z0-9]+", " ", metin).strip()


def dogal_sira(yol):
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", yol.name)]


def metin_oku(yol):
    for kodlama in ("utf-8-sig", "cp1254", "latin-1"):
        try:
            return yol.read_text(encoding=kodlama)
        except UnicodeDecodeError:
            continue
    return ""


def baslik_aciklama(video, metin_dosyalari):
    ayni_ad = video.with_suffix(".txt")
    if ayni_ad.exists():
        satirlar = [s.rstrip() for s in metin_oku(ayni_ad).splitlines()]
        dolu = [i for i, s in enumerate(satirlar) if s.strip()]
        if dolu:
            baslik = satirlar[dolu[0]].strip()
            aciklama = "\n".join(satirlar[dolu[0] + 1:]).strip()
            return baslik, aciklama, ayni_ad.name

    aranan = sade(video.stem)
    for dosya in metin_dosyalari:
        satirlar = metin_oku(dosya).splitlines()
        for i, satir in enumerate(satirlar):
            if aranan and aranan in sade(satir):
                blok = []
                for s in satirlar[i + 1:]:
                    if not s.strip() and blok and not blok[-1].strip():
                        break
                    blok.append(s.rstrip())
                dolu = [s for s in blok if s.strip()]
                if dolu:
                    return dolu[0].strip(), "\n".join(dolu[1:]).strip(), dosya.name

    baslik = re.sub(r"[_\-]+", " ", video.stem).strip()
    return baslik, "", None


def etiketler(baslik, aciklama):
    etiket = re.findall(r"#(\w+)", f"{baslik} {aciklama}")
    sabit = ["Dilolog", "YDS", "İngilizce", "YDS taktik"]
    return list(dict.fromkeys(etiket + sabit))[:15]


def plan_olustur(klasor, atla, baslangic, saat):
    videolar = sorted(
        (p for p in klasor.iterdir() if p.suffix.lower() in VIDEO_UZANTILARI),
        key=dogal_sira,
    )
    metinler = sorted(p for p in klasor.iterdir() if p.suffix.lower() == ".txt")
    atlanacak = [sade(a) for a in atla]

    plan, gun = [], baslangic
    for video in videolar:
        if any(a in sade(video.stem) for a in atlanacak):
            print(f"ATLANDI (zaten yüklendi): {video.name}")
            continue
        baslik, aciklama, kaynak = baslik_aciklama(video, metinler)
        yayin = dt.datetime.combine(gun, saat, tzinfo=SAAT_DILIMI)
        plan.append({
            "dosya": video.name,
            "baslik": baslik[:100],
            "aciklama": aciklama[:5000],
            "etiketler": etiketler(baslik, aciklama),
            "metin_kaynagi": kaynak,
            "yayin": yayin.isoformat(),
        })
        gun += dt.timedelta(days=1)
    return plan


def youtube_baglan(client_secret, token_yolu):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    kapsam = ["https://www.googleapis.com/auth/youtube.upload"]
    kimlik = None
    if token_yolu.exists():
        kimlik = Credentials.from_authorized_user_file(str(token_yolu), kapsam)
    if not kimlik or not kimlik.valid:
        if kimlik and kimlik.expired and kimlik.refresh_token:
            kimlik.refresh(Request())
        else:
            kimlik = InstalledAppFlow.from_client_secrets_file(str(client_secret), kapsam).run_local_server(port=0)
        token_yolu.write_text(kimlik.to_json())
    return build("youtube", "v3", credentials=kimlik)


def yukle(youtube, video_yolu, oge, kategori):
    from googleapiclient.http import MediaFileUpload

    yayin_utc = dt.datetime.fromisoformat(oge["yayin"]).astimezone(dt.timezone.utc)
    govde = {
        "snippet": {
            "title": oge["baslik"],
            "description": oge["aciklama"],
            "tags": oge["etiketler"],
            "categoryId": kategori,
            "defaultLanguage": "tr",
            "defaultAudioLanguage": "tr",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": yayin_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "selfDeclaredMadeForKids": False,
        },
    }
    medya = MediaFileUpload(str(video_yolu), chunksize=8 * 1024 * 1024, resumable=True)
    istek = youtube.videos().insert(part="snippet,status", body=govde, media_body=medya)
    yanit = None
    while yanit is None:
        durum, yanit = istek.next_chunk()
        if durum:
            print(f"  %{int(durum.progress() * 100)}", end="\r", flush=True)
    return yanit["id"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path, help='Ör. ~/Desktop/"Dilolog Taktik videoları"')
    ap.add_argument("--saat", default="18:00", help="Türkiye saatiyle yayın saati (varsayılan 18:00)")
    ap.add_argument("--baslangic", help="İlk yayın günü YYYY-AA-GG (varsayılan: yarın)")
    ap.add_argument("--atla", nargs="*", default=["bağlaç"], help="Adında bu kelimeler geçen videoları atla")
    ap.add_argument("--client-secret", type=Path, default=Path("client_secret.json"))
    ap.add_argument("--kategori", default="27", help="YouTube kategori kimliği (27 = Eğitim)")
    ap.add_argument("--deneme", action="store_true", help="Yüklemeden sadece planı göster")
    a = ap.parse_args()

    klasor = a.klasor.expanduser()
    if not klasor.is_dir():
        sys.exit(f"Klasör bulunamadı: {klasor}")
    saat = dt.time.fromisoformat(a.saat)
    baslangic = (dt.date.fromisoformat(a.baslangic) if a.baslangic
                 else dt.datetime.now(SAAT_DILIMI).date() + dt.timedelta(days=1))

    durum_yolu = klasor / DURUM_DOSYASI
    durum = json.loads(durum_yolu.read_text()) if durum_yolu.exists() else {}

    plan = plan_olustur(klasor, a.atla, baslangic, saat)
    # Daha önce yüklenenler eski tarihlerini korur; kalanlar sırayla sonraki günlere kayar.
    yuklenen = [o for o in plan if o["dosya"] in durum]
    kalan = [o for o in plan if o["dosya"] not in durum]
    if yuklenen:
        son = max(dt.datetime.fromisoformat(durum[o["dosya"]]["yayin"]).date() for o in yuklenen)
        ilk = max(baslangic, son + dt.timedelta(days=1))
        for i, o in enumerate(kalan):
            o["yayin"] = dt.datetime.combine(ilk + dt.timedelta(days=i), saat, tzinfo=SAAT_DILIMI).isoformat()

    for o in plan:
        etiket = "YÜKLENDİ" if o["dosya"] in durum else "BEKLİYOR"
        tarih = durum.get(o["dosya"], o)["yayin"][:16].replace("T", " ")
        print(f"[{etiket}] {tarih}  {o['dosya']}")
        print(f"    Başlık : {o['baslik']}")
        print(f"    Metin  : {o['metin_kaynagi'] or 'BULUNAMADI, dosya adı kullanıldı'}")
    if a.deneme or not kalan:
        return

    youtube = youtube_baglan(a.client_secret.expanduser(), klasor / "youtube_token.json")
    for o in kalan:
        print(f"Yükleniyor: {o['dosya']} -> {o['yayin']}")
        try:
            vid = yukle(youtube, klasor / o["dosya"], o, a.kategori)
        except Exception as hata:  # kota dolduğunda kaldığı yerden devam edebilmek için
            print(f"\nDURDU: {hata}\nYarın aynı komutu tekrar çalıştırın; kaldığı yerden devam eder.")
            break
        durum[o["dosya"]] = {"video_id": vid, "yayin": o["yayin"]}
        durum_yolu.write_text(json.dumps(durum, ensure_ascii=False, indent=2))
        print(f"  Tamam: https://youtu.be/{vid}")


if __name__ == "__main__":
    main()
