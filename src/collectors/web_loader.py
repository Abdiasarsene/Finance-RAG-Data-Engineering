# scraped_urls/web_loader.py
import time
import os
import json
import hashlib
import requests
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup

RAW_URLS_DIR = Path("./data/urls")
RAW_URLS_DIR.mkdir(parents=True, exist_ok=True)

class WebLoader:
    def __init__(self, save_dir=RAW_URLS_DIR):
        self.save_dir = save_dir

    # Générer un nom de fichier unique à partir de l'URL
    def url_to_filename(self, url: str) -> str:
        url_hash = hashlib.sha1(url.encode("utf-8")).hexdigest()
        return os.path.join(self.save_dir, f"{url_hash}.json")

    # Télécharger l'URL et extraire le contenu texte
    def fetch_url(self, url: str) -> dict:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url,headers=headers, timeout=10)
            status = resp.status_code

            if status != 200:
                content_text, title = "",""
            else:
                soup = BeautifulSoup(resp.text, "html.parser")
                content_text = soup.get_text(separator="\n", strip=True)
                title = soup.title.string if soup.title else ""

            data = {
                "source": "web",
                "date_collected": datetime.now(timezone.utc).isoformat(),
                "raw_content": content_text,
                "metadata": {
                    "url": url,
                    "title": title,
                    "http_status":status
                }
            }
            return data

        except Exception as e:
            print(f"[ERROR] Failed to fetch {url} : {e}")
            return {
                "url": url,
                "title": "",
                "date_scraped": datetime.now(timezone.utc).isoformat(),
                "http_status": None,
                "content": ""
            }

    # Sauvegarder le snapshot JSON dans data/urls/
    def save_json(self, data: dict):
        filename = self.url_to_filename(data["metadata"]["url"])
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[INFO] Saved {filename}")

    # Télécharger et sauvegarder plusieurs URLs
    def load_urls(self, url_list: list):
        for url in url_list:
            data = self.fetch_url(url)
            self.save_json(data)
            time.sleep(5)

if __name__ == "__main__":
    urls = [
        "https://www.psbedu.paris/fr/actus/quest-ce-que-la-finance-dentreprise",
        "https://www.earlypay.com.au/blog/business-finance-fundamentals-infographic/",
        "https://ifim.edu.in/understanding-business-finance-for-beginners/",
        "https://shs.cairn.info/fondements-de-la-finance-de-marche--9782140297427-page-13?lang=fr",
        "https://www.business.govt.nz/tax-and-accounting/business-finance-basics/introduction-to-business-financej",
        "https://finance.yahoo.com/markets/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAACmRPuSwGBeVdhLP-OJrXETsLbfTgk0pgaOI8dKYOG5ZQxm1U1pA6KS84n4GJStDbdb-jko9OmMLFJaUIhzo7xoxoEIDkDIcLp3UBZvRwP7AbXLBTOugPSBYHCEi8GkVCCVXlf8JcMSHYaFFQjzri87pwGyMTAiYXsEwlvQAbndc"
        "https://corporatefinanceinstitute.com/resources/wealth-management/what-is-finance-definition/",
        "https://www.google.com/finance/?hl=fr"
    ]
    loader = WebLoader()
    loader.load_urls(urls)