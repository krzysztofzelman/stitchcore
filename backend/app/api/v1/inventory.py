"""Inventory endpoints — locations, stock, adjustments, movements."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.schemas import (
    LocationCreate, LocationResponse, StockResponse, StockAdjust,
    MovementResponse, MessageResponse, PaginatedResponse,
)
from app.services import inventory as inventory_service

router = APIRouter(dependencies=[Depends(get_current_admin)])


@router.get("/locations", response_model=list[LocationResponse])
async def list_locations(db: AsyncSession = Depends(get_db)):
    return await inventory_service.list_locations(db)


@router.post("/locations", response_model=LocationResponse)
async def create_location(body: LocationCreate, db: AsyncSession = Depends(get_db)):
    return await inventory_service.create_location(db, body.model_dump())


@router.get("/stock", response_model=list[StockResponse])
async def get_stock(
    variant_id: int | None = Query(None),
    low_stock: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    items = await inventory_service.get_stock(db, variant_id, low_stock)
    results = []
    for item in items:
        loc_code = item.location.code if item.location else None
        results.append(StockResponse(
            id=item.id, variant_id=item.variant_id, location_id=item.location_id,
            quantity=item.quantity, reserved_quantity=item.reserved_quantity,
            low_stock_threshold=item.low_stock_threshold, location_code=loc_code,
        ))
    return results


@router.post("/stock/adjust", response_model=StockResponse)
async def adjust_stock(body: StockAdjust, db: AsyncSession = Depends(get_db)):
    inv = await inventory_service.adjust_stock(db, body.variant_id, body.location_id, body.quantity, body.notes)
    loc_code = inv.location.code if inv.location else None
    return StockResponse(
        id=inv.id, variant_id=inv.variant_id, location_id=inv.location_id,
        quantity=inv.quantity, reserved_quantity=inv.reserved_quantity,
        low_stock_threshold=inv.low_stock_threshold, location_code=loc_code,
    )


@router.get("/movements", response_model=PaginatedResponse)
async def list_movements(
    variant_id: int | None = Query(None),
    page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    movements, total = await inventory_service.list_movements(db, variant_id, page, page_size)
    return PaginatedResponse(
        count=total,
        results=[MovementResponse.model_validate(m).model_dump() for m in movements],
        page=page, page_size=page_size,
    )
