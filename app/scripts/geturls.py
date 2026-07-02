import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/productcatalog/"

res = requests.get(CATALOG_URL)
soup = BeautifulSoup(res.text, "html.parser")

urls = []

for a in soup.find_all("a", href=True):
    href = a["href"]

    if "/products/product-catalog/view/" in href:
        full_url = BASE_URL + href if href.startswith("/") else href
        urls.append(full_url)

urls = list(set(urls))

with open("data/urls.txt", "w") as f:
    for url in urls:
        f.write(url + "\n")

print("Total URLs:", len(urls))