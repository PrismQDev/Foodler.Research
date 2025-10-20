# Foodler Usage Examples

## Quick Start

### 1. Setting Up Your Fridge Inventory

First, add some items to your fridge:

```bash
# Add fresh produce
python main.py fridge add "Tomatoes" 500 g --expiry 2025-10-25 --calories 18 --protein 0.9 --carbs 3.9 --fats 0.2

# Add protein sources
python main.py fridge add "Chicken breast" 600 g --expiry 2025-10-23 --calories 165 --protein 31 --carbs 0 --fats 3.6

# Add dairy
python main.py fridge add "Milk" 1000 ml --expiry 2025-10-22 --calories 42 --protein 3.4 --carbs 5 --fats 1

# Add grains
python main.py fridge add "Brown rice" 1000 g --calories 370 --protein 7.9 --carbs 77 --fats 2.9
```

### 2. View Your Inventory

```bash
python main.py fridge list
```

Output:
```
=== Fridge Inventory ===

[1] Tomatoes: 500.0 g
    Expiry: 2025-10-25
    Nutrition: 18.0 kcal, P: 0.9g, C: 3.9g, F: 0.2g

[2] Chicken breast: 600.0 g
    Expiry: 2025-10-23
    Nutrition: 165.0 kcal, P: 31.0g, C: 0.0g, F: 3.6g

[3] Milk: 1000.0 ml
    Expiry: 2025-10-22
    Nutrition: 42.0 kcal, P: 3.4g, C: 5.0g, F: 1.0g

[4] Brown rice: 1000.0 g
    Expiry: N/A
    Nutrition: 370.0 kcal, P: 7.9g, C: 77.0g, F: 2.9g
```

### 3. Check Expiring Items

```bash
python main.py fridge expiring --days 7
```

This will show all items expiring within the next 7 days.

## Calculating Your Nutritional Needs

### Calculate Personalized Daily Requirements

```bash
python main.py calculate needs --age 30 --weight 75 --height 180 --gender male --activity moderate
```

Output:
```
=== Your Daily Nutritional Needs ===

Calories: 2713.69 kcal
Protein: 118.85 g
Carbs: 373.13 g
Fats: 82.92 g
Fiber: 38 g
```

Different activity levels:
- `sedentary`: Little or no exercise
- `light`: Light exercise 1-3 days/week
- `moderate`: Moderate exercise 3-5 days/week
- `active`: Hard exercise 6-7 days/week
- `very_active`: Very hard exercise & physical job

### Calculate Meal Balance

```bash
python main.py calculate meal
```

This interactive command will:
1. Show you all available items in your fridge
2. Ask you to select items for your meal
3. Ask for the quantity of each item
4. Calculate the total nutritional value
5. Show percentage of daily needs
6. Tell you if the meal is balanced

Example interaction:
```
=== Available Items ===

1. Tomatoes (500.0 g)
2. Chicken breast (600.0 g)
3. Milk (1000.0 ml)
4. Brown rice (1000.0 g)

Select items for your meal (comma-separated numbers):
> 2,4

How much Chicken breast (in grams)?
> 150

How much Brown rice (in grams)?
> 80

=== Meal Analysis ===

Total Nutrition:
  Calories: 543.50 (20.0% of daily needs)
  Protein: 52.82 (44.4% of daily needs)
  Carbs: 61.60 (16.5% of daily needs)
  Fats: 8.72 (10.5% of daily needs)

⚠ This meal could be better balanced
```

## Working with Discounts

### Browse Current Discounts

```bash
python main.py discounts list --limit 10
```

This will show the top 10 current food discounts from kupi.cz.

### Search for Specific Products

```bash
python main.py discounts search "chicken"
```

This searches for discounts on chicken products.

## Looking Up Nutritional Information

### Get Nutrition Facts

```bash
python main.py nutrition lookup "banana"
```

Output:
```
=== Nutritional Info for 'banana' (per 100g) ===

Calories: 89 kcal
Protein: 1.1 g
Carbs: 23 g
Fats: 0.3 g
Fiber: 2.6 g
Sugar: 12 g
```

Use this to add accurate nutritional data when adding items to your fridge.

## Advanced Usage

### Using Python API Directly

You can also use Foodler programmatically in your Python scripts:

```python
from foodler.database import FridgeDatabase
from foodler.calculator import NutritionCalculator
from foodler.scrapers import NutritionScraper

# Initialize database
db = FridgeDatabase()

# Add items
db.add_item("Eggs", 12, "pieces", calories=155, protein=13, carbs=1.1, fats=11)

# Get all items
items = db.get_all_items()
for item in items:
    print(f"{item.name}: {item.quantity} {item.unit}")

# Calculate nutrition
calculator = NutritionCalculator()

# Set custom needs
needs = calculator.set_custom_needs(
    age=25,
    weight=70,
    height=175,
    gender='male',
    activity_level='moderate'
)

# Calculate meal balance
foods = [
    {'name': 'Chicken', 'quantity': 150, 'calories': 165, 'protein': 31, 'carbs': 0, 'fats': 3.6},
    {'name': 'Rice', 'quantity': 100, 'calories': 370, 'protein': 7.9, 'carbs': 77, 'fats': 2.9}
]

balance = calculator.calculate_meal_balance(foods)
print(f"Total calories: {balance['totals']['calories']}")
print(f"Is balanced: {balance['is_balanced']}")

# Clean up
db.close()
```

### Creating a Weekly Meal Plan

```python
from foodler.calculator import NutritionCalculator

calculator = NutritionCalculator()

# Define a meal plan
meal_plan = [
    {
        'name': 'Monday Breakfast',
        'ingredients': [
            {'name': 'Oatmeal', 'quantity': 50, 'unit': 'g'},
            {'name': 'Banana', 'quantity': 120, 'unit': 'g'},
            {'name': 'Milk', 'quantity': 200, 'unit': 'ml'}
        ]
    },
    {
        'name': 'Monday Lunch',
        'ingredients': [
            {'name': 'Chicken breast', 'quantity': 150, 'unit': 'g'},
            {'name': 'Rice', 'quantity': 100, 'unit': 'g'},
            {'name': 'Broccoli', 'quantity': 150, 'unit': 'g'}
        ]
    }
]

# Get current fridge inventory
from foodler.database import FridgeDatabase
db = FridgeDatabase()
fridge_inventory = db.get_all_items()

# Create shopping list
shopping_list = calculator.create_shopping_list(meal_plan, fridge_inventory)

print("Shopping List:")
for item in shopping_list:
    print(f"- {item['name']}: {item['quantity']} {item['unit']}")

db.close()
```

## Tips and Best Practices

1. **Keep Your Inventory Updated**: Regularly update quantities as you use items
2. **Add Expiry Dates**: This helps prevent food waste
3. **Use Accurate Nutritional Data**: Look up values in kaloricke tabulky for Czech foods
4. **Plan Your Meals**: Use the meal calculator to ensure balanced nutrition
5. **Check Expiring Items Daily**: Use `fridge expiring` to plan meals around items that need to be used soon
6. **Track Your Progress**: Calculate your needs and monitor if you're meeting them

## Common Workflows

### Workflow 1: Weekly Grocery Shopping

1. Check what's expiring: `python main.py fridge expiring --days 7`
2. Plan meals around expiring items
3. Check for discounts: `python main.py discounts list`
4. Create shopping list based on meal plan
5. Add new items after shopping

### Workflow 2: Daily Meal Planning

1. Calculate your daily needs (do once)
2. Check fridge inventory: `python main.py fridge list`
3. Plan breakfast using meal calculator
4. Plan lunch using remaining needs
5. Plan dinner to complete daily requirements

### Workflow 3: Using Discounts Effectively

1. Browse current discounts
2. Look up nutritional values for discounted items
3. Check if you have space in fridge
4. Add purchased discounted items to inventory
5. Plan meals using the discounted items

## Troubleshooting

### Database Issues

If you encounter database errors, try:
```bash
# Remove the database file and start fresh
rm fridge.db
```

### Web Scraping Issues

Note that the web scrapers need to be customized based on the actual HTML structure of the target websites. If scraping doesn't work:

1. Check if the website is accessible
2. Review the HTML structure of the page
3. Update the selectors in the scraper code
4. Consider rate limiting if getting blocked

### Missing Nutritional Data

If nutritional data isn't available:
1. Look it up manually on kaloricke tabulky websites
2. Add it when creating fridge items using the `--calories`, `--protein`, `--carbs`, `--fats` flags
3. Use approximate values from similar foods if exact data isn't available

## Getting Help

For more information:
- Check the README.md for installation and setup
- Review the code documentation in each module
- Open an issue on GitHub for bugs or feature requests