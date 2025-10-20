"""Fridge inventory database management."""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

Base = declarative_base()


class FoodItem(Base):
    """Model for food items in the fridge."""
    
    __tablename__ = 'food_items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    expiry_date = Column(DateTime)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    added_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<FoodItem(name='{self.name}', quantity={self.quantity} {self.unit})>"


class FridgeDatabase:
    """Manages the fridge inventory database."""
    
    def __init__(self, db_path='fridge.db'):
        """Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_item(self, name, quantity, unit, expiry_date=None, 
                 calories=None, protein=None, carbs=None, fats=None):
        """Add a food item to the fridge inventory.
        
        Args:
            name: Name of the food item
            quantity: Quantity of the item
            unit: Unit of measurement (e.g., 'kg', 'pieces', 'l')
            expiry_date: Optional expiry date
            calories: Optional calorie content per unit
            protein: Optional protein content per unit
            carbs: Optional carbohydrate content per unit
            fats: Optional fat content per unit
            
        Returns:
            The created FoodItem object
        """
        item = FoodItem(
            name=name,
            quantity=quantity,
            unit=unit,
            expiry_date=expiry_date,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats
        )
        self.session.add(item)
        self.session.commit()
        return item
    
    def get_all_items(self):
        """Get all items from the fridge inventory.
        
        Returns:
            List of all FoodItem objects
        """
        return self.session.query(FoodItem).all()
    
    def get_item_by_name(self, name):
        """Get food items by name.
        
        Args:
            name: Name of the food item to search for
            
        Returns:
            List of matching FoodItem objects
        """
        return self.session.query(FoodItem).filter(FoodItem.name.like(f'%{name}%')).all()
    
    def update_quantity(self, item_id, new_quantity):
        """Update the quantity of a food item.
        
        Args:
            item_id: ID of the item to update
            new_quantity: New quantity value
            
        Returns:
            The updated FoodItem object or None if not found
        """
        item = self.session.query(FoodItem).filter(FoodItem.id == item_id).first()
        if item:
            item.quantity = new_quantity
            self.session.commit()
        return item
    
    def delete_item(self, item_id):
        """Delete a food item from the inventory.
        
        Args:
            item_id: ID of the item to delete
            
        Returns:
            True if deleted, False if not found
        """
        item = self.session.query(FoodItem).filter(FoodItem.id == item_id).first()
        if item:
            self.session.delete(item)
            self.session.commit()
            return True
        return False
    
    def get_expiring_soon(self, days=7):
        """Get items that will expire soon.
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of FoodItem objects expiring within the specified days
        """
        from datetime import timedelta
        now = datetime.now(timezone.utc)
        future_date = now + timedelta(days=days)
        return self.session.query(FoodItem).filter(
            FoodItem.expiry_date <= future_date,
            FoodItem.expiry_date >= now
        ).all()
    
    def close(self):
        """Close the database session."""
        self.session.close()
