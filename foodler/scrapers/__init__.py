"""Scrapers module for fetching data from external sources."""

from .kupi_scraper import KupiScraper
from .nutrition_scraper import NutritionScraper

__all__ = ["KupiScraper", "NutritionScraper"]
