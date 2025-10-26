"""Multi-source nutrition scraper combining API clients."""

from typing import Dict, Optional, List
import logging

from .openfoodfacts_api import OpenFoodFactsAPI

try:
    from .usda_api import USDAFoodDataAPI
    USDA_AVAILABLE = True
except ImportError:
    USDA_AVAILABLE = False

logger = logging.getLogger(__name__)


class NutritionScraper:
    """
    Multi-source nutrition scraper.
    
    Combines multiple nutrition APIs for comprehensive coverage:
    1. Open Food Facts - Primary source (Czech/Slovak + global products)
    2. USDA FoodData Central - Secondary source (requires API key)
    """
    
    def __init__(self, usda_api_key: Optional[str] = None, 
                 country_code: Optional[str] = 'cz'):
        """Initialize the scraper with multiple API sources.
        
        Args:
            usda_api_key: Optional USDA API key for broader coverage
            country_code: Country code to prioritize results (e.g., 'cz', 'sk')
        """
        self.openfoodfacts = OpenFoodFactsAPI()
        self.country_code = country_code
        
        # Initialize USDA API if key is provided
        self.usda = None
        if USDA_AVAILABLE and usda_api_key:
            try:
                self.usda = USDAFoodDataAPI(usda_api_key)
                logger.info("USDA FoodData Central API initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize USDA API: {e}")
        
        logger.info(f"NutritionScraper initialized (country: {country_code})")
    
    def get_nutrition_info(self, food_name: str) -> Optional[Dict[str, float]]:
        """Get nutritional information for a food item.
        
        Tries multiple sources in order of priority:
        1. Open Food Facts (prioritizing country-specific products)
        2. USDA FoodData Central (if available)
        
        Args:
            food_name: Name of the food item
            
        Returns:
            Dictionary containing nutritional values per 100g:
            - name: Product name
            - brand: Brand name (if available)
            - calories: Calorie content (kcal)
            - protein: Protein content (g)
            - carbs: Carbohydrate content (g)
            - fats: Fat content (g)
            - fiber: Fiber content (g)
            - sugars: Sugar content (g)
            - salt: Salt content (g)
            - source: Data source name
            
            Returns None if food not found in any source
        """
        # Try Open Food Facts first (better for Czech/Slovak products)
        logger.info(f"Searching for '{food_name}' in Open Food Facts")
        nutrition = self.openfoodfacts.get_nutrition_info(food_name, self.country_code)
        
        if nutrition and nutrition.get('calories', 0) > 0:
            logger.info(f"Found '{food_name}' in Open Food Facts")
            return nutrition
        
        # Fall back to USDA if available
        if self.usda:
            logger.info(f"Searching for '{food_name}' in USDA FoodData Central")
            nutrition = self.usda.get_nutrition_info(food_name)
            
            if nutrition and nutrition.get('calories', 0) > 0:
                logger.info(f"Found '{food_name}' in USDA FoodData Central")
                return nutrition
        
        logger.warning(f"No nutrition data found for '{food_name}'")
        return None
    
    def get_detailed_info(self, food_name: str) -> Optional[Dict]:
        """Get detailed nutritional information including vitamins and minerals.
        
        Args:
            food_name: Name of the food item
            
        Returns:
            Dictionary with detailed nutritional information or None if not found
        """
        # Try Open Food Facts first
        logger.info(f"Searching for detailed info of '{food_name}' in Open Food Facts")
        detailed = self.openfoodfacts.get_detailed_info(food_name, self.country_code)
        
        if detailed:
            logger.info(f"Found detailed info for '{food_name}' in Open Food Facts")
            return detailed
        
        # Fall back to USDA if available
        if self.usda:
            logger.info(f"Searching for detailed info of '{food_name}' in USDA")
            detailed = self.usda.get_detailed_info(food_name)
            
            if detailed:
                logger.info(f"Found detailed info for '{food_name}' in USDA")
                return detailed
        
        logger.warning(f"No detailed nutrition data found for '{food_name}'")
        return None
    
    def search_foods(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for food items matching the query.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching foods with basic info
        """
        results = []
        
        # Search Open Food Facts
        logger.info(f"Searching for '{query}' in Open Food Facts")
        off_results = self.openfoodfacts.search_products(
            query, page_size=limit, country=self.country_code
        )
        
        for product in off_results:
            results.append({
                'name': product.get('product_name', ''),
                'brand': product.get('brands', ''),
                'source': 'Open Food Facts'
            })
        
        # If we have fewer than requested, try USDA
        if len(results) < limit and self.usda:
            logger.info(f"Searching for '{query}' in USDA")
            usda_results = self.usda.search_foods(query, page_size=limit - len(results))
            
            for food in usda_results:
                results.append({
                    'name': food.get('description', ''),
                    'brand': food.get('brandOwner', ''),
                    'source': 'USDA FoodData Central'
                })
        
        logger.info(f"Found {len(results)} foods matching '{query}'")
        return results[:limit]
    
    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """Get product information by barcode.
        
        Currently only supports Open Food Facts (barcode scanning).
        
        Args:
            barcode: Product barcode (EAN-13, UPC, etc.)
            
        Returns:
            Product dictionary or None if not found
        """
        logger.info(f"Looking up barcode {barcode} in Open Food Facts")
        product = self.openfoodfacts.get_product_by_barcode(barcode)
        
        if product:
            logger.info(f"Found product with barcode {barcode}")
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
                'image_url': product.get('image_url', ''),
                'source': 'Open Food Facts'
            }
        
        logger.warning(f"No product found with barcode {barcode}")
        return None
