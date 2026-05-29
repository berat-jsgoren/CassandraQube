import requests
import json
import time
import csv

# --- AYARLAR ---
API_KEY = "BURAYA KENDİ KEY NUMARANIZI GİRECEKSİNİZ"
BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
CSV_DOSYA_ADI = "nvd_tum_cve_veritabani.csv"

RESULTS_PER_PAGE = 2000  # Tek seferde çekebileceğimiz maksimum paket (Hızlanması için artırdık)

def fetch_all_nvd_cves():
    start_index = 0
    total_results = 1  # Döngünün başlaması için geçici bir değer
    headers = {}
    
    if API_KEY and API_KEY != "BURAYADA KENDİ APİNİZİ GİRECEKSİNİZ":
        headers["apiKey"] = API_KEY
        print("[+] API Anahtarı aktif. Maksimum hızda çalışılıyor.")
        delay = 1
    else:
        print("[!] API Anahtarı yok. Güvenli (Yavaş) modda çalışılıyor.")
        delay = 6

    with open(CSV_DOSYA_ADI, mode="w", newline="", encoding="utf-8") as dosya:
        yazici = csv.writer(dosya)
        yazici.writerow(["CVE ID", "Yayın Tarihi", "Analiz Durumu", "CVSS Skoru", "Zafiyet Açıklaması"])

        # start_index, API'den gelen gerçek toplam veri sayısından küçük olduğu sürece çekmeye devam et
        while start_index < total_results:
            
            params = {
                "startIndex": start_index,
                "resultsPerPage": RESULTS_PER_PAGE
            }
            
            try:
                response = requests.get(BASE_URL, headers=headers, params=params, timeout=20)
                
                if response.status_code in [403, 429]:
                    print("[-] Rate Limit! Engel yememek için 15 saniye duraklatılıyor...")
                    time.sleep(15)
                    continue
                    
                response.raise_for_status()
                data = response.json()
                
                # KRİTİK DEĞİŞİKLİK: NVD'deki güncel toplam CVE sayısını dinamik olarak alıyoruz
                total_results = data.get("totalResults", 0)
                
                if start_index == 0:
                    print(f"[+ ] Sistemde toplam {total_results} adet CVE kaydı bulundu!")
                    print("[+] Tarama işlemi başlatıldı, bu işlem zaman alacaktır...\n")

            except requests.exceptions.RequestException as e:
                print(f"[-] Bağlantı hatası: {e}. 10 saniye sonra tekrar denenecek...")
                time.sleep(10)
                continue
                
            vulnerabilities = data.get("vulnerabilities", [])
            if not vulnerabilities:
                break
                
            for item in vulnerabilities:
                cve_data = item.get("cve", {})
                cve_id = cve_data.get("id", "N/A")
                published = cve_data.get("published", "N/A")
                status = cve_data.get("vulnStatus", "N/A")
                
                descriptions = cve_data.get("descriptions", [])
                description = descriptions[0].get("value", "Açıklama Yok") if descriptions else "Açıklama Yok"
                
                metrics = cve_data.get("metrics", {})
                cvss_score = "N/A"
                if "cvssMetricV31" in metrics:
                    cvss_score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
                elif "cvssMetricV30" in metrics:
                    cvss_score = metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]
                elif "cvssMetricV2" in metrics:
                    cvss_score = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]
                
                yazici.writerow([cve_id, published, status, cvss_score, description])
                
            print(f"[+] İndeks {start_index} ile {start_index + len(vulnerabilities)} arası başarıyla kaydedildi. (Toplam: {total_results})")
            
            # Bir sonraki sayfa için indeksi ilerlet
            start_index += RESULTS_PER_PAGE
            time.sleep(delay)

    print(f"\n[+] Muazzam! Tüm NVD veritabanı '{CSV_DOSYA_ADI}' dosyasına indirildi.")

if __name__ == "__main__":
    fetch_all_nvd_cves()