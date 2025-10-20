"""Nutrition calculator for balanced food intake."""

from typing import Dict, List, Optional
from datetime import datetime


class NutritionCalculator:
    """Calculates balanced food intake based on nutritional needs."""
    
    # Recommended daily intake values (can be customized)
    DEFAULT_DAILY_NEEDS = {
        'calories': 2000,  # kcal
        'protein': 50,     # grams
        'carbs': 275,      # grams
        'fats': 70,        # grams
        'fiber': 25        # grams
    }
    
    def __init__(self, daily_needs: Optional[Dict[str, float]] = None):
        """Initialize the calculator with daily nutritional needs.
        
        Args:
            daily_needs: Dictionary of daily nutritional requirements.
                        If None, uses DEFAULT_DAILY_NEEDS
        """
        self.daily_needs = daily_needs or self.DEFAULT_DAILY_NEEDS.copy()
    
    def set_custom_needs(self, age: int, weight: float, height: float, 
                        gender: str, activity_level: str) -> Dict[str, float]:
        """Calculate personalized daily nutritional needs.
        
        Uses Harris-Benedict equation and activity multipliers.
        
        Args:
            age: Age in years
            weight: Weight in kg
            height: Height in cm
            gender: 'male' or 'female'
            activity_level: 'sedentary', 'light', 'moderate', 'active', 'very_active'
            
        Returns:
            Dictionary of calculated daily needs
        """
        # Calculate Basal Metabolic Rate (BMR) using Harris-Benedict equation
        if gender.lower() == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        # Activity multipliers
        activity_multipliers = {
            'sedentary': 1.2,      # Little or no exercise
            'light': 1.375,        # Light exercise 1-3 days/week
            'moderate': 1.55,      # Moderate exercise 3-5 days/week
            'active': 1.725,       # Hard exercise 6-7 days/week
            'very_active': 1.9     # Very hard exercise & physical job
        }
        
        multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
        daily_calories = bmr * multiplier
        
        # Calculate macronutrient needs
        # Protein: 15-20% of calories (4 cal/g)
        # Carbs: 45-65% of calories (4 cal/g)
        # Fats: 20-35% of calories (9 cal/g)
        
        self.daily_needs = {
            'calories': round(daily_calories, 2),
            'protein': round((daily_calories * 0.175) / 4, 2),  # 17.5% of calories
            'carbs': round((daily_calories * 0.55) / 4, 2),     # 55% of calories
            'fats': round((daily_calories * 0.275) / 9, 2),     # 27.5% of calories
            'fiber': 25 if gender.lower() == 'female' else 38   # Recommended daily fiber
        }
        
        return self.daily_needs
    
    def calculate_meal_balance(self, foods: List[Dict[str, any]]) -> Dict[str, any]:
        """Calculate nutritional balance of a meal.
        
        Args:
            foods: List of food dictionaries containing:
                  - name: Food name
                  - quantity: Amount (in grams or specified unit)
                  - calories, protein, carbs, fats: Nutritional values per 100g
                  
        Returns:
            Dictionary with total nutrition and percentage of daily needs
        """
        totals = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fats': 0
        }
        
        for food in foods:
            quantity = food.get('quantity', 0)
            # Assume nutritional values are per 100g
            factor = quantity / 100
            
            for nutrient in totals.keys():
                totals[nutrient] += food.get(nutrient, 0) * factor
        
        # Calculate percentage of daily needs
        percentages = {
            nutrient: round((totals[nutrient] / self.daily_needs.get(nutrient, 1)) * 100, 2)
            for nutrient in totals.keys()
        }
        
        return {
            'totals': totals,
            'percentages': percentages,
            'daily_needs': self.daily_needs,
            'is_balanced': self._is_balanced(percentages)
        }
    
    def _is_balanced(self, percentages: Dict[str, float], 
                     tolerance: float = 15) -> bool:
        """Check if a meal is balanced within tolerance.
        
        Args:
            percentages: Dictionary of nutrient percentages
            tolerance: Acceptable deviation percentage
            
        Returns:
            True if all nutrients are within 100 ± tolerance percent
        """
        target = 33.33  # For 3 meals a day
        return all(
            target - tolerance <= percent <= target + tolerance
            for percent in percentages.values()
        )
    
    def suggest_foods_to_balance(self, current_intake: Dict[str, float],
                                foods_available: List[Dict]) -> List[Dict]:
        """Suggest foods to add for better balance.
        
        Args:
            current_intake: Dictionary of current nutritional intake
            foods_available: List of available foods to choose from
            
        Returns:
            List of suggested foods with quantities
        """
        suggestions = []
        
        # Calculate deficits
        deficits = {
            nutrient: max(0, self.daily_needs[nutrient] - current_intake.get(nutrient, 0))
            for nutrient in self.daily_needs.keys()
        }
        
        # Find the most deficient nutrient
        if not deficits or max(deficits.values()) == 0:
            return suggestions  # Already balanced
        
        primary_deficit = max(deficits.items(), key=lambda x: x[1])[0]
        
        # Rank available foods by their content of the deficient nutrient
        ranked_foods = sorted(
            foods_available,
            key=lambda f: f.get(primary_deficit, 0),
            reverse=True
        )
        
        # Suggest top foods
        for food in ranked_foods[:3]:
            if food.get(primary_deficit, 0) > 0:
                # Calculate suggested quantity
                needed = deficits[primary_deficit]
                content_per_100g = food.get(primary_deficit, 1)
                suggested_quantity = (needed / content_per_100g) * 100
                
                suggestions.append({
                    'name': food.get('name'),
                    'suggested_quantity': round(suggested_quantity, 2),
                    'reason': f'High in {primary_deficit}',
                    'provides': {
                        primary_deficit: content_per_100g
                    }
                })
        
        return suggestions
    
    def create_shopping_list(self, meal_plan: List[Dict], 
                           fridge_inventory: List[Dict]) -> List[Dict]:
        """Create a shopping list based on meal plan and current inventory.
        
        Args:
            meal_plan: List of planned meals with ingredients
            fridge_inventory: Current fridge contents
            
        Returns:
            List of items to buy with quantities
        """
        shopping_list = []
        needed_items = {}
        
        # Calculate total needed quantities
        for meal in meal_plan:
            for ingredient in meal.get('ingredients', []):
                name = ingredient.get('name')
                quantity = ingredient.get('quantity', 0)
                unit = ingredient.get('unit', 'g')
                
                key = f"{name}_{unit}"
                needed_items[key] = needed_items.get(key, 0) + quantity
        
        # Check against fridge inventory
        inventory_dict = {
            f"{item.get('name')}_{item.get('unit')}": item.get('quantity', 0)
            for item in fridge_inventory
        }
        
        # Calculate what needs to be bought
        for key, needed_qty in needed_items.items():
            available_qty = inventory_dict.get(key, 0)
            if needed_qty > available_qty:
                name, unit = key.rsplit('_', 1)
                shopping_list.append({
                    'name': name,
                    'quantity': needed_qty - available_qty,
                    'unit': unit
                })
        
        return shopping_list
