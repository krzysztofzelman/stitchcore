"""Product endpoints — CRUD for categories, products, variants."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin
from app.models.user import User
from app.schemas import (
    CategoryCreate, CategoryResponse, ProductCreate, ProductUpdate,
    ProductResponse, ProductListItem, VariantCreate, VariantResponse,
    MessageResponse, PaginatedResponse,
)
from app.services import product as product_service

router = APIRouter()


# ── Categories ──────────────────────────────────────────────────────────────

@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await product_service.list_categories(db)


@router.post("/categories", response_model=CategoryResponse, dependencies=[Depends(get_current_admin)])
async def create_category(body: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await product_service.create_category(db, body.model_dump())


# ── Products ────────────────────────────────────────────────────────────────

@router.get("/products", response_model=PaginatedResponse)
async def list_products(
    search: str = Query(""), category_id: int | None = Query(None),
    page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    products, total = await product_service.list_products(db, search, category_id, page, page_size)
    results = []
    for p in products:
        cat_name = p.category.name if p.category else None
        results.append(ProductListItem(
            id=p.id, name=p.name, slug=p.slug, price=float(p.price),
            compare_price=float(p.compare_price) if p.compare_price else None,
            brand=p.brand, category_name=cat_name, has_variants=len(p.variants) > 0,
        ))
    return PaginatedResponse(count=total, results=[r.model_dump() for r in results], page=page, page_size=page_size)


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/products", response_model=ProductResponse, dependencies=[Depends(get_current_admin)])
async def create_product(body: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await product_service.create_product(db, body.model_dump())


@router.put("/products/{product_id}", response_model=ProductResponse, dependencies=[Depends(get_current_admin)])
async def update_product(product_id: int, body: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await product_service.update_product(db, product_id, body.model_dump(exclude_none=True))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/products/{product_id}/variants", response_model=VariantResponse, dependencies=[Depends(get_current_admin)])
async def create_variant(product_id: int, body: VariantCreate, db: AsyncSession = Depends(get_db)):
    return await product_service.create_variant(db, product_id, body.model_dump())
