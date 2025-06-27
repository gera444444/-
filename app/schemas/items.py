from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int

    class Config:
        from_attributes = True