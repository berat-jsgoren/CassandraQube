import os
import sys
import requests
import json
import time
import threading

# --- PDF GENERATOR KÜTÜPHANELERİ ---
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
# Türkçe font desteği için gerekli modüller
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- TÜRKÇE FONT KAYIT MOTORU ---
def turkce_font_ayarla():
    """Sistemdeki Arial fontunu ReportLab'e kaydederek Türkçe karakter sorununu çözer."""
    try:
        # Windows, Linux ve Mac sistemlerdeki standart Arial font yollarını dene
        font_yollari = [
            "C:\\Windows\\Fonts\\arial.ttf",          # Windows normal
            "C:\\Windows\\Fonts\\arialbd.ttf",        # Windows bold
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", # Linux alternatifi
            "/Library/Fonts/Arial.ttf"                # Mac alternatifi
        ]
        
        # Normal fontu kaydet
        if os.path.exists("C:\\Windows\\Fonts\\arial.ttf"):
            pdfmetrics.registerFont(TTFont('TurkishArial', 'C:\\Windows\\Fonts\\arial.ttf'))
            pdfmetrics.registerFont(TTFont('TurkishArialBold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
        elif os.path.exists("/Library/Fonts/Arial.ttf"):
            pdfmetrics.registerFont(TTFont('TurkishArial', '/Library/Fonts/Arial.ttf'))
            pdfmetrics.registerFont(TTFont('TurkishArialBold', '/Library/Fonts/ArialBold.ttf'))
        else:
            # Eğer sistem fontu bulunamazsa ReportLab'in standart Helvetica fontuna döner (Kutucuk kalabilir)
            pdfmetrics.registerFont(TTFont('TurkishArial', 'Helvetica'))
            pdfmetrics.registerFont(TTFont('TurkishArialBold', 'Helvetica-Bold'))
            
    except Exception as e:
        print(f"[!] Font yükleme uyarısı: {e}. Standart font kullanılacak.")

# --- GÖRSEL AYARLAR VE EKRAN TEMİZLEME ---
def ekrani_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- HAREKETLİ SİBER MASKOT (LOADING ANIMATION) ---
def siber_dedektif_animasyonu(durum_etkinligi, dosya_adı):
    animasyon_karakterleri = [
        "   [ 🕵️‍♂️ ]  Scanning...   ",
        "   [ 🔍 ]  Analyzing...  ",
        "   [ 🛡️ ]  Shielding...  ",
        "   [ 🤖 ]  Thinking...   "
    ]
    
    maskotlar = [
        r"""
          🤖/
         /|  
         / \ 
        Cassandra is looking...
        """,
        r"""
         \🤖 
          |/ 
         / \ 
        Cassandra is reading...
        """,
        r"""
          🤖 
         /|\ 
          |  
        Cassandra is auditing...
        """
    ]
    
    idx = 0
    while not durum_etkinligi.is_set():
        ekrani_temizle()
        print("\n\033[1;36m" + "="*50)
        print("⚡ CASSANDRA SİBER GÜVENLİK MOTORU ÇALIŞIYOR")
        print("="*50 + "\033[0m")
        print(maskotlar[idx % len(maskotlar)])
        print(f"\033[1;33m{animasyon_karakterleri[idx % len(animasyon_karakterleri)]}\033[0m")
        print(f"\033[1;30mHedef Dosya: {dosya_adı}\033[0m")
        print("\033[1;30mLütfen bekleyin, yapay zeka derin analizi tamamlıyor...\033[0m")
        idx += 1
        time.sleep(0.5)

# --- OK TUŞU SEÇİM MOTORU ---
def terminalde_dosya_sec(dosya_listesi):
    if not dosya_listesi: return None
    secili_indeks = 0
    
    if os.name == 'nt':
        import msvcrt
        def tus_al():
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ch = msvcrt.getch()
                if ch == b'H': return "yukari"
                if ch == b'P': return "asagi"
            if ch == b'\r': return "enter"
            return None
    else:
        import tty, termios
        def tus_al():
            fd = sys.stdin.fileno()
            eski_ayarlar = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    ch2 = sys.stdin.read(2)
                    if ch2 == '[A': return "yukari"
                    if ch2 == '[B': return "asagi"
                if ch == '\r' or ch == '\n': return "enter"
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, eski_ayarlar)
            return None

    while True:
        ekrani_temizle()
        print("\033[1;35m==================================================")
        print("📁 🛡️ CASSANDRA - CODESPACE AUDITOR")
        print("(UP/DOWN ile gez, ENTER ile dosyayı seç)")
        print("==================================================\033[0m")
        for i, dosya in enumerate(dosya_listesi):
            if i == secili_indeks:
                print(f"  \033[1;31m👉 [➔ {dosya}]\033[0m")
            else:
                print(f"     📄 {dosya}")
        print("\033[1;35m==================================================\033[0m")
        tus = tus_al()
        if tus == "yukari": secili_indeks = (secili_indeks - 1) % len(dosya_listesi)
        elif tus == "asagi": secili_indeks = (secili_indeks + 1) % len(dosya_listesi)
        elif tus == "enter": return dosya_listesi[secili_indeks]

# --- PREMIUM PDF RAPORLAYICI ---
def renkli_pdf_raporu_olustur(ai_metni, kaynak_dosya):
    pdf_adi = "CASSANDRA_GÜVENLİK_RAPORU.pdf"
    doc = SimpleDocTemplate(pdf_adi, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    
    KoyuKirmizi = colors.HexColor("#8B0000")
    KoyuLacivert = colors.HexColor("#1A252C")
    MetinRengi = colors.HexColor("#333333")
    
    # Fontları Türkçe destekleyen 'TurkishArial' ile güncelledik
    baslik_stili = ParagraphStyle('Baslik', parent=styles['Heading1'], fontName='TurkishArialBold', fontSize=22, textColor=KoyuKirmizi, spaceAfter=15)
    alt_baslik_stili = ParagraphStyle('AltBaslik', parent=styles['Heading2'], fontName='TurkishArialBold', fontSize=13, textColor=KoyuLacivert, spaceBefore=14, spaceAfter=8)
    normal_stil = ParagraphStyle('NormalMetin', parent=styles['Normal'], fontName='TurkishArial', fontSize=10, textColor=MetinRengi, leading=15, spaceAfter=8)
    
    # Kod blokları için de Courier yerine TurkishArial kullanarak Türkçe karakterleri koruyoruz
    kod_stili = ParagraphStyle('KodBlogu', parent=styles['Normal'], fontName='TurkishArial', fontSize=9, textColor=colors.HexColor("#1E6B1E"), backColor=colors.HexColor("#F5F5F5"), borderPadding=8, spaceAfter=12, leading=13)

    story.append(Paragraph("🛡️ CASSANDRA PREMIUM SECURITY REPORT", baslik_stili))
    story.append(Paragraph(f"<b>Hedef Dosya:</b> {kaynak_dosya} | <b>Tarih:</b> {time.strftime('%Y-%m-%d')}", normal_stil))
    story.append(Spacer(1, 15))
    
    tablo_cizgi = Table([[""]], colWidths=[530])
    tablo_cizgi.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 2, KoyuLacivert)]))
    story.append(tablo_cizgi)
    story.append(Spacer(1, 15))

    kod_blogu_aktif = False
    kod_icerigi = []
    
    for satir in ai_metni.split("\n"):
        satir_strip = satir.strip()
        
        if satir_strip.startswith("```"):
            if not kod_blogu_aktif:
                kod_blogu_aktif = True
            else:
                kod_blogu_aktif = False
                story.append(Paragraph("<br/>".join(kod_icerigi), kod_stili))
                kod_icerigi = []
            continue
            
        if kod_blogu_aktif:
            # HTML karakter çakışmalarını önle
            güvenli_satir = satir.replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
            kod_icerigi.append(güvenli_satir)
            continue
            
        if satir_strip.startswith("###"):
            story.append(Paragraph(satir_strip.replace("###", "").strip(), alt_baslik_stili))
        elif satir_strip.startswith("##"):
            story.append(Paragraph(satir_strip.replace("##", "").strip(), baslik_stili))
        elif satir_strip:
            islenmis_satir = satir
            # Markdown kalın fontları HTML tag'ine dönüştür
            while "**" in islenmis_satir:
                islenmis_satir = islenmis_satir.replace("**", "<b>", 1).replace("**", "</b>", 1)
            # Tire ile başlayan listeleri güzelleştir
            if islenmis_satir.strip().startswith("-"):
                islenmis_satir = f"• {islenmis_satir.strip()[1:].strip()}"
            story.append(Paragraph(islenmis_satir, normal_stil))

    doc.build(story)

# --- OPENAI API BAĞLANTISI ---
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def api_anahtarini_al():
    print("\n\033[1;32m🔑 CASSANDRA AI AUTH LAYER\033[0m")
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key and env_key.startswith("sk-"):
        return env_key
    while True:
        user_key = input("👉 OpenAI API Key'inizi giriniz: ").strip()
        if user_key: return user_key

def api_ile_kod_analiz_et(dosya_yolu, api_key):
    if not os.path.exists(dosya_yolu):
        print(f"[-] Hata: '{dosya_yolu}' dosyası bulunamadı.")
        return

    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        kaynak_kod = dosya.read()

    durum_etkinligi = threading.Event()
    animasyon_thread = threading.Thread(target=siber_dedektif_animasyonu, args=(durum_etkinligi, dosya_yolu))
    animasyon_thread.daemon = True 
    animasyon_thread.start()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    sistem_talimati = """
Sen kıdemli bir Siber Güvenlik Denetçisi ve Baş Yazılım Mimarısın. 
Sana verilen kaynak kodu siber güvenlik açıkları, mantık hataları ve performans için analiz et. 
Yanıtını tam olarak şu 3 ana bölümden oluşan, profesyonel bir Türkçe Markdown raporu olarak sun:

### BÖLÜM 1: SİBER GÜVENLİK ZAFİYETLERİ (OWASP & CVE MAPPING)
- **Zafiyet Adı & Derecesi:**
- **İlgili Satır:**
- **CWE & CVE Referansı:**
- **Teknik Açıklama:**
- **Güvenli Kod Yaması:**

### BÖLÜM 2: İŞ MANTIĞI VE AKIŞ HATALARI
### BÖLÜM 3: PERFORMANS VE REFACTORING ÖNERİLERİ
"""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": sistem_talimati},
            {"role": "user", "content": f"Dosya: {dosya_yolu}\n--- KOD ---\n{kaynak_kod}"}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(OPENAI_URL, headers=headers, json=payload, timeout=90)
        
        durum_etkinligi.set()
        animasyon_thread.join(timeout=1)
        
        ekrani_temizle()
        
        if response.status_code == 401:
            print("[-] Hata: API anahtarın geçersiz veya hatalı!")
            return
            
        response.raise_for_status()
        ai_raporu = response.json()["choices"][0]["message"]["content"]
        
        print("\n[+] Analiz başarıyla tamamlandı! PDF Raporu oluşturuluyor...")
        renkli_pdf_raporu_olustur(ai_raporu, dosya_yolu)
        print(f"\n\033[1;32m[🏆 BAŞARILI] Raporunuz PDF formatında basıldı! -> CASSANDRA_GÜVENLİK_RAPORU.pdf\033[0m\n")

    except Exception as e:
        durum_etkinligi.set()
        ekrani_temizle()
        print(f"[-] Hata Oluştu veya İstek Zaman Aşımına Uğradı: {e}")

if __name__ == "__main__":
    ekrani_temizle()
    # İlk iş olarak Türkçe font motorunu çalıştır
    turkce_font_ayarla()
    
    guncel_script_adi = os.path.basename(__file__)
    tum_dosyalar = os.listdir(".")
    
    taranabilir_dosyalar = [d for d in tum_dosyalar if os.path.isfile(d) and d != guncel_script_adi and not d.endswith(".pdf")]
    
    if not taranabilir_dosyalar:
        print(f"[-] Hata: Klasörde analiz edilecek kod dosyası bulunamadı!")
        sys.exit(1)
        
    secilen_hedef_dosya = terminalde_dosya_sec(taranabilir_dosyalar)
    if secilen_hedef_dosya:
        ekrani_temizle()
        secilen_api_key = api_anahtarini_al()
        api_ile_kod_analiz_et(secilen_hedef_dosya, secilen_api_key)