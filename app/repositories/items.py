from app.db.models import Item
from app.schemas.items import ItemCreate, ItemOut
from .base import BaseRepository

class ItemRepository(BaseRepository[Item, ItemCreate, ItemOut]):
    def get_by_category(self, category: str):
        return self.db.query(Item).filter(Item.category == category).all()