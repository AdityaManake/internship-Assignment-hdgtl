import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

headers = {
    "User-Agent": "Mozilla/5.0",
}

base_url = "https://magicpin.in/india/Ahmedabad/All/Fitness/"

areas = [
    "All", "Ellis-Bridge", "Satellite", "Navrangpura", "Vastrapur",
    "Bodakdev", "C-G-Road", "Paldi", "Maninagar", "Khanpur",
    "Lal-Darwaja", "Naranpura", "Thaltej", "Prahlad-Nagar",
    "Bopal", "Gota", "Chandkheda", "Memnagar", "Ambawadi",
    "Shahibaug", "Ashram-Road", "Gurukul", "Drive-In-Road",
    "Jodhpur", "Vejalpur", "Vastral", "Nikol", "Naroda",
    "Bapunagar", "Gomtipur", "Odhav", "Isanpur", "Jamalpur",
    "Sarkhej", "S-G-Highway", "Ghatlodiya", "Ranip",
    "Sabarmati", "Wadaj", "Chandlodia"
]


def fetch_page(url):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return BeautifulSoup(res.text, "html.parser")
    except:
        return None


def get_links(soup):
    data = []
    if soup is None:
        return data

    links = soup.find_all("a", href=True)
    pattern = re.compile(r'/Ahmedabad/([^/]+)/Fitness/([^/]+)/store/([^/]+)/')

    seen = set()
    for link in links:
        href = link.get("href")
        if not href:
            continue
        match = pattern.search(href)
        if match:
            sid = match.group(3)
            if sid in seen:
                continue
            seen.add(sid)
            data.append({
                "url": f"https://magicpin.in{href}",
                "area": match.group(1),
                "name": match.group(2)
            })

    return data


def get_details(url):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return {}
        soup = BeautifulSoup(res.text, "html.parser")
    except:
        return {}
    out = {}
    t = soup.find("title")
    if t:
        txt = t.get_text()
        out["name"] = txt.split(",")[0]

    return out


def main():
    print("Scraping gyms...")

    all_links = {}

    for area in areas:
        url = base_url if area == "All" else f"https://magicpin.in/india/Ahmedabad/{area}/Fitness/"
        soup = fetch_page(url)
        gyms = get_links(soup)
        for g in gyms:
            if g["url"] not in all_links:
                all_links[g["url"]] = g
        time.sleep(random.uniform(1, 2))

    rows = []
    count = 0

    for url, g in all_links.items():
        count += 1
        details = get_details(url)
        area_clean = g["area"].replace("-", " ").title()
        rows.append({
            "GYM Name": details.get("name", g["name"].replace("-", " ").title()),
            "Address": f"{area_clean}, Ahmedabad, Gujarat",
            "Area": area_clean,
            "City": "Ahmedabad",
            "State": "Gujarat"
        })
        time.sleep(random.uniform(0.5, 1.2))
        if count >= 120:
            break
    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["GYM Name"])
    df = df.sort_values("Area")
    df.to_csv("task1.csv", index=False)
    print(f"Done. {len(df)} gyms saved to gyms.csv")


if __name__ == "__main__":
    main()