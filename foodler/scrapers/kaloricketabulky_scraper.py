"""
KalorickeTabulky.cz web scraper for nutrition data.

WARNING: This scraper may violate kaloricketabulky.cz Terms of Service.
- No official API exists for kaloricketabulky.cz
- Web scraping may be against their ToS
- Use at your own risk
- Consider using Open Food Facts API instead (foodler/scrapers/openfoodfacts_api.py)

This implementation is based on jimrs/kaloricketabulky-scraper approach.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging
import time
import json
from urllib.parse import urljoin, quote

logger = logging.getLogger(__name__)


class KalorickeTabulkyScraper:
    """
    Web scraper for kaloricketabulky.cz nutrition database.
    
    WARNING: This scraper may violate the website's Terms of Service.
    Use responsibly and consider alternatives like Open Food Facts API.
    """
    
    BASE_URL = "https://www.kaloricketabulky.cz"
    
    def __init__(self, rate_limit_seconds: float = 1.0):
        """
        Initialize the scraper.
        
        Args:
            rate_limit_seconds: Delay between requests to avoid overwhelming server
        """
        self.rate_limit = rate_limit_seconds
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Foodler Research Project - Educational Use Only',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'cs,en;q=0.9',
        })
        self.last_request_time = 0
        
        logger.warning(
            "KalorickeTabulkyScraper: This may violate kaloricketabulky.cz ToS. "
            "Consider using Open Food Facts API instead."
        )
    
    def _rate_limited_request(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        """Make a rate-limited HTTP request."""
        # Enforce rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            self.last_request_time = time.time()
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            raise
    
    def search_foods(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search for foods by name.
        
        Args:
            query: Search query (food name)
            limit: Maximum number of results to return
            
        Returns:
            List of food dictionaries with basic info
            
        Note: This is a placeholder implementation. Actual HTML structure
        needs to be inspected from kaloricketabulky.cz to complete.
        """
        try:
            # Note: This URL structure is hypothetical and needs verification
            search_url = urljoin(self.BASE_URL, f"/vyhledavani/{quote(query)}")
            
            logger.info(f"Searching for '{query}' on kaloricketabulky.cz")
            response = self._rate_limited_request(search_url)
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Placeholder: Actual selectors need to be determined by inspecting the site
            # This is an example structure that would need to be adapted
            foods = []
            
            # Example: Find food items (actual class names need verification)
            food_items = soup.find_all('div', class_='food-item', limit=limit)
            
            if not food_items:
                # Try alternative selectors
                food_items = soup.find_all('tr', class_='food-row', limit=limit)
            
            for item in food_items:
                try:
                    food = self._parse_food_item(item)
                    if food:
                        foods.append(food)
                except Exception as e:
                    logger.warning(f"Failed to parse food item: {e}")
                    continue
            
            logger.info(f"Found {len(foods)} foods for query '{query}'")
            return foods
            
        except Exception as e:
            logger.error(f"Search failed for '{query}': {e}")
            return []
    
    def _parse_food_item(self, item) -> Optional[Dict]:
        """
        Parse a food item from HTML element.
        
        Note: This is a placeholder. Actual implementation needs to be
        based on real HTML structure from kaloricketabulky.cz
        """
        try:
            # Placeholder selectors - need to be verified against actual site
            food = {
                'name': self._safe_extract(item, 'h3', 'a', 'span.name'),
                'food_id': self._extract_id(item),
                'calories': self._safe_extract_number(item, 'span.calories', 'td.calories'),
                'source': 'kaloricketabulky.cz'
            }
            
            # Only return if we got at least a name
            if food['name']:
                return food
            return None
            
        except Exception as e:
            logger.debug(f"Failed to parse food item: {e}")
            return None
    
    def get_food_details(self, food_id: str) -> Optional[Dict]:
        """
        Get detailed nutrition information for a specific food.
        
        Args:
            food_id: Food identifier from kaloricketabulky.cz
            
        Returns:
            Dictionary with detailed nutrition data or None if not found
            
        Note: This is a placeholder implementation. Actual HTML structure
        needs to be inspected from kaloricketabulky.cz to complete.
        """
        try:
            # Hypothetical URL structure
            detail_url = urljoin(self.BASE_URL, f"/potraviny/{food_id}")
            
            logger.info(f"Fetching details for food_id: {food_id}")
            response = self._rate_limited_request(detail_url)
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Parse nutrition table
            nutrition = self._parse_nutrition_table(soup)
            
            if nutrition:
                nutrition['food_id'] = food_id
                nutrition['source'] = 'kaloricketabulky.cz'
                return nutrition
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get details for food_id {food_id}: {e}")
            return None
    
    def _parse_nutrition_table(self, soup) -> Optional[Dict]:
        """
        Parse nutrition facts from page.
        
        Note: Placeholder implementation - needs actual HTML structure.
        """
        try:
            # Try to find nutrition table
            table = soup.find('table', class_='nutrition-facts')
            if not table:
                table = soup.find('table', id='nutrition')
            if not table:
                # Try finding any table with nutrition data
                tables = soup.find_all('table')
                for t in tables:
                    if 'kalorie' in t.get_text().lower() or 'energie' in t.get_text().lower():
                        table = t
                        break
            
            if not table:
                logger.warning("No nutrition table found")
                return None
            
            nutrition = {
                'name': self._safe_extract(soup, 'h1', 'h2'),
                'calories': 0.0,
                'protein': 0.0,
                'carbs': 0.0,
                'fats': 0.0,
                'fiber': 0.0,
                'sugars': 0.0,
                'salt': 0.0,
            }
            
            # Parse table rows
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    label = cells[0].get_text().strip().lower()
                    value_text = cells[1].get_text().strip()
                    
                    # Try to extract number
                    value = self._extract_number_from_text(value_text)
                    
                    # Map Czech labels to fields
                    if 'energie' in label or 'kalorie' in label:
                        nutrition['calories'] = value
                    elif 'bílkovin' in label or 'protein' in label:
                        nutrition['protein'] = value
                    elif 'sacharid' in label or 'carbohydrate' in label:
                        nutrition['carbs'] = value
                    elif 'tuk' in label and 'nenasycen' not in label:
                        nutrition['fats'] = value
                    elif 'vláknina' in label or 'fiber' in label:
                        nutrition['fiber'] = value
                    elif 'cukr' in label or 'sugar' in label:
                        nutrition['sugars'] = value
                    elif 'sůl' in label or 'salt' in label or 'sodík' in label:
                        nutrition['salt'] = value
            
            return nutrition
            
        except Exception as e:
            logger.error(f"Failed to parse nutrition table: {e}")
            return None
    
    def get_nutrition_info(self, food_name: str) -> Optional[Dict]:
        """
        Search for food and return nutrition info.
        
        Args:
            food_name: Name of the food to search for
            
        Returns:
            Dictionary with nutrition data (per 100g) or None if not found
        """
        # Search for the food
        results = self.search_foods(food_name, limit=1)
        
        if not results:
            logger.info(f"No results found for '{food_name}'")
            return None
        
        # Get the first result
        food = results[0]
        
        # If we have a food_id, get detailed info
        if food.get('food_id'):
            details = self.get_food_details(food['food_id'])
            if details:
                return details
        
        # Return what we have from search results
        return food
    
    def scrape_category(self, category: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Scrape all foods from a specific category.
        
        Args:
            category: Category name or URL path
            limit: Maximum number of items to scrape
            
        Returns:
            List of food dictionaries
            
        Note: Placeholder implementation - needs actual site structure.
        """
        try:
            category_url = urljoin(self.BASE_URL, f"/kategorie/{quote(category)}")
            
            logger.info(f"Scraping category: {category}")
            response = self._rate_limited_request(category_url)
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            foods = []
            items = soup.find_all('div', class_='food-item')
            
            if not items:
                items = soup.find_all('tr', class_='food-row')
            
            for i, item in enumerate(items):
                if limit and i >= limit:
                    break
                    
                try:
                    food = self._parse_food_item(item)
                    if food:
                        foods.append(food)
                except Exception as e:
                    logger.warning(f"Failed to parse item: {e}")
                    continue
            
            logger.info(f"Scraped {len(foods)} foods from category '{category}'")
            return foods
            
        except Exception as e:
            logger.error(f"Failed to scrape category '{category}': {e}")
            return []
    
    def export_to_json(self, foods: List[Dict], filename: str):
        """Export scraped data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(foods, f, ensure_ascii=False, indent=2)
            logger.info(f"Exported {len(foods)} foods to {filename}")
        except Exception as e:
            logger.error(f"Failed to export to JSON: {e}")
    
    def export_to_csv(self, foods: List[Dict], filename: str):
        """Export scraped data to CSV file."""
        try:
            import csv
            
            if not foods:
                logger.warning("No foods to export")
                return
            
            # Get all unique keys
            fieldnames = set()
            for food in foods:
                fieldnames.update(food.keys())
            fieldnames = sorted(fieldnames)
            
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(foods)
            
            logger.info(f"Exported {len(foods)} foods to {filename}")
        except Exception as e:
            logger.error(f"Failed to export to CSV: {e}")
    
    # Helper methods
    
    def _safe_extract(self, element, *selectors) -> str:
        """Try multiple selectors to extract text."""
        for selector in selectors:
            try:
                if '.' in selector or '#' in selector:
                    found = element.select_one(selector)
                else:
                    found = element.find(selector)
                
                if found:
                    return found.get_text().strip()
            except:
                continue
        return ''
    
    def _safe_extract_number(self, element, *selectors) -> float:
        """Try multiple selectors to extract a number."""
        text = self._safe_extract(element, *selectors)
        return self._extract_number_from_text(text)
    
    def _extract_number_from_text(self, text: str) -> float:
        """Extract first number from text."""
        import re
        # Remove common units and extract number
        text = text.replace(',', '.').replace(' ', '')
        match = re.search(r'(\d+\.?\d*)', text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        return 0.0
    
    def _extract_id(self, element) -> Optional[str]:
        """Try to extract food ID from element."""
        # Try data attributes
        for attr in ['data-id', 'data-food-id', 'id']:
            if element.has_attr(attr):
                return element[attr]
        
        # Try to extract from href
        link = element.find('a')
        if link and link.has_attr('href'):
            href = link['href']
            # Extract ID from URL pattern like /food/12345 or /potraviny/12345
            import re
            match = re.search(r'/(?:food|potraviny)/(\d+)', href)
            if match:
                return match.group(1)
        
        return None


# Convenience function
def scrape_kaloricketabulky(food_name: str) -> Optional[Dict]:
    """
    Quick function to scrape nutrition info for a food.
    
    WARNING: May violate kaloricketabulky.cz Terms of Service.
    
    Args:
        food_name: Name of food to search for
        
    Returns:
        Dictionary with nutrition data or None
    """
    scraper = KalorickeTabulkyScraper()
    return scraper.get_nutrition_info(food_name)
