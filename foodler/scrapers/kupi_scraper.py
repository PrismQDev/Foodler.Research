"""Scraper for kupi.cz food discount portal using kupiapi library."""

from typing import List, Dict, Optional
import logging

try:
    from kupiapi import Kupi
    KUPIAPI_AVAILABLE = True
except ImportError:
    KUPIAPI_AVAILABLE = False
    logging.warning(
        "kupiapi library not installed. "
        "Install with: pip install kupiapi"
    )

logger = logging.getLogger(__name__)


class KupiScraper:
    """Scrapes food discounts from kupi.cz using kupiapi library."""
    
    def __init__(self):
        """Initialize the scraper."""
        if not KUPIAPI_AVAILABLE:
            raise ImportError(
                "kupiapi library is required. Install with: pip install kupiapi"
            )
        
        self.kupi = Kupi()
        logger.info("KupiScraper initialized with kupiapi library")
    
    def get_discounts(self, category: Optional[str] = None) -> List[Dict[str, str]]:
        """Fetch current food discounts.
        
        Args:
            category: Optional category filter (e.g., 'potraviny', 'maso')
            
        Returns:
            List of dictionaries containing discount information:
            - name: Product name
            - price: Discounted price
            - original_price: Original price
            - discount: Discount percentage
            - store: Store name
            - valid_until: Validity date
        """
        try:
            if category:
                discounts = self.kupi.get_discounts_by_category(category)
            else:
                # Default to food category
                discounts = self.kupi.get_discounts_by_category('potraviny')
            
            logger.info(f"Fetched {len(discounts)} discounts from kupi.cz")
            return discounts
            
        except Exception as e:
            logger.error(f"Error fetching discounts from kupi.cz: {e}")
            return []
    
    def get_discounts_by_shop(self, shop_name: str) -> List[Dict[str, str]]:
        """Get discounts for a specific shop.
        
        Args:
            shop_name: Shop name (e.g., 'tesco', 'lidl', 'kaufland', 'albert', 'billa')
            
        Returns:
            List of discounts from the specified shop
        """
        try:
            discounts = self.kupi.get_discounts_by_shop(shop_name.lower())
            logger.info(f"Fetched {len(discounts)} discounts from {shop_name}")
            return discounts
            
        except Exception as e:
            logger.error(f"Error fetching discounts from {shop_name}: {e}")
            return []
    
    def search_product(self, product_name: str) -> List[Dict[str, str]]:
        """Search for specific product discounts.
        
        Args:
            product_name: Name of the product to search for
            
        Returns:
            List of matching discounts
        """
        try:
            discounts = self.kupi.search_discounts(product_name)
            logger.info(f"Found {len(discounts)} discounts matching '{product_name}'")
            return discounts
            
        except Exception as e:
            logger.error(f"Error searching for '{product_name}': {e}")
            return []
    
    def get_best_deals(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get the best current deals sorted by discount percentage.
        
        Args:
            limit: Maximum number of deals to return
            
        Returns:
            List of top discounts sorted by discount percentage
        """
        discounts = self.get_discounts()
        
        if not discounts:
            return []
        
        # Sort by discount percentage
        try:
            sorted_discounts = sorted(
                discounts,
                key=lambda x: self._extract_discount_percent(x),
                reverse=True
            )
            result = sorted_discounts[:limit]
            logger.info(f"Returning top {len(result)} deals")
            return result
            
        except Exception as e:
            logger.error(f"Error sorting discounts: {e}")
            return discounts[:limit]
    
    @staticmethod
    def _extract_discount_percent(discount: Dict[str, str]) -> float:
        """Extract discount percentage from discount data.
        
        Args:
            discount: Discount dictionary
            
        Returns:
            Discount percentage as float
        """
        # Try different possible keys for discount percentage
        discount_str = discount.get('discount', discount.get('discount_percent', '0%'))
        
        try:
            # Remove '%' and any other non-numeric characters except '.' and '-'
            cleaned = ''.join(c for c in str(discount_str) if c.isdigit() or c in '.-')
            return float(cleaned) if cleaned else 0.0
        except (ValueError, AttributeError):
            return 0.0
