"""Command-line interface for Foodler application."""

import click
from datetime import datetime
from foodler.database import FridgeDatabase
from foodler.scrapers import KupiScraper, NutritionScraper
from foodler.calculator import NutritionCalculator


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Foodler - Food management and nutrition calculator.
    
    Calculate balanced food intake from your fridge inventory,
    kupi.cz discounts, and nutritional value tables.
    """
    pass


@cli.group()
def fridge():
    """Manage fridge inventory."""
    pass


@fridge.command('add')
@click.argument('name')
@click.argument('quantity', type=float)
@click.argument('unit')
@click.option('--calories', type=float, help='Calories per unit')
@click.option('--protein', type=float, help='Protein per unit')
@click.option('--carbs', type=float, help='Carbs per unit')
@click.option('--fats', type=float, help='Fats per unit')
def fridge_add(name, quantity, unit, calories, protein, carbs, fats):
    """Add item to fridge inventory."""
    db = FridgeDatabase()
    
    item = db.add_item(
        name=name,
        quantity=quantity,
        unit=unit,
        calories=calories,
        protein=protein,
        carbs=carbs,
        fats=fats
    )
    
    click.echo(f"Added: {item.name} ({item.quantity} {item.unit})")
    db.close()


@fridge.command('list')
def fridge_list():
    """List all items in fridge."""
    db = FridgeDatabase()
    items = db.get_all_items()
    
    if not items:
        click.echo("Fridge is empty!")
        return
    
    click.echo("\n=== Fridge Inventory ===\n")
    for item in items:
        last_used = item.last_used_date.strftime('%Y-%m-%d') if item.last_used_date else 'Never'
        click.echo(f"[{item.id}] {item.name}: {item.quantity} {item.unit}")
        click.echo(f"    Last used: {last_used} | Meals without: {item.meals_without}")
        if item.calories:
            click.echo(f"    Nutrition: {item.calories} kcal, "
                      f"P: {item.protein}g, C: {item.carbs}g, F: {item.fats}g")
        click.echo()
    
    db.close()


@fridge.command('cycle')
@click.option('--limit', default=10, help='Number of items to show')
def fridge_cycle(limit):
    """Show items that should be used soon to cycle through inventory."""
    db = FridgeDatabase()
    items = db.get_items_to_use(limit)
    
    if not items:
        click.echo("No items in fridge!")
        return
    
    click.echo(f"\n=== Items to Use Next (Cycling Priority) ===\n")
    for item in items:
        last_used = item.last_used_date.strftime('%Y-%m-%d') if item.last_used_date else 'Never used'
        click.echo(f"[{item.id}] {item.name}: {item.quantity} {item.unit}")
        click.echo(f"    Last used: {last_used} | Meals without: {item.meals_without}")
        click.echo()
    
    db.close()


@fridge.command('used')
@click.argument('item_id', type=int)
def fridge_used(item_id):
    """Mark an item as used in a meal."""
    db = FridgeDatabase()
    
    item = db.mark_as_used(item_id)
    if item:
        click.echo(f"Marked {item.name} as used!")
        click.echo(f"Last used date updated and meals_without reset to 0.")
    else:
        click.echo(f"Item {item_id} not found")
    
    db.close()


@fridge.command('remove')
@click.argument('item_id', type=int)
def fridge_remove(item_id):
    """Remove item from fridge."""
    db = FridgeDatabase()
    
    if db.delete_item(item_id):
        click.echo(f"Removed item {item_id}")
    else:
        click.echo(f"Item {item_id} not found")
    
    db.close()


@cli.group()
def discounts():
    """Browse food discounts from kupi.cz."""
    pass


@discounts.command('list')
@click.option('--limit', default=10, help='Number of discounts to show')
def discounts_list(limit):
    """Show current food discounts."""
    scraper = KupiScraper()
    deals = scraper.get_best_deals(limit=limit)
    
    if not deals:
        click.echo("No discounts found. Note: This feature requires web scraping implementation.")
        return
    
    click.echo(f"\n=== Top {limit} Discounts ===\n")
    for deal in deals:
        click.echo(f"{deal.get('name')}")
        click.echo(f"  Price: {deal.get('price')} (was {deal.get('original_price')})")
        click.echo(f"  Discount: {deal.get('discount')}")
        click.echo(f"  Store: {deal.get('store')}")
        click.echo()


@discounts.command('search')
@click.argument('product')
def discounts_search(product):
    """Search for product discounts."""
    scraper = KupiScraper()
    results = scraper.search_product(product)
    
    if not results:
        click.echo(f"No discounts found for '{product}'")
        return
    
    click.echo(f"\n=== Discounts for '{product}' ===\n")
    for result in results:
        click.echo(f"{result.get('name')}")
        click.echo(f"  Price: {result.get('price')}")
        click.echo(f"  Store: {result.get('store')}")
        click.echo()


@cli.group()
def nutrition():
    """Get nutritional information."""
    pass


@nutrition.command('lookup')
@click.argument('food_name')
def nutrition_lookup(food_name):
    """Look up nutritional values for a food."""
    scraper = NutritionScraper()
    info = scraper.get_nutrition_info(food_name)
    
    if not info:
        click.echo(f"Nutritional information not found for '{food_name}'")
        return
    
    click.echo(f"\n=== Nutritional Info for '{food_name}' (per 100g) ===\n")
    click.echo(f"Calories: {info['calories']} kcal")
    click.echo(f"Protein: {info['protein']} g")
    click.echo(f"Carbs: {info['carbs']} g")
    click.echo(f"Fats: {info['fats']} g")
    if 'fiber' in info:
        click.echo(f"Fiber: {info['fiber']} g")
    if 'sugar' in info:
        click.echo(f"Sugar: {info['sugar']} g")


@cli.group()
def calculate():
    """Calculate balanced food intake."""
    pass


@calculate.command('needs')
@click.option('--age', type=int, required=True, help='Age in years')
@click.option('--weight', type=float, required=True, help='Weight in kg')
@click.option('--height', type=float, required=True, help='Height in cm')
@click.option('--gender', type=click.Choice(['male', 'female']), required=True)
@click.option('--activity', 
              type=click.Choice(['sedentary', 'light', 'moderate', 'active', 'very_active']),
              default='moderate',
              help='Activity level')
def calculate_needs(age, weight, height, gender, activity):
    """Calculate personalized daily nutritional needs."""
    calculator = NutritionCalculator()
    needs = calculator.set_custom_needs(age, weight, height, gender, activity)
    
    click.echo("\n=== Your Daily Nutritional Needs ===\n")
    click.echo(f"Calories: {needs['calories']} kcal")
    click.echo(f"Protein: {needs['protein']} g")
    click.echo(f"Carbs: {needs['carbs']} g")
    click.echo(f"Fats: {needs['fats']} g")
    click.echo(f"Fiber: {needs['fiber']} g")


@calculate.command('meal')
def calculate_meal():
    """Calculate nutritional balance of foods from fridge."""
    db = FridgeDatabase()
    items = db.get_all_items()
    
    if not items:
        click.echo("Fridge is empty! Add items first.")
        db.close()
        return
    
    click.echo("\n=== Available Items ===\n")
    for i, item in enumerate(items, 1):
        click.echo(f"{i}. {item.name} ({item.quantity} {item.unit})")
    
    selection = click.prompt("\nSelect items for your meal (comma-separated numbers)", type=str)
    
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected_items = [items[i] for i in indices if 0 <= i < len(items)]
    except (ValueError, IndexError):
        click.echo("Invalid selection")
        db.close()
        return
    
    # Get quantities
    foods = []
    for item in selected_items:
        try:
            qty = click.prompt(f"\nHow much {item.name} (in grams)?", type=float)
            foods.append({
                'name': item.name,
                'quantity': qty,
                'calories': item.calories or 0,
                'protein': item.protein or 0,
                'carbs': item.carbs or 0,
                'fats': item.fats or 0
            })
        except (ValueError, click.Abort):
            click.echo(f"Invalid quantity, skipping {item.name}")
    
    if foods:
        calculator = NutritionCalculator()
        balance = calculator.calculate_meal_balance(foods)
        
        click.echo("\n=== Meal Analysis ===\n")
        click.echo("Total Nutrition:")
        for nutrient, value in balance['totals'].items():
            percentage = balance['percentages'][nutrient]
            click.echo(f"  {nutrient.capitalize()}: {value:.2f} ({percentage:.1f}% of daily needs)")
        
        if balance['is_balanced']:
            click.echo("\n✓ This meal is well balanced!")
        else:
            click.echo("\n⚠ This meal could be better balanced")
    
    db.close()


if __name__ == '__main__':
    cli()
