"""
Example scripts demonstrating API usage for nutrition data and discounts.

This file shows practical examples of using the new API integrations:
1. Open Food Facts API for nutrition data
2. USDA FoodData Central API for additional nutrition coverage
3. Kupiapi library for kupi.cz discounts
"""

# Example 1: Basic nutrition lookup using Open Food Facts
def example_openfoodfacts_basic():
    """Basic usage of Open Food Facts API."""
    from foodler.scrapers import OpenFoodFactsAPI
    
    print("=== Example 1: Open Food Facts - Basic Nutrition Lookup ===\n")
    
    api = OpenFoodFactsAPI()
    
    # Search for a food item
    food_name = "banán"  # Czech for banana
    nutrition = api.get_nutrition_info(food_name, country='cz')
    
    if nutrition:
        print(f"Food: {nutrition['name']}")
        print(f"Brand: {nutrition['brand']}")
        print(f"Per 100g:")
        print(f"  Calories: {nutrition['calories']} kcal")
        print(f"  Protein: {nutrition['protein']} g")
        print(f"  Carbs: {nutrition['carbs']} g")
        print(f"  Fats: {nutrition['fats']} g")
        print(f"  Fiber: {nutrition['fiber']} g")
        print(f"  Sugars: {nutrition['sugars']} g")
        print(f"Source: {nutrition['source']}")
    else:
        print(f"No nutrition data found for '{food_name}'")
    
    print()


# Example 2: Barcode scanning with Open Food Facts
def example_openfoodfacts_barcode():
    """Demonstrate barcode lookup."""
    from foodler.scrapers import OpenFoodFactsAPI
    
    print("=== Example 2: Open Food Facts - Barcode Lookup ===\n")
    
    api = OpenFoodFactsAPI()
    
    # Example barcode (Nutella)
    barcode = "3017620422003"
    product = api.get_product_by_barcode(barcode)
    
    if product:
        print(f"Product found by barcode {barcode}:")
        print(f"  Name: {product.get('product_name', 'N/A')}")
        print(f"  Brands: {product.get('brands', 'N/A')}")
        print(f"  Quantity: {product.get('quantity', 'N/A')}")
        
        nutriments = product.get('nutriments', {})
        print(f"  Calories: {nutriments.get('energy-kcal_100g', 0)} kcal/100g")
    else:
        print(f"No product found with barcode {barcode}")
    
    print()


# Example 3: Detailed nutrition info with vitamins and minerals
def example_openfoodfacts_detailed():
    """Get detailed nutritional information."""
    from foodler.scrapers import OpenFoodFactsAPI
    
    print("=== Example 3: Open Food Facts - Detailed Nutrition ===\n")
    
    api = OpenFoodFactsAPI()
    
    food_name = "broccoli"
    detailed = api.get_detailed_info(food_name)
    
    if detailed:
        print(f"Food: {detailed['name']}")
        print("\nMacronutrients per 100g:")
        print(f"  Calories: {detailed['calories']} kcal")
        print(f"  Protein: {detailed['protein']} g")
        print(f"  Carbs: {detailed['carbs']} g")
        print(f"  Fats: {detailed['fats']} g")
        
        print("\nVitamins:")
        print(f"  Vitamin A: {detailed['vitamin_a']} µg")
        print(f"  Vitamin C: {detailed['vitamin_c']} mg")
        
        print("\nMinerals:")
        print(f"  Calcium: {detailed['calcium']} mg")
        print(f"  Iron: {detailed['iron']} mg")
        
        print(f"\nNutri-Score: {detailed['nutriscore_grade']}")
    
    print()


# Example 4: Using USDA FoodData Central API
def example_usda_api():
    """Demonstrate USDA API usage (requires API key)."""
    from foodler.scrapers import USDAFoodDataAPI
    import os
    
    print("=== Example 4: USDA FoodData Central API ===\n")
    
    # Get API key from environment variable
    api_key = os.environ.get('USDA_API_KEY')
    
    if not api_key:
        print("USDA API key not found in environment variables.")
        print("Get one at: https://fdc.nal.usda.gov/api-key-signup.html")
        print("Set it with: export USDA_API_KEY='your-key-here'")
        return
    
    api = USDAFoodDataAPI(api_key)
    
    # Search for a food
    food_name = "chicken breast"
    nutrition = api.get_nutrition_info(food_name)
    
    if nutrition:
        print(f"Food: {nutrition['name']}")
        print(f"Brand: {nutrition['brand']}")
        print(f"Per 100g:")
        print(f"  Calories: {nutrition['calories']} kcal")
        print(f"  Protein: {nutrition['protein']} g")
        print(f"  Carbs: {nutrition['carbs']} g")
        print(f"  Fats: {nutrition['fats']} g")
        print(f"Source: {nutrition['source']}")
    
    print()


# Example 5: Multi-source nutrition lookup
def example_multi_source():
    """Use NutritionScraper with multiple sources."""
    from foodler.scrapers import NutritionScraper
    import os
    
    print("=== Example 5: Multi-Source Nutrition Lookup ===\n")
    
    # Initialize with optional USDA API key
    usda_key = os.environ.get('USDA_API_KEY')
    scraper = NutritionScraper(usda_api_key=usda_key, country_code='cz')
    
    # Search for foods
    foods_to_search = ["kuřecí prsa", "brambory", "mrkev"]
    
    for food in foods_to_search:
        print(f"Searching for: {food}")
        nutrition = scraper.get_nutrition_info(food)
        
        if nutrition:
            print(f"  Found: {nutrition['name']}")
            print(f"  Calories: {nutrition['calories']} kcal/100g")
            print(f"  Source: {nutrition['source']}")
        else:
            print(f"  Not found")
        print()


# Example 6: Search for products
def example_search_products():
    """Search for multiple products."""
    from foodler.scrapers import NutritionScraper
    
    print("=== Example 6: Search Products ===\n")
    
    scraper = NutritionScraper(country_code='cz')
    
    query = "jogurt"
    results = scraper.search_foods(query, limit=5)
    
    print(f"Search results for '{query}':")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['name']} - {result['brand']} ({result['source']})")
    
    print()


# Example 7: Kupi.cz discounts using kupiapi
def example_kupi_discounts():
    """Get discounts from kupi.cz using kupiapi library."""
    from foodler.scrapers import KupiScraper
    
    print("=== Example 7: Kupi.cz Discounts ===\n")
    
    try:
        scraper = KupiScraper()
        
        # Get food discounts
        print("Getting food discounts from kupi.cz...")
        discounts = scraper.get_discounts(category='potraviny')
        
        print(f"Found {len(discounts)} food discounts")
        
        # Show first 5
        for i, discount in enumerate(discounts[:5], 1):
            print(f"\n{i}. {discount.get('name', 'N/A')}")
            print(f"   Price: {discount.get('price', 'N/A')}")
            print(f"   Store: {discount.get('store', 'N/A')}")
        
    except ImportError:
        print("kupiapi library not installed.")
        print("Install with: pip install kupiapi")
    
    print()


# Example 8: Search specific product discounts
def example_kupi_search():
    """Search for specific product discounts."""
    from foodler.scrapers import KupiScraper
    
    print("=== Example 8: Kupi.cz - Search Product Discounts ===\n")
    
    try:
        scraper = KupiScraper()
        
        # Search for chicken products
        product = "kuřecí"
        print(f"Searching for '{product}' discounts...")
        
        discounts = scraper.search_product(product)
        
        print(f"Found {len(discounts)} discounts for '{product}'")
        
        for i, discount in enumerate(discounts[:3], 1):
            print(f"\n{i}. {discount.get('name', 'N/A')}")
            print(f"   Price: {discount.get('price', 'N/A')}")
            print(f"   Discount: {discount.get('discount', 'N/A')}")
            print(f"   Store: {discount.get('store', 'N/A')}")
        
    except ImportError:
        print("kupiapi library not installed.")
        print("Install with: pip install kupiapi")
    
    print()


# Example 9: Get discounts by store
def example_kupi_by_store():
    """Get discounts from specific stores."""
    from foodler.scrapers import KupiScraper
    
    print("=== Example 9: Kupi.cz - Discounts by Store ===\n")
    
    try:
        scraper = KupiScraper()
        
        stores = ['tesco', 'lidl', 'kaufland']
        
        for store in stores:
            print(f"\n{store.upper()} Discounts:")
            discounts = scraper.get_discounts_by_shop(store)
            print(f"  Found {len(discounts)} discounts")
            
            if discounts:
                # Show first discount
                first = discounts[0]
                print(f"  Example: {first.get('name', 'N/A')} - {first.get('price', 'N/A')}")
        
    except ImportError:
        print("kupiapi library not installed.")
        print("Install with: pip install kupiapi")
    
    print()


# Example 10: Get best deals
def example_best_deals():
    """Find the best current deals."""
    from foodler.scrapers import KupiScraper
    
    print("=== Example 10: Kupi.cz - Best Deals ===\n")
    
    try:
        scraper = KupiScraper()
        
        print("Finding best deals...")
        best_deals = scraper.get_best_deals(limit=5)
        
        print(f"Top {len(best_deals)} deals:\n")
        
        for i, deal in enumerate(best_deals, 1):
            print(f"{i}. {deal.get('name', 'N/A')}")
            print(f"   Discount: {deal.get('discount', 'N/A')}")
            print(f"   Price: {deal.get('price', 'N/A')}")
            print(f"   Store: {deal.get('store', 'N/A')}")
            print()
        
    except ImportError:
        print("kupiapi library not installed.")
        print("Install with: pip install kupiapi")


# Main function to run all examples
def main():
    """Run all examples."""
    import sys
    
    examples = {
        '1': ('Open Food Facts - Basic', example_openfoodfacts_basic),
        '2': ('Open Food Facts - Barcode', example_openfoodfacts_barcode),
        '3': ('Open Food Facts - Detailed', example_openfoodfacts_detailed),
        '4': ('USDA API', example_usda_api),
        '5': ('Multi-Source Lookup', example_multi_source),
        '6': ('Search Products', example_search_products),
        '7': ('Kupi.cz Discounts', example_kupi_discounts),
        '8': ('Kupi.cz Search', example_kupi_search),
        '9': ('Kupi.cz by Store', example_kupi_by_store),
        '10': ('Best Deals', example_best_deals),
    }
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num in examples:
            name, func = examples[example_num]
            print(f"\nRunning: {name}\n")
            func()
        else:
            print(f"Example {example_num} not found.")
            print("Available examples:", ', '.join(examples.keys()))
    else:
        print("API Integration Examples")
        print("=" * 50)
        print("\nAvailable examples:")
        for num, (name, _) in examples.items():
            print(f"  {num}: {name}")
        print("\nRun with: python api_examples.py <example_number>")
        print("Or run all examples:")
        print()
        
        # Run all examples
        for num, (name, func) in examples.items():
            try:
                func()
            except Exception as e:
                print(f"Error in example {num}: {e}\n")


if __name__ == '__main__':
    main()
