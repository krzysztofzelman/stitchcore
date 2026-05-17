"""Seed the database with sample data — categories, products, variants, locations."""

import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_factory
from app.core.security import hash_password
from app.models.user import User
from app.models.product import Category, Product, ProductVariant
from app.models.inventory import WarehouseLocation, Inventory


logger = logging.getLogger(__name__)


async def seed(db: AsyncSession) -> None:
    """Insert sample data if the products table is empty."""

    existing = await db.scalar(select(Product).limit(1))
    if existing:
        logger.info("Products already exist, skipping seed.")
        return

    # ── Categories ──────────────────────────────────────────────────────
    categories = [
        Category(name="Odzież", slug="odziez", description="Ubrania i akcesoria odzieżowe"),
        Category(name="Obuwie", slug="obuwie", description="Buty i obuwie sportowe"),
        Category(name="Akcesoria", slug="akcesoria", description="Torby, plecaki, czapki i inne"),
    ]
    db.add_all(categories)
    await db.flush()
    cat_map = {c.name: c.id for c in categories}

    # ── Products ────────────────────────────────────────────────────────
    products_data = [
        {
            "name": "T-Shirt Basic",
            "slug": "t-shirt-basic",
            "description": "Klasyczny bawełniany T-shirt. Idealny na co dzień. Dostępny w kilku kolorach.",
            "price": 79.99,
            "compare_price": 99.99,
            "category_id": cat_map["Odzież"],
            "brand": "StitchCore",
        },
        {
            "name": "Jeansy Slim Fit",
            "slug": "jeansy-slim-fit",
            "description": "Nowoczesne jeansy o dopasowanym kroju. Wykonane z elastycznego denimu.",
            "price": 199.99,
            "compare_price": None,
            "category_id": cat_map["Odzież"],
            "brand": "StitchCore",
        },
        {
            "name": "Buty Sportowe Air",
            "slug": "buty-sportowe-air",
            "description": "Lekkie buty sportowe z amortyzacją powietrzną. Idealne do biegania i codziennego użytku.",
            "price": 349.99,
            "compare_price": 429.99,
            "category_id": cat_map["Obuwie"],
            "brand": "StitchCore",
        },
        {
            "name": "Plecak Miejski",
            "slug": "plecak-miejski",
            "description": "Pojemny plecak miejski z kieszenią na laptopa. Wodoodporny materiał.",
            "price": 159.99,
            "compare_price": None,
            "category_id": cat_map["Akcesoria"],
            "brand": "StitchCore",
        },
        {
            "name": "Czapka Beanie",
            "slug": "czapka-beanie",
            "description": "Ciepła czapka zimowa z miękkiej dzianiny. Uniwersalny fason.",
            "price": 49.99,
            "compare_price": 59.99,
            "category_id": cat_map["Akcesoria"],
            "brand": "StitchCore",
        },
    ]
    products = [Product(**p) for p in products_data]
    db.add_all(products)
    await db.flush()

    # ── Variants ────────────────────────────────────────────────────────
    for product in products:
        variants = []
        if product.slug == "t-shirt-basic":
            for size in ["S", "M", "L", "XL"]:
                for color in ["Czarny", "Biały"]:
                    variants.append(ProductVariant(
                        product_id=product.id,
                        sku=f"TSH-{size[:1]}-{color[:3].upper()}",
                        size=size,
                        color=color,
                    ))
        elif product.slug == "jeansy-slim-fit":
            for size in ["30", "32", "34", "36"]:
                for color in ["Ciemny", "Jasny"]:
                    variants.append(ProductVariant(
                        product_id=product.id,
                        sku=f"JNS-{size}-{color[:3].upper()}",
                        size=size,
                        color=color,
                    ))
        elif product.slug == "buty-sportowe-air":
            for size in ["40", "42", "44", "46"]:
                variants.append(ProductVariant(
                    product_id=product.id,
                    sku=f"BUT-{size}",
                    size=size,
                    color="Czarny",
                ))
        elif product.slug == "plecak-miejski":
            for color in ["Czarny", "Granatowy", "Szary"]:
                variants.append(ProductVariant(
                    product_id=product.id,
                    sku=f"PLK-{color[:3].upper()}",
                    size="One Size",
                    color=color,
                ))
        elif product.slug == "czapka-beanie":
            for color in ["Czarny", "Szary", "Bordowy"]:
                variants.append(ProductVariant(
                    product_id=product.id,
                    sku=f"CAP-{color[:3].upper()}",
                    size="One Size",
                    color=color,
                ))
        db.add_all(variants)
    await db.flush()

    # ── Warehouse locations ─────────────────────────────────────────────
    locations = [
        WarehouseLocation(code="A-01-01", zone="A", aisle="1", rack="1", shelf="1", description="Główna lokalizacja"),
        WarehouseLocation(code="A-01-02", zone="A", aisle="1", rack="1", shelf="2", description="Zapas"),
    ]
    db.add_all(locations)
    await db.flush()

    # ── Initial stock ───────────────────────────────────────────────────
    variants = (await db.execute(select(ProductVariant))).scalars().all()
    for variant in variants:
        db.add(Inventory(
            variant_id=variant.id,
            location_id=locations[0].id,
            quantity=50,
            low_stock_threshold=5,
        ))

    await db.commit()
    count = len(products)
    logger.info("Seeded %d products with variants and stock.", count)
    print(f"✓ Dodano {count} produktów z wariantami i stanami magazynowymi.")


async def main():
    logging.basicConfig(level=logging.INFO)
    async with async_session_factory() as session:
        await seed(session)


if __name__ == "__main__":
    asyncio.run(main())
