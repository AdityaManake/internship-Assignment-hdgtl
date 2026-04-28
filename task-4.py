import pandas as pd
import os
from urllib.parse import urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def build_map(category, entries):
    """helper to build url_map entries grouped by category"""
    return {k: (category, v) for k, v in entries.items()}

url_map = {}
url_map.update(build_map("Education", {
    "playschools": "Play Schools", "play-schools": "Play Schools", "preschools": "Pre Schools",
    "pre-schools": "Pre Schools", "schools": "Schools", "tuitions": "Tuitions",
    "coaching": "Coaching", "training": "Training", "colleges": "Colleges",
    "universities": "Universities", "nursery": "Nursery Schools", "daycare": "Day Care",
    "creche": "Creche", "montessori": "Montessori", "computer-training": "Computer Training",
    "spoken-english": "Spoken English",
}))
url_map.update(build_map("Healthcare", {
    "doctors": "Doctors", "hospitals": "Hospitals", "clinics": "Clinics", "dentists": "Dentists",
    "dental": "Dental Clinics", "pharmacies": "Pharmacies", "homeopathy-pharmacies": "Homeopathy",
    "homeopathy": "Homeopathy", "ayurvedic": "Ayurvedic", "physiotherapy": "Physiotherapy",
    "eye-hospitals": "Eye Hospitals", "skin-clinics": "Skin Clinics", "pathology": "Pathology Labs",
    "diagnostics": "Diagnostics", "veterinary": "Veterinary", "orthopaedic": "Orthopaedic",
    "gynecologist": "Gynecologist", "pediatrician": "Pediatrician", "health": "General Health",
}))
url_map.update(build_map("Real Estate", {
    "flats": "Flats", "apartments": "Apartments", "plots": "Plots", "villas": "Villas",
    "pg": "PG / Paying Guest", "paying-guest": "PG / Paying Guest", "hostel": "Hostel",
    "commercial-property": "Commercial Property", "real-estate": "Real Estate",
    "property": "Property", "rent": "Rental", "builders": "Builders",
}))
url_map.update(build_map("Services", {
    "packers-movers": "Packers & Movers", "packers-and-movers": "Packers & Movers",
    "plumbers": "Plumbers", "electricians": "Electricians", "pest-control": "Pest Control",
    "ac-repair": "AC Repair", "car-repair": "Car Repair", "car-service": "Car Service",
    "interior-designers": "Interior Design", "architects": "Architects",
    "event-management": "Event Management", "catering": "Catering",
    "security-services": "Security Services", "cleaning-services": "Cleaning Services",
    "laundry": "Laundry", "courier": "Courier", "taxi": "Taxi Services",
    "travel": "Travel Services", "photography": "Photography", "wedding": "Wedding Services",
    "beauty-parlour": "Beauty Parlour", "salon": "Salon", "spa": "Spa",
    "gym": "Gym / Fitness", "fitness": "Fitness", "yoga": "Yoga",
}))
url_map.update(build_map("Food & Dining", {
    "restaurants": "Restaurants", "tiffin": "Tiffin Services", "bakery": "Bakery",
    "caterers": "Caterers", "sweet-shops": "Sweet Shops",
}))
url_map.update(build_map("Legal & Finance", {
    "lawyers": "Lawyers", "advocates": "Advocates", "ca": "Chartered Accountants",
    "chartered-accountants": "Chartered Accountants", "tax-consultants": "Tax Consultants",
    "insurance": "Insurance", "loans": "Loans",
}))
url_map.update(build_map("Automotive", {
    "car-dealers": "Car Dealers", "bike-dealers": "Bike Dealers",
    "driving-schools": "Driving Schools", "car-accessories": "Car Accessories",
    "tyre-dealers": "Tyre Dealers",
}))
url_map.update(build_map("Shopping", {
    "furniture": "Furniture", "electronics": "Electronics", "mobiles": "Mobile Phones",
    "jewellery": "Jewellery", "clothing": "Clothing", "supermarket": "Supermarket",
    "grocery": "Grocery",
}))
kw_map = {
    "play school": ("Education", "Play Schools"), "pre school": ("Education", "Pre Schools"),
    "school": ("Education", "Schools"), "tuition": ("Education", "Tuitions"),
    "coaching": ("Education", "Coaching"), "college": ("Education", "Colleges"),
    "doctor": ("Healthcare", "Doctors"), "hospital": ("Healthcare", "Hospitals"),
    "dentist": ("Healthcare", "Dentists"), "pharmacy": ("Healthcare", "Pharmacies"),
    "flat": ("Real Estate", "Flats"), "apartment": ("Real Estate", "Apartments"),
    "pg near me": ("Real Estate", "PG / Paying Guest"), "property": ("Real Estate", "Property"),
    "packers": ("Services", "Packers & Movers"), "plumber": ("Services", "Plumbers"),
    "electrician": ("Services", "Electricians"), "pest control": ("Services", "Pest Control"),
    "salon": ("Services", "Salon"), "gym": ("Services", "Gym / Fitness"),
    "restaurant": ("Food & Dining", "Restaurants"), "lawyer": ("Legal & Finance", "Lawyers"),
    "car dealer": ("Automotive", "Car Dealers"), "furniture": ("Shopping", "Furniture"),
}

domain_map = {
    "99acres": ("Real Estate", "Property Listings"), "magicbricks": ("Real Estate", "Property Listings"),
    "housing": ("Real Estate", "Property Listings"), "practo": ("Healthcare", "Medical Services"),
    "lybrate": ("Healthcare", "Medical Services"), "zomato": ("Food & Dining", "Food Delivery"),
    "swiggy": ("Food & Dining", "Food Delivery"), "naukri": ("Jobs", "Job Portal"),
    "indeed": ("Jobs", "Job Portal"),
}

def classify(keyword, url):
    """figure out (Category, Sub-Category) using URL path, then keyword, then domain"""
    try:
        path = urlparse(url).path.lower()
        parts = path.strip("/").split("/")
    except:
        parts = []

    for p in parts:
        if p.strip() in url_map:
            return url_map[p.strip()]
    for p in parts:
        for key in url_map:
            if key in p:
                return url_map[key]

    kw_lower = keyword.lower()
    for noise in ["near me", "best", "top"]:
        kw_lower = kw_lower.replace(noise, "")
    kw_lower = kw_lower.strip()
    for key, val in kw_map.items():
        if key in keyword.lower():
            return val

    try:
        domain = urlparse(url).netloc.lower()
        for site, cat in domain_map.items():
            if site in domain:
                return cat
        if "sulekha" in domain:
            return ("Services", parts[0].replace("-", " ").title() if parts else "General")
    except:
        pass

    return ("Uncategorized", "Unknown")

def process_sheet(filepath, label):
    df = pd.read_csv(filepath)
    results = df.apply(lambda r: classify(r["Keyword"], r["URL"]), axis=1, result_type="expand")
    df[["Category", "Sub-Category"]] = results
    print(f"\n{label}: {len(df)} rows")
    print(df["Category"].value_counts().to_string())
    return df

if __name__ == "__main__":
    print("Task 4 - Research Data Mapping\n" + "-" * 35)

    df1 = process_sheet(os.path.join(SCRIPT_DIR, "task4_input_sheet1.csv"), "Sheet 1")
    df2 = process_sheet(os.path.join(SCRIPT_DIR, "task4_input_sheet2.csv"), "Sheet 2")

    df1.to_csv(os.path.join(SCRIPT_DIR, "task4_sheet1.csv"), index=False, encoding="utf-8-sig")
    df2.to_csv(os.path.join(SCRIPT_DIR, "task4_sheet2.csv"), index=False, encoding="utf-8-sig")

    combined = pd.concat([df1, df2], ignore_index=True)
    combined.to_csv(os.path.join(SCRIPT_DIR, "task4.csv"), index=False, encoding="utf-8-sig")

    print(f"\nTotal: {len(combined)} rows saved")
    print("\nFirst 10:")
    print(combined.head(10).to_string(index=False))
    print(f"\nBreakdown:\n{combined['Category'].value_counts().to_string()}")
