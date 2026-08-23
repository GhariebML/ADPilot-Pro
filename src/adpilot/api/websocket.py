"""WebSocket endpoints and connection manager for real-time campaign telemetry and streaming."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel

from ..core.agent_events import AgentLifecycleEvent, event_bus

logger = logging.getLogger(__name__)

ws_router = APIRouter(tags=["WebSocket Telemetry"])


class ConnectionManager:
    """Manages active WebSocket client connections and broadcasts real-time event streams."""

    def __init__(self) -> None:
        # campaign_id -> set of active WebSockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, campaign_id: str) -> None:
        """Accept new WebSocket connection and subscribe to campaign event queue."""
        await websocket.accept()
        if campaign_id not in self.active_connections:
            self.active_connections[campaign_id] = set()
        self.active_connections[campaign_id].add(websocket)
        logger.info("WebSocket client connected to campaign: %s (Total: %d)", campaign_id, len(self.active_connections[campaign_id]))

    def disconnect(self, websocket: WebSocket, campaign_id: str) -> None:
        """Remove disconnected WebSocket from active pool."""
        if campaign_id in self.active_connections:
            self.active_connections[campaign_id].discard(websocket)
            if not self.active_connections[campaign_id]:
                del self.active_connections[campaign_id]
        logger.info("WebSocket client disconnected from campaign: %s", campaign_id)

    async def send_event(self, websocket: WebSocket, event: AgentLifecycleEvent) -> None:
        """Send a single serialized event to a WebSocket client."""
        try:
            await websocket.send_text(event.model_dump_json())
        except Exception as exc:
            logger.warning("Error sending WebSocket message: %s", exc)

    async def broadcast_to_campaign(self, campaign_id: str, message: dict) -> None:
        """Broadcast arbitrary JSON message to all clients of a campaign."""
        if campaign_id in self.active_connections:
            dead_sockets = set()
            payload = json.dumps(message)
            for ws in self.active_connections[campaign_id]:
                try:
                    await ws.send_text(payload)
                except Exception:
                    dead_sockets.add(ws)
            for dead_ws in dead_sockets:
                self.disconnect(dead_ws, campaign_id)


manager = ConnectionManager()


@ws_router.websocket("/ws/campaigns/{campaign_id}")
async def campaign_telemetry_stream(websocket: WebSocket, campaign_id: str) -> None:
    """Bi-directional real-time telemetry stream for a specific campaign.
    
    Streams:
    - Agent start/finish events
    - Real-time token streaming and thought traces
    - Stage transitions
    - Adversarial debate arguments
    - Anomaly detections
    """
    await manager.connect(websocket, campaign_id)
    queue: asyncio.Queue[AgentLifecycleEvent] = asyncio.Queue(maxsize=500)
    event_bus.register_campaign_queue(campaign_id, queue)
    
    # Send historical events for this campaign immediately upon connect
    history = event_bus.get_events(campaign_id=campaign_id)
    for past_event in history[-50:]:  # last 50 events
        await manager.send_event(websocket, past_event)

    async def event_sender() -> None:
        """Forward events from queue to WebSocket."""
        try:
            while True:
                event = await queue.get()
                await manager.send_event(websocket, event)
                queue.task_done()
        except asyncio.CancelledError:
            pass

    sender_task = asyncio.create_task(event_sender())

    try:
        while True:
            # Listen for client-side control commands (e.g. pause, inject prompt, ping)
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                action = msg.get("action")
                if action == "ping":
                    await websocket.send_text(json.dumps({"type": "pong", "timestamp": str(asyncio.get_event_loop().time())}))
                elif action == "interrupt":
                    logger.warning("Client requested pipeline interrupt for campaign %s", campaign_id)
                    await websocket.send_text(json.dumps({"type": "interrupt_ack", "campaign_id": campaign_id}))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket, campaign_id)
    except Exception as exc:
        logger.warning("WebSocket unexpected error on %s: %s", campaign_id, exc)
        manager.disconnect(websocket, campaign_id)
    finally:
        sender_task.cancel()
        event_bus.unregister_campaign_queue(campaign_id, queue)


@ws_router.websocket("/ws/system/telemetry")
async def system_global_telemetry(websocket: WebSocket) -> None:
    """Global system-wide WebSocket stream for real-time observability across all campaigns."""
    campaign_id = "*"
    await manager.connect(websocket, campaign_id)
    queue: asyncio.Queue[AgentLifecycleEvent] = asyncio.Queue(maxsize=1000)
    event_bus.register_campaign_queue(campaign_id, queue)

    async def event_sender() -> None:
        try:
            while True:
                event = await queue.get()
                await manager.send_event(websocket, event)
                queue.task_done()
        except asyncio.CancelledError:
            pass

    sender_task = asyncio.create_task(event_sender())

    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, campaign_id)
    finally:
        sender_task.cancel()
        event_bus.unregister_campaign_queue(campaign_id, queue)
