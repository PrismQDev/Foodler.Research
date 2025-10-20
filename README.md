# Foodler.Research

An application for calculating balanced food intake from your fridge inventory, kupi.cz food discounts, and nutritional value tables (kaloricke tabulky).

## Overview

Foodler helps you:
- 🥗 Manage your fridge inventory with expiry tracking
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
python main.py fridge add "Chicken breast" 500 g --expiry 2025-10-25 --calories 165 --protein 31 --carbs 0 --fats 3.6
python main.py fridge add "Broccoli" 300 g --expiry 2025-10-22 --calories 34 --protein 2.8 --carbs 7 --fats 0.4
```

List all items:
```bash
python main.py fridge list
```

Check items expiring soon:
```bash
python main.py fridge expiring --days 7
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
- Track expiry dates
- Store nutritional information
- Get alerts for expiring items

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

## Note on Web Scraping

The scraper implementations include placeholder code that needs to be adapted based on the actual HTML structure of the target websites (kupi.cz and kaloricke tabulky). Web scraping should be done responsibly:

- Respect robots.txt
- Implement rate limiting
- Cache results when appropriate
- Handle errors gracefully
- Consider using official APIs when available

## Future Enhancements

- [ ] Web UI using Flask or Django
- [ ] Meal planning with AI recommendations
- [ ] Recipe suggestions based on available ingredients
- [ ] Integration with more discount portals
- [ ] Mobile app version
- [ ] Barcode scanning for easy item entry
- [ ] Data visualization and reporting
- [ ] Multi-user support

## License

This is a research project. Please add appropriate license information.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.