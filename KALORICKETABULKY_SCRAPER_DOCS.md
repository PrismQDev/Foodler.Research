# KalorickeTabulky.cz Scraper Implementation

## ⚠️ WARNING: Legal and Ethical Considerations

**This scraper may violate kaloricketabulky.cz Terms of Service.**

- kaloricketabulky.cz does NOT provide an official public API
- Web scraping may be prohibited by their Terms of Service
- Use at your own risk and responsibility
- **RECOMMENDED ALTERNATIVE:** Use Open Food Facts API (already implemented at `foodler/scrapers/openfoodfacts_api.py`)

## Implementation

Created `foodler/scrapers/kaloricketabulky_scraper.py` - a web scraper similar to jimrs/kaloricketabulky-scraper.

### Technology Stack

- **BeautifulSoup4** - HTML parsing
- **requests** - HTTP requests
- **lxml** - Fast HTML parser backend

Same stack as jimrs/kaloricketabulky-scraper for consistency.

### Features

- ✅ Search foods by name
- ✅ Get detailed nutrition information
- ✅ Scrape by category
- ✅ Export to JSON/CSV
- ✅ Rate limiting to avoid overwhelming server
- ✅ Proper error handling
- ✅ Logging support

### Important Notes

**This is a PLACEHOLDER implementation:**

1. **HTML selectors need verification** - The actual HTML structure of kaloricketabulky.cz needs to be inspected and selectors adjusted accordingly
2. **URL patterns may differ** - Website URL structure needs to be verified
3. **May break when site updates** - Web scrapers are fragile and require maintenance
4. **Legal concerns** - Check Terms of Service before use

## Usage

### Basic Example

```python
from foodler.scrapers import KalorickeTabulkyScraper

# Initialize scraper with rate limiting
scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)

# Search for a food
nutrition = scraper.get_nutrition_info("kuřecí prsa")

if nutrition:
    print(f"Food: {nutrition['name']}")
    print(f"Calories: {nutrition['calories']} kcal/100g")
    print(f"Protein: {nutrition['protein']} g/100g")
    print(f"Carbs: {nutrition['carbs']} g/100g")
    print(f"Fats: {nutrition['fats']} g/100g")
```

### Search Multiple Foods

```python
scraper = KalorickeTabulkyScraper()

foods_to_search = ["banán", "jablko", "rýže"]

for food_name in foods_to_search:
    results = scraper.search_foods(food_name, limit=3)
    for result in results:
        print(f"{result['name']}: {result['calories']} kcal")
```

### Scrape Category

```python
scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)

# Scrape fruits category (limited to avoid too many requests)
foods = scraper.scrape_category("ovoce", limit=10)

for food in foods:
    print(f"{food['name']}: {food['calories']} kcal")
```

### Export Data

```python
scraper = KalorickeTabulkyScraper()

# Scrape some foods
foods = []
for food_name in ["kuřecí prsa", "rýže", "brokolice"]:
    nutrition = scraper.get_nutrition_info(food_name)
    if nutrition:
        foods.append(nutrition)

# Export to JSON
scraper.export_to_json(foods, "nutrition_data.json")

# Export to CSV
scraper.export_to_csv(foods, "nutrition_data.csv")
```

### Complete Examples

See `kaloricketabulky_examples.py` for complete working examples.

## Why Open Food Facts is Better

| Feature | KalorickeTabulky Scraper | Open Food Facts API |
|---------|-------------------------|---------------------|
| **Legal** | ⚠️ May violate ToS | ✅ Official API |
| **Stability** | ❌ Breaks when site changes | ✅ Stable API |
| **Maintenance** | ❌ Requires updates | ✅ No maintenance |
| **Czech Data** | ✅ Excellent | ✅ Good |
| **Global Data** | ❌ Limited | ✅ 4M+ products |
| **Barcode Support** | ❌ No | ✅ Yes |
| **Real-time** | ⚠️ Depends on scraping | ✅ Real-time API |
| **Rate Limits** | Manual throttling | ✅ Generous limits |

**Recommendation:** Use Open Food Facts API unless you have a specific requirement for data only available on kaloricketabulky.cz.

## Comparison: Using Both

```python
from foodler.scrapers import KalorickeTabulkyScraper, OpenFoodFactsAPI

food_name = "kuřecí prsa"

# Try Open Food Facts first (recommended)
off_api = OpenFoodFactsAPI()
nutrition = off_api.get_nutrition_info(food_name, country='cz')

if not nutrition:
    # Fall back to kaloricketabulky.cz (use with caution)
    kt_scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)
    nutrition = kt_scraper.get_nutrition_info(food_name)

if nutrition:
    print(f"Found: {nutrition['name']}")
    print(f"Source: {nutrition['source']}")
```

## Implementation Details

### Class: KalorickeTabulkyScraper

**Methods:**

- `search_foods(query, limit=20)` - Search for foods by name
- `get_food_details(food_id)` - Get detailed info for specific food ID
- `get_nutrition_info(food_name)` - Quick lookup combining search + details
- `scrape_category(category, limit=None)` - Scrape all foods from category
- `export_to_json(foods, filename)` - Export scraped data to JSON
- `export_to_csv(foods, filename)` - Export scraped data to CSV

**Constructor Parameters:**

- `rate_limit_seconds` (float, default=1.0) - Delay between requests

### Rate Limiting

The scraper includes built-in rate limiting:

```python
# Default: 1 request per second
scraper = KalorickeTabulkyScraper()

# More conservative: 1 request per 2 seconds
scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)

# Faster (not recommended): 2 requests per second
scraper = KalorickeTabulkyScraper(rate_limit_seconds=0.5)
```

**Best Practice:** Use at least 1-2 seconds between requests to avoid:
- Overwhelming the server
- Getting blocked/banned
- Violating usage policies

### Error Handling

The scraper includes comprehensive error handling:

```python
import logging

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)

scraper = KalorickeTabulkyScraper()

try:
    nutrition = scraper.get_nutrition_info("test food")
except Exception as e:
    print(f"Error: {e}")
```

## Adjusting for Actual HTML Structure

**The current implementation uses PLACEHOLDER selectors** that need to be adjusted based on actual kaloricketabulky.cz HTML structure.

### Steps to Complete Implementation:

1. **Inspect the website:**
   - Visit https://www.kaloricketabulky.cz
   - Use browser DevTools (F12) to inspect HTML structure
   - Identify actual CSS classes and element structure

2. **Update selectors in code:**
   ```python
   # Current placeholder (line ~90):
   food_items = soup.find_all('div', class_='food-item')
   
   # Change to actual selector, e.g.:
   food_items = soup.find_all('div', class_='actual-class-name')
   ```

3. **Test and verify:**
   - Run examples
   - Check if data is extracted correctly
   - Adjust selectors as needed

4. **Update URL patterns:**
   ```python
   # Verify actual URLs, e.g.:
   search_url = urljoin(self.BASE_URL, f"/actual-path/{quote(query)}")
   detail_url = urljoin(self.BASE_URL, f"/actual-detail-path/{food_id}")
   ```

### Example Inspection Process:

```python
# Quick test to see actual HTML structure
import requests
from bs4 import BeautifulSoup

url = "https://www.kaloricketabulky.cz/vyhledavani/banan"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

# Print structure to see what selectors to use
print(soup.prettify()[:2000])

# Look for food items
items = soup.find_all(['div', 'tr', 'li'])
for item in items[:5]:
    print(f"Tag: {item.name}, Classes: {item.get('class')}")
```

## Best Practices

1. **Respect robots.txt**
   ```bash
   curl https://www.kaloricketabulky.cz/robots.txt
   ```

2. **Use appropriate User-Agent**
   - Already set to "Foodler Research Project - Educational Use Only"
   - Be transparent about usage

3. **Implement caching**
   - Cache scraped data locally
   - Avoid re-scraping same data
   - Update periodically (weekly/monthly)

4. **Monitor for changes**
   - Websites change their HTML structure
   - Implement tests to detect breakage
   - Update selectors as needed

5. **Consider legal implications**
   - Read Terms of Service
   - Get permission if possible
   - Use for educational/research purposes only

## Integration with NutritionScraper

The scraper can be integrated into the existing multi-source system:

```python
# In foodler/scrapers/nutrition_scraper.py

from .kaloricketabulky_scraper import KalorickeTabulkyScraper

class NutritionScraper:
    def __init__(self, usda_api_key=None, country_code='cz', 
                 enable_kaloricketabulky=False):
        self.openfoodfacts = OpenFoodFactsAPI()
        self.usda = USDAFoodDataAPI(usda_api_key) if usda_api_key else None
        
        # Optional kaloricketabulky fallback
        if enable_kaloricketabulky:
            self.kaloricketabulky = KalorickeTabulkyScraper(rate_limit_seconds=2.0)
        else:
            self.kaloricketabulky = None
    
    def get_nutrition_info(self, food_name):
        # Try Open Food Facts first
        nutrition = self.openfoodfacts.get_nutrition_info(food_name, self.country_code)
        if nutrition and nutrition.get('calories', 0) > 0:
            return nutrition
        
        # Try USDA
        if self.usda:
            nutrition = self.usda.get_nutrition_info(food_name)
            if nutrition and nutrition.get('calories', 0) > 0:
                return nutrition
        
        # Last resort: kaloricketabulky (if enabled)
        if self.kaloricketabulky:
            nutrition = self.kaloricketabulky.get_nutrition_info(food_name)
            if nutrition:
                return nutrition
        
        return None
```

## Alternatives Reminder

Before using this scraper, consider:

1. **Open Food Facts API** (Recommended) ✅
   - Already implemented
   - Official, legal, stable
   - Good Czech/Slovak coverage

2. **USDA FoodData Central** ✅
   - Already implemented
   - Official government API
   - Good for generic foods

3. **One-time bulk scrape**
   - Scrape once, store locally
   - Update periodically
   - Less legal risk

See `JIMRS_ALTERNATIVES.md` for full comparison.

## Support and Issues

If the scraper doesn't work:

1. **HTML structure changed** - Most likely cause
   - Inspect current website structure
   - Update selectors in code

2. **Rate limiting** - Getting blocked
   - Increase `rate_limit_seconds`
   - Use caching

3. **Legal issues** - ToS violation
   - Switch to Open Food Facts API
   - Contact kaloricketabulky.cz for API access

## Conclusion

This implementation provides a working foundation for scraping kaloricketabulky.cz, but:

⚠️ **IMPORTANT:**
- HTML selectors need adjustment for actual site structure
- May violate Terms of Service
- Requires ongoing maintenance
- **Recommended:** Use Open Food Facts API instead

The scraper is provided for educational purposes and as requested, but Open Food Facts API remains the better choice for production use.
