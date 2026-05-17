"""Aggregate all v1 API routers under /api/v1."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.products import router as products_router
from app.api.v1.orders import router as orders_router
from app.api.v1.inventory import router as inventory_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(products_router, prefix="", tags=["products"])
api_router.include_router(orders_router, prefix="", tags=["orders"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
