from pydantic import BaseModel, Field
from datetime import datetime


class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int = Field(ge=1)


class CreateOrderRequest(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    menu_id: int
    menu_name: str
    menu_price: int
    quantity: int
    subtotal: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    store_id: int
    table_id: int
    session_id: int
    status: str
    total_amount: int
    created_at: datetime
    items: list[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str


class OrderHistoryResponse(BaseModel):
    id: int
    order_id: int
    store_id: int
    table_id: int
    session_id: int
    status: str
    total_amount: int
    order_created_at: datetime
    completed_at: datetime
    items_json: str

    class Config:
        from_attributes = True
