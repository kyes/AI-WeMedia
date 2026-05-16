"""FastAPI application factory and entry point."""
from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, make_asgi_app

from app.api.v1.router import router as api_v1_router
from app.config import get_settings
from app.core.exceptions import register_exception_handlers

settings = get_settings()
logger = structlog.get_logger()

# ─── Metrics ─────────────────────────────────────────────────────────────────

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP request count",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
)


# ─── Application lifespan ────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting AI WeMedia backend", version=settings.app_version, env=settings.app_env)
    yield
    logger.info("Shutting down AI WeMedia backend")


# ─── App factory ─────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "AI智能自媒体运营平台 REST API\n\n"
            "涵盖智能选题、多模态内容生成、用户画像、数据分析、跨平台分发与商业变现五大核心模块。"
        ),
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── CORS ─────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app_allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Request logging & metrics middleware ─────────────────────────────
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        start = time.monotonic()
        response = await call_next(request)
        latency = time.monotonic() - start
        endpoint = request.url.path
        REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
        REQUEST_LATENCY.labels(request.method, endpoint).observe(latency)
        logger.debug(
            "request",
            method=request.method,
            path=endpoint,
            status=response.status_code,
            latency_ms=round(latency * 1000, 2),
        )
        return response

    # ── Exception handlers ───────────────────────────────────────────────
    register_exception_handlers(app)

    # ── Routers ──────────────────────────────────────────────────────────
    app.include_router(api_v1_router)

    # ── Prometheus metrics endpoint ──────────────────────────────────────
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    # ── Health check ─────────────────────────────────────────────────────
    @app.get("/health", tags=["系统 System"], include_in_schema=False)
    async def health():
        return {"status": "ok", "version": settings.app_version}

    return app


app = create_app()
