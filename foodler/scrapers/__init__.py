"""Scrapers module for fetching data from external sources."""

from .kupi_scraper import KupiScraper
from .nutrition_scraper import NutritionScraper
from .openfoodfacts_api import OpenFoodFactsAPI
from .kaloricketabulky_scraper import KalorickeTabulkyScraper

try:
    from .usda_api import USDAFoodDataAPI
    __all__ = [
        "KupiScraper", 
        "NutritionScraper", 
        "OpenFoodFactsAPI", 
        "USDAFoodDataAPI",
        "KalorickeTabulkyScraper"
    ]
except ImportError:
    __all__ = [
        "KupiScraper", 
        "NutritionScraper", 
        "OpenFoodFactsAPI",
        "KalorickeTabulkyScraper"
    ]
