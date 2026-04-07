import requests
from bs4 import BeautifulSoup
import json
import csv
import time

BASE_URL = "http://quotes.toscrape.com/page/{}/"

def scrape_quotes():
    data = []
    page = 1

    while True:
        print(f"Scraping halaman {page}...")
        url = BASE_URL.format(page)
        response = requests.get(url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            break

        for q in quotes:
            text = q.find("span", class_="text").text
            author = q.find("small", class_="author").text

            data.append({
                "quote": text,
                "author": author
            })

        page += 1
        time.sleep(2) 

    return data


def save_json(data):
    with open("data/hasil.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_csv(data):
    with open("data/hasil.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["quote", "author"])
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    hasil = scrape_quotes()
    save_json(hasil)
    save_csv(hasil)
    print("✅ Data berhasil disimpan ke JSON & CSV")