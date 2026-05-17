"""Order endpoints — create, list, get, update status."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin
from app.models.user import User
from app.schemas import OrderCreate, OrderResponse, OrderStatusUpdate, MessageResponse, PaginatedResponse
from app.services import order as order_service

router = APIRouter()


@router.get("/orders", response_model=PaginatedResponse)
async def list_orders(
    page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    uid = None if user.role == "admin" else user.id
    orders, total = await order_service.list_orders(db, uid, page, page_size)
    return PaginatedResponse(
        count=total,
        results=[OrderResponse.model_validate(o).model_dump() for o in orders],
        page=page, page_size=page_size,
    )


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    order = await order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if user.role != "admin" and order.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return order


@router.post("/orders", response_model=OrderResponse)
async def create_order(
    body: OrderCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    order = await order_service.create_order(db, user.id, body.model_dump())
    return order


@router.patch("/orders/{order_id}/status", response_model=OrderResponse, dependencies=[Depends(get_current_admin)])
async def update_order_status(order_id: int, body: OrderStatusUpdate, db: AsyncSession = Depends(get_db)):
    order = await order_service.update_order_status(db, order_id, body.status, body.tracking_number)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
