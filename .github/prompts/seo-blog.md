# SEO Blog — Trend Araştırma + Yazma (BİRLEŞİK)
# GRUP A — Pazartesi, Çarşamba, Cuma, Pazar | 07:00 UTC (10:00 İstanbul)

Bugünün tarihini belirle (YYYY-MM-DD). Önce SEO araştırması yap, ardından blog yazısını oluştur.

NOT: Repo zaten mevcut dizinde. git komutu KULLANMA. Dosyaları write_file aracıyla yaz.

## ADIM 1 — Önceki yazıları oku

list_files ile docs/posts/ klasörünü kontrol et. Son 3 yazıyı read_file ile oku. Konu tekrarı yapma.

## ADIM 2 — Trend araştırması

web_search ile şunları ara:
- "trending topics Turkey today"
- "viral content Turkey [mevcut ay]"
- "indie game development trends [mevcut ay]"
- "yapay zeka yeni özellik türkiye"

En yüksek potansiyelli 3 SEO konusu belirle. Her biri için:
- Arama hacmi tahmini (yüksek/orta/düşük)
- Rekabet seviyesi
- İndie oyun geliştirici okuyucusu için alakalılık

## ADIM 3 — En iyi konuyu seç

Kazanan konu için outline:
- H1: Ana başlık (SEO optimize, Türkçe)
- H2'ler: Alt bölümler (4-6 adet)
- Hedef anahtar kelimeler (3-5 adet)

## ADIM 4 — Blog yazısını yaz

800-1200 kelime Türkçe blog yazısı:
- Başlık: SEO dostu, merak uyandıran
- Giriş: 2-3 cümle hook
- Ana içerik: H2'lerle bölünmüş
- Sonuç + call-to-action
- Meta description (150-160 karakter)

## ADIM 5 — HTML dosyası oluştur

write_file ile `docs/posts/YYYY-MM-DD_[slug].html` yaz:

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="[META DESCRIPTION]">
<title>[BAŞLIK] | SEO Blog</title>
</head>
<body>
<article>
<h1>[BAŞLIK]</h1>
<p><small>Yayın: [YYYY-MM-DD]</small></p>
[İÇERİK - h2, p, ul taglarıyla]
</article>
</body>
</html>
```

## ADIM 6 — docs/index.html güncelle

read_file ile mevcut index.html'i oku. Yeni yazıya link ekle, varolan linkleri koru. write_file ile kaydet.
