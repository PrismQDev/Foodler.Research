# Foodler.Research

An application for calculating balanced food intake from your fridge inventory, kupi.cz food discounts, and nutritional value tables (kaloricke tabulky).

## Overview

Foodler helps you:
- 🥗 Manage your fridge inventory with usage tracking
- 🔄 Cycle through food items to avoid waste
- 💰 Find food discounts from kupi.cz
- 📊 Get nutritional information from kaloricke tabulky
- ⚖️ Calculate balanced food intake based on your needs
- 🛒 Generate shopping lists

## Why Python?

This application is built in **Python** for several key reasons:

1. **Web Scraping Excellence**: Python has industry-leading libraries for web scraping:
   - `BeautifulSoup4` and `lxml` for HTML parsing
   - `requests` for HTTP operations
   - Easy to handle dynamic content and various website structures

2. **Data Processing**: Strong ecosystem for data manipulation:
   - `pandas` for data analysis
   - Easy integration with databases via `SQLAlchemy`
   - Rich built-in data structures

3. **Rapid Development**: Python's simplicity allows for:
   - Quick prototyping and iteration
   - Clear, readable code
   - Extensive standard library
   - Large community support

4. **Versatility**: Can easily expand to:
   - Web applications (Flask/Django)
   - Data analysis and visualization
   - Machine learning for meal recommendations
   - API integrations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/PrismQDev/Foodler.Research.git
cd Foodler.Research
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Fridge Inventory Management

Add items to your fridge:
```bash
python main.py fridge add "Chicken breast" 500 g --calories 165 --protein 31 --carbs 0 --fats 3.6
python main.py fridge add "Broccoli" 300 g --calories 34 --protein 2.8 --carbs 7 --fats 0.4
```

List all items:
```bash
python main.py fridge list
```

Check which items to use next (cycling priority):
```bash
python main.py fridge cycle
```

Mark an item as used in a meal:
```bash
# Default (Breakfast)
python main.py fridge used <item_id>

# Specify meal: 1=Breakfast, 2=Lunch, 3=Dinner, 4=Snack
python main.py fridge used <item_id> --meal 2
```

Remove an item:
```bash
python main.py fridge remove <item_id>
```

### Browse Discounts

Find current food discounts from kupi.cz:
```bash
python main.py discounts list --limit 10
```

Search for specific product discounts:
```bash
python main.py discounts search "chicken"
```

### Nutritional Information

Look up nutritional values:
```bash
python main.py nutrition lookup "banana"
```

### Calculate Balanced Intake

Calculate your personalized daily needs:
```bash
python main.py calculate needs --age 30 --weight 70 --height 175 --gender male --activity moderate
```

Analyze a meal from your fridge:
```bash
python main.py calculate meal
```

## Project Structure

```
Foodler.Research/
├── foodler/
│   ├── __init__.py
│   ├── cli.py                    # Command-line interface
│   ├── database/
│   │   ├── __init__.py
│   │   └── fridge_db.py         # Fridge inventory database
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── kupi_scraper.py      # kupi.cz discount scraper
│   │   └── nutrition_scraper.py  # Nutritional data scraper
│   └── calculator/
│       ├── __init__.py
│       └── nutrition_calculator.py  # Balanced intake calculator
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
└── README.md
```

## Features

### 1. Fridge Inventory Database
- Store food items with quantities and units
- Track last used meal (date + meal number: Breakfast=1, Lunch=2, Dinner=3, Snack=4)
- Track meals without using each item
- Store nutritional information
- Get cycling priority to help rotate through food

### 2. Discount Scraper (kupi.cz)
- Browse current food discounts
- Search for specific products
- Compare prices across stores
- Find best deals by discount percentage

### 3. Nutrition Scraper (kaloricke tabulky)
- Look up nutritional values
- Get detailed macro and micronutrient information
- Search food database

### 4. Balanced Intake Calculator
- Calculate personalized daily nutritional needs
- Based on age, weight, height, gender, and activity level
- Uses Harris-Benedict equation
- Analyze meal nutritional balance
- Suggest foods to improve balance
- Generate shopping lists

## Development

### Dependencies

- **requests**: HTTP library for API calls and web scraping
- **beautifulsoup4**: HTML/XML parsing for web scraping
- **lxml**: Fast XML/HTML parser
- **sqlalchemy**: SQL toolkit and ORM for database
- **pandas**: Data analysis and manipulation
- **click**: Command-line interface framework

### Extending the Application

The modular design allows easy extension:

1. **Add new scrapers**: Create new scraper classes in `foodler/scrapers/`
2. **Enhance calculator**: Add new calculation methods in `foodler/calculator/`
3. **New databases**: Add new database models in `foodler/database/`
4. **CLI commands**: Add new commands in `foodler/cli.py`

## API Integrations ⭐ NEW!

The application now integrates with multiple APIs for comprehensive nutrition data and discount information:

### Nutrition Data APIs

#### 1. Open Food Facts (Primary - Recommended)
- **Free & Open Source** - No API key required
- **Global Coverage** - 4+ million products from 150+ countries
- **Czech/Slovak Products** - Excellent coverage of local products
- **Features**: Nutrition data, ingredients, allergens, Nutri-Score, barcode scanning

**Example Usage:**
```python
from foodler.scrapers import OpenFoodFactsAPI

api = OpenFoodFactsAPI()
nutrition = api.get_nutrition_info("banán", country='cz')
print(f"Calories: {nutrition['calories']} kcal/100g")
```

#### 2. USDA FoodData Central (Secondary - Optional)
- **Free** - Requires API key from https://fdc.nal.usda.gov/
- **300,000+ Foods** - Comprehensive US food database
- **Detailed Nutrients** - Extensive vitamin and mineral data
- Set API key: `export USDA_API_KEY='your-key-here'`

**Combined Multi-Source Usage:**
```python
from foodler.scrapers import NutritionScraper

scraper = NutritionScraper(usda_api_key='your-key', country_code='cz')
nutrition = scraper.get_nutrition_info("chicken breast")  # Auto tries multiple sources
```

### Discount Data API

#### Kupi.cz Integration (via kupiapi)
- **Free** - Open-source Python library
- **Czech Market** - All major retailers (Tesco, Lidl, Kaufland, Albert, Billa)
- **Features**: Current discounts, search, category filtering, store filtering

**Example Usage:**
```python
from foodler.scrapers import KupiScraper

scraper = KupiScraper()
discounts = scraper.get_discounts(category='potraviny')
chicken_deals = scraper.search_product('kuřecí')
best_deals = scraper.get_best_deals(limit=10)
```

### API Examples

See `api_examples.py` for comprehensive usage examples:
```bash
python api_examples.py        # List all examples
python api_examples.py 1      # Run specific example
```

For detailed API research and recommendations, see [API_RESEARCH.md](API_RESEARCH.md).

For alternatives to web scraping tools (like jimrs/kaloricketabulky-scraper), see [JIMRS_ALTERNATIVES.md](JIMRS_ALTERNATIVES.md).

## Note on Web Scraping

The application now primarily uses official and community-maintained APIs instead of web scraping:

- **Open Food Facts API**: Official API, no scraping needed
- **USDA FoodData Central**: Official government API
- **Kupi.cz**: Uses `kupiapi` library (maintained scraper)

API usage best practices:
- Respect rate limits
- Cache results when appropriate
- Handle errors gracefully
- Set appropriate User-Agent headers
- Store API keys securely (environment variables)

## Future Enhancements

- [x] API integration for nutrition data (Open Food Facts, USDA)
- [x] API integration for discounts (kupiapi)
- [x] Barcode scanning support (via Open Food Facts)
- [ ] Web UI using Flask or Django
- [ ] Meal planning with AI recommendations
- [ ] Recipe suggestions based on available ingredients
- [ ] Integration with more discount portals
- [ ] Mobile app version
- [ ] Data visualization and reporting
- [ ] Multi-user support

## License

This is a research project. Please add appropriate license information.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.