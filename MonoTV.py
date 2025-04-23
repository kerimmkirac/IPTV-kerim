
import re
from httpx import Client
from Kekik.cli import konsol as log  

class MonoTV:
    def __init__(self, m3u_dosyasi):
        self.m3u_dosyasi = m3u_dosyasi
        self.httpx = Client(
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"
            }
        )

    def yayin_urlini_al(self):
        json_endpoint = "https://casintrotv12.com/domain.php"
        log.log(f"[cyan][~] domain.php çağrılıyor: {json_endpoint}")
        try:
            response = self.httpx.get(json_endpoint)
            json_data = response.json()
            yayin_url = json_data["baseurl"].replace("\\/", "/")
            log.log(f"[green][+] Yayın URL bulundu: {yayin_url}")
            return yayin_url
        except Exception as e:
            raise ValueError(f"Yayın URL'si alınamadı: {e}")

    def m3u_guncelle(self):
        with open(self.m3u_dosyasi, "r", encoding="utf-8") as f:
            m3u_icerik = f.read()

        yeni_yayin_url = self.yayin_urlini_al()

        # Referer'i monotv olanları bul
        pattern = re.compile(
            r'(#EXTVLCOPT:http-referrer=(https?://[^/]*monotv[^/]*\.[^\s/]+).+?\n)(https?://[^ \n\r]+)', 
            re.IGNORECASE
        )

        eslesmeler = list(pattern.finditer(m3u_icerik))

        if not eslesmeler:
            raise ValueError("Referer'i monotv olan yayınlar bulunamadı!")

        log.log(f"[yellow][~] Toplam {len(eslesmeler)} adet yayın bulundu, güncelleniyor...")

        for eslesme in eslesmeler:
            eski_link = eslesme[3]
            yeni_link = re.sub(r'https?://[^/]+', yeni_yayin_url, eski_link)
            log.log(f"[blue]• {eski_link} → {yeni_link}")
            m3u_icerik = m3u_icerik.replace(eski_link, yeni_link)

        with open(self.m3u_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)

        log.log(f"[green][✓] Tüm monotv refererli yayın URL'leri başarıyla güncellendi.")

if __name__ == "__main__":
    guncelle = MonoTV("Kanallar/kerim.m3u")
    guncelle.m3u_guncelle()
