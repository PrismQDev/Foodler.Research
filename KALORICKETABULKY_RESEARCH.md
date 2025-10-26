# KalorickeTabulky.cz API and Database Research

## Executive Summary

**KalorickeTabulky.cz does NOT provide an official public API.** All available tools are community-created reverse-engineered solutions or web scrapers.

**Recommendation:** Use **Open Food Facts API** as primary nutrition source instead. Open Food Facts has surprisingly good Czech/Slovak product coverage and provides an official, stable API. Use kaloricketabulky.cz only as a supplementary source for products not found in Open Food Facts.

**For detailed information on web scraping libraries and alternatives, see [SCRAPING_ALTERNATIVES.md](SCRAPING_ALTERNATIVES.md).**

---

## Available Community Tools

### 1. TomasHubelbauer/kaloricke-tabulky-api

**Repository:** https://github.com/TomasHubelbauer/kaloricke-tabulky-api  
**Documentation:** https://tomashubelbauer.github.io/kaloricke-tabulky-api/

**Type:** JavaScript/Node.js library (dependency-free)

**Features:**
- User authentication and session management
- Weight recording and tracking
- Fetch recent weight entries
- Cookie/session handling

**Functionality Overview:**
```javascript
// getCookies.js - Authentication
async function getCookies(email, password) {
  // Returns session cookies for authenticated access
}

// getRecentWeight.js - Fetch weight data
async function getRecentWeight(cookies) {
  // Returns array of recent weight records
}

// recordWeight.js - Add weight entry
async function recordWeight(cookies, weight) {
  // Records new weight for current date
}
```

**Limitations:**
- Only handles user account features (weight tracking)
- Does NOT provide access to nutrition database
- Password must be hashed client-side (requires browser dev tools)
- Session-based authentication

**Use Case:** Personal weight tracking only

---

### 2. francbohuslav/kaloricke-tabulky-api

**Repository:** https://github.com/francbohuslav/kaloricke-tabulky-api

**Type:** TypeScript library

**Installation:**
```bash
npm i francbohuslav/kaloricke-tabulky-api
```

**Features:**
- REST API client (`Client` class)
- Czech command interpreter (`Commander` class)
- More comprehensive than TomasHubelbauer's library
- TypeScript type definitions

**Key Classes:**

**`Client` Class:**
```typescript
// Direct REST API interaction
// Handles authentication and requests
```

**`Commander` Class:**
```typescript
// Executes Czech language commands
// Controls www.kaloricketabulky.cz programmatically
```

**Advantages:**
- Written in TypeScript (better type safety)
- More feature-complete
- Command-based control interface

**Limitations:**
- Still based on reverse-engineered endpoints
- No official documentation
- Focus on user account features, not nutrition database

---

### 3. jimrs/kaloricketabulky-scraper

**Repository:** https://github.com/jimrs/kaloricketabulky-scraper

**Type:** Python web scraper

**Purpose:** Extract the entire nutrition database from kaloricketabulky.cz

**Technology Stack:**
- **BeautifulSoup4** - HTML parsing
- **requests** - HTTP requests
- **lxml** - Fast XML/HTML parser (likely)
- **Python 3.x** - Core language

**Why This Stack:**
- kaloricketabulky.cz is mostly static HTML
- No heavy JavaScript rendering required
- BeautifulSoup handles Czech characters well
- Fast and reliable for bulk scraping

**Features:**
- Scrapes complete food database
- Exports to CSV or JSON format
- Structured data extraction
- One-time bulk download

**Output Data Structure:**
```python
{
  "food_id": "12345",
  "name": "Kuřecí prsa",
  "description": "Kuřecí maso bez kůže",
  "brand": "XYZ Foods",
  "category": "Maso a masné výrobky",
  "nutrients_per_100g": {
    "calories": 165,
    "protein": 31,
    "carbs": 0,
    "fats": 3.6,
    "fiber": 0,
    "sugar": 0,
    "sodium": 0.07
  },
  "serving_size": "100g",
  "ingredients": "..."
}
```

**Best For:**
- One-time database extraction
- Building local nutrition database
- Offline nutrition lookup
- Research and analysis

**Limitations:**
- Requires web scraping (slow)
- May violate Terms of Service
- Needs periodic re-scraping for updates
- No real-time data

---

## Database Structure (Reverse-Engineered)

Based on scraper analysis, kaloricketabulky.cz database contains:

### Food Items Table

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique food identifier |
| name | String | Food name (Czech) |
| name_alt | String | Alternative names |
| description | Text | Product description |
| brand | String | Brand/manufacturer |
| category_id | Integer | Food category FK |
| is_verified | Boolean | User-verified data |

### Nutrients Table (per 100g)

| Nutrient | Field Name | Unit |
|----------|------------|------|
| Energy | calories | kcal |
| Protein | protein | g |
| Carbohydrates | carbohydrates | g |
| Sugars | sugars | g |
| Fat | fat | g |
| Saturated Fat | saturated_fat | g |
| Fiber | fiber | g |
| Sodium | sodium | g |
| Salt | salt | g |

### Additional Tables

- **Categories** - Food categories hierarchy
- **Serving Sizes** - Standard portion sizes
- **User Ratings** - Community ratings and notes
- **Ingredients** - Ingredient lists (when available)
- **Allergens** - Allergen information

---

## Reverse-Engineered API Endpoints

**⚠️ Warning:** These endpoints are not officially documented and may change without notice.

### Authentication

```
POST https://www.kaloricketabulky.cz/api/login
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",
  "password_hash": "client-side-hashed-password"
}

Response:
Set-Cookie: session_id=...
{
  "status": "success",
  "user_id": 12345
}
```

**Password Hashing:**
- Password is hashed client-side before transmission
- Must capture hashed password from browser developer tools
- Algorithm varies (check current implementation)

### Weight Management

```
GET https://www.kaloricketabulky.cz/api/weight/recent
Cookie: session_id=...

Response:
{
  "weights": [
    {"date": "2025-10-25", "weight": 75.5},
    {"date": "2025-10-24", "weight": 76.0}
  ]
}
```

```
POST https://www.kaloricketabulky.cz/api/weight/record
Cookie: session_id=...
Content-Type: application/json

Request Body:
{
  "date": "2025-10-25",
  "weight": 75.5
}
```

### Food Database (Undocumented)

**Note:** Nutrition data endpoints are not reverse-engineered in public libraries. Would require additional analysis.

Likely structure:
```
GET /api/foods/search?q={query}
GET /api/foods/{food_id}
GET /api/categories
```

---

## Web Scraping Strategy

For extracting nutrition data without API:

### 1. Search Page Scraping

```python
import requests
from bs4 import BeautifulSoup

# Search for food
url = "https://www.kaloricketabulky.cz/search"
params = {"q": "kuřecí prsa"}
response = requests.get(url, params=params)

soup = BeautifulSoup(response.content, 'html.parser')

# Parse search results
# Structure varies - requires inspection
results = soup.find_all('div', class_='food-item')

for result in results:
    food_id = result.get('data-id')
    name = result.find('h3').text
    # ... extract other fields
```

### 2. Detail Page Scraping

```python
# Get detailed nutrition info
detail_url = f"https://www.kaloricketabulky.cz/food/{food_id}"
response = requests.get(detail_url)

soup = BeautifulSoup(response.content, 'html.parser')

# Extract nutrition table
nutrition_table = soup.find('table', class_='nutrition-facts')

nutrients = {}
for row in nutrition_table.find_all('tr'):
    label = row.find('td', class_='nutrient-name').text
    value = row.find('td', class_='nutrient-value').text
    nutrients[label] = float(value)
```

### 3. Best Practices

**Rate Limiting:**
```python
import time
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)  # 10 requests per minute
def fetch_food_data(food_id):
    # Your scraping code
    time.sleep(1)  # Additional delay
```

**Caching:**
```python
import sqlite3
from datetime import datetime, timedelta

def get_cached_or_fetch(food_id, cache_duration_days=30):
    # Check cache first
    cached = db.get_cached_food(food_id)
    
    if cached and cached['updated'] > datetime.now() - timedelta(days=cache_duration_days):
        return cached['data']
    
    # Fetch fresh data
    data = scrape_food_data(food_id)
    db.cache_food(food_id, data)
    return data
```

**Error Handling:**
```python
def safe_scrape(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

---

## Legal and Ethical Considerations

### Terms of Service

⚠️ **Important:** Review kaloricketabulky.cz Terms of Service before scraping

**Typical restrictions:**
- Automated access may be prohibited
- Commercial use restrictions
- Rate limiting requirements
- Attribution requirements

### robots.txt

Check robots.txt before scraping:
```
https://www.kaloricketabulky.cz/robots.txt
```

**Respect directives:**
- User-agent restrictions
- Disallowed paths
- Crawl-delay requirements

### Best Practices

1. **Rate Limiting:** Never exceed reasonable request rates
2. **User-Agent:** Use descriptive User-Agent with contact info
3. **Caching:** Cache results to minimize requests
4. **Attribution:** Give credit when using data
5. **Updates:** Monitor for site changes, update scrapers
6. **Alternatives:** Consider official APIs when available

---

## Integration Recommendations

### Recommended Approach for Foodler.Research

**Primary Source:** Open Food Facts API
- Official API, stable and documented
- Good Czech/Slovak coverage
- No legal concerns
- Free, no API key required

**Supplementary Source:** KalorickeTabulky.cz (if needed)
- Use only for products not in Open Food Facts
- Implement as fallback with proper error handling
- Consider one-time bulk scrape → local database

**Implementation Strategy:**

```python
from foodler.scrapers import NutritionScraper

# Current implementation uses Open Food Facts + USDA
scraper = NutritionScraper(country_code='cz')

# Search Open Food Facts first
nutrition = scraper.get_nutrition_info("kuřecí prsa")

# If not found and kaloricketabulky.cz integration added:
if not nutrition:
    nutrition = scraper.get_from_kaloricketabulky("kuřecí prsa")
```

### If You Must Use KalorickeTabulky.cz

**Option 1: One-Time Database Extraction**
```bash
# Use jimrs/kaloricketabulky-scraper
git clone https://github.com/jimrs/kaloricketabulky-scraper
cd kaloricketabulky-scraper
python scraper.py --output foods.json

# Import to local database
python import_to_db.py foods.json
```

**Option 2: Real-Time Scraping (Not Recommended)**
- Higher risk of ToS violation
- Slower performance
- Brittle implementation
- Requires constant maintenance

**Option 3: Hybrid Approach**
- Bulk scrape once for base data
- Store in local database
- Periodic refresh (monthly/quarterly)
- Real-time lookup from Open Food Facts

---

## Comparison: KalorickeTabulky.cz vs Open Food Facts

| Feature | KalorickeTabulky.cz | Open Food Facts |
|---------|---------------------|-----------------|
| **Official API** | ❌ No | ✅ Yes |
| **API Key Required** | N/A | ✅ No |
| **Czech Products** | ✅ Excellent | ✅ Good |
| **Slovak Products** | ✅ Excellent | ✅ Good |
| **International** | ❌ Limited | ✅ Excellent (4M+) |
| **Barcode Scanning** | ❌ No API | ✅ Yes |
| **Legal Concerns** | ⚠️ Scraping | ✅ Open License |
| **Stability** | ❌ May break | ✅ Stable |
| **Documentation** | ❌ Community only | ✅ Official docs |
| **Python Support** | ⚠️ Limited | ✅ Easy |
| **Update Frequency** | Manual scraping | Real-time |
| **Data Quality** | ✅ Good | ✅ Good |

---

## Conclusion

**For Foodler.Research Project:**

1. ✅ **Use Open Food Facts API** as implemented
   - Already integrated and working
   - Legal and stable
   - Good Czech/Slovak coverage

2. ⚠️ **KalorickeTabulky.cz as fallback only**
   - Only if specific products not found
   - Use bulk scrape → local DB approach
   - Not real-time scraping

3. ❌ **Do not rely on KalorickeTabulky.cz API**
   - No official API exists
   - Legal/ethical concerns with scraping
   - Maintenance burden

**Implementation Priority:**
1. Keep Open Food Facts (Primary) ✅ Done
2. Keep USDA (Secondary) ✅ Done  
3. Add KalorickeTabulky.cz (Tertiary) - Only if needed

---

## Web Scraping Alternatives

For detailed comparison of web scraping libraries for both Python and C#, see **[SCRAPING_ALTERNATIVES.md](SCRAPING_ALTERNATIVES.md)**.

### Quick Summary

**Python Libraries:**
- **BeautifulSoup + requests** - What jimrs/kaloricketabulky-scraper likely uses
- **Scrapy** - For large-scale production scraping
- **Selenium** - For JavaScript-heavy sites (slower)
- **Playwright** - Modern alternative to Selenium (faster)

**C# Libraries:**
- **HtmlAgilityPack** - Forgiving HTML parser (like BeautifulSoup)
- **AngleSharp** - Modern HTML5-compliant parser
- **Puppeteer Sharp** - Browser automation (.NET port of Puppeteer)
- **Selenium WebDriver** - Cross-browser automation

**For kaloricketabulky.cz:**
- **Recommended:** BeautifulSoup (Python) or AngleSharp (C#) for static content
- **Only if needed:** Playwright or Puppeteer Sharp for dynamic content

---

## References

- TomasHubelbauer API: https://github.com/TomasHubelbauer/kaloricke-tabulky-api
- francbohuslav API: https://github.com/francbohuslav/kaloricke-tabulky-api
- jimrs Scraper: https://github.com/jimrs/kaloricketabulky-scraper
- Open Food Facts: https://world.openfoodfacts.org/data
- USDA FoodData Central: https://fdc.nal.usda.gov/
- Web Scraping Alternatives: [SCRAPING_ALTERNATIVES.md](SCRAPING_ALTERNATIVES.md)
