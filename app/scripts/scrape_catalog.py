import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

urls = open("data/urls.txt").read().splitlines()

catalog = []

def safe_get(text):
    return text.strip() if text else ""

for url in urls:
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        name = safe_get(soup.title.text)

        description = ""
        desc_tag = soup.find("meta", {"name": "description"})
        if desc_tag:
            description = desc_tag.get("content", "")

        # simple skill extraction (basic version)
        skills = []
        for li in soup.find_all("li"):
            skills.append(li.text.strip())

        item = {
            "name": name,
            "url": url,
            "description": description,
            "skills": skills[:5],  # limit noise
            "category": "SHL Assessment",
            "duration": None,
            "scraped_at": datetime.utcnow().isoformat()
        }

        catalog.append(item)

        print("Scraped:", name)

    except Exception as e:
        print("Error:", url, e)

with open("catalog.json", "w") as f:
    json.dump(catalog, f, indent=2)

print("DONE. Total:", len(catalog))