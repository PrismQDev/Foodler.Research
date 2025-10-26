# Web Scraping Libraries: Python and C# Alternatives

## Overview

This document provides a comprehensive comparison of web scraping libraries for Python and C#, specifically in the context of scraping nutrition databases like kaloricketabulky.cz.

---

## Python Web Scraping Libraries

### 1. BeautifulSoup4 (+ requests)

**Type:** HTML/XML Parser  
**Best for:** Static pages, simple scraping

**Features:**
- Parses HTML and XML documents
- Handles malformed/broken HTML gracefully
- Multiple parser backends (html.parser, lxml, html5lib)
- CSS selectors and tree navigation
- Lightweight and easy to learn

**Installation:**
```bash
pip install beautifulsoup4 requests lxml
```

**Example Usage:**
```python
import requests
from bs4 import BeautifulSoup

url = "https://www.kaloricketabulky.cz/search?q=banán"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

# Extract food items
items = soup.find_all('div', class_='food-item')
for item in items:
    name = item.find('h3').text
    calories = item.find('span', class_='calories').text
    print(f"{name}: {calories}")
```

**Pros:**
- ✅ Easy to learn and use
- ✅ Great for beginners
- ✅ Excellent HTML parsing
- ✅ Lightweight and fast for static content
- ✅ Flexible parser options

**Cons:**
- ❌ Cannot handle JavaScript-rendered content
- ❌ No browser automation
- ❌ Requires separate HTTP library (requests)
- ❌ Not suitable for dynamic sites

**Used by jimrs/kaloricketabulky-scraper:** Yes, likely uses BeautifulSoup + requests

---

### 2. Scrapy

**Type:** Full web scraping framework  
**Best for:** Large-scale crawling, production scraping

**Features:**
- Complete framework with spiders, pipelines, and middleware
- Asynchronous request handling
- Built-in data export (JSON, CSV, XML)
- Automatic throttling and retry logic
- XPath and CSS selector support
- Logging and debugging tools

**Installation:**
```bash
pip install scrapy
```

**Example Usage:**
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
                'protein': item.css('span.protein::text').get(),
            }
        
        # Follow pagination
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

**Pros:**
- ✅ Very fast (asynchronous)
- ✅ Built for large-scale scraping
- ✅ Robust error handling
- ✅ Data pipelines for processing
- ✅ Rate limiting built-in
- ✅ Excellent for crawling multiple pages

**Cons:**
- ❌ Steeper learning curve
- ❌ Overkill for simple projects
- ❌ Limited JavaScript handling (needs additional tools)
- ❌ More complex setup

---

### 3. Selenium

**Type:** Browser automation  
**Best for:** Dynamic content, JavaScript-heavy sites

**Features:**
- Controls real browsers (Chrome, Firefox, Edge, Safari)
- Executes JavaScript
- Simulates user interactions (clicks, typing, scrolling)
- Handles AJAX and dynamic content
- Screenshots and PDF generation

**Installation:**
```bash
pip install selenium
# Also need ChromeDriver or geckodriver
```

**Example Usage:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.kaloricketabulky.cz/')

# Wait for dynamic content to load
wait = WebDriverWait(driver, 10)
items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'food-item')))

for item in items:
    name = item.find_element(By.TAG_NAME, 'h3').text
    print(name)

driver.quit()
```

**Pros:**
- ✅ Handles JavaScript-rendered content
- ✅ Can interact with page elements
- ✅ Works with any browser-visible content
- ✅ Good for login/authentication flows
- ✅ Mature and widely used

**Cons:**
- ❌ Slow (browser overhead)
- ❌ Resource-intensive
- ❌ Complex setup (browser drivers)
- ❌ Not suitable for large-scale scraping
- ❌ Higher maintenance

---

### 4. Playwright

**Type:** Modern browser automation  
**Best for:** Modern web apps, reliable automation

**Features:**
- Multi-browser support (Chromium, Firefox, WebKit)
- Fast and reliable
- Better performance than Selenium
- Auto-waiting for elements
- Network interception
- Mobile emulation

**Installation:**
```bash
pip install playwright
playwright install  # Downloads browsers
```

**Example Usage:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://www.kaloricketabulky.cz/')
    
    # Wait for content
    page.wait_for_selector('.food-item')
    
    items = page.query_selector_all('.food-item')
    for item in items:
        name = item.query_selector('h3').inner_text()
        print(name)
    
    browser.close()
```

**Pros:**
- ✅ Faster than Selenium
- ✅ More reliable
- ✅ Better API design
- ✅ Auto-waiting reduces flakiness
- ✅ Network request interception
- ✅ Multiple browser engines

**Cons:**
- ❌ Newer (smaller community)
- ❌ Still resource-intensive
- ❌ Browser installation required
- ❌ Overkill for static sites

---

### 5. httpx (Alternative to requests)

**Type:** Modern HTTP client  
**Best for:** Async HTTP requests

**Features:**
- Async/await support
- HTTP/2 support
- Similar API to requests
- Better performance for concurrent requests

**Installation:**
```bash
pip install httpx
```

**Example Usage:**
```python
import httpx
import asyncio
from bs4 import BeautifulSoup

async def scrape_food(food_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://www.kaloricketabulky.cz/food/{food_id}')
        soup = BeautifulSoup(response.content, 'lxml')
        return soup.find('h1').text

async def main():
    tasks = [scrape_food(i) for i in range(1, 100)]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

---

## C# Web Scraping Libraries

### 1. HtmlAgilityPack

**Type:** HTML Parser  
**Best for:** Static pages, broken HTML

**Features:**
- Forgiving HTML parser
- XPath support
- Handles malformed HTML
- .NET Standard compatible
- Lightweight

**Installation:**
```bash
dotnet add package HtmlAgilityPack
```

**Example Usage:**
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
    var calories = item.SelectSingleNode(".//span[@class='calories']").InnerText;
    Console.WriteLine($"{name}: {calories}");
}
```

**Pros:**
- ✅ Handles broken HTML well
- ✅ Easy to use
- ✅ Mature and stable
- ✅ Good performance
- ✅ XPath support

**Cons:**
- ❌ No native CSS selectors (can add Fizzler)
- ❌ No JavaScript handling
- ❌ Less strict than modern parsers

---

### 2. AngleSharp

**Type:** HTML5-compliant parser  
**Best for:** Modern, well-formed HTML

**Features:**
- W3C standards compliant
- Native CSS selector support
- DOM manipulation
- LINQ-friendly API
- Can parse CSS and SVG

**Installation:**
```bash
dotnet add package AngleSharp
```

**Example Usage:**
```csharp
using AngleSharp;
using AngleSharp.Dom;

var config = Configuration.Default.WithDefaultLoader();
var context = BrowsingContext.New(config);
var document = await context.OpenAsync("https://www.kaloricketabulky.cz/");

var foodItems = document.QuerySelectorAll("div.food-item");

foreach (var item in foodItems)
{
    var name = item.QuerySelector("h3")?.TextContent;
    var calories = item.QuerySelector("span.calories")?.TextContent;
    Console.WriteLine($"{name}: {calories}");
}
```

**Pros:**
- ✅ Modern and standards-compliant
- ✅ Native CSS selectors
- ✅ Better DOM accuracy
- ✅ LINQ integration
- ✅ Active development

**Cons:**
- ❌ Slower than HtmlAgilityPack
- ❌ Higher memory usage
- ❌ Less forgiving of broken HTML
- ❌ No JavaScript execution

---

### 3. Puppeteer Sharp

**Type:** Browser automation  
**Best for:** JavaScript-heavy sites

**Features:**
- Headless Chrome/Chromium control
- JavaScript execution
- Screenshots and PDFs
- User interaction simulation
- Network monitoring

**Installation:**
```bash
dotnet add package PuppeteerSharp
```

**Example Usage:**
```csharp
using PuppeteerSharp;

var browserFetcher = new BrowserFetcher();
await browserFetcher.DownloadAsync();

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

**Pros:**
- ✅ Handles JavaScript
- ✅ Full browser automation
- ✅ Screenshots and PDFs
- ✅ Network interception
- ✅ .NET port of popular tool

**Cons:**
- ❌ Resource-intensive
- ❌ Slower than parsers
- ❌ Complex setup
- ❌ Browser download required

---

### 4. Selenium WebDriver (C#)

**Type:** Browser automation  
**Best for:** Cross-browser testing and scraping

**Features:**
- Multiple browser support
- Well-established
- Large community
- Grid support for parallel testing

**Installation:**
```bash
dotnet add package Selenium.WebDriver
dotnet add package Selenium.WebDriver.ChromeDriver
```

**Example Usage:**
```csharp
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;

var options = new ChromeOptions();
options.AddArgument("--headless");

using var driver = new ChromeDriver(options);
driver.Navigate().GoToUrl("https://www.kaloricketabulky.cz/");

var foodItems = driver.FindElements(By.ClassName("food-item"));

foreach (var item in foodItems)
{
    var name = item.FindElement(By.TagName("h3")).Text;
    Console.WriteLine(name);
}

driver.Quit();
```

**Pros:**
- ✅ Multi-browser support
- ✅ Mature ecosystem
- ✅ Large community
- ✅ Good documentation

**Cons:**
- ❌ Slower than modern alternatives
- ❌ Can be flaky
- ❌ Resource-intensive
- ❌ Driver management complexity

---

## Comparison Tables

### Python Libraries Comparison

| Library | Static | Dynamic | Speed | Difficulty | Best Use Case |
|---------|--------|---------|-------|------------|---------------|
| **BeautifulSoup** | ✅ | ❌ | ⚡⚡⚡ | Easy | Simple static pages |
| **Scrapy** | ✅ | ⚠️ | ⚡⚡⚡⚡ | Medium | Large-scale crawling |
| **Selenium** | ✅ | ✅ | ⚡ | Medium | JavaScript sites |
| **Playwright** | ✅ | ✅ | ⚡⚡ | Medium | Modern web apps |

### C# Libraries Comparison

| Library | Static | Dynamic | Speed | Difficulty | Best Use Case |
|---------|--------|---------|-------|------------|---------------|
| **HtmlAgilityPack** | ✅ | ❌ | ⚡⚡⚡ | Easy | Broken HTML |
| **AngleSharp** | ✅ | ❌ | ⚡⚡ | Easy | Modern HTML5 |
| **Puppeteer Sharp** | ✅ | ✅ | ⚡ | Medium | JavaScript sites |
| **Selenium** | ✅ | ✅ | ⚡ | Medium | Cross-browser |

---

## What jimrs/kaloricketabulky-scraper Uses

Based on typical Python scraper patterns for Czech websites:

**Likely Stack:**
- **BeautifulSoup4** for HTML parsing
- **requests** or **httpx** for HTTP requests
- **lxml** as the parser backend (faster than html.parser)

**Why This Stack:**
- kaloricketabulky.cz is mostly static content
- No heavy JavaScript rendering required
- Simple and reliable
- Fast for bulk scraping

**Typical Code Structure:**
```python
import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_food_database():
    foods = []
    
    # Iterate through categories or search results
    for page in range(1, 100):
        url = f"https://www.kaloricketabulky.cz/foods?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract food items
        items = soup.find_all('div', class_='food-item')
        for item in items:
            food = {
                'name': item.find('h3').text.strip(),
                'calories': float(item.find('span', class_='calories').text),
                # ... more fields
            }
            foods.append(food)
        
        time.sleep(1)  # Rate limiting
    
    # Export to JSON
    with open('foods.json', 'w', encoding='utf-8') as f:
        json.dump(foods, f, ensure_ascii=False, indent=2)
```

---

## Recommendations for KalorickeTabulky.cz Scraping

### Python Recommendations

**For One-Time Bulk Scraping:**
```
BeautifulSoup + requests + lxml
```
- Simple and fast
- Good for static content
- Easy to maintain

**For Production/Repeated Scraping:**
```
Scrapy
```
- Better error handling
- Built-in rate limiting
- Data pipelines
- More robust

**If JavaScript Required:**
```
Playwright > Selenium
```
- Playwright is faster and more reliable
- Better for modern websites

### C# Recommendations

**For Static Content:**
```
AngleSharp or HtmlAgilityPack
```
- AngleSharp for modern, well-formed HTML
- HtmlAgilityPack for broken/old HTML

**For Dynamic Content:**
```
Puppeteer Sharp
```
- More modern than Selenium
- Better performance
- Easier API

---

## Complete Example: Multi-Library Approach

### Python: Hybrid Approach
```python
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class KalorickyScraperHybrid:
    def __init__(self):
        self.session = requests.Session()
        
    def scrape_static(self, url):
        """Use BeautifulSoup for static pages"""
        response = self.session.get(url)
        return BeautifulSoup(response.content, 'lxml')
    
    def scrape_dynamic(self, url):
        """Use Playwright for dynamic pages"""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page.wait_for_selector('.food-item')
            html = page.content()
            browser.close()
            return BeautifulSoup(html, 'lxml')
```

### C#: Hybrid Approach
```csharp
public class KalorickyScraperHybrid
{
    private readonly HttpClient _httpClient = new();
    
    public async Task<IDocument> ScrapeStaticAsync(string url)
    {
        // Use AngleSharp for static pages
        var html = await _httpClient.GetStringAsync(url);
        var context = BrowsingContext.New(Configuration.Default);
        return await context.OpenAsync(req => req.Content(html));
    }
    
    public async Task<IDocument> ScrapeDynamicAsync(string url)
    {
        // Use Puppeteer Sharp for dynamic pages
        await using var browser = await Puppeteer.LaunchAsync(new LaunchOptions
        {
            Headless = true
        });
        await using var page = await browser.NewPageAsync();
        await page.GoToAsync(url);
        var html = await page.GetContentAsync();
        
        var context = BrowsingContext.New(Configuration.Default);
        return await context.OpenAsync(req => req.Content(html));
    }
}
```

---

## Summary

**For jimrs/kaloricketabulky-scraper:**
- Uses **BeautifulSoup + requests** (most likely)
- Good choice for static Czech nutrition site
- Simple, reliable, fast

**Python Alternatives:**
1. **Scrapy** - For production/scale
2. **Playwright** - If JavaScript needed
3. **httpx + BeautifulSoup** - Async requests

**C# Alternatives:**
1. **AngleSharp** - Modern, standards-compliant
2. **HtmlAgilityPack** - Forgiving of errors
3. **Puppeteer Sharp** - For JavaScript sites

**Best Practice:**
Use simple tools (BeautifulSoup/HtmlAgilityPack) for static sites, only upgrade to browser automation (Playwright/Puppeteer Sharp) when JavaScript rendering is required.
