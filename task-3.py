import requests
import pandas as pd
import os 

url = "https://overpass-api.de/api/interpreter"
query = """
[out:json];
area["name"="Pune"]->.searchArea;
(
  node["tourism"](area.searchArea);
);
out body;
"""

headers = {
    "User-Agent": "PuneTourismScraper/1.0"
}

response = requests.post(url, data={'data': query}, headers=headers, timeout=60)
try:
    data=response.json()
except:
    print("Invalid JSON response")
    print(response.text)
    exit()

rows=[]
for elems in data['elements']:
    tags=elems.get('tags',{})
    rows.append({
        "Name": tags.get("name"),
        "Type":tags.get("tourism"),
        "Latitude": elems.get("lat"),
        "Longitude": elems.get("lon")
    })

df=pd.DataFrame(rows)

df= df.dropna(subset=["Name"])

output_dir="assignment"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_file=os.path.join(output_dir,"task-3.csv")

df.to_csv(output_file,index=False)

print(f"Done — {len(df)} records saved to {output_file}")
