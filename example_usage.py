#!/usr/bin/env python3
"""Example script demonstrating Foodler API usage."""

from foodler.database import FridgeDatabase
from foodler.calculator import NutritionCalculator
from foodler.scrapers import NutritionScraper, KupiScraper
from datetime import datetime, timedelta

def main():
    print("=== Foodler API Example ===\n")
    
    # 1. Initialize database
    print("1. Setting up fridge inventory...")
    db = FridgeDatabase('example_fridge.db')
    
    # 2. Add some items
    print("   Adding items to fridge...")
    db.add_item(
        name="Chicken breast",
        quantity=600,
        unit="g",
        calories=165,
        protein=31,
        carbs=0,
        fats=3.6
    )
    
    db.add_item(
        name="Brown rice",
        quantity=1000,
        unit="g",
        calories=370,
        protein=7.9,
        carbs=77,
        fats=2.9
    )
    
    db.add_item(
        name="Broccoli",
        quantity=400,
        unit="g",
        calories=34,
        protein=2.8,
        carbs=7,
        fats=0.4
    )
    
    # 3. List all items
    print("\n2. Current inventory:")
    items = db.get_all_items()
    for item in items:
        print(f"   - {item.name}: {item.quantity} {item.unit}")
    
    # 4. Check items to cycle through
    print("\n3. Items to use next (cycling priority):")
    items_to_use = db.get_items_to_use(limit=5)
    for item in items_to_use:
        print(f"   - {item.name} (last used: {item.last_used_meal}, meals without: {item.meals_without})")
    
    # 4b. Simulate using an item in breakfast
    print("\n   Simulating breakfast preparation...")
    if items:
        chicken = items[0]  # Use the first item (chicken)
        db.mark_as_used(chicken.id, meal_number=1)  # 1 = Breakfast
        print(f"   Marked {chicken.name} as used in Breakfast")
        print(f"   Last used meal: {chicken.last_used_meal}")
        
        # Increment meals_without for items not used
        db.increment_meals_without(exclude_ids=[chicken.id])
        print(f"   Incremented meals_without counter for unused items")
    
    # 5. Calculate personalized nutritional needs
    print("\n4. Calculating nutritional needs...")
    calculator = NutritionCalculator()
    needs = calculator.set_custom_needs(
        age=30,
        weight=75,
        height=180,
        gender='male',
        activity_level='moderate'
    )
    
    print(f"   Daily needs:")
    print(f"   - Calories: {needs['calories']:.0f} kcal")
    print(f"   - Protein: {needs['protein']:.0f} g")
    print(f"   - Carbs: {needs['carbs']:.0f} g")
    print(f"   - Fats: {needs['fats']:.0f} g")
    
    # 6. Plan and analyze a meal
    print("\n5. Planning a meal...")
    meal_foods = [
        {'name': 'Chicken breast', 'quantity': 200, 'calories': 165, 'protein': 31, 'carbs': 0, 'fats': 3.6},
        {'name': 'Brown rice', 'quantity': 150, 'calories': 370, 'protein': 7.9, 'carbs': 77, 'fats': 2.9},
        {'name': 'Broccoli', 'quantity': 100, 'calories': 34, 'protein': 2.8, 'carbs': 7, 'fats': 0.4}
    ]
    
    balance = calculator.calculate_meal_balance(meal_foods)
    
    print(f"   Meal nutrition:")
    print(f"   - Calories: {balance['totals']['calories']:.0f} kcal ({balance['percentages']['calories']:.1f}% of daily)")
    print(f"   - Protein: {balance['totals']['protein']:.0f} g ({balance['percentages']['protein']:.1f}% of daily)")
    print(f"   - Carbs: {balance['totals']['carbs']:.0f} g ({balance['percentages']['carbs']:.1f}% of daily)")
    print(f"   - Fats: {balance['totals']['fats']:.0f} g ({balance['percentages']['fats']:.1f}% of daily)")
    
    if balance['is_balanced']:
        print("   ✓ This meal is well balanced!")
    else:
        print("   ⚠ This meal could be better balanced")
    
    # 7. Create a shopping list
    print("\n6. Creating shopping list...")
    meal_plan = [
        {
            'name': 'Lunch',
            'ingredients': [
                {'name': 'Chicken breast', 'quantity': 300, 'unit': 'g'},
                {'name': 'Rice', 'quantity': 200, 'unit': 'g'},
                {'name': 'Tomatoes', 'quantity': 150, 'unit': 'g'}
            ]
        }
    ]
    
    fridge_inventory = [
        {'name': 'Chicken breast', 'quantity': 600, 'unit': 'g'},
        {'name': 'Rice', 'quantity': 100, 'unit': 'g'}
    ]
    
    shopping_list = calculator.create_shopping_list(meal_plan, fridge_inventory)
    
    if shopping_list:
        print("   Items to buy:")
        for item in shopping_list:
            print(f"   - {item['name']}: {item['quantity']} {item['unit']}")
    else:
        print("   You have everything you need!")
    
    # 8. Demonstrate scrapers (will fail without internet/in sandboxed environment)
    print("\n7. Testing scrapers...")
    print("   Note: Scrapers require internet access and proper site structure")
    
    nutrition_scraper = NutritionScraper()
    kupi_scraper = KupiScraper()
    
    print("   - Nutrition scraper initialized")
    print("   - Discount scraper initialized")
    
    # Clean up
    db.close()
    print("\n=== Example completed successfully! ===")
    print("\nThe example database 'example_fridge.db' has been created.")
    print("You can explore it or delete it when done.")


if __name__ == '__main__':
    main()
