Selamlar Ben Berat Cassandra topluluğu adına yaptığım aracı duyurmak istiyorum normal görevim aslında CVE sitesinin scaper yazarak CVE çekmekti bunu yaptım yaklaşık
300 binden fazla CVE çeken bir scaper yazdım bu ama DevSecOps a olan ilgimi tutamadığım için bu yaptığım aracı SonarQube tarzı bir araç haline getirmeyi düşündüm umarım
herkes için faydalı bir araç olur :)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---- ARACI KULLANMA ADIMLARI ----


1. Adım: Ücretsiz NVD API Anahtarı (Key) Alma

Sistemin zafiyet taraması yapabilmesi için NIST veritabanına bağlanması gerekir. NVD API anahtarı almak tamamen ücretsizdir.

  1  nvd.nist.gov/developers/request-an-api-key adresine gidin.

  2  Ekranda istenen 3 adet kişisel/kurumsal bilgiyi doldurarak başvurunuzu gönderin.

  3 E-posta adresinize NVD tarafından bir onay maili gelecektir. Mailin ilk kısmında bir aktivasyon linki ve size özel tanımlanmış bir UUID kodu yer alır.

  4  Maildeki UUID kodunu kopyalayın ve verilen aktivasyon linkine tıklayın.

  5 Açılan sayfaya ilk başta kayıt olduğunuz e-posta adresinizi ve kopyaladığınız UUID kodunu girin.

  6  Kısa bir süre bekledikten sonra sistem size özel API Key (Anahtar) çıktısını verecektir. Bu anahtarı güvenli bir yere not edin.

📂 2. Adım: CVE Veritabanını Bilgisayara İndirme

  1  Proje klasörünüzün içinde bulunan cve_veritabanı_cekici.py dosyasını bir kod editörüyle açın.

  2 Dosyanın 7. ve 18. satırlarında yer alan ve yorum satırı olarak belirtilen BURAYA KENDİ KEY NUMARANIZI GİRECEKSİNİZ alanını bulun.

  3  Aldığınız NVD API anahtarını, tırnak işaretlerini kaldırmadan (örn: "ANAH-TAR-IN-IZ") ilgili yerlere yapıştırın ve dosyayı kaydedin.

  4 cve_veritabanı_cekici.py kodunu çalıştırın. Bu işlem yaklaşık 300.000 adet güncel CVE verisini bilgisayarınıza otomatik olarak indirecektir.

  5      ⚠️ Çok Önemli Not: İndirilen veritabanı dosyasının, asıl ana araç ile kesinlikle aynı klasörde (dizinde) bulunması gerekmektedir. Aynı şekilde analiz edeceğiniz (zafiyet barındıran) kaynak kod dosyalarınızın da yine bu ortak klasör içinde olması şarttır.

  6 Not: Bu veritabanı çekme işlemini sistemi ilk kez kurarken sadece bir defaya mahsus yapmanız yeterlidir.
  

🤖 3. Adım: Yapay Zekâ Analiz Aracını Başlatma

 1 Tüm dosyaların aynı klasörde olduğundan emin olduktan sonra asıl ana kodumuz olan ai_analyze.py dosyasını terminal üzerinden başlatın.

  2 Program açıldığında sizden OpenAI API Anahtarınızı (Key) talep edecektir. OpenAI hesabınızdan aldığınız API anahtarını terminale kopyalayıp yapıştırın ve Enter'a basın.

   3 Sistem, bulunduğunuz klasörün içindeki tüm dosyaları tarayacak ve karşınıza şık bir terminal listesi çıkaracaktır.

   4 Analiz edilmesini istediğiniz hedef kod dosyasını klavyenizin yön (ok) tuşları ile seçip Enter tuşuna basın.

📊 Sonuç ve Raporlama

Yapay zekâ ve zafiyet analiz motoru tarama işlemini tamamladıktan sonra, aynı klasörün içerisine zafiyetleri ve çözüm önerilerini içeren detaylı bir PDF analiz raporu otomatik olarak kaydedilecektir.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










