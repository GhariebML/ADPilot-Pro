"""Server-Sent Events (SSE) streaming router for real-time campaign token and stage tracking."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from ..core.agent_events import AgentEventBus, AgentLifecycleEvent

logger = logging.getLogger(__name__)

sse_router = APIRouter(prefix="/api/campaigns", tags=["Streaming"])


async def sse_event_generator(campaign_id: str, request: Request) -> AsyncGenerator[str, None]:
    """Generate Server-Sent Events for a specific campaign as agents execute."""
    queue: asyncio.Queue[AgentLifecycleEvent] = asyncio.Queue(maxsize=100)
    bus = AgentEventBus()

    bus.register_campaign_queue(campaign_id, queue)

    # Initial connection confirmation event
    yield f"data: {json.dumps({'event_type': 'connected', 'campaign_id': campaign_id, 'message': 'SSE streaming channel established'})}\n\n"

    try:
        while True:
            if await request.is_disconnected():
                logger.info("SSE client disconnected for campaign %s", campaign_id)
                break

            try:
                # Wait for next event with a 15s keepalive ping timeout
                event = await asyncio.wait_for(queue.get(), timeout=15.0)
                payload = event.model_dump() if hasattr(event, "model_dump") else event.dict()
                yield f"data: {json.dumps(payload)}\n\n"
            except asyncio.TimeoutError:
                # Send heartbeat keepalive ping comment
                yield ": keepalive ping\n\n"
    except asyncio.CancelledError:
        pass
    finally:
        bus.unregister_campaign_queue(campaign_id, queue)


@sse_router.get("/{campaign_id}/stream")
async def stream_campaign_events(campaign_id: str, request: Request):
    """Subscribe to live token-by-token and lifecycle SSE events for a campaign."""
    if not campaign_id or len(campaign_id.strip()) == 0:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")

    return StreamingResponse(
        sse_event_generator(campaign_id, request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
