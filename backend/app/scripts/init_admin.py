"""Auto-create admin user on first startup if no admin exists."""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User

logger = logging.getLogger(__name__)

ADMIN_EMAIL = "admin@stitchcore.pl"
ADMIN_PASSWORD = "admin123"


async def init_admin(db: AsyncSession) -> None:
    """Check if any admin user exists. If not, create one."""

    existing_admin = await db.scalar(
        select(User).where(User.role == "admin")
    )
    if existing_admin:
        logger.info("Admin user already exists (%s), skipping creation.", existing_admin.email)
        return

    admin = User(
        email=ADMIN_EMAIL,
        hashed_password=hash_password(ADMIN_PASSWORD),
        first_name="Admin",
        last_name="StitchCore",
        role="admin",
        is_active=True,
    )
    db.add(admin)
    await db.commit()
    logger.info("Created default admin user: %s / %s", ADMIN_EMAIL, ADMIN_PASSWORD)
