"""USDA FoodData Central API client for nutrition data."""

import requests
from typing import Optional, Dict, List
import logging
import os

logger = logging.getLogger(__name__)


class USDAFoodDataAPI:
    """Client for USDA FoodData Central API - US Government nutrition database."""
    
    BASE_URL = "https://api.nal.usda.gov/fdc/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the API client.
        
        Args:
            api_key: USDA API key. If not provided, will try to read from
                    USDA_API_KEY environment variable
        """
        self.api_key = api_key or os.environ.get('USDA_API_KEY')
        if not self.api_key:
            logger.warning(
                "USDA API key not provided. "
                "Get one at https://fdc.nal.usda.gov/api-key-signup.html"
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Foodler - Food Management App - v0.1.0'
        })
    
    def search_foods(self, query: str, page_number: int = 1, 
                    page_size: int = 25, data_type: Optional[List[str]] = None) -> List[Dict]:
        """Search for foods in the USDA database.
        
        Args:
            query: Search query (food name, keywords)
            page_number: Page number (starting from 1)
            page_size: Results per page (max 200)
            data_type: Optional list of data types to include:
                      ['Foundation', 'SR Legacy', 'Survey (FNDDS)', 'Branded']
            
        Returns:
            List of food dictionaries
        """
        if not self.api_key:
            logger.error("USDA API key required for search")
            return []
        
        try:
            url = f"{self.BASE_URL}/foods/search"
            params = {
                'api_key': self.api_key,
                'query': query,
                'pageNumber': page_number,
                'pageSize': min(page_size, 200)
            }
            
            if data_type:
                params['dataType'] = ','.join(data_type)
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('foods', [])
            
        except requests.RequestException as e:
            logger.error(f"Error searching USDA foods for '{query}': {e}")
            return []
    
    def get_food_by_id(self, fdc_id: int) -> Optional[Dict]:
        """Get detailed food information by FDC ID.
        
        Args:
            fdc_id: USDA FoodData Central ID
            
        Returns:
            Food dictionary with full details or None if not found
        """
        if not self.api_key:
            logger.error("USDA API key required")
            return None
        
        try:
            url = f"{self.BASE_URL}/food/{fdc_id}"
            params = {'api_key': self.api_key}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Error fetching USDA food ID {fdc_id}: {e}")
            return None
    
    def get_nutrition_info(self, food_name: str) -> Optional[Dict]:
        """Get nutritional information for a food item.
        
        Args:
            food_name: Name of the food item
            
        Returns:
            Dictionary containing nutritional values per 100g:
            - name: Food description
            - calories: Energy in kcal
            - protein: Protein in g
            - carbs: Carbohydrates in g
            - fats: Total fat in g
            - fiber: Dietary fiber in g
            - sugars: Total sugars in g
            - sodium: Sodium in mg
            
            Returns None if food not found or API key missing
        """
        foods = self.search_foods(food_name, page_size=1)
        
        if foods:
            food = foods[0]
            
            # Build nutrient dictionary for easy lookup
            nutrients_dict = {}
            for nutrient in food.get('foodNutrients', []):
                name = nutrient.get('nutrientName', '')
                value = nutrient.get('value', 0.0)
                nutrients_dict[name] = value
            
            nutrition_info = {
                'name': food.get('description', ''),
                'brand': food.get('brandOwner', ''),
                'fdc_id': food.get('fdcId'),
                'data_type': food.get('dataType', ''),
                
                # Energy
                'calories': nutrients_dict.get('Energy', 0.0),
                
                # Macronutrients
                'protein': nutrients_dict.get('Protein', 0.0),
                'carbs': nutrients_dict.get('Carbohydrate, by difference', 0.0),
                'fats': nutrients_dict.get('Total lipid (fat)', 0.0),
                'fiber': nutrients_dict.get('Fiber, total dietary', 0.0),
                'sugars': nutrients_dict.get('Sugars, total including NLEA', 
                                            nutrients_dict.get('Sugars, Total', 0.0)),
                
                # Other nutrients
                'sodium': nutrients_dict.get('Sodium, Na', 0.0) / 1000,  # Convert mg to g
                'cholesterol': nutrients_dict.get('Cholesterol', 0.0) / 1000,  # Convert mg to g
                
                'source': 'USDA FoodData Central'
            }
            
            logger.info(f"Found USDA nutrition info for '{food_name}': {nutrition_info['name']}")
            return nutrition_info
        
        logger.info(f"No USDA nutrition info found for '{food_name}'")
        return None
    
    def get_detailed_info(self, food_name: str) -> Optional[Dict]:
        """Get detailed nutritional information including all available nutrients.
        
        Args:
            food_name: Name of the food item
            
        Returns:
            Dictionary with comprehensive nutritional information
        """
        foods = self.search_foods(food_name, page_size=1)
        
        if foods:
            food = foods[0]
            fdc_id = food.get('fdcId')
            
            # Get full details
            full_food = self.get_food_by_id(fdc_id)
            if not full_food:
                return None
            
            # Build comprehensive nutrient dictionary
            nutrients_dict = {}
            for nutrient in full_food.get('foodNutrients', []):
                name = nutrient.get('nutrient', {}).get('name', '')
                value = nutrient.get('amount', 0.0)
                unit = nutrient.get('nutrient', {}).get('unitName', '')
                nutrients_dict[name] = {'value': value, 'unit': unit}
            
            detailed_info = {
                'name': full_food.get('description', ''),
                'brand': full_food.get('brandOwner', ''),
                'fdc_id': fdc_id,
                'data_type': full_food.get('dataType', ''),
                'ingredients': full_food.get('ingredients', ''),
                
                # Macronutrients
                'calories': self._get_nutrient_value(nutrients_dict, 'Energy'),
                'protein': self._get_nutrient_value(nutrients_dict, 'Protein'),
                'carbs': self._get_nutrient_value(nutrients_dict, 'Carbohydrate, by difference'),
                'fats': self._get_nutrient_value(nutrients_dict, 'Total lipid (fat)'),
                'fiber': self._get_nutrient_value(nutrients_dict, 'Fiber, total dietary'),
                'sugars': self._get_nutrient_value(nutrients_dict, 'Sugars, total including NLEA'),
                
                # Fat breakdown
                'saturated_fats': self._get_nutrient_value(nutrients_dict, 'Fatty acids, total saturated'),
                'monounsaturated_fats': self._get_nutrient_value(nutrients_dict, 'Fatty acids, total monounsaturated'),
                'polyunsaturated_fats': self._get_nutrient_value(nutrients_dict, 'Fatty acids, total polyunsaturated'),
                'trans_fats': self._get_nutrient_value(nutrients_dict, 'Fatty acids, total trans'),
                'cholesterol': self._get_nutrient_value(nutrients_dict, 'Cholesterol') / 1000,  # mg to g
                
                # Vitamins
                'vitamin_a': self._get_nutrient_value(nutrients_dict, 'Vitamin A, RAE'),
                'vitamin_c': self._get_nutrient_value(nutrients_dict, 'Vitamin C, total ascorbic acid'),
                'vitamin_d': self._get_nutrient_value(nutrients_dict, 'Vitamin D (D2 + D3)'),
                'vitamin_e': self._get_nutrient_value(nutrients_dict, 'Vitamin E (alpha-tocopherol)'),
                'vitamin_k': self._get_nutrient_value(nutrients_dict, 'Vitamin K (phylloquinone)'),
                'thiamin': self._get_nutrient_value(nutrients_dict, 'Thiamin'),
                'riboflavin': self._get_nutrient_value(nutrients_dict, 'Riboflavin'),
                'niacin': self._get_nutrient_value(nutrients_dict, 'Niacin'),
                'vitamin_b6': self._get_nutrient_value(nutrients_dict, 'Vitamin B-6'),
                'folate': self._get_nutrient_value(nutrients_dict, 'Folate, total'),
                'vitamin_b12': self._get_nutrient_value(nutrients_dict, 'Vitamin B-12'),
                
                # Minerals
                'calcium': self._get_nutrient_value(nutrients_dict, 'Calcium, Ca') / 1000,  # mg to g
                'iron': self._get_nutrient_value(nutrients_dict, 'Iron, Fe') / 1000,
                'magnesium': self._get_nutrient_value(nutrients_dict, 'Magnesium, Mg') / 1000,
                'phosphorus': self._get_nutrient_value(nutrients_dict, 'Phosphorus, P') / 1000,
                'potassium': self._get_nutrient_value(nutrients_dict, 'Potassium, K') / 1000,
                'sodium': self._get_nutrient_value(nutrients_dict, 'Sodium, Na') / 1000,
                'zinc': self._get_nutrient_value(nutrients_dict, 'Zinc, Zn') / 1000,
                
                'source': 'USDA FoodData Central'
            }
            
            return detailed_info
        
        return None
    
    @staticmethod
    def _get_nutrient_value(nutrients_dict: Dict, nutrient_name: str) -> float:
        """Helper to safely extract nutrient value."""
        nutrient = nutrients_dict.get(nutrient_name, {})
        if isinstance(nutrient, dict):
            return nutrient.get('value', 0.0)
        return 0.0
