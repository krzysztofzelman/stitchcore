"""Auth service — registration, login, token management."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token, create_refresh_token, decode_token,
    hash_password, verify_password,
)
from app.models.user import User, RefreshToken


async def register_user(db: AsyncSession, email: str, password: str, first_name: str = "", last_name: str = "") -> User:
    existing = await db.scalar(select(User).where(User.email == email))
    if existing:
        raise ValueError("Email already registered")
    user = User(
        email=email,
        hashed_password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        role="customer",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def create_tokens(db: AsyncSession, user: User) -> dict:
    data = {"sub": str(user.id)}
    access = create_access_token(data)
    refresh = create_refresh_token(data)
    rt = RefreshToken(
        token=refresh,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(rt)
    await db.commit()
    return {"access_token": access, "refresh_token": refresh}


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> dict | None:
    payload = decode_token(refresh_token)
    if not payload:
        return None
    stored = await db.scalar(select(RefreshToken).where(RefreshToken.token == refresh_token))
    if not stored:
        return None
    user_id = payload.get("sub")
    access = create_access_token({"sub": user_id})
    return {"access_token": access, "refresh_token": refresh_token}
