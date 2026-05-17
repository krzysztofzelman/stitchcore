"""FastAPI application entry point."""

import asyncio
import logging
import subprocess
import sys

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, async_session_factory
from app.api.v1.router import api_router

logger = logging.getLogger(__name__)


async def run_alembic_migration():
    """Run Alembic migrations via subprocess on startup."""
    result = await asyncio.to_thread(
        subprocess.run,
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True, text=True, cwd=".",
    )
    if result.returncode != 0:
        logger.error("Alembic migration failed:\n%s", result.stderr)
        raise RuntimeError(f"Alembic migration failed (exit {result.returncode})")
    logger.info("Alembic migrations applied successfully.")


async def init_admin_user():
    """Create default admin user if none exists."""
    from app.scripts.init_admin import init_admin
    async with async_session_factory() as session:
        await init_admin(session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting StitchCore API...")
    await run_alembic_migration()
    await init_admin_user()
    yield
    await engine.dispose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "StitchCore API", "version": "1.0.0"}
