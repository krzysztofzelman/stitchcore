"""Product service — CRUD for categories, products, and variants."""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Category, Product, ProductVariant, ProductImage


async def list_categories(db: AsyncSession) -> list[Category]:
    result = await db.execute(select(Category).where(Category.is_active).order_by(Category.name))
    return result.scalars().all()


async def create_category(db: AsyncSession, data: dict) -> Category:
    cat = Category(**data)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def list_products(db: AsyncSession, search: str = "", category_id: int | None = None,
                        page: int = 1, page_size: int = 25) -> tuple[list[Product], int]:
    query = select(Product).where(Product.is_active)
    count_q = select(func.count()).select_from(Product).where(Product.is_active)
    if search:
        like = f"%{search}%"
        query = query.where(Product.name.ilike(like))
        count_q = count_q.where(Product.name.ilike(like))
    if category_id:
        query = query.where(Product.category_id == category_id)
        count_q = count_q.where(Product.category_id == category_id)
    total = (await db.execute(count_q)).scalar() or 0
    query = query.options(selectinload(Product.category), selectinload(Product.variants))
    query = query.order_by(Product.id.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all(), total


async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.category), selectinload(Product.variants), selectinload(Product.images))
    )
    return result.scalar_one_or_none()


async def create_product(db: AsyncSession, data: dict) -> Product:
    product = Product(**data)
    db.add(product)
    await db.commit()
    # Re-fetch with eager loads to avoid async lazy-load errors
    result = await db.execute(
        select(Product)
        .where(Product.id == product.id)
        .options(selectinload(Product.category), selectinload(Product.variants), selectinload(Product.images))
    )
    return result.scalar_one()


async def update_product(db: AsyncSession, product_id: int, data: dict) -> Product | None:
    product = await get_product_by_id(db, product_id)
    if not product:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(product, key, value)
    await db.commit()
    # Re-fetch with eager loads
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.category), selectinload(Product.variants), selectinload(Product.images))
    )
    return result.scalar_one()


async def create_variant(db: AsyncSession, product_id: int, data: dict) -> ProductVariant:
    variant = ProductVariant(product_id=product_id, **data)
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    return variant
