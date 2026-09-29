"""Dilolog Google Ads arama kampanyası: Google Ads Editor içe aktarma CSV'si üretir.

Çalıştır: python3 build.py  ->  dilolog_google_ads_editor.csv
Karakter sınırlarını (başlık 30, açıklama 90, yol 15) kontrol eder.
"""
import csv
import sys

SITE = "https://dilolog.com"
CAMPAIGN = "Dilolog | Arama | TR | Trafik"
BUDGET = "300"            # TRY / gün
MAX_CPC = "6"             # Maksimum tıklama TBM sınırı (TRY)

AD_GROUPS = {
    "Marka": {
        "path": ("Dilolog", "Dil-Ogren"),
        "keywords": [("dilolog", "Exact"), ("dilolog", "Phrase"), ("dilolog com", "Phrase"),
                     ("dilolog uygulama", "Phrase"), ("dilolog giriş", "Phrase")],
        "headlines": ["Dilolog Resmi Sitesi", "Dilolog ile Dil Öğren", "Dilolog'a Hemen Katıl",
                      "Konuşarak Dil Öğren", "Günlük Dil Pratiği", "Kendi Hızında İlerle",
                      "Hedefine Göre Program", "Her Seviyeye Uygun", "Hemen Başla",
                      "Online Dil Öğrenme", "Akıcı Konuşmaya Adım At", "Dilolog'u Keşfet"],
        "descriptions": ["Dilolog ile yabancı dili konuşarak öğren. Hedefine uygun pratikle her gün ilerle.",
                         "Seviyene uygun içerikler ve konuşma pratiği Dilolog'da. Hemen başla.",
                         "İstediğin yerden, istediğin zaman dil pratiği yap. Dilolog'u şimdi keşfet.",
                         "Akıcı konuşmak için düzenli pratik şart. Dilolog ile bugün ilk adımı at."],
    },
    "İngilizce Öğren": {
        "path": ("Ingilizce", "Ogren"),
        "keywords": [("ingilizce öğren", "Phrase"), ("online ingilizce öğren", "Phrase"),
                     ("ingilizce öğrenme", "Phrase"), ("evde ingilizce öğrenmek", "Phrase"),
                     ("hızlı ingilizce öğrenme", "Phrase"), ("ingilizce nasıl öğrenilir", "Phrase"),
                     ("[ingilizce öğren]", "Exact"), ("[online ingilizce]", "Exact")],
        "headlines": ["Online İngilizce Öğren", "İngilizceyi Konuşarak Öğren", "Dilolog ile İngilizce",
                      "Evden İngilizce Öğren", "Her Gün Kısa Pratik", "Seviyene Göre İngilizce",
                      "İngilizce Konuşma Pratiği", "Akıcı İngilizceye Adım At", "Kendi Hızında Öğren",
                      "Günlük İngilizce Pratiği", "Hemen Başla", "Başlangıçtan İleriye"],
        "descriptions": ["İngilizceyi ezberleyerek değil, konuşarak öğren. Dilolog ile her gün pratik yap.",
                         "Seviyene uygun derslerle İngilizceni geliştir. İstediğin yerden, istediğin zaman.",
                         "Günlük hayatta kullanacağın İngilizceyi öğren. Dilolog'u şimdi keşfet.",
                         "Kısa ve düzenli pratiklerle kalıcı öğrenme. Hemen başla, farkı gör."],
    },
    "Konuşma Pratiği": {
        "path": ("Konusma", "Pratigi"),
        "keywords": [("ingilizce konuşma pratiği", "Phrase"), ("yabancı dil konuşma pratiği", "Phrase"),
                     ("speaking pratiği", "Phrase"), ("ingilizce speaking geliştirme", "Phrase"),
                     ("ingilizce konuşamıyorum", "Phrase"), ("ingilizce pratik yapma", "Phrase"),
                     ("[ingilizce konuşma pratiği]", "Exact")],
        "headlines": ["İngilizce Konuşma Pratiği", "Konuşarak Akıcılaş", "Speaking'ini Geliştir",
                      "Konuşma Korkusunu Yen", "Dilolog ile Pratik Yap", "Günlük Konuşma Pratiği",
                      "Gerçek Diyaloglarla Öğren", "Her Gün Biraz Konuş", "Akıcı Konuşmaya Başla",
                      "Evden Konuşma Pratiği", "Hemen Pratiğe Başla", "Seviyene Uygun Diyaloglar"],
        "descriptions": ["Anlıyorum ama konuşamıyorum mu diyorsun? Dilolog ile düzenli konuşma pratiği yap.",
                         "Gerçek hayattan diyaloglarla konuşma becerini geliştir. Hemen başla.",
                         "Konuşma pratiğini günlük rutinine ekle. İstediğin zaman, istediğin yerden.",
                         "Akıcı konuşmanın yolu pratikten geçer. Dilolog ile bugün ilk adımı at."],
    },
    "Online Dil Kursu": {
        "path": ("Online", "Dil-Kursu"),
        "keywords": [("online dil kursu", "Phrase"), ("online ingilizce kursu", "Phrase"),
                     ("internetten ingilizce kursu", "Phrase"), ("uzaktan dil eğitimi", "Phrase"),
                     ("yetişkinler için ingilizce kursu", "Phrase"), ("[online dil kursu]", "Exact")],
        "headlines": ["Online Dil Kursu", "Dilolog Online Dil Eğitimi", "Kursa Gitmeden Öğren",
                      "Esnek Saatlerle Öğren", "Yetişkinler İçin İngilizce", "Seviyene Göre Program",
                      "Evden Dil Eğitimi", "Konuşma Odaklı Eğitim", "Kendi Hızında İlerle",
                      "Hemen Başla", "Yoğun Tempoya Uygun", "Dil Öğrenmenin Kolay Yolu"],
        "descriptions": ["Kursa gitmeden, kendi programına göre dil öğren. Dilolog ile konuşma odaklı eğitim.",
                         "Yoğun tempoda bile düzenli pratik mümkün. Esnek saatlerle istediğin zaman öğren.",
                         "Seviyene uygun içeriklerle adım adım ilerle. Dilolog'u şimdi keşfet.",
                         "Konuşma odaklı online dil eğitimiyle hedefine daha hızlı ulaş. Hemen başla."],
    },
    "Dil Öğrenme Uygulaması": {
        "path": ("Dil", "Uygulamasi"),
        "keywords": [("dil öğrenme uygulaması", "Phrase"), ("ingilizce öğrenme uygulaması", "Phrase"),
                     ("en iyi dil öğrenme uygulaması", "Phrase"), ("dil öğrenme sitesi", "Phrase"),
                     ("ingilizce öğrenme sitesi", "Phrase"), ("[dil öğrenme uygulaması]", "Exact")],
        "headlines": ["Dil Öğrenme Uygulaması", "Dilolog ile Dil Öğren", "Cebindeki Dil Koçu",
                      "Konuşma Odaklı Uygulama", "Her Gün Kısa Pratik", "Seviyene Göre İçerik",
                      "İstediğin Yerde Öğren", "Kendi Hızında İlerle", "Hemen Başla",
                      "Akıcı Konuşmaya Adım At", "Dil Öğrenmeyi Alışkanlık Yap", "Dilolog'u Keşfet"],
        "descriptions": ["Dil öğrenmeyi günlük alışkanlığa dönüştür. Dilolog ile kısa ve etkili pratikler.",
                         "Konuşma odaklı içeriklerle yabancı dilini geliştir. İstediğin yerden erişim.",
                         "Seviyene uygun içeriklerle adım adım ilerle. Dilolog'u şimdi keşfet.",
                         "Ezber yerine kullanarak öğren. Dilolog ile bugün başla."],
    },
}

CAMPAIGN_NEGATIVES = [
    "iş ilanı", "iş ilanları", "öğretmen alımı", "maaş", "kariyer", "pdf", "indir", "torrent",
    "crack", "apk", "çeviri", "tercüme", "translate", "sözlük", "kelime anlamı", "şarkı sözleri",
    "ödev", "ders notu", "kpss", "yds soruları", "çıkmış sorular", "wikipedia", "nedir",
]

SITELINKS = [
    ("Hemen Başla", "Seviyeni seç", "Dakikalar içinde başla", "/"),
    ("Nasıl Çalışır?", "Konuşma odaklı yöntem", "Adım adım öğrenme", "/"),
    ("İngilizce Öğren", "Her seviyeye uygun", "Günlük pratiklerle ilerle", "/"),
    ("Konuşma Pratiği", "Gerçek diyaloglar", "Akıcılığını geliştir", "/"),
]
CALLOUTS = ["Konuşma Odaklı", "Her Seviyeye Uygun", "Kendi Hızında Öğren",
            "İstediğin Yerden Erişim", "Günlük Kısa Pratikler", "Esnek Program"]

LIMITS = {"Headline": 30, "Description": 90, "Path": 15, "Sitelink": 25, "SitelinkDesc": 35, "Callout": 25}


def check(kind, text, where):
    if len(text) > LIMITS[kind]:
        sys.exit(f"{where}: '{text}' {len(text)} > {LIMITS[kind]} karakter")


def main():
    cols = ["Campaign", "Campaign Type", "Networks", "Budget", "Budget type", "Bid Strategy Type",
            "Max CPC", "Languages", "Location", "Campaign Status", "Ad Group", "Ad Group Status",
            "Keyword", "Criterion Type", "Ad type", "Final URL", "Path 1", "Path 2"]
    cols += [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)]
    cols += ["Sitelink text", "Description line 1", "Description line 2", "Callout text", "Status"]
    rows = []

    def row(**kw):
        r = {c: "" for c in cols}
        r.update({k.replace("_", " "): v for k, v in kw.items()})
        rows.append(r)

    row(Campaign=CAMPAIGN, Campaign_Type="Search", Networks="Google search", Budget=BUDGET,
        Budget_type="Daily", Bid_Strategy_Type="Maximize clicks", Max_CPC=MAX_CPC,
        Languages="tr", Campaign_Status="Paused")
    row(Campaign=CAMPAIGN, Location="Turkey")

    for kw in CAMPAIGN_NEGATIVES:
        row(Campaign=CAMPAIGN, Keyword=kw, Criterion_Type="Campaign Negative Phrase")

    for name, g in AD_GROUPS.items():
        row(Campaign=CAMPAIGN, Ad_Group=name, Ad_Group_Status="Enabled")
        for text, match in g["keywords"]:
            text = text.strip("[]")
            row(Campaign=CAMPAIGN, Ad_Group=name, Keyword=text, Criterion_Type=match, Status="Enabled")
        p1, p2 = g["path"]
        check("Path", p1, name); check("Path", p2, name)
        ad = dict(Campaign=CAMPAIGN, Ad_Group=name, Ad_type="Responsive search ad",
                  Final_URL=SITE, Path_1=p1, Path_2=p2, Status="Enabled")
        for i, h in enumerate(g["headlines"], 1):
            check("Headline", h, name); ad[f"Headline_{i}"] = h
        for i, d in enumerate(g["descriptions"], 1):
            check("Description", d, name); ad[f"Description_{i}"] = d
        row(**ad)

    for text, d1, d2, path in SITELINKS:
        check("Sitelink", text, "sitelink"); check("SitelinkDesc", d1, text); check("SitelinkDesc", d2, text)
        row(Campaign=CAMPAIGN, Sitelink_text=text, Description_line_1=d1, Description_line_2=d2,
            Final_URL=SITE + path, Status="Enabled")
    for c in CALLOUTS:
        check("Callout", c, "callout")
        row(Campaign=CAMPAIGN, Callout_text=c, Status="Enabled")

    with open("dilolog_google_ads_editor.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)
    kws = sum(len(g["keywords"]) for g in AD_GROUPS.values())
    print(f"OK: {len(AD_GROUPS)} reklam grubu, {kws} anahtar kelime, {len(AD_GROUPS)} RSA, "
          f"{len(CAMPAIGN_NEGATIVES)} negatif, {len(SITELINKS)} site bağlantısı, {len(CALLOUTS)} açıklama metni")


if __name__ == "__main__":
    main()
