"""API v1 master router aggregating all versioned endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from .routes.health import router as health_router

v1_router = APIRouter()

# Mount health & diagnostics routes under /api/v1
v1_router.include_router(health_router)
from ...api.v1.simulations import router as sim_router
v1_router.include_router(sim_router, prefix='/simulations', tags=['Simulation'])


__all__ = ["v1_router"]

