"""Pydantic schemas — auth, product, order, inventory, common."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, EmailStr

# ─── Auth ───────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str = ""
    last_name: str = ""

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    created_at: datetime | None = None

    class Config:
        from_attributes = True

# ─── Product ────────────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: str = ""
    parent_id: int | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    parent_id: int | None = None
    is_active: bool

    class Config:
        from_attributes = True

class VariantCreate(BaseModel):
    sku: str
    size: str = ""
    color: str = ""
    price_adjustment: float = 0

class VariantResponse(BaseModel):
    id: int
    product_id: int
    sku: str
    size: str
    color: str
    price_adjustment: float
    is_active: bool

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    slug: str
    description: str = ""
    price: float
    compare_price: float | None = None
    category_id: int | None = None
    brand: str = ""

class ProductUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    price: float | None = None
    compare_price: float | None = None
    category_id: int | None = None
    brand: str | None = None
    is_active: bool | None = None

class ImageResponse(BaseModel):
    id: int
    image: str
    alt_text: str
    is_primary: bool

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    price: float
    compare_price: float | None = None
    category_id: int | None = None
    brand: str
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    category: CategoryResponse | None = None
    variants: list[VariantResponse] = []
    images: list[ImageResponse] = []

    class Config:
        from_attributes = True

class ProductListItem(BaseModel):
    id: int
    name: str
    slug: str
    price: float
    compare_price: float | None = None
    brand: str
    category_name: str | None = None
    has_variants: bool = False

    class Config:
        from_attributes = True

# ─── Order ──────────────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    product_id: int
    variant_id: int | None = None
    product_name: str
    variant_label: str = ""
    quantity: int = 1
    unit_price: float

class OrderCreate(BaseModel):
    items: list[OrderItemCreate]
    shipping_address: str = ""
    shipping_method: str = "pickup"
    notes: str = ""

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    variant_id: int | None = None
    product_name: str
    variant_label: str
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int | None = None
    status: str
    total: float
    shipping_address: str
    shipping_method: str
    tracking_number: str
    notes: str
    created_at: datetime | None = None
    items: list[OrderItemResponse] = []

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str
    tracking_number: str | None = None

# ─── Inventory ──────────────────────────────────────────────────────────────

class LocationCreate(BaseModel):
    code: str
    zone: str = ""
    aisle: str = ""
    rack: str = ""
    shelf: str = ""
    description: str = ""

class LocationResponse(BaseModel):
    id: int
    code: str
    zone: str
    aisle: str
    rack: str
    shelf: str
    description: str
    is_active: bool

    class Config:
        from_attributes = True

class StockResponse(BaseModel):
    id: int
    variant_id: int
    location_id: int
    quantity: int
    reserved_quantity: int
    low_stock_threshold: int
    location_code: str | None = None

    class Config:
        from_attributes = True

class StockAdjust(BaseModel):
    variant_id: int
    location_id: int
    quantity: int
    notes: str = ""

class MovementResponse(BaseModel):
    id: int
    variant_id: int
    movement_type: str
    quantity: int
    reference: str
    notes: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True

# ─── Common ─────────────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    message: str

class PaginatedResponse(BaseModel):
    count: int
    results: list[Any]
    page: int = 1
    page_size: int = 25
