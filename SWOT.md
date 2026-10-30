# DİNÇMAK FOCUS 3 Eksen CNC Freze: SWOT Analizi (Safety 4.0 bakışı)

> Safety 4.0 Bootcamp (AİMSAD) kapsamında hazırlanmış bir eğitim çıktısıdır; resmî denetim, uygunluk
> değerlendirmesi veya CE garantisi değildir. "Varsayım" diye işaretlenen maddeler sahada doğrulanmalıdır.

## Makine özeti

| Özellik | Değer | Kaynak |
|---|---|---|
| Model | FOCUS (FOCUS.2136), 3 eksen CNC freze / router | dincmak.com ürün sayfası, katalog |
| Çalışma alanı | 2100 x 3600 mm, Z 300 mm | Katalog s. 20 |
| Makine ölçüsü | 4750 x 2750 x 2260 mm | Katalog s. 20 |
| Spindle | 8/10 kW elektrospindle, HSK F63 | Ürün sayfası |
| Takım magazini | 12'li lineer magazin | Ürün sayfası |
| Takım ölçümü | Otomatik takım boyu ölçümü ve ofset düzeltme | Ürün sayfası |
| Tabla | Çok bölgeli vakum tabla | Ürün sayfası |
| Kontrol | PC tabanlı CNC kontrol paneli (FOCUS ailesi) | Katalog s. 21 |
| Malzeme | Ahşap, plastik, alüminyum; opsiyonla kapı işleme | Ürün sayfası |
| Servis | Online destek, otomasyon desteği, 1000 m²+ yedek parça deposu, 80+ ülke | Katalog |

## SWOT

### Güçlü yönler (Strengths)

- **Deneyim ve servis ağı:** 1979'dan beri ahşap işleme makinesi üretimi, 80+ ülkede kurulu makine, kendi
  yedek parça deposu, online destek ve otomasyon desteği. Olay anında üreticiye ulaşmak kolay.
- **Hatayı azaltan otomasyon:** Otomatik takım boyu ölçümü ve ofset düzeltme, elle ayardan doğan yanlış
  ofset riskini (takımın tablaya dalması, kırılıp fırlaması) azaltır.
- **Parça tutma:** Çok bölgeli vakum tabla parçanın kopup fırlama riskini azaltır.
- **Güçlü ve esnek yapı:** 8/10 kW HSK F63 spindle, 12'li magazin, geniş 2100 x 3600 mm tabla; giriş
  seviyesinde fiyat/performans, kapı işleme opsiyonu.
- **Ayrılabilir emniyet mimarisi:** E-stop / alan koruma, safety rölesi/PLC, STO zinciri, CNC kontrolünden
  bağımsız kurulabiliyor (Lab 1-4'te tanımlandı).

### Zayıf yönler (Weaknesses)

- **PC tabanlı kontrol:** Genel amaçlı işletim sistemi (varsayım: Windows), yama yükü, USB ve zararlı
  yazılım yüzeyi; CNC parametreleri (takım ofseti, devir sınırı, yazılım limitleri) bu PC'de duruyor.
- **Uzak destek kanalı:** Online destek çoğu sahada ortak hesapla, sürekli açık ve kayıtsız çalışıyor olabilir
  (varsayım). MFA, kişisel hesap ve oturum kaydı yoksa en kolay saldırı kapısıdır (Lab 3, senaryo 1: skor 18).
- **Alan koruması belirsiz:** Katalog ULTRA gibi modellerde güvenlik çiti/kabini gösteriyor, FOCUS sayfasında
  ışık bariyeri, tampon veya çit belirtilmemiş. Alan koruması müşteri kurulumuna kalabiliyor.
- **Görünmeyen yazılım zinciri:** Kamuya açık SBOM, güvenlik açığı bildirim süreci (PSIRT) ve güvenli
  güncelleme kanalı bilgisi yok.
- **G-kodu taşıma:** CAM'den makineye dosya USB ile taşınıyorsa bütünlük kontrolü yoktur (Lab 3, senaryo 2).

### Fırsatlar (Opportunities)

- **AB Siber Dayanıklılık Yasası (CRA):** Bildirim yükümlülükleri 11 Eylül 2026'dan beri yürürlükte, tamamı
  11 Aralık 2027'de uygulanacak. 80+ ülkeye ihracat yapan bir üretici için "CRA'ya hazır" olmak AB pazarında
  ayırt edici bir özellik olur.
- **Yeni Makine Yönetmeliği (AB) 2023/1230:** 20 Ocak 2027'den itibaren uygulanacak. Bozulmaya karşı koruma
  (Ek III 1.1.9) ve kontrol sistemlerinin kötü niyetli girişimlere dayanıklılığı (Ek III 1.2.1) gereksinimlerine
  erken uyum rekabet avantajı sağlar.
- **Güvenli uzak destek bir hizmet paketine dönüşebilir:** VPN + jump server + MFA + oturum kaydı +
  varsayılan kapalı erişim, ücretli servis sözleşmesine eklenebilir.
- **IEC 62443-4-1 / 4-2:** Güvenli ürün geliştirme süreci ve bileşen gereksinimleri ile SBOM ve yama
  yönetimini kurumsallaştırmak; müşteriye Evidence Pack olarak sunmak.
- **Sektörde öncülük:** AİMSAD ve Safety 4.0 Bootcamp çıktılarıyla (Machine Starter Pack) üyeler arasında
  örnek olmak.
- **YZ destekli kalite:** Kamera ile levha kusuru ve parça konumu tespiti; ancak yalnız fail-safe mimariyle
  (Lab 7: monitoring, confidence threshold, fallback, human override).

### Tehditler (Threats)

- **Siberden fiziksel zarara giden zincir:** Uzak erişim veya USB üzerinden takım ofseti ya da spindle devir
  sınırının değiştirilmesi, takımın kırılıp fırlamasına ve operatörün yaralanmasına yol açabilir. Ürün
  sorumluluğu ve itibar riski doğar.
- **Fidye yazılımı:** CNC kontrol PC'sinin kilitlenmesi üretimi durdurur, müşteri üreticiden hızlı çözüm bekler.
- **Uyumsuzluğun bedeli:** CRA'nın temel gereksinimlerine uyulmazsa 15 milyon € veya dünya cirosunun %2,5'ine
  kadar ceza ve AB pazarına erişim kaybı söz konusu.
- **Rekabet:** Avrupalı rakipler siber güvenlik belgeli ürünlerle, Uzak Doğulu rakipler düşük fiyatla geliyor.
- **Tedarik zinciri:** Üçüncü taraf CNC yazılımı, sürücü ve kütüphane zafiyetleri SBOM olmadan görünmez
  kalır (Lab 5).

## Stratejiler (TOWS)

| | Fırsatlar (O) | Tehditler (T) |
|---|---|---|
| **Güçlü (S)** | **SO:** Servis ağını ve online desteği "güvenli uzak destek" paketine çevirip CRA'ya hazır ürün olarak AB'de pazarlamak. | **ST:** Otomatik takım ölçümü ve ayrı safety zincirini, ofset ve devir sınırı değişikliğini tespit eden kontrollerle güçlendirmek; değişiklikte makine güvenli durumda kalmalı. |
| **Zayıf (W)** | **WO:** SBOM, PSIRT ve imzalı güncelleme kanalını IEC 62443-4-1 ile kurup CRA ve Makine Yönetmeliği uyumunu belgelemek. | **WT:** Online desteği VPN + jump server + MFA + kişisel hesap + kayıt arkasına almak, USB'yi kilitlemek, CNC PC'yi ayrı bölgeye almak; FOCUS için alan korumasını standart donanım yapmak. |

## Öncelikli 5 eylem

1. Online destek: varsayılan kapalı, VPN + jump server + MFA, teknisyen başına kişisel hesap, tam oturum kaydı.
2. Safety rölesi/PLC'ye ağdan ve CNC PC'den yazma yolunu kapatmak; safety parametre değişikliğini tespit etmek.
3. FOCUS için SBOM çıkarmak ve güvenlik açığı bildirim sürecini (24 sa / 72 sa / 14 gün) tanımlamak.
4. CNC PC'yi ayrı makine bölgesine almak, USB'yi kilitlemek, G-kodu aktarımını kontrollü yapmak.
5. Alan korumasını (ışık bariyeri, tampon veya çit) FOCUS'ta standart yapmak ve PL'yi EN ISO 13849-1 /
   EN ISO 19085-3'e göre doğrulamak.

## Kaynaklar

- [DİNÇMAK FOCUS ürün sayfası](https://www.dincmak.com/urun/focus/)
- [DİNÇMAK kataloğu](https://www.dincmak.com/documents/catalog/)
- AİMSAD (Ağaç İşleme Makine Sanayicileri Derneği): [WoodTech haberi](https://www.haberler.com/ekonomi/uluslararasi-agac-isleme-makineleri-fuari-woodtech-istanbul-da-basladi-17922673-haberi/)
- Safety 4.0 Bootcamp laboratuvar föyleri (Lab 1-7), DİNÇMAK FOCUS sürümü
