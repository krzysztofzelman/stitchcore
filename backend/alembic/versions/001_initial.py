"""Initial migration — create all tables.

Revision ID: 001
Revises:
Create Date: 2025-01-01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(255), unique=True, index=True),
        sa.Column("hashed_password", sa.String(255)),
        sa.Column("first_name", sa.String(100), server_default=""),
        sa.Column("last_name", sa.String(100), server_default=""),
        sa.Column("phone", sa.String(20), server_default=""),
        sa.Column("role", sa.Enum("admin", "customer", name="user_role"), server_default="customer"),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("token", sa.String(500), unique=True, index=True),
        sa.Column("user_id", sa.Integer()),
        sa.Column("expires_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), unique=True),
        sa.Column("slug", sa.String(120), unique=True, index=True),
        sa.Column("description", sa.Text(), server_default=""),
        sa.Column("image", sa.String(500), server_default=""),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("categories.id"), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255)),
        sa.Column("slug", sa.String(280), unique=True, index=True),
        sa.Column("description", sa.Text(), server_default=""),
        sa.Column("price", sa.Numeric(12, 2)),
        sa.Column("compare_price", sa.Numeric(12, 2), nullable=True),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id"), nullable=True),
        sa.Column("brand", sa.String(100), server_default=""),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "product_variants",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id")),
        sa.Column("sku", sa.String(100), unique=True, index=True),
        sa.Column("size", sa.String(20), server_default=""),
        sa.Column("color", sa.String(50), server_default=""),
        sa.Column("price_adjustment", sa.Numeric(12, 2), server_default="0"),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "product_images",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id")),
        sa.Column("image", sa.String(500)),
        sa.Column("alt_text", sa.String(255), server_default=""),
        sa.Column("is_primary", sa.Boolean(), server_default="0"),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("order_number", sa.String(20), unique=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("status", sa.Enum("pending", "confirmed", "processing", "shipped", "delivered", "cancelled", name="order_status"), server_default="pending"),
        sa.Column("total", sa.Numeric(12, 2), server_default="0"),
        sa.Column("shipping_address", sa.Text(), server_default=""),
        sa.Column("shipping_method", sa.String(100), server_default="pickup"),
        sa.Column("tracking_number", sa.String(100), server_default=""),
        sa.Column("notes", sa.Text(), server_default=""),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id")),
        sa.Column("product_id", sa.Integer()),
        sa.Column("variant_id", sa.Integer(), nullable=True),
        sa.Column("product_name", sa.String(255)),
        sa.Column("variant_label", sa.String(100), server_default=""),
        sa.Column("quantity", sa.Integer(), server_default="1"),
        sa.Column("unit_price", sa.Numeric(12, 2)),
    )
    op.create_table(
        "warehouse_locations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(50), unique=True, index=True),
        sa.Column("zone", sa.String(20), server_default=""),
        sa.Column("aisle", sa.String(20), server_default=""),
        sa.Column("rack", sa.String(20), server_default=""),
        sa.Column("shelf", sa.String(20), server_default=""),
        sa.Column("description", sa.String(255), server_default=""),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "inventory",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("variant_id", sa.Integer(), index=True),
        sa.Column("location_id", sa.Integer(), sa.ForeignKey("warehouse_locations.id")),
        sa.Column("quantity", sa.Integer(), server_default="0"),
        sa.Column("reserved_quantity", sa.Integer(), server_default="0"),
        sa.Column("low_stock_threshold", sa.Integer(), server_default="5"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "stock_movements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("variant_id", sa.Integer(), index=True),
        sa.Column("location_id", sa.Integer(), sa.ForeignKey("warehouse_locations.id")),
        sa.Column("movement_type", sa.Enum("inbound", "outbound", "transfer", "adjustment", "reservation", "unreservation", name="movement_type")),
        sa.Column("quantity", sa.Integer()),
        sa.Column("reference", sa.String(100), server_default=""),
        sa.Column("notes", sa.Text(), server_default=""),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("stock_movements")
    op.drop_table("inventory")
    op.drop_table("warehouse_locations")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("product_images")
    op.drop_table("product_variants")
    op.drop_table("products")
    op.drop_table("categories")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS user_role")
    op.execute("DROP TYPE IF EXISTS order_status")
    op.execute("DROP TYPE IF EXISTS movement_type")
