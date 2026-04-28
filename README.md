# Honeybee Digital— Assignment

---

## Task 1 — Scraping Gym & Fitness Center Data from MagicPin

For this task, I scraped gym and fitness center listings from MagicPin for Ahmedabad. I started by listing around 40 areas (like Satellite, Navrangpura, Bopal, etc.) and looped through each area page to collect gym links. I used regex to filter valid store URLs and avoided duplicates by tracking store IDs.

After collecting the links, I visited each gym page to extract the name and basic details. The data was stored in a DataFrame with fields like name, area, city, and state. I also cleaned area names to make them more readable. To reduce the chances of getting blocked, I added random delays between requests. The final dataset was saved as `<span>gyms.csv</span>` after removing duplicates.

---

## Task 2 — Scraping Product Listings from Amazon India

In this task, I collected product data from Amazon search results across different categories like electronics, books, fashion, and more. For each search query, I scraped the first two pages and extracted details like product title, price, and ratings.

Since Amazon has bot detection, I rotated User-Agent headers and added random delays between requests. The scraper uses BeautifulSoup to parse product cards and handles missing values by assigning "N/A" where needed. After collecting the data, I performed some basic cleaning — removing duplicate entries, handling null values, and standardizing text fields by trimming unnecessary spaces. Once the data was cleaned and consistent, I saved it as `<span>task2.csv</span>`, along with category labels for easier analysis.


---

## Task 3 — Fetching Tourist Attractions in Pune via OpenStreetMap API

This task involved using the Overpass API instead of scraping websites. I wrote a query to fetch all tourism-related locations in Pune. The API returns structured JSON, which made it easier to work with compared to HTML scraping.

From the response, I extracted details like name, type, and coordinates. I removed entries without names and stored the cleaned data in a CSV file. Compared to the scraping tasks, this felt more straightforward since the data was already structured.

---

## Task 4 — Keyword and URL Categorization

In this task, I categorized keywords and URLs into business categories and sub-categories. I worked on this in Excel by adding new columns for classification. Instead of handling each row individually, I used sorting and filtering to group similar patterns, which made the process much faster.

I mainly used the URL structure to assign categories, since it usually gives a clear idea of the service. If the URL wasn’t clear, I relied on the keyword to understand the intent. I also used Find and drag-fill to speed up repetitive work and keep the data consistent.

---
