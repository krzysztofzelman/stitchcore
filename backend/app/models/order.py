"""Order and order item models."""

from datetime import datetime

from sqlalchemy import DateTime, Enum, Numeric, String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum(
            "pending", "confirmed", "processing", "shipped",
            "delivered", "cancelled", name="order_status"
        ),
        default="pending",
    )
    total: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    shipping_address: Mapped[str] = mapped_column(Text, default="")
    shipping_method: Mapped[str] = mapped_column(String(100), default="pickup")
    tracking_number: Mapped[str] = mapped_column(String(100), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column()
    variant_id: Mapped[int | None] = mapped_column(nullable=True)
    product_name: Mapped[str] = mapped_column(String(255))
    variant_label: Mapped[str] = mapped_column(String(100), default="")
    quantity: Mapped[int] = mapped_column(default=1)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2))

    order = relationship("Order", back_populates="items")
