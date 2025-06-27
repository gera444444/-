from fastapi import APIRouter, Depends
from app.schemas.items import ItemCreate, ItemOut
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.repositories.items import ItemRepository
from app.db.models import Item

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemOut)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db)
):
    item_repo = ItemRepository(Item, db)
    return item_repo.create(item)