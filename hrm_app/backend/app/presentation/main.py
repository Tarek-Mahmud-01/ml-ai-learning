"""FastAPI app factory — composition + CORS + routers. Thin, no logic."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..infrastructure.config import settings
from ..infrastructure.db.session import init_db
from .routers import admin, chat, employees, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()               # create tables if missing
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="HRM Detective API", version="1.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    def health() -> dict:
        return {"status": "ok"}

    app.include_router(employees.router)
    app.include_router(reports.router)
    app.include_router(admin.router)
    app.include_router(chat.router)
    return app


app = create_app()
