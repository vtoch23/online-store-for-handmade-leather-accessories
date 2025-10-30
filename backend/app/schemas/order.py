from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item."""
    pass


class OrderItem(OrderItemBase):
    """Schema for order item response."""
    id: int
    price_at_purchase: float
    product_name: Optional[str] = None
    product_image_url: Optional[str] = None

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base order schema."""
    shipping_address: str = Field(..., min_length=10)


class OrderCreate(OrderBase):
    """Schema for creating an order."""
    items: List[OrderItemCreate]


class Order(OrderBase):
    """Schema for order response."""
    id: int
    user_id: int
    total_amount: float
    status: OrderStatus
    items: List[OrderItem]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
