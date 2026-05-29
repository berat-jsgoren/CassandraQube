import os
import sqlite3
import pickle
import base64

# =====================================================================
# CASSANDRA TEST LABORATUVARI: ZAFİYETLİ YÖNETİM PANELİ MOTORU
# =====================================================================

# ZAFİYET 1: Hardcoded Credentials (Kod içine gömülmüş kritik şifreler ve API anahtarları)
ADMIN_DB_PASSWORD = "SuperSecureAdminPassword2026!"
AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7INVALIDKEY/SECRET/998877"
ENCRYPTION_KEY = b"secret_key_12345"


def kullanıcı_giriş_sistemi(username, password):
    """Kullanıcı girişini kontrol eden fonksiyon."""
    print(f"[*] Giriş denemesi yapılıyor: {username}")
    
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    
    # ZAFİYET 2: SQL Injection (SQLi) - Kullanıcı girdisi doğrudan sorguya eklenmiş
    # Saldırgan ' OR '1'='1 girdiğinde şifresiz giriş yapabilir.
    sorgu = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        cursor.execute(sorgu)
        user = cursor.fetchone()
        conn.close()
        return user
    except Exception as e:
        print(f"[-] Veritabanı hatası: {e}")
        return None


def sunucu_ping_aracı(ip_adresi):
    """Sistem yöneticisinin ağdaki cihazları pinglemesini sağlayan araç."""
    print(f"[*] Ping atılacak hedef: {ip_adresi}")
    
    # ZAFİYET 3: Command Injection (Sistem Komut Enjeksiyonu)
    # Saldırgan ip_adresi kısmına "127.0.0.1; cat /etc/passwd" yazarak işletim sisteminde komut çalıştırabilir.
    komut = f"ping -c 4 {ip_adresi}"
    
    # Tehlikeli os.system kullanımı
    os.system(komut)


def sistem_günlüklerini_oku(dosya_adı):
    """Sistem log dosyalarını okuyup ekrana basan fonksiyon."""
    # ZAFİYET 4: Path Traversal (Dizin Gezinme / Arbitrary File Read)
    # Girdi kontrolü olmadığı için saldırgan dosya adı yerine "../../etc/passwd" veya "..\..\Windows\win.ini" verebilir.
    log_dizini = "/var/log/app/"
    tam_yol = os.path.join(log_dizini, dosya_adı)
    
    print(f"[*] Okunacak log dosyası: {tam_yol}")
    
    if os.path.exists(tam_yol):
        with open(tam_yol, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "[-] Log dosyası bulunamadı."


def kullanıcı_profil_yedegi_yukle(cookie_verisi):
    """Kullanıcının tarayıcısındaki yedek profil verisini çözüp yükler."""
    print("[*] Kullanıcı yedek profili geri yükleniyor...")
    
    try:
        # ZAFİYET 5: Insecure Deserialization (Güvensiz Nesne Serileştirme)
        # pickle.loads() fonksiyonuna dışarıdan gelen kontrolsüz veri verilmesi Remote Code Execution (RCE) açığı doğurur.
        ham_veri = base64.b64decode(cookie_verisi)
        profil_objesi = pickle.loads(ham_veri)
        return profil_objesi
    except Exception as e:
        return f"[-] Profil yükleme hatası: {e}"


def yedekleme_klasorunu_temizle():
    """Geçici yedekleme klasörünü siler."""
    # ZAFİYET 6: Insecure Temporary File / Permission Issues
    # Sabit bir geçici dizin kullanımı ve yetki kontrolü olmadan işlem yapılması
    gecici_dizin = "/tmp/backup_data"
    if os.path.exists(gecici_dizin):
        os.chmod(gecici_dizin, 0o777)  # Herkese tam yetki verilmiş (Büyük Risk)
        print("[+] Geçici dizin temizleme yetkileri ayarlandı.")


# --- TEST ÇALIŞTIRMA SENARYOLARI (SİMÜLASYON) ---
if __name__ == "__main__":
    print("=== Cassandra Zafiyet Laboratuvarı Aktif ===")
    
    # Kodun normal şartlarda nasıl çalıştığını simüle ediyoruz
    # (api_analyzer.py bu fonksiyon çağrılarını ve yukarıdaki zafiyetli satırları tek tek inceleyecek)
    kullanıcı_giriş_sistemi("admin", "12345")
    sunucu_ping_aracı("8.8.8.8")
    sistem_günlüklerini_oku("app.log")