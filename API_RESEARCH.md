# API Research for Kalorické Tabuľky and Kupi.cz

This document provides comprehensive research on available APIs for nutrition data (kalorické tabuľky) and food discount services (kupi.cz and alternatives).

## Table of Contents
1. [Nutrition APIs (Kalorické Tabuľky)](#nutrition-apis)
2. [Food Discount APIs (Kupi.cz)](#food-discount-apis)
3. [Recommendations](#recommendations)
4. [Integration Examples](#integration-examples)

---

## Nutrition APIs (Kalorické Tabuľky)

### 1. KalorickeTabulky.cz (Unofficial API)

**Type:** Unofficial scraper/API  
**Language:** JavaScript/Node.js  
**Cost:** Free (open source)  
**Coverage:** Czech/Slovak nutrition data

**Features:**
- Login functionality
- Weight recording and tracking
- Fetching recorded weights
- Basic user data management

**Limitations:**
- Does not officially provide food nutrition data endpoints
- May require web scraping or API extension for full nutrition tables
- Unofficial implementation (may break if website changes)

**Resources:**
- GitHub: https://github.com/TomasHubelbauer/kaloricke-tabulky-api
- Documentation: https://tomashubelbauer.github.io/kaloricke-tabulky-api/

**Python Integration:** Would require porting or using Node.js subprocess

---

### 2. Open Food Facts API ⭐ (Recommended)

**Type:** Official open-source API  
**Cost:** Free  
**Coverage:** Global (4+ million products, 150+ countries, includes Czech/Slovak products)

**Features:**
- Comprehensive nutrition data (calories, protein, carbs, fats, fiber, sugars)
- Ingredient lists and allergen information
- Eco-scores and Nutri-scores
- Barcode lookup
- Product images
- Crowdsourced and continuously updated
- RESTful API with JSON responses
- Multiple data formats (API, CSV, JSONL, MongoDB)

**API Endpoints:**
```
GET https://world.openfoodfacts.org/api/v2/product/{barcode}
GET https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&json=1
```

**Licensing:**
- Database: Open Database License (ODbL)
- Contents: Database Contents License
- Images: Creative Commons Attribution ShareAlike

**Resources:**
- API Documentation: https://world.openfoodfacts.org/data
- GitHub: https://github.com/openfoodfacts/openfoodfacts
- API Guide: https://wiki.openfoodfacts.org/API

**Python Integration:** Easy via requests library or official SDK

---

### 3. USDA FoodData Central API

**Type:** Official government API  
**Cost:** Free (requires API key)  
**Coverage:** 300,000+ foods (primarily US foods)

**Features:**
- Extensive nutrient data (macro and micronutrients)
- Branded foods, generic foods, experimental data
- Ingredient information
- Serving sizes
- RESTful JSON API

**API Endpoints:**
```
GET https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key}&query={query}
GET https://api.nal.usda.gov/fdc/v1/food/{fdcId}?api_key={key}
```

**Limitations:**
- Primarily US food database (limited Czech/Slovak coverage)
- Requires API key registration

**Resources:**
- API Documentation: https://fdc.nal.usda.gov/api-spec/fdc_api.html
- API Guide: https://fdc.nal.usda.gov/api-guide.html
- Registration: https://fdc.nal.usda.gov/

**Python Integration:** Easy via requests library

---

### 4. CalorieNinjas API

**Type:** Commercial API (free tier available)  
**Cost:** Free tier: 100,000 requests/month  
**Coverage:** 100,000+ foods globally

**Features:**
- Nutrition and recipe data
- Natural language queries (e.g., "1 cup of rice")
- Detailed macronutrient information
- Simple RESTful API

**API Endpoint:**
```
GET https://api.calorieninjas.com/v1/nutrition?query={query}
Header: X-Api-Key: {your_api_key}
```

**Resources:**
- Website: https://calorieninjas.com/
- API Documentation: https://calorieninjas.com/api

**Python Integration:** Easy via requests library

---

### 5. Nutritics Food Data API

**Type:** Commercial API  
**Cost:** Paid (enterprise pricing)  
**Coverage:** EU compliance, official national databases

**Features:**
- Comprehensive nutrition and allergen data
- Regional compliance (includes EU)
- Official database integration
- Branded product data

**Resources:**
- Website: https://www.nutritics.com/en/product/food-data-api/

**Recommendation:** Only for commercial/enterprise applications

---

## Food Discount APIs (Kupi.cz)

### 1. Kupiapi ⭐ (Recommended for Kupi.cz)

**Type:** Unofficial Python scraper library  
**Cost:** Free (open source)  
**Coverage:** Czech Republic (kupi.cz)

**Features:**
- Scrape sales and discounts from kupi.cz
- Filter by category, shop, or search terms
- Recipe data extraction
- JSON output format
- Easy Python integration

**Installation:**
```bash
pip install kupiapi
```

**Basic Usage:**
```python
from kupiapi import Kupi

kupi = Kupi()

# Get discounts by category
discounts = kupi.get_discounts_by_category('potraviny')

# Get discounts by shop
tesco_deals = kupi.get_discounts_by_shop('tesco')

# Search for specific products
chicken_deals = kupi.search_discounts('kuřecí')
```

**Resources:**
- GitHub: https://github.com/vorava/kupiapi
- PyPI: https://pypi.org/project/kupiapi/

**Python Integration:** Direct integration, already a Python library

---

### 2. Alternative Discount Portals

While kupi.cz is the most popular, here are alternatives (would require custom scrapers):

#### AkcniCeny.cz
- Similar service to kupi.cz
- Supermarket promotions and flyers
- No official API (would require web scraping)
- Website: https://www.akcniceny.cz/

#### LetakySlevy.cz
- Aggregates sales flyers and promotions
- No official API (would require web scraping)
- Website: https://www.letakyslevy.cz/

#### Tipli.cz
- Cashback and coupons platform
- Includes some food retailer deals
- No official API (would require web scraping)

#### Direct Retailer APIs
- **Tesco.cz, Lidl.cz, Kaufland.cz, Albert.cz, Billa.cz**
- Most retailers don't provide public APIs
- Would require individual web scraping solutions

---

## Recommendations

### For Nutrition Data (Kalorické Tabuľky)

**Primary Choice: Open Food Facts API**
- ✅ Free and open source
- ✅ Excellent global coverage including Czech/Slovak products
- ✅ Comprehensive data (nutrition, ingredients, allergens)
- ✅ Active community and regular updates
- ✅ Easy Python integration
- ✅ Barcode support for mobile scanning
- ✅ No API key required for basic usage

**Secondary Choice: USDA FoodData Central**
- Good for generic food items
- More comprehensive nutrient breakdowns
- Free but requires API key
- Limited Czech/Slovak specific products

**For Specific Czech/Slovak Coverage:**
- Consider combining Open Food Facts with local web scraping from kaloricketabulky.cz
- Use Open Food Facts as primary source
- Fall back to web scraping for items not in Open Food Facts

### For Food Discounts (Kupi.cz)

**Primary Choice: kupiapi Python Library**
- ✅ Already a Python library (perfect fit for this project)
- ✅ Specifically designed for kupi.cz
- ✅ Actively maintained
- ✅ Easy integration
- ✅ Supports filtering and searching

**Implementation Strategy:**
1. Use kupiapi as the main discount data source
2. Implement proper error handling
3. Add caching to reduce scraping frequency
4. Respect rate limiting to avoid being blocked

---

## Integration Examples

### Example 1: Open Food Facts Integration

```python
"""Open Food Facts API integration for nutrition data."""

import requests
from typing import Optional, Dict, List

class OpenFoodFactsAPI:
    """Client for Open Food Facts API."""
    
    BASE_URL = "https://world.openfoodfacts.org"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Foodler - Food Management App - v0.1.0'
        })
    
    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """Get product by barcode."""
        url = f"{self.BASE_URL}/api/v2/product/{barcode}"
        response = self.session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1:
                return data.get('product')
        return None
    
    def search_products(self, query: str, page: int = 1, page_size: int = 20) -> List[Dict]:
        """Search for products."""
        url = f"{self.BASE_URL}/cgi/search.pl"
        params = {
            'search_terms': query,
            'json': 1,
            'page': page,
            'page_size': page_size,
            'fields': 'product_name,nutriments,brands,quantity,image_url'
        }
        
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('products', [])
        return []
    
    def get_nutrition_info(self, product_name: str) -> Optional[Dict]:
        """Get nutrition info for a product."""
        products = self.search_products(product_name, page_size=1)
        
        if products:
            product = products[0]
            nutriments = product.get('nutriments', {})
            
            return {
                'name': product.get('product_name', ''),
                'brand': product.get('brands', ''),
                'quantity': product.get('quantity', ''),
                'calories': nutriments.get('energy-kcal_100g', 0.0),
                'protein': nutriments.get('proteins_100g', 0.0),
                'carbs': nutriments.get('carbohydrates_100g', 0.0),
                'fats': nutriments.get('fat_100g', 0.0),
                'fiber': nutriments.get('fiber_100g', 0.0),
                'sugars': nutriments.get('sugars_100g', 0.0),
                'salt': nutriments.get('salt_100g', 0.0),
                'image_url': product.get('image_url', '')
            }
        return None
```

### Example 2: USDA FoodData Central Integration

```python
"""USDA FoodData Central API integration."""

import requests
from typing import Optional, Dict, List

class USDAFoodDataAPI:
    """Client for USDA FoodData Central API."""
    
    BASE_URL = "https://api.nal.usda.gov/fdc/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
    
    def search_foods(self, query: str, page_size: int = 25) -> List[Dict]:
        """Search for foods."""
        url = f"{self.BASE_URL}/foods/search"
        params = {
            'api_key': self.api_key,
            'query': query,
            'pageSize': page_size
        }
        
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('foods', [])
        return []
    
    def get_food_by_id(self, fdc_id: int) -> Optional[Dict]:
        """Get detailed food info by FDC ID."""
        url = f"{self.BASE_URL}/food/{fdc_id}"
        params = {'api_key': self.api_key}
        
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_nutrition_info(self, food_name: str) -> Optional[Dict]:
        """Get nutrition info for a food item."""
        foods = self.search_foods(food_name, page_size=1)
        
        if foods:
            food = foods[0]
            nutrients = {n['nutrientName']: n['value'] 
                        for n in food.get('foodNutrients', [])}
            
            return {
                'name': food.get('description', ''),
                'calories': nutrients.get('Energy', 0.0),
                'protein': nutrients.get('Protein', 0.0),
                'carbs': nutrients.get('Carbohydrate, by difference', 0.0),
                'fats': nutrients.get('Total lipid (fat)', 0.0),
                'fiber': nutrients.get('Fiber, total dietary', 0.0),
                'sugars': nutrients.get('Sugars, total including NLEA', 0.0)
            }
        return None
```

### Example 3: Kupiapi Integration

```python
"""Kupi.cz integration using kupiapi library."""

from kupiapi import Kupi
from typing import List, Dict

class KupiDiscountAPI:
    """Wrapper for kupiapi library."""
    
    def __init__(self):
        self.kupi = Kupi()
    
    def get_food_discounts(self) -> List[Dict]:
        """Get current food discounts."""
        # Get discounts from food category
        return self.kupi.get_discounts_by_category('potraviny')
    
    def search_product_discounts(self, product_name: str) -> List[Dict]:
        """Search for specific product discounts."""
        return self.kupi.search_discounts(product_name)
    
    def get_discounts_by_store(self, store_name: str) -> List[Dict]:
        """Get discounts for a specific store."""
        stores = {
            'tesco': 'tesco',
            'lidl': 'lidl',
            'kaufland': 'kaufland',
            'albert': 'albert',
            'billa': 'billa'
        }
        
        store_key = stores.get(store_name.lower())
        if store_key:
            return self.kupi.get_discounts_by_shop(store_key)
        return []
    
    def get_best_deals(self, limit: int = 10) -> List[Dict]:
        """Get best deals sorted by discount percentage."""
        all_discounts = self.get_food_discounts()
        
        # Sort by discount percentage if available
        sorted_deals = sorted(
            all_discounts,
            key=lambda x: self._extract_discount_percent(x),
            reverse=True
        )
        
        return sorted_deals[:limit]
    
    @staticmethod
    def _extract_discount_percent(discount: Dict) -> float:
        """Extract discount percentage from discount data."""
        # Implementation depends on kupiapi data structure
        discount_str = discount.get('discount', '0%')
        try:
            return float(discount_str.replace('%', '').strip())
        except (ValueError, AttributeError):
            return 0.0
```

### Example 4: Combined Multi-Source Nutrition Lookup

```python
"""Combined nutrition lookup from multiple sources."""

from typing import Optional, Dict

class MultiSourceNutritionAPI:
    """Combines multiple nutrition APIs for better coverage."""
    
    def __init__(self, usda_api_key: Optional[str] = None):
        self.openfoodfacts = OpenFoodFactsAPI()
        self.usda = USDAFoodDataAPI(usda_api_key) if usda_api_key else None
    
    def get_nutrition_info(self, food_name: str) -> Optional[Dict]:
        """
        Get nutrition info, trying multiple sources.
        Priority: Open Food Facts -> USDA
        """
        # Try Open Food Facts first (better for branded/Czech products)
        nutrition = self.openfoodfacts.get_nutrition_info(food_name)
        
        if nutrition and nutrition.get('calories', 0) > 0:
            nutrition['source'] = 'Open Food Facts'
            return nutrition
        
        # Fall back to USDA if available
        if self.usda:
            nutrition = self.usda.get_nutrition_info(food_name)
            if nutrition and nutrition.get('calories', 0) > 0:
                nutrition['source'] = 'USDA FoodData Central'
                return nutrition
        
        return None
```

---

## Implementation Checklist

- [ ] Install kupiapi: `pip install kupiapi`
- [ ] Add Open Food Facts API client to scrapers
- [ ] Add USDA API client to scrapers (optional)
- [ ] Update nutrition_scraper.py with API integrations
- [ ] Update kupi_scraper.py to use kupiapi library
- [ ] Add proper error handling and retries
- [ ] Implement caching to reduce API calls
- [ ] Add rate limiting
- [ ] Update CLI to support API-based lookups
- [ ] Update documentation with API usage examples
- [ ] Add configuration for API keys (environment variables)
- [ ] Add tests for API integrations

---

## Best Practices

1. **API Key Management**
   - Store API keys in environment variables
   - Never commit API keys to version control
   - Use `.env` files with python-dotenv

2. **Rate Limiting**
   - Implement delays between requests
   - Respect API rate limits
   - Use exponential backoff for retries

3. **Caching**
   - Cache nutrition data locally
   - Implement TTL (time-to-live) for cached data
   - Use database or file-based caching

4. **Error Handling**
   - Handle network errors gracefully
   - Provide fallback mechanisms
   - Log errors for debugging

5. **User Agent**
   - Always set a descriptive User-Agent
   - Include contact information in User-Agent
   - Follow API provider guidelines

---

## License Compliance

### Open Food Facts
- Database: ODbL (Open Database License)
- Must attribute Open Food Facts
- Share-alike for derivative databases
- Commercial use allowed

### USDA FoodData Central
- Public domain (US Government)
- Free to use
- No attribution required
- Commercial use allowed

### Kupiapi
- Check repository license (MIT/GPL)
- Respect website terms of service
- Implement rate limiting
- Commercial use: verify license

---

## Next Steps

1. Integrate Open Food Facts API as primary nutrition source
2. Replace kupi_scraper.py placeholder with kupiapi library
3. Add configuration management for API keys
4. Implement caching layer
5. Add comprehensive error handling
6. Update CLI commands to use APIs
7. Add tests for API integrations
8. Document API usage in README
