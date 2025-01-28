from pydantic import BaseModel, Field
from typing import List, Optional

class MenuBase(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None
    price: float = Field(gt=0)

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: int

    class Config:
        orm_mode: True

class OrderItemBase(BaseModel):
    menu_item_id: int
    observation: Optional[str] = None
    quantity: int = Field(gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    menu_item: Menu

    class Config:
        orm_mode: True

class OrderBase(BaseModel):
    status: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    items: List[OrderItem]

    class Config:
        orm_mode: True

class MenuCreateBatch(BaseModel):
    menus: List[MenuCreate]