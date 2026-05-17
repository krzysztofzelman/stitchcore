"""Inventory service — locations, stock levels, movements."""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.inventory import WarehouseLocation, Inventory, StockMovement


async def list_locations(db: AsyncSession) -> list[WarehouseLocation]:
    result = await db.execute(select(WarehouseLocation).where(WarehouseLocation.is_active).order_by(WarehouseLocation.code))
    return result.scalars().all()


async def create_location(db: AsyncSession, data: dict) -> WarehouseLocation:
    loc = WarehouseLocation(**data)
    db.add(loc)
    await db.commit()
    await db.refresh(loc)
    return loc


async def get_stock(db: AsyncSession, variant_id: int | None = None,
                    low_stock: bool = False) -> list[Inventory]:
    query = select(Inventory).options(selectinload(Inventory.location))
    if variant_id:
        query = query.where(Inventory.variant_id == variant_id)
    if low_stock:
        query = query.where(Inventory.quantity <= Inventory.low_stock_threshold)
    query = query.order_by(Inventory.variant_id)
    result = await db.execute(query)
    return result.scalars().all()


async def adjust_stock(db: AsyncSession, variant_id: int, location_id: int,
                        quantity: int, notes: str = "") -> Inventory:
    inv = await db.scalar(
        select(Inventory)
        .options(selectinload(Inventory.location))
        .where(
            Inventory.variant_id == variant_id,
            Inventory.location_id == location_id,
        )
    )
    if inv:
        inv.quantity += quantity
    else:
        inv = Inventory(variant_id=variant_id, location_id=location_id, quantity=quantity)
        db.add(inv)
    movement = StockMovement(
        variant_id=variant_id,
        location_id=location_id,
        movement_type="inbound" if quantity > 0 else "outbound",
        quantity=abs(quantity),
        notes=notes,
    )
    db.add(movement)
    await db.commit()
    # Re-query with eager load since refresh() would strip the relationship
    inv = await db.scalar(
        select(Inventory)
        .options(selectinload(Inventory.location))
        .where(Inventory.id == inv.id)
    )
    return inv


async def list_movements(db: AsyncSession, variant_id: int | None = None,
                          page: int = 1, page_size: int = 25) -> tuple[list[StockMovement], int]:
    query = select(StockMovement)
    count_q = select(func.count()).select_from(StockMovement)
    if variant_id:
        query = query.where(StockMovement.variant_id == variant_id)
        count_q = count_q.where(StockMovement.variant_id == variant_id)
    total = (await db.execute(count_q)).scalar() or 0
    query = query.order_by(StockMovement.id.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all(), total
