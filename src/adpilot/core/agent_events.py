"""Structured execution events for ADPilot Agent lifecycle and real-time streaming tracking."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AgentEventType(str, Enum):
    """Lifecycle and streaming event types emitted during execution."""

    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    AGENT_THOUGHT = "agent_thought"
    AGENT_TOKEN = "agent_token"
    AGENT_DEBATE = "agent_debate"
    PIPELINE_STAGE_UPDATE = "pipeline_stage_update"
    ANOMALY_ALERT = "anomaly_alert"
    HITL_PENDING = "hitl_pending"


class AgentLifecycleEvent(BaseModel):
    """Structured telemetry event payload for agent execution traceability."""

    event_type: AgentEventType = Field(..., description="Type of event")
    campaign_id: str = Field(..., description="ID of the campaign context being processed")
    agent_id: str = Field(..., description="Canonical agent ID (e.g. 'strategy_agent')")
    input_reference: Optional[str] = Field(default=None, description="Summary or hash of input data")
    output_reference: Optional[str] = Field(default=None, description="Summary or hash of produced output")
    model: str = Field(default="default", description="Model used for this execution")
    latency: float = Field(default=0.0, ge=0.0, description="Execution duration in seconds")
    status: str = Field(..., description="Status ('started', 'completed', 'failed', 'streaming', 'debating')")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Confidence score if available")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="ISO UTC timestamp")
    error_message: Optional[str] = Field(default=None, description="Error details if execution failed")
    thought_content: Optional[str] = Field(default=None, description="Intermediate thought chain or token stream")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional structured execution telemetry")


EventListener = Callable[[AgentLifecycleEvent], None]
AsyncEventListener = Callable[[AgentLifecycleEvent], Any]


class AgentEventBus:
    """Singleton event bus for emitting and subscribing to agent execution and streaming events."""

    _instance: Optional[AgentEventBus] = None

    def __new__(cls) -> AgentEventBus:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._listeners: List[EventListener] = []
            cls._instance._async_listeners: List[AsyncEventListener] = []
            cls._instance._events_history: List[AgentLifecycleEvent] = []
            cls._instance._campaign_queues: Dict[str, Set[asyncio.Queue]] = {}
        return cls._instance

    def subscribe(self, listener: EventListener) -> None:
        """Register a synchronous subscriber."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: EventListener) -> None:
        """Unregister a synchronous subscriber."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def subscribe_async(self, listener: AsyncEventListener) -> None:
        """Register an asynchronous subscriber."""
        if listener not in self._async_listeners:
            self._async_listeners.append(listener)

    def unsubscribe_async(self, listener: AsyncEventListener) -> None:
        """Unregister an asynchronous subscriber."""
        if listener in self._async_listeners:
            self._async_listeners.remove(listener)

    def register_campaign_queue(self, campaign_id: str, queue: asyncio.Queue) -> None:
        """Register an asyncio queue to receive real-time events for a specific campaign."""
        if campaign_id not in self._campaign_queues:
            self._campaign_queues[campaign_id] = set()
        self._campaign_queues[campaign_id].add(queue)

    def unregister_campaign_queue(self, campaign_id: str, queue: asyncio.Queue) -> None:
        """Unregister an asyncio queue."""
        if campaign_id in self._campaign_queues:
            self._campaign_queues[campaign_id].discard(queue)
            if not self._campaign_queues[campaign_id]:
                del self._campaign_queues[campaign_id]

    def emit(self, event: AgentLifecycleEvent) -> None:
        """Emit an event to all subscribers and queues."""
        self._events_history.append(event)
        
        # Log high-level events
        if event.event_type not in (AgentEventType.AGENT_TOKEN, AgentEventType.AGENT_THOUGHT):
            logger.info(
                "AgentEventBus | %s | agent=%s, campaign=%s, status=%s, latency=%.3fs",
                event.event_type.value,
                event.agent_id,
                event.campaign_id,
                event.status,
                event.latency,
            )

        # Dispatch to synchronous listeners
        for listener in list(self._listeners):
            try:
                listener(event)
            except Exception as exc:
                logger.warning("AgentEventBus | Listener exception: %s", exc)

        # Dispatch to campaign-specific async queues (for WebSockets)
        if event.campaign_id in self._campaign_queues:
            for q in list(self._campaign_queues[event.campaign_id]):
                try:
                    q.put_nowait(event)
                except asyncio.QueueFull:
                    logger.warning("AgentEventBus | Queue full for campaign %s", event.campaign_id)
                except Exception as exc:
                    logger.warning("AgentEventBus | Async queue push error: %s", exc)

        # Broadcast to global queues if campaign_id is '*'
        if "*" in self._campaign_queues:
            for q in list(self._campaign_queues["*"]):
                try:
                    q.put_nowait(event)
                except Exception:
                    pass

    async def emit_async(self, event: AgentLifecycleEvent) -> None:
        """Asynchronously emit an event."""
        self.emit(event)
        for async_listener in list(self._async_listeners):
            try:
                res = async_listener(event)
                if asyncio.iscoroutine(res):
                    await res
            except Exception as exc:
                logger.warning("AgentEventBus | Async listener exception: %s", exc)

    def get_events(
        self, campaign_id: Optional[str] = None, agent_id: Optional[str] = None
    ) -> List[AgentLifecycleEvent]:
        """Retrieve historical events filtered by campaign or agent."""
        events = self._events_history
        if campaign_id:
            events = [e for e in events if e.campaign_id == campaign_id]
        if agent_id:
            events = [e for e in events if e.agent_id == agent_id]
        return list(events)

    def clear(self) -> None:
        """Clear all event history and active queues."""
        self._events_history.clear()
        self._campaign_queues.clear()


# Global default instance
event_bus = AgentEventBus()
