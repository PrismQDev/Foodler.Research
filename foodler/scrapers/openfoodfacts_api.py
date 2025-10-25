"""Open Food Facts API client for nutrition data."""

import requests
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class OpenFoodFactsAPI:
    """Client for Open Food Facts API - Free, open-source nutrition database."""
    
    BASE_URL = "https://world.openfoodfacts.org"
    
    def __init__(self):
        """Initialize the API client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Foodler - Food Management App - v0.1.0 - Contact: github.com/PrismQDev/Foodler.Research'
        })
    
    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """Get product information by barcode.
        
        Args:
            barcode: Product barcode (EAN-13, UPC, etc.)
            
        Returns:
            Product dictionary or None if not found
        """
        try:
            url = f"{self.BASE_URL}/api/v2/product/{barcode}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 1:
                return data.get('product')
            
            logger.info(f"Product with barcode {barcode} not found")
            return None
            
        except requests.RequestException as e:
            logger.error(f"Error fetching product by barcode {barcode}: {e}")
            return None
    
    def search_products(self, query: str, page: int = 1, page_size: int = 20,
                       country: Optional[str] = None) -> List[Dict]:
        """Search for products by name.
        
        Args:
            query: Search query (product name, brand, etc.)
            page: Page number (starting from 1)
            page_size: Number of results per page (max 100)
            country: Optional country code to filter results (e.g., 'cz', 'sk')
            
        Returns:
            List of product dictionaries
        """
        try:
            url = f"{self.BASE_URL}/cgi/search.pl"
            params = {
                'search_terms': query,
                'json': 1,
                'page': page,
                'page_size': min(page_size, 100),
                'fields': 'product_name,nutriments,brands,quantity,image_url,countries_tags'
            }
            
            if country:
                params['tagtype_0'] = 'countries'
                params['tag_contains_0'] = 'contains'
                params['tag_0'] = country
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('products', [])
            
        except requests.RequestException as e:
            logger.error(f"Error searching products for '{query}': {e}")
            return []
    
    def get_nutrition_info(self, food_name: str, country: Optional[str] = None) -> Optional[Dict]:
        """Get nutritional information for a food item.
        
        Args:
            food_name: Name of the food item to search for
            country: Optional country code to prioritize results (e.g., 'cz', 'sk')
            
        Returns:
            Dictionary containing nutritional values per 100g:
            - name: Product name
            - brand: Brand name
            - quantity: Package quantity
            - calories: Calorie content (kcal)
            - protein: Protein content (g)
            - carbs: Carbohydrate content (g)
            - fats: Fat content (g)
            - fiber: Fiber content (g)
            - sugars: Sugar content (g)
            - salt: Salt content (g)
            - saturated_fats: Saturated fat content (g)
            - image_url: Product image URL
            
            Returns None if food not found
        """
        products = self.search_products(food_name, page_size=1, country=country)
        
        if products:
            product = products[0]
            nutriments = product.get('nutriments', {})
            
            nutrition_info = {
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
                'saturated_fats': nutriments.get('saturated-fat_100g', 0.0),
                'image_url': product.get('image_url', ''),
                'source': 'Open Food Facts'
            }
            
            logger.info(f"Found nutrition info for '{food_name}': {nutrition_info['name']}")
            return nutrition_info
        
        logger.info(f"No nutrition info found for '{food_name}'")
        return None
    
    def get_detailed_info(self, food_name: str, country: Optional[str] = None) -> Optional[Dict]:
        """Get detailed nutritional information including vitamins and minerals.
        
        Args:
            food_name: Name of the food item
            country: Optional country code to prioritize results
            
        Returns:
            Dictionary with detailed nutritional information including vitamins and minerals
        """
        products = self.search_products(food_name, page_size=1, country=country)
        
        if products:
            product = products[0]
            nutriments = product.get('nutriments', {})
            
            # Extract all available nutrient data
            detailed_info = {
                'name': product.get('product_name', ''),
                'brand': product.get('brands', ''),
                'quantity': product.get('quantity', ''),
                'categories': product.get('categories', ''),
                'ingredients_text': product.get('ingredients_text', ''),
                
                # Macronutrients
                'calories': nutriments.get('energy-kcal_100g', 0.0),
                'protein': nutriments.get('proteins_100g', 0.0),
                'carbs': nutriments.get('carbohydrates_100g', 0.0),
                'fats': nutriments.get('fat_100g', 0.0),
                'fiber': nutriments.get('fiber_100g', 0.0),
                'sugars': nutriments.get('sugars_100g', 0.0),
                'salt': nutriments.get('salt_100g', 0.0),
                'sodium': nutriments.get('sodium_100g', 0.0),
                
                # Fat breakdown
                'saturated_fats': nutriments.get('saturated-fat_100g', 0.0),
                'monounsaturated_fats': nutriments.get('monounsaturated-fat_100g', 0.0),
                'polyunsaturated_fats': nutriments.get('polyunsaturated-fat_100g', 0.0),
                'trans_fats': nutriments.get('trans-fat_100g', 0.0),
                'cholesterol': nutriments.get('cholesterol_100g', 0.0),
                
                # Vitamins (if available)
                'vitamin_a': nutriments.get('vitamin-a_100g', 0.0),
                'vitamin_c': nutriments.get('vitamin-c_100g', 0.0),
                'vitamin_d': nutriments.get('vitamin-d_100g', 0.0),
                'vitamin_e': nutriments.get('vitamin-e_100g', 0.0),
                
                # Minerals (if available)
                'calcium': nutriments.get('calcium_100g', 0.0),
                'iron': nutriments.get('iron_100g', 0.0),
                'magnesium': nutriments.get('magnesium_100g', 0.0),
                'potassium': nutriments.get('potassium_100g', 0.0),
                'zinc': nutriments.get('zinc_100g', 0.0),
                
                # Scores and grades
                'nutriscore_grade': product.get('nutriscore_grade', ''),
                'nova_group': product.get('nova_group', ''),
                
                # Other info
                'image_url': product.get('image_url', ''),
                'serving_size': product.get('serving_size', '100g'),
                'source': 'Open Food Facts'
            }
            
            return detailed_info
        
        return None
    
    def search_by_category(self, category: str, page: int = 1, page_size: int = 20) -> List[Dict]:
        """Search products by category.
        
        Args:
            category: Category name (e.g., 'vegetables', 'dairy', 'meat')
            page: Page number
            page_size: Results per page
            
        Returns:
            List of products in the category
        """
        try:
            url = f"{self.BASE_URL}/category/{category}/{page}.json"
            params = {'page_size': min(page_size, 100)}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('products', [])
            
        except requests.RequestException as e:
            logger.error(f"Error searching category '{category}': {e}")
            return []
