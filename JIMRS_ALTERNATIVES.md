# Alternatives to jimrs/kaloricketabulky-scraper

## Overview

This document provides a comprehensive overview of alternatives to the jimrs/kaloricketabulky-scraper tool for accessing Czech/Slovak nutrition data.

---

## Recommended Alternative: Use Official APIs ⭐

### Option 1: Open Food Facts API (RECOMMENDED)

**Already implemented in this project** ✅

**Why choose this over scraping:**
- ✅ Official, stable API (no scraping needed)
- ✅ Good Czech/Slovak product coverage (4M+ products globally)
- ✅ No legal concerns
- ✅ Barcode scanning support
- ✅ Free, no API key required
- ✅ Real-time data updates
- ✅ Already integrated in `foodler/scrapers/openfoodfacts_api.py`

**Example:**
```python
from foodler.scrapers import OpenFoodFactsAPI

api = OpenFoodFactsAPI()
nutrition = api.get_nutrition_info("kuřecí prsa", country='cz')
```

**Documentation:** See `foodler/scrapers/openfoodfacts_api.py` and `api_examples.py`

---

### Option 2: USDA FoodData Central API

**Already implemented in this project** ✅

**Why choose this:**
- ✅ Official US Government API
- ✅ Comprehensive nutrient data
- ✅ Free (requires API key)
- ✅ Already integrated in `foodler/scrapers/usda_api.py`

**Limitation:** Limited Czech/Slovak specific products (good for generic foods)

**Example:**
```python
from foodler.scrapers import USDAFoodDataAPI

api = USDAFoodDataAPI(api_key='your-key')
nutrition = api.get_nutrition_info("chicken breast")
```

---

## If You Must Scrape KalorickeTabulky.cz

### Community Tools (Alternatives to jimrs scraper)

#### 1. TomasHubelbauer/kaloricke-tabulky-api (Node.js)

**Repository:** https://github.com/TomasHubelbauer/kaloricke-tabulky-api

**Technology:** JavaScript/Node.js

**Features:**
- User authentication
- Weight tracking
- Session management

**Limitations:**
- ❌ Does NOT provide nutrition database access
- ❌ Only user account features
- ❌ Requires password hashing

**Use Case:** Weight tracking only, not nutrition data

**Not a real alternative** for nutrition database scraping.

---

#### 2. francbohuslav/kaloricke-tabulky-api (TypeScript)

**Repository:** https://github.com/francbohuslav/kaloricke-tabulky-api

**Technology:** TypeScript

**Features:**
- REST API client
- Czech command interpreter
- More comprehensive than TomasHubelbauer

**Installation:**
```bash
npm i francbohuslav/kaloricke-tabulky-api
```

**Limitations:**
- ❌ Still unofficial/reverse-engineered
- ❌ Focus on user features, not nutrition database
- ❌ Node.js/TypeScript (not Python)

**Use Case:** Advanced user account automation

**Not ideal** for nutrition database scraping.

---

#### 3. Build Your Own Python Scraper

**Technologies:**

**Option A: BeautifulSoup (Simple - Like jimrs)**
```python
import requests
from bs4 import BeautifulSoup
import json

def scrape_kaloricketabulky(food_name):
    url = f"https://www.kaloricketabulky.cz/search?q={food_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Parse food items
    items = soup.find_all('div', class_='food-item')
    foods = []
    
    for item in items:
        food = {
            'name': item.find('h3').text.strip(),
            'calories': item.find('span', class_='calories').text,
            # Add more fields...
        }
        foods.append(food)
    
    return foods
```

**Pros:**
- ✅ Simple and lightweight
- ✅ Same stack as jimrs scraper
- ✅ Easy to customize

**Cons:**
- ❌ Requires maintenance when site changes
- ❌ Legal/ToS concerns
- ❌ Static content only

---

**Option B: Scrapy (Production/Large-Scale)**
```python
import scrapy

class KalorickySpider(scrapy.Spider):
    name = 'kaloricke'
    start_urls = ['https://www.kaloricketabulky.cz/']
    
    def parse(self, response):
        for item in response.css('div.food-item'):
            yield {
                'name': item.css('h3::text').get(),
                'calories': item.css('span.calories::text').get(),
            }
```

**Pros:**
- ✅ Fast (asynchronous)
- ✅ Built for large-scale scraping
- ✅ Better error handling
- ✅ Data pipelines

**Cons:**
- ❌ More complex setup
- ❌ Overkill for simple tasks

---

**Option C: Playwright (If JavaScript Required)**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://www.kaloricketabulky.cz/')
    page.wait_for_selector('.food-item')
    
    items = page.query_selector_all('.food-item')
    for item in items:
        name = item.query_selector('h3').inner_text()
        print(name)
    
    browser.close()
```

**Pros:**
- ✅ Handles JavaScript
- ✅ More reliable than Selenium
- ✅ Modern API

**Cons:**
- ❌ Slower (browser overhead)
- ❌ More complex

---

## C# Alternatives

If you need a C# solution instead of Python:

### Option 1: HtmlAgilityPack (Like BeautifulSoup)

```csharp
using HtmlAgilityPack;
using System.Net.Http;

var client = new HttpClient();
var html = await client.GetStringAsync("https://www.kaloricketabulky.cz/");

var doc = new HtmlDocument();
doc.LoadHtml(html);

var foodItems = doc.DocumentNode.SelectNodes("//div[@class='food-item']");
foreach (var item in foodItems)
{
    var name = item.SelectSingleNode(".//h3").InnerText;
    Console.WriteLine(name);
}
```

---

### Option 2: AngleSharp (Modern HTML5)

```csharp
using AngleSharp;

var config = Configuration.Default.WithDefaultLoader();
var context = BrowsingContext.New(config);
var document = await context.OpenAsync("https://www.kaloricketabulky.cz/");

var foodItems = document.QuerySelectorAll("div.food-item");
foreach (var item in foodItems)
{
    var name = item.QuerySelector("h3")?.TextContent;
    Console.WriteLine(name);
}
```

---

### Option 3: Puppeteer Sharp (JavaScript Support)

```csharp
using PuppeteerSharp;

await using var browser = await Puppeteer.LaunchAsync(new LaunchOptions
{
    Headless = true
});

await using var page = await browser.NewPageAsync();
await page.GoToAsync("https://www.kaloricketabulky.cz/");

var foodItems = await page.QuerySelectorAllAsync("div.food-item");
foreach (var item in foodItems)
{
    var name = await item.QuerySelectorAsync("h3");
    var nameText = await name.EvaluateFunctionAsync<string>("e => e.textContent");
    Console.WriteLine(nameText);
}
```

---

## Comparison Table

| Alternative | Type | Difficulty | Czech Data | Legal | Maintained |
|-------------|------|------------|------------|-------|------------|
| **Open Food Facts API** ⭐ | Official API | Easy | Good | ✅ Yes | ✅ Active |
| **USDA API** | Official API | Easy | Limited | ✅ Yes | ✅ Active |
| **jimrs/scraper** | Python scraper | Easy | Excellent | ⚠️ ToS | ❓ Unknown |
| **TomasHubelbauer** | Node.js API | Medium | None* | ⚠️ ToS | ⚠️ Inactive |
| **francbohuslav** | TypeScript | Medium | None* | ⚠️ ToS | ✅ Active |
| **Custom BeautifulSoup** | Python scraper | Easy | Excellent | ⚠️ ToS | ✅ You maintain |
| **Custom Scrapy** | Python scraper | Medium | Excellent | ⚠️ ToS | ✅ You maintain |
| **Custom Playwright** | Python scraper | Medium | Excellent | ⚠️ ToS | ✅ You maintain |
| **HtmlAgilityPack** | C# scraper | Easy | Excellent | ⚠️ ToS | ✅ You maintain |
| **AngleSharp** | C# scraper | Easy | Excellent | ⚠️ ToS | ✅ You maintain |
| **Puppeteer Sharp** | C# scraper | Medium | Excellent | ⚠️ ToS | ✅ You maintain |

*Only provides user account features, not nutrition database access

---

## Recommendations

### Best Overall: Open Food Facts API ⭐⭐⭐⭐⭐

**Already implemented in this project!**

```python
from foodler.scrapers import NutritionScraper

# Multi-source with automatic fallback
scraper = NutritionScraper(country_code='cz')
nutrition = scraper.get_nutrition_info("kuřecí prsa")
# Tries: Open Food Facts → USDA → Returns None
```

**Why:**
1. No legal issues
2. Official and stable
3. Good Czech/Slovak coverage
4. No maintenance burden
5. Already integrated
6. Free and open

---

### If You Need 100% Czech-Specific Data

**Option 1: One-Time Bulk Scrape**

Use jimrs/kaloricketabulky-scraper or build your own to:
1. Scrape entire database once
2. Import to local database
3. Use local data for lookups
4. Update quarterly/monthly

**Advantages:**
- ✅ Complete Czech database
- ✅ Fast lookups (local)
- ✅ No repeated scraping
- ✅ Offline access

**Disadvantages:**
- ⚠️ Legal concerns (check ToS)
- ❌ Data gets stale
- ❌ Requires updates

---

**Option 2: Hybrid Approach (RECOMMENDED)**

```python
from foodler.scrapers import NutritionScraper

scraper = NutritionScraper(country_code='cz')

# Try Open Food Facts first
nutrition = scraper.get_nutrition_info("česneková polévka")

if not nutrition:
    # Fall back to local cached kaloricketabulky.cz data
    nutrition = get_from_local_cache("česneková polévka")

if not nutrition:
    # Last resort: real-time scrape (rate-limited)
    nutrition = scrape_kaloricketabulky_cz("česneková polévka")
    cache_result(nutrition)
```

---

### If Building from Scratch

**Python:**
1. **Simple sites:** BeautifulSoup + requests (like jimrs)
2. **Production:** Scrapy
3. **JavaScript sites:** Playwright

**C#:**
1. **Simple sites:** HtmlAgilityPack or AngleSharp
2. **JavaScript sites:** Puppeteer Sharp

---

## Migration Path from jimrs/scraper

### Current State (Using jimrs)
```python
# Hypothetical jimrs usage
from kaloricketabulky_scraper import scrape_database

foods = scrape_database()
# Returns: List of all foods with nutrition data
```

### Recommended Migration: Switch to Open Food Facts

```python
from foodler.scrapers import OpenFoodFactsAPI

api = OpenFoodFactsAPI()

# Search for Czech products
foods = api.search_products("mléko", country='cz', page_size=100)

for food in foods:
    nutrition = {
        'name': food['product_name'],
        'calories': food['nutriments'].get('energy-kcal_100g', 0),
        'protein': food['nutriments'].get('proteins_100g', 0),
        # ... more fields
    }
```

### Benefits of Migration
- ✅ No legal concerns
- ✅ No maintenance required
- ✅ Barcode scanning support
- ✅ Real-time updates
- ✅ Global coverage + Czech products

---

## Summary

**Best Alternative to jimrs/kaloricketabulky-scraper:**

**Use Open Food Facts API (already implemented)** 🎯

It's already integrated in this project at `foodler/scrapers/openfoodfacts_api.py` and provides:
- Good Czech/Slovak coverage
- Official, stable API
- No legal issues
- No maintenance
- Free access

**For 100% Czech data:** Use hybrid approach (Open Food Facts + local cache of scraped data)

**For building custom scraper:** 
- Python: BeautifulSoup (simple) or Scrapy (production)
- C#: HtmlAgilityPack or AngleSharp

---

## Related Documentation

- **SCRAPING_ALTERNATIVES.md** - Detailed comparison of all scraping libraries
- **KALORICKETABULKY_RESEARCH.md** - Analysis of kaloricketabulky.cz tools
- **API_RESEARCH.md** - Comprehensive API comparison
- **api_examples.py** - Working code examples

---

## Quick Start

**Already using this project? You have the best alternative built-in:**

```python
from foodler.scrapers import NutritionScraper

# Automatic multi-source lookup (Open Food Facts + USDA)
scraper = NutritionScraper(country_code='cz')
nutrition = scraper.get_nutrition_info("banán")

print(f"Calories: {nutrition['calories']} kcal/100g")
print(f"Source: {nutrition['source']}")  # Shows which API was used
```

**This is better than jimrs/scraper because:**
- ✅ No legal issues
- ✅ Official APIs
- ✅ Automatic fallback
- ✅ Already implemented
- ✅ Well tested
