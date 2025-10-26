"""
Example usage of KalorickeTabulkyScraper

WARNING: This scraper may violate kaloricketabulky.cz Terms of Service.
Use at your own risk. Consider using Open Food Facts API instead.
"""

from foodler.scrapers import KalorickeTabulkyScraper
import json


def example_basic_search():
    """Example 1: Basic food search"""
    print("=== Example 1: Basic Food Search ===\n")
    
    scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)
    
    # Search for a food
    food_name = "kuřecí prsa"
    print(f"Searching for: {food_name}")
    
    nutrition = scraper.get_nutrition_info(food_name)
    
    if nutrition:
        print(f"\nFood: {nutrition.get('name', 'N/A')}")
        print(f"Calories: {nutrition.get('calories', 0)} kcal/100g")
        print(f"Protein: {nutrition.get('protein', 0)} g/100g")
        print(f"Carbs: {nutrition.get('carbs', 0)} g/100g")
        print(f"Fats: {nutrition.get('fats', 0)} g/100g")
        print(f"Source: {nutrition.get('source', 'N/A')}")
    else:
        print("No results found")
    
    print()


def example_search_multiple():
    """Example 2: Search for multiple foods"""
    print("=== Example 2: Search Multiple Foods ===\n")
    
    scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)
    
    foods_to_search = ["banán", "jablko", "brambory"]
    
    for food_name in foods_to_search:
        print(f"Searching: {food_name}")
        results = scraper.search_foods(food_name, limit=3)
        
        if results:
            print(f"  Found {len(results)} results:")
            for i, food in enumerate(results, 1):
                print(f"    {i}. {food.get('name', 'N/A')} - {food.get('calories', 0)} kcal")
        else:
            print(f"  No results")
        print()


def example_scrape_category():
    """Example 3: Scrape a food category"""
    print("=== Example 3: Scrape Category ===\n")
    
    scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)
    
    # Scrape a category (limit to avoid too many requests)
    category = "ovoce"  # fruits
    print(f"Scraping category: {category} (limited to 5 items)")
    
    foods = scraper.scrape_category(category, limit=5)
    
    print(f"Found {len(foods)} foods:")
    for food in foods:
        print(f"  - {food.get('name', 'N/A')}: {food.get('calories', 0)} kcal")
    
    print()


def example_export_data():
    """Example 4: Export scraped data"""
    print("=== Example 4: Export Data ===\n")
    
    scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)
    
    # Search for multiple foods
    foods_to_scrape = ["kuřecí prsa", "rýže", "brokolice"]
    all_foods = []
    
    for food_name in foods_to_scrape:
        print(f"Scraping: {food_name}")
        nutrition = scraper.get_nutrition_info(food_name)
        if nutrition:
            all_foods.append(nutrition)
    
    print(f"\nScraped {len(all_foods)} foods")
    
    # Export to JSON
    json_file = "/tmp/kaloricketabulky_data.json"
    scraper.export_to_json(all_foods, json_file)
    print(f"Exported to: {json_file}")
    
    # Export to CSV
    csv_file = "/tmp/kaloricketabulky_data.csv"
    scraper.export_to_csv(all_foods, csv_file)
    print(f"Exported to: {csv_file}")
    
    print()


def example_with_error_handling():
    """Example 5: Proper error handling"""
    print("=== Example 5: With Error Handling ===\n")
    
    try:
        scraper = KalorickeTabulkyScraper(rate_limit_seconds=1.0)
        
        food_name = "neexistující potravina xyz123"
        print(f"Searching for: {food_name}")
        
        nutrition = scraper.get_nutrition_info(food_name)
        
        if nutrition:
            print(f"Found: {nutrition.get('name')}")
        else:
            print("Not found - this is expected for non-existent food")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print("This is normal - the scraper may fail if site structure changes")
    
    print()


def example_compare_with_openfoodfacts():
    """Example 6: Compare with Open Food Facts API"""
    print("=== Example 6: Compare with Open Food Facts ===\n")
    
    from foodler.scrapers import OpenFoodFactsAPI
    
    food_name = "banán"
    
    # Try KalorickeTabulky (may have legal issues)
    print(f"Searching '{food_name}' in KalorickeTabulky.cz:")
    kt_scraper = KalorickeTabulkyScraper(rate_limit_seconds=2.0)
    kt_result = kt_scraper.get_nutrition_info(food_name)
    
    if kt_result:
        print(f"  Found: {kt_result.get('name', 'N/A')}")
        print(f"  Calories: {kt_result.get('calories', 0)} kcal")
    else:
        print("  Not found (or scraper needs HTML structure adjustment)")
    
    # Try Open Food Facts (recommended, legal, stable)
    print(f"\nSearching '{food_name}' in Open Food Facts:")
    off_api = OpenFoodFactsAPI()
    off_result = off_api.get_nutrition_info(food_name, country='cz')
    
    if off_result:
        print(f"  Found: {off_result.get('name', 'N/A')}")
        print(f"  Calories: {off_result.get('calories', 0)} kcal")
        print(f"  Source: {off_result.get('source', 'N/A')}")
        print("\n  ✅ RECOMMENDED: Use Open Food Facts API - legal, stable, no ToS issues")
    else:
        print("  Not found")
    
    print()


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("KalorickeTabulkyScraper Examples")
    print("="*60)
    print("\n⚠️  WARNING: This scraper may violate kaloricketabulky.cz ToS")
    print("Consider using Open Food Facts API instead (see Example 6)")
    print("="*60 + "\n")
    
    # Note: These examples may not work without adjusting HTML selectors
    # to match actual kaloricketabulky.cz structure
    
    print("NOTE: These examples are placeholders. The scraper needs HTML")
    print("selectors adjusted to match actual kaloricketabulky.cz structure.\n")
    
    try:
        # Only run comparison example by default
        example_compare_with_openfoodfacts()
        
        # Uncomment to run other examples (may fail without proper HTML selectors):
        # example_basic_search()
        # example_search_multiple()
        # example_scrape_category()
        # example_export_data()
        # example_with_error_handling()
        
    except Exception as e:
        print(f"\nExample failed: {e}")
        print("This is expected - scraper needs HTML structure inspection")
        print("to set correct selectors for kaloricketabulky.cz")


if __name__ == '__main__':
    main()
