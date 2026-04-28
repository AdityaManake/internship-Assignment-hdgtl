import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

def get_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
    }

categories = [
    {"category": "Electronics", "subcategory": "Mobile Phones", "url": "https://www.amazon.in/s?k=mobile+phones&i=electronics"},
    {"category": "Electronics", "subcategory": "Laptops", "url": "https://www.amazon.in/s?k=laptops&i=computers"},
    {"category": "Electronics", "subcategory": "Headphones", "url": "https://www.amazon.in/s?k=headphones&i=electronics"},
    {"category": "Home & Kitchen", "subcategory": "Kitchen Appliances", "url": "https://www.amazon.in/s?k=kitchen+appliances&i=kitchen"},
    {"category": "Home & Kitchen", "subcategory": "Home Decor", "url": "https://www.amazon.in/s?k=home+decor&i=kitchen"},
    {"category": "Books", "subcategory": "Fiction", "url": "https://www.amazon.in/s?k=fiction+books&i=stripbooks"},
    {"category": "Fashion", "subcategory": "Men's T-Shirts", "url": "https://www.amazon.in/s?k=mens+tshirts&i=apparel"},
    {"category": "Fashion", "subcategory": "Women's Dresses", "url": "https://www.amazon.in/s?k=womens+dresses&i=apparel"},
    {"category": "Sports & Fitness", "subcategory": "Fitness Equipment", "url": "https://www.amazon.in/s?k=fitness+equipment&i=sporting"},
    {"category": "Beauty", "subcategory": "Skincare", "url": "https://www.amazon.in/s?k=skincare+products&i=beauty"},
]


def scrape_page(url, category, subcategory, page=1):
    items = []

    if page > 1:
        url = url + f"&page={page}"
    try:
        res = requests.get(url, headers=get_headers())
        if res.status_code != 200:
            return items
    except:
        return items

    soup = BeautifulSoup(res.text, "html.parser")

    cards = soup.find_all("div", attrs={"data-component-type": "s-search-result"})

    if not cards:
        cards = soup.find_all("div", class_=re.compile("s-result-item"))

    for c in cards:
        obj = {}

        title_tag = c.find("h2")
        if title_tag:
            obj["Product Title"] = title_tag.get_text(strip=True)
        else:
            continue
        price = c.find("span", class_="a-price-whole")
        if price:
            val = price.get_text(strip=True).replace(",", "")
            obj["Price"] = "₹" + val
        else:
            obj["Price"] = "N/A"
        rating = c.find("span", class_="a-icon-alt")
        if rating:
            txt = rating.get_text()
            m = re.search(r'([\d.]+)', txt)
            obj["Rating"] = m.group(1) if m else "N/A"
        else:
            obj["Rating"] = "N/A"
        obj["Category"] = category
        obj["Subcategory"] = subcategory
        items.append(obj)

    return items

def main():
    print("Scraping products...")

    all_items = []

    for cat in categories:
        for p in range(1, 3):
            data = scrape_page(cat["url"], cat["category"], cat["subcategory"], p)
            all_items.extend(data)
            time.sleep(random.uniform(2, 4))

    df = pd.DataFrame(all_items)
    df = df.drop_duplicates(subset=["Product Title"])
    df.replace("N/A", pd.NA, inplace=True)
    df.dropna(inplace=True)
    df.dropna
    for col in ["Product Title", "Category", "Subcategory"]:
        df[col] = df[col].astype(str).str.strip()
    df = df.reset_index(drop=True)
    df.to_csv("task2.csv", index=False)
    print(f"Done. {len(df)} products saved to task2.csv")

if __name__ == "__main__":
    main()