"""Order service — CRUD and status management."""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem
from app.models.inventory import Inventory, StockMovement


async def _generate_order_number(db: AsyncSession) -> str:
    count = (await db.execute(select(func.count()).select_from(Order))).scalar() or 0
    return f"SC-{count + 10001}"


async def create_order(db: AsyncSession, user_id: int | None, data: dict) -> Order:
    items_data = data.pop("items", [])
    total = sum(item["unit_price"] * item["quantity"] for item in items_data)
    order = Order(
        order_number=await _generate_order_number(db),
        user_id=user_id,
        total=total,
        **data,
    )
    db.add(order)
    await db.flush()
    for item in items_data:
        oi = OrderItem(order_id=order.id, **item)
        db.add(oi)
        # Reserve stock
        variant_id = item.get("variant_id")
        if variant_id:
            stock = await db.scalar(
                select(Inventory).where(Inventory.variant_id == variant_id)
            )
            if stock:
                stock.reserved_quantity = (stock.reserved_quantity or 0) + item["quantity"]
                movement = StockMovement(
                    variant_id=variant_id,
                    location_id=stock.location_id,
                    movement_type="reservation",
                    quantity=item["quantity"],
                    reference=f"order-{order.order_number}",
                )
                db.add(movement)
    await db.commit()
    await db.refresh(order)
    result = await db.execute(
        select(Order).where(Order.id == order.id).options(selectinload(Order.items))
    )
    return result.scalar_one()


async def list_orders(db: AsyncSession, user_id: int | None = None,
                      page: int = 1, page_size: int = 25) -> tuple[list[Order], int]:
    query = select(Order)
    count_q = select(func.count()).select_from(Order)
    if user_id:
        query = query.where(Order.user_id == user_id)
        count_q = count_q.where(Order.user_id == user_id)
    total = (await db.execute(count_q)).scalar() or 0
    query = query.options(selectinload(Order.items))
    query = query.order_by(Order.id.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all(), total


async def get_order_by_id(db: AsyncSession, order_id: int) -> Order | None:
    result = await db.execute(
        select(Order).where(Order.id == order_id).options(selectinload(Order.items))
    )
    return result.scalar_one_or_none()


async def update_order_status(db: AsyncSession, order_id: int, status: str,
                              tracking_number: str | None = None) -> Order | None:
    order = await get_order_by_id(db, order_id)
    if not order:
        return None
    order.status = status
    if tracking_number:
        order.tracking_number = tracking_number
    await db.commit()
    await db.refresh(order)
    return order
