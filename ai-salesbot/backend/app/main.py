from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import get_settings
from .api.v1.auth import router as auth_router
from .api.v1.bots import router as bots_router
from .api.v1.dialogs import router as dialogs_router
from .api.v1.uploads import router as uploads_router
from .api.v1.analytics import router as analytics_router
from .api.v1.billing import router as billing_router
from .db.init_db import init_db


settings = get_settings()

app = FastAPI(title="AI SalesBot API", version="1.0.0")

origins: List[str] = [o.strip() for o in settings.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static media
media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "media"))
app.mount("/api/media", StaticFiles(directory=media_dir), name="media")

# API routes
api_prefix = "/api/v1"
app.include_router(auth_router, prefix=api_prefix)
app.include_router(bots_router, prefix=api_prefix)
app.include_router(dialogs_router, prefix=api_prefix)
app.include_router(uploads_router, prefix=api_prefix)
app.include_router(analytics_router, prefix=api_prefix)
app.include_router(billing_router, prefix=api_prefix)


@app.on_event("startup")
def _on_startup() -> None:
    # Create tables for MVP; in production rely on Alembic migrations
    init_db()