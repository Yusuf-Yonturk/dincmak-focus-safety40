"""Genel lab föyü şablonunu DİNÇMAK FOCUS 3 eksen CNC freze makinesine göre doldurur.

Kullanım: python fill_dincmak.py <bos_genel.pdf> <cikti.pdf>
"""
import sys
import pymupdf

SRC, OUT = sys.argv[1], sys.argv[2]
REG = "/usr/share/fonts/carlito/Carlito-Regular.ttf"
BOLD = "/usr/share/fonts/carlito/Carlito-Bold.ttf"
SERIF = "/usr/share/fonts/noto/NotoSerif-Bold.ttf"
INK = (0x1F / 255, 0x33 / 255, 0x50 / 255)
WHITE = (1, 1, 1)
GREY = (0x5A / 255, 0x6B / 255, 0x7B / 255)
COVER = (0xCF / 255, 0xE0 / 255, 0xEE / 255)

doc = pymupdf.open(SRC)
FONT_R = pymupdf.Font(fontfile=REG)
FONT_B = pymupdf.Font(fontfile=BOLD)
overflow = []


def fonts(page):
    page.insert_font(fontname="cr", fontfile=REG)
    page.insert_font(fontname="cb", fontfile=BOLD)
    page.insert_font(fontname="sb", fontfile=SERIF)


def box(page, rect, text, size=8.3, minsize=6.2, bold=False, align=0, color=INK):
    """Metni kutuya sığana kadar küçülterek yazar."""
    r = pymupdf.Rect(rect)
    s = size
    while s >= minsize:
        rc = page.insert_textbox(r, text, fontname="cb" if bold else "cr", fontsize=s,
                                 color=color, align=align, lineheight=1.18)
        if rc >= 0:
            return s
        s -= 0.2
    overflow.append((page.number + 1, text[:50]))
    return None


def clear_rules(page, rect):
    """Kutunun tamamen içinde kalan noktalı yazı çizgilerini siler; metin ve arka plan kalır."""
    page.add_redact_annot(pymupdf.Rect(rect), fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                          text=pymupdf.PDF_REDACT_TEXT_NONE)
    fonts(page)


def ans(page, q_top, last_line, text):
    """Soru metninin altından son noktalı çizginin hemen üstüne kadar yazar."""
    rect = (68, q_top + 12.3, 554, last_line - 0.6)
    clear_rules(page, (60, rect[1], 560, rect[3]))
    return box(page, rect, text, size=8.0, minsize=7.0)


def spans(page, needle):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(sp["text"] for sp in l["spans"])
            if needle in t:
                out.append((l, l["spans"][0]))
    return out


def replace_line(page, needle, new, font="cr", size=None, color=None, spaced=False, center=False):
    """Şablondaki bir satırın yalnız metnini siler (arka plan kalır), yerine yenisini yazar."""
    found = spans(page, needle)
    assert found, (page.number + 1, needle)
    l, sp = found[0]
    rect = pymupdf.Rect(l["bbox"])
    origin = sp["origin"]
    size = size or sp["size"]
    if color is None:
        c = sp["color"]
        color = ((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)
    page.add_redact_annot(rect + (-1, -1, 1, 1), fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    fonts(page)
    fobj = {"cr": FONT_R, "cb": FONT_B}.get(font)
    x, y = origin
    if center:
        w = fobj.text_length(new, size)
        x = (rect.x0 + rect.x1) / 2 - w / 2
    if spaced:  # başlıktaki harf aralıklı yazımı taklit et
        for ch in new:
            page.insert_text((x, y), ch, fontname=font, fontsize=size, color=color)
            x += fobj.text_length(ch, size) + size * 0.36
    else:
        page.insert_text((x, y), new, fontname=font, fontsize=size, color=color)


FOOT = "SAFETY 4.0 BOOTCAMP · DİNÇMAK FOCUS Sürümü · Bu bir eğitim çıktısıdır, resmî denetim değildir."


def lab_page(pno, n):
    page = doc[pno]
    replace_line(page, "G E N E L", "", font="cb")
    # harf aralıklı başlığı kendimiz kuralım
    x, y = 87.9, 35.0
    title = f"LABORATUVAR {n} · "
    for ch in title:
        page.insert_text((x, y), ch, fontname="cb", fontsize=8.5, color=WHITE)
        x += FONT_B.text_length(ch, 8.5) + 8.5 * 0.36
    for ch in "DİNÇMAK FOCUS · 3 Eksen CNC Freze":
        page.insert_text((x, y), ch, fontname="cb", fontsize=8.5, color=WHITE)
        x += FONT_B.text_length(ch, 8.5) + 8.5 * 0.36
    replace_line(page, "SAFETY 4.0 BOOTCAMP", FOOT)
    page.insert_text((481, 112.3), "09.10.2026", fontname="cr", fontsize=9, color=INK)
    page.insert_text((76, 112.3), "Yusuf Yontürk (No: 240541165)", fontname="cr", fontsize=9, color=INK)
    page.insert_text((271, 112.3), "4-B Gündüz", fontname="cr", fontsize=9, color=INK)
    return page


# ---------------------------------------------------------------- Kapak
p = doc[0]
replace_line(p, "Laboratuvar Föyleri", "Laboratuvar Föyleri · DİNÇMAK FOCUS · 3 Eksen CNC Freze",
             font="sb", size=15.5)
replace_line(p, "Tüm laboratuvarlar gün boyu",
             "Tüm laboratuvarlar AİMSAD üyesi DİNÇMAK'ın FOCUS (FOCUS.2136) 3 eksen CNC freze makinesine uyarlanmıştır:")
replace_line(p, "işlenir.",
             "2100x3600 mm vakum tabla · 8/10 kW HSK F63 spindle · 12'li takım magazini · PC tabanlı CNC kontrol · online servis.")

# ---------------------------------------------------------------- LAB 1
p = lab_page(1, 1)
L1 = [
    (358.2, 393.8, "Portal ve Z kafası 2100x3600 mm tabla üzerinde hızla hareket eder: ezilme/sıkışma, dönen takımla kesilme, kırılan takımın veya vakumdan "
                   "kopan parçanın fırlaması, talaş/toz. Operatör parça yüklerken, takım değiştirirken veya sıkışma giderirken zarar görür."),
    (403.9, 438.8, "Alana girişte ve E-stop'ta tehlikeli hareketi durdurmak: E-stop ya da ışık bariyeri/güvenlik tamponu tetiklenince safety rölesi/PLC "
                   "portal servolarını STO ile keser, spindle'ı frenleyip durdurur (önce SS1, sonra STO); makine Safe State'e geçer."),
    (448.9, 483.8, "Alttaki ayrı safety yolunda: E-stop + ışık bariyeri/tampon, safety rölesi/PLC ve sürücülerin STO girişleri; bu üç kutuyu 'safety-related "
                   "control system' diye çerçevelerim. PC tabanlı CNC kontrolü, CAM ve online destek bunun dışındadır."),
    (493.9, 528.8, "CNC kontrolü (PC + hareket kartı/PLC) G-kodunu yürütür: eksen, devir, takım değişimi, vakum. Safety rölesi/PLC yalnız korur: sertifikalı, "
                   "çift kanallı, kendini denetler, arızada güvenli duruma geçer. Windows PC çökse de E-stop çalışmalıdır."),
    (538.9, 573.8, "PLr/SIL, fonksiyonun riske uygun güvenilirlikte olmasını sağlar (EN ISO 13849-1, ahşap CNC için EN ISO 19085-3). Portal ezilmesi ve takım "
                   "ağır yaralar; genellikle PL c veya d istenir. Parametre bozulursa PLr anlamsız kalır."),
    (583.9, 618.8, "Portal servoları ve spindle torksuz, hareketsiz: eksenler STO ile durur, spindle frenlenip tamamen durana kadar koruma kilitli kalır. "
                   "Yeniden çalışma ancak reset, alanın boş olduğunun doğrulanması ve kasıtlı başlatmayla olur."),
    (628.9, 681.8, "Safety rölesi/PLC konfigürasyonu ve parametreleri (ışık bariyeri muting/blanking, bypass, durma süreleri, güvenli hız); CNC kontrol PC'sindeki "
               "parametreler (yazılım limitleri, spindle azami devri, takım boyu ofsetleri, vakum izleme); bunları yükleyen servis yazılımı ve USB; ağ üzerinden "
               "kontrol PC'sine ulaşan yollar; DİNÇMAK online destek bağlantısı; firmware/yazılım güncelleme yolu ve paylaşılan hesaplar."),
    (691.9, 744.0, "Dijital kesişim noktasından: PC tabanlı CNC kontrolüne online destek (uzak masaüstü), ofis ağı/CAM bilgisayarı veya USB ile girilir. Oradan takım "
               "boyu ofseti, spindle devir sınırı ya da yazılım limitleri değiştirilir; takım tablaya dalar, kırılır ve fırlar. Safety ayarı ağdan yazılabiliyorsa "
               "ışık bariyeri/tampon bypass edilir; portal operatörün üzerine gelir ve durmaz."),
]
for q, last, t in L1:
    ans(p, q, last, t)

# ---------------------------------------------------------------- LAB 2
p = lab_page(2, 2)
found = spans(p, "PLC · HMI")
r = pymupdf.Rect(found[0][0]["bbox"])
p.add_redact_annot(pymupdf.Rect(50, r.y0 - 1, 546, r.y0 + 24), fill=False)
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
fonts(p)
box(p, (51.8, r.y0 - 1, 540, r.y0 + 25),
    "CNC kontrol PC'si (Windows + CNC yazılımı) · Hareket kartı / PLC · Servo sürücüler + spindle inverter · Safety rölesi/PLC (E-stop, ışık bariyeri, tampon) · "
    "Operatör paneli + el çarkı · Takım ölçüm sensörü · Vakum pompası · CAM bilgisayarı · DİNÇMAK online destek · USB portu · Ofis ağı (ERP/e-posta)",
    size=9.0, color=(0x16 / 255, 0x23 / 255, 0x3B / 255))
L2 = [
    (270.4, 340.5, "Safety bölgesi: safety rölesi/PLC, E-stop, ışık bariyeri/tampon, STO girişleri. Makine kontrol bölgesi: CNC kontrol PC'si, hareket kartı/PLC, "
               "servo sürücüler, spindle inverter, operatör paneli/el çarkı, takım ölçüm sensörü, vakum pompası (USB portu kilitlenir). Mühendislik bölgesi: "
               "CAM bilgisayarı (G-kodu üretimi). Dış bölge (DMZ): DİNÇMAK online destek erişimi. Kurumsal bölge: ofis ağı (ERP/e-posta)."),
    (350.7, 402.8, "Safety rölesi/PLC kendi bölgesinde, en yüksek kritiklikte, çünkü insanı korur. CNC kontrol PC'sinden mantıksal olarak bağımsızdır: Windows çökse "
               "veya ele geçirilse de E-stop ve ışık bariyeri çalışır. Ofisten, ağdan ve uzak destekten doğrudan ulaşılamaz; konfigürasyonu yalnız yerinde ve "
               "yetkiyle değişir. Böylece bir bölgenin ele geçirilmesi safety fonksiyonuna yayılmaz."),
    (412.9, 465.8, "(1) Ofis ile CAM arası: güvenlik duvarı, yalnız gerekli servisler. (2) CAM ile CNC kontrol arası: G-kodu USB yerine kontrollü dosya aktarımıyla, "
               "bütünlüğü kontrol edilerek. (3) Online destek ile CNC kontrol arası: VPN + jump server, MFA, oturum kaydı, müşteri onayı. (4) CNC kontrol ile "
               "Safety arası: yalnız durum bilgisi okunur; safety konfigürasyonu yazma yalnız yerel ve yetkili. (5) USB: kilitli, tarama istasyonundan geçer."),
]
for q, last, t in L2:
    ans(p, q, last, t)
rows = [527.2, 552.8, 578.2, 603.8, 629.2, 654.8, 680.2]
B = [
    "Jump server. Online destek tek denetim noktasından geçer, kayıt alınır; CNC PC'ye doğrudan erişim olmaz.",
    "VPN. İnternete açık uzak masaüstü portu kapanır; trafik şifreli ve tanımlı uçlarla sınırlı.",
    "MFA. Servis parolası sızsa da tek başına CNC kontrol PC'sine giriş sağlamaz.",
    "Kişisel. Her DİNÇMAK teknisyenine ayrı hesap; kim neyi değiştirdi izlenir, iş bitince kapanır.",
    "Tam oturum kaydı. Parametre/ofset değişikliği olay sonrası kanıtlanır, kötüye kullanım caydırılır.",
    "Varsayılan kapalı. Müşteri onayıyla, bakım penceresinde açılır; iş bitince kapanır.",
]
for i, t in enumerate(B):
    box(p, (355, rows[i] + 2, 553, rows[i + 1] - 1), t, size=7.8)

# ---------------------------------------------------------------- LAB 3
p = lab_page(3, 3)
R = [234.0, 273.8, 312.8, 352.5]
S3 = [
    ("Saldırgan; internete açık, ortak parolalı online destek (uzak masaüstü); CNC PC'de takım boyu ofsetini ve spindle devir sınırını değiştirir; "
     "takım tablaya dalıp kırılır, parça fırlar; operatör ağır yaralanır.", 3, 3, 2, "Kritik"),
    ("Oltalamayla ofis ağına giren saldırgan; CAM bilgisayarı / USB ile taşınan G-kodu; hızlı Z dalışı ve yanlış koordinat ekler; takım kelepçeye "
     "çarpar, parça fırlar; yakındaki operatörde darbe yaralanması.", 2, 2, 3, "Yüksek"),
    ("Saldırgan; ele geçirilmiş CNC PC / servis yazılımı; safety rölesi/PLC parametresini (muting, tampon) bozar; operatör tablaya parça koyarken "
     "portal hareket eder; ezilme, ağır yaralanma.", 1, 3, 2, "Orta"),
]
cols = [(215, 270), (270, 326), (326, 382), (382, 473), (473, 556)]
for i, (t, l_, s_, e_, pr) in enumerate(S3):
    y0, y1 = R[i], R[i + 1]
    box(p, (43, y0 + 2, 213, y1 - 1), t, size=7.4, minsize=6.0)
    vals = [str(l_), str(s_), str(e_), str(l_ * s_ * e_), pr]
    for (cx0, cx1), v in zip(cols, vals):
        box(p, (cx0, (y0 + y1) / 2 - 6, cx1, (y0 + y1) / 2 + 8), v, size=9, bold=True, align=1)
ans(p, 386.7, 438.8,
    "Senaryo 1: online destek erişimi internete açık ve ortak parolalı olduğu için istismarı kolay (L=3) ve takımın kırılıp fırlaması operatörü "
    "ağır yaralayabilir (S=3).")
ans(p, 449.7, 501.8,
    "Evet, senaryo 3: S=3 ama skor 6 (Orta) kaldı. Risk kaydında S=3 olanları ayrı işaretler, skordan bağımsız öne alırım; safety rölesi/PLC'ye "
    "ağdan ve CNC PC'den yazma yolunu kapatmayı öncelikli önlem olarak yazarım.")

# ---------------------------------------------------------------- LAB 4
p = lab_page(4, 4)
clear_rules(p, (43, 239, 290, 307.6))
box(p, (50, 239, 285, 307.6),
    "Tipik kurulum (sahada doğrulanmalı): PC tabanlı CNC kontrolü fabrika/ofis ağıyla aynı düz ağda. DİNÇMAK online destek için uzak masaüstü "
    "aracı sürekli açık; ortak hesap, tek parola; VPN, MFA ve oturum kaydı yok. G-kodu CAM bilgisayarından USB ile taşınıyor. Uzaktan bağlanan "
    "kişi CNC parametrelerine ve takım ofsetlerine erişebiliyor.", size=8.0)
clear_rules(p, (306, 239, 554, 307.6))
box(p, (312, 239, 549, 307.6),
    "Online destek yalnız VPN + jump server (DMZ) + MFA ile; teknisyen başına kişisel hesap, tam oturum kaydı, müşteri onayıyla açılan "
    "varsayılan kapalı erişim. CNC kontrol PC'si ayrı makine bölgesinde; G-kodu kontrollü dosya aktarımıyla gelir, USB kilitli. Safety "
    "rölesi/PLC bu yoldan ayrı kalır, ağdan yazılamaz.", size=8.0)
ans(p, 356.7, 408.8,
    "Etkilenmemeli; etkilenirse tasarım hatalıdır. E-stop ve ışık bariyeri/tampon ayrı safety rölesi/PLC ve donanım STO ile çalışır; saldırgan PC'de "
    "ne yaparsa yapsın portal ve spindle durur. Ama safety ayarları ağdan yazılabiliyorsa ya da takım ofseti/devir sınırı gibi CNC parametreleriyle "
    "takım fırlatılabiliyorsa etkilenir; bu yüzden yazma yolları kapatılmalı.")
ans(p, 418.9, 471.8,
    "Emniyet fonksiyonu (E-stop, alan koruma, güvenli durma) CNC kontrol PC'sinden, ağdan ve uzak erişimden mantıksal ve fiziksel olarak bağımsız "
    "çalışmalıdır: bu yollardan safety parametresi veya programı yazılamamalı, bypass/muting uzaktan açılamamalı, spindle devir sınırı ve eksen "
    "limitleri yetkisiz değiştirilememeli; değişiklik tespit edilmeli ve makine güvenli durumda kalmalıdır.")

# ---------------------------------------------------------------- LAB 5
p = lab_page(5, 5)
L5 = [
    (366.4, 401.2, "(1) Bileşen: SBOM'da Component X, FOCUS'un hareket kartı/PLC firmware'inde var mı, DİNÇMAK'tan teyit. (2) Sürüm 2.4 etkilenen "
                   "aralıkta mı, bültenden doğrula. (3) Ağdan, online destekten veya USB'den ulaşılabilir mi? Üçü de evetse etkilenirim."),
    (411.4, 446.2, "Hayır: CVSS 9.8 ciddiyeti ölçer, ortamımdaki riski değil. Önce ulaşılabilirliğe bakar, geçici önlem alırım (online desteği kapat, "
                   "CNC PC'yi ağdan ayır); yama planlı bakımda. Aktif istismar kanıtı varsa kontrollü durdururum."),
    (456.4, 491.2, "Önce test. PC imajı, makine parametreleri ve takım tablosu yedeklenir; DİNÇMAK'ın doğruladığı yama tabla boşken referans programla "
                   "kuru çalıştırmayla denenir, sonra planlı bakımda uygulanır; geri dönüş planı hazırdır."),
    (502.2, 537.0, "Etkileyebilir; firmware durma/hız davranışını değiştirebilir. Sürüm notlarına bakar, değişiklik kaydı açarım; yama sonrası E-stop, "
                   "ışık bariyeri/tampon tepkisi ve spindle durma süresi test edilir. Belirsizse safety yeniden doğrulanır."),
    (547.2, 599.2, "Online destek erişimini kapatmak ya da VPN + jump server + MFA arkasına almak; CNC kontrol PC'sini ayrı bölgeye alıp zafiyetli servise "
                   "erişimi güvenlik duvarıyla kısıtlamak; USB'yi kapatmak; uygulama beyaz listesi, izleme ve alarm eklemek; en kısa sürede yama planlamak. "
                   "Kalan risk kaydedilir ve sahibi atanır."),
]
for q, last, t in L5:
    ans(p, q, last, t)

# ---------------------------------------------------------------- LAB 6
p = lab_page(6, 6)
L6 = [
    (250.9, 303.0, "Bakım/otomasyon sorumlusunu, BT/OT güvenlik sorumlusunu, yöneticimi ve DİNÇMAK servisini ararım. İlk üç eylem: (1) tablada ve portal yolunda "
               "kimse olmadığından emin olup feed hold ile programı, sonra spindle'ı kontrollü durdururum; (2) şüpheli servis hesabını kapatır, online destek "
               "bağlantısını keserim (reset veya güç kesme yok); (3) zamanı ve gördüklerimi not ederim."),
    (313.2, 366.0, "Emniyet: E-stop, ışık bariyeri/tampon ve safety parametrelerini referans yedekle karşılaştırır, fonksiyon testi yapmadan çalıştırmam; takım "
               "ofsetleri, spindle devir sınırı, yazılım limitleri ve son G-kodları da karşılaştırılır. Kanıt: CNC PC logları, uzak masaüstü/VPN/güvenlik duvarı "
               "logları, parametre kopyaları; hiçbir şey resetlenmez. Hesap: şüpheli servis hesabı kapatılır, parolalar değişir."),
    (376.2, 411.0, "Olayın var olduğu, kötü niyet şüphesi, fark edilme zamanı (10:15), etkilenen makine (FOCUS, seri no, yazılım sürümü), olası etki, "
                   "ilk bulgular ve acil önlemler. Üretici DİNÇMAK aktif istismarı 24 saatte CSIRT/ENISA'ya erken uyarıyla bildirir."),
    (421.2, 456.0, "Kök neden (muhtemelen ele geçirilen online destek hesabı), etki, önlemler. Bakım: parametre farkı + safety testi; BT/OT güvenlik: "
                   "log analizi, kanıt; DİNÇMAK uyum sorumlusu: bildirim metni ve yama; yönetici: onay."),
    (466.2, 501.0, "Uzak masaüstü, VPN/jump server, kimlik doğrulama ve güvenlik duvarı logları; CNC parametre, takım tablosu ve safety yedekleri "
                   "(önce/sonra); G-kodları; safety testleri; zaman çizelgesi. Loglar değiştirilmeden saklanır."),
]
for q, last, t in L6:
    ans(p, q, last, t)

# ---------------------------------------------------------------- LAB 7
p = lab_page(7, 7)
replace_line(p, "Robot", "CNC", font="cb", center=True)
L7 = [
    (246.4, 298.5, "Kamera levhadaki çatlağı/büyük budağı kaçırırsa parça işlemede kırılıp fırlayabilir. Tek modele güvenilmez: bağımsız ikinci kontrol (vakum "
               "basıncı izleme, parça var/konum sensörü, spindle yükü/akım izleme) ve örnekleme ile operatör kontrolü olur. Vakum yetersizse işleme "
               "başlamaz. Hata oranı izlenir (monitoring)."),
    (308.7, 361.5, "Fark etme: görüntü tutarlılık kontrolleri (parlaklık, odak, kare sıklığı, ani dağılım kayması), kamera kimliği/imzası, tabla referans "
               "işaretleri veya takım probu ile konum doğrulama. Şüpheli girdide program başlamaz; parça RED/manuel kontrole alınır, alarm verilir, olay "
               "kaydedilir. Tekrarlanırsa YZ devre dışı bırakılıp manuel moda geçilir."),
    (371.7, 423.8, "Eşik risk analizine göre belirlenir (örneğin %90-95 altı otomatik karar için yetersiz, sahada doğrulanır). Altında model karar vermez: CNC "
               "işlemeye başlamaz, operatöre sorulur; yanıt yoksa fallback olarak parça RED ya da manuel konumlandırmayla işlenir. Sık düşerse YZ kapatılır. "
               "YZ hiçbir zaman E-stop/ışık bariyerinin yerine geçmez."),
]
for q, last, t in L7:
    ans(p, q, last, t)
rows = [485.2, 510.8, 536.2, 561.8]
T7 = [
    "Bağımsız ikinci kontrol (vakum, konum, spindle yükü) + operatör onayı; hata oranı izlenir. Kavram: monitoring, human override.",
    "Şüpheli girdide işleme başlamaz; RED/manuel kontrol, alarm. Kavram: fail-safe, monitoring, fallback.",
    "Eşik altında operatöre sor, yoksa RED/manuel konumlandırma. Kavram: confidence threshold, fallback, human override.",
]
for i, t in enumerate(T7):
    box(p, (199, rows[i] + 2, 553, rows[i + 1] - 1), t, size=7.8)

doc.set_metadata({"title": "Safety 4.0 Bootcamp - Lab Föyleri - DİNÇMAK FOCUS", "producer": "PyMuPDF"})
doc.save(OUT, garbage=3, deflate=True)
print("yazildi:", OUT)
print("tasma:", overflow or "yok")
