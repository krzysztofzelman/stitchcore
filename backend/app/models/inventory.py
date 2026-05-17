"""Warehouse location, inventory stock, and movement models."""

from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, Numeric, String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class WarehouseLocation(Base):
    __tablename__ = "warehouse_locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    zone: Mapped[str] = mapped_column(String(20), default="")
    aisle: Mapped[str] = mapped_column(String(20), default="")
    rack: Mapped[str] = mapped_column(String(20), default="")
    shelf: Mapped[str] = mapped_column(String(20), default="")
    description: Mapped[str] = mapped_column(String(255), default="")
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    inventory_items = relationship("Inventory", back_populates="location")


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    variant_id: Mapped[int] = mapped_column(index=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("warehouse_locations.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=5)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    location = relationship("WarehouseLocation", back_populates="inventory_items")


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    variant_id: Mapped[int] = mapped_column(index=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("warehouse_locations.id"))
    movement_type: Mapped[str] = mapped_column(
        Enum(
            "inbound", "outbound", "transfer", "adjustment",
            "reservation", "unreservation", name="movement_type"
        )
    )
    quantity: Mapped[int] = mapped_column()
    reference: Mapped[str] = mapped_column(String(100), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
