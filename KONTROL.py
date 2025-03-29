import requests
import re
from rich.console import Console

console = Console()

class IPTVParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.kanallar = []
        self.oturum = requests.Session()
        self.oturum.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def dosya_parse(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            icerik = file.read()

        kanal_bloklari = re.findall(r'#EXTINF:-1([^\n]*)\n([^#\n]+)', icerik)
        
        for kanal_bilgi, kanal_url in kanal_bloklari:
            kanal = {}
            
            # tvg-name özelliğini kanal adı olarak kullan
            name_match = re.search(r'tvg-name="([^"]+)"', kanal_bilgi)
            if name_match:
                kanal['ad'] = name_match.group(1)
            else:
                continue  # tvg-name yoksa bu kanalı atla
            
            # Diğer özellikleri ekle
            kanal['url'] = kanal_url.strip()
            kanal['user-agent'] = None
            
            self.kanallar.append(kanal)

    def kanallar_kontrol(self):
        for kanal in self.kanallar:
            console.print(f"[~] Kontrol Ediliyor : {kanal['ad']}")
            
            try:
                response = self.oturum.get(kanal['url'], stream=True, timeout=5)
                if response.status_code == 200:
                    console.print(f"[+] Kontrol Edildi   : {kanal['ad']}")
                else:
                    console.print(f"[!] {response.status_code} » {kanal['url']} » {kanal['ad']}")
            except Exception as e:
                console.print(f"[!] Hata » {kanal['url']} » {kanal['ad']} » {str(e)}")

    def run(self):
        self.dosya_parse()
        self.kanallar_kontrol()

if __name__ == "__main__":
    parser = IPTVParser("kerim.m3u")
    parser.run()
