import re
from httpx import Client
from Kekik.cli import konsol as log  # ya da print de olur
from parsel import Selector

class MonoTV:
    def __init__(self, m3u_dosyasi):
        self.m3u_dosyasi = m3u_dosyasi
        self.httpx = Client(
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"
            }
        )
        self.sabit_domain = "https://monotv523.com"

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

        # Sadece referrer'ı monotv523.com olan satırları bul
        pattern = r'(https?:\/\/[^\/]+\.(?:workers\.dev|shop|click|cfd)\/[^\s]+\.m3u8[^\n]*\n#EXTVLCOPT:http-referrer=https:\/\/monotv523\.com\/)'
        
        if not (eski_yayinlar := re.findall(pattern, m3u_icerik)):
            raise ValueError("M3U dosyasında monotv523 referanslı yayın URL'leri bulunamadı!")

        yeni_yayin_url = self.yayin_urlini_al()

        for eski_yayin in set(eski_yayinlar):  # Tekrarları önlemek için set kullanıyoruz
            log.log(f"[yellow][~] Eski Yayın URL : {eski_yayin.split()[0]}")
            # Yalnızca URL kısmını değiştir (referrer kısmını koru)
            yeni_satir = eski_yayin.replace(eski_yayin.split()[0], yeni_yayin_url)
            m3u_icerik = m3u_icerik.replace(eski_yayin, yeni_satir)

        with open(self.m3u_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)

        log.log(f"[green][✓] M3U dosyası başarıyla güncellendi. Sadece monotv523.com referanslı yayınlar değiştirildi.")

if __name__ == "__main__":
    guncelle = MonoTV("Kanallar/kerim.m3u")
    guncelle.m3u_guncelle()
