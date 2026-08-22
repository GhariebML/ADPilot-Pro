"""Structured execution events for ADPilot Agent lifecycle tracking."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AgentEventType(str, Enum):
    """Lifecycle event types emitted by all agents during execution."""

    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"


class AgentLifecycleEvent(BaseModel):
    """Structured telemetry event payload for agent execution traceability."""

    event_type: AgentEventType = Field(..., description="Type of event ('agent_started', 'agent_completed', 'agent_failed')")
    campaign_id: str = Field(..., description="ID of the campaign context being processed")
    agent_id: str = Field(..., description="Canonical agent ID (e.g. 'strategy_agent')")
    input_reference: Optional[str] = Field(default=None, description="Summary or hash of input data")
    output_reference: Optional[str] = Field(default=None, description="Summary or hash of produced output")
    model: str = Field(default="default", description="Model used for this execution")
    latency: float = Field(default=0.0, ge=0.0, description="Execution duration in seconds")
    status: str = Field(..., description="Status ('started', 'completed', 'failed')")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Confidence score if available")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="ISO UTC timestamp")
    error_message: Optional[str] = Field(default=None, description="Error details if execution failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional structured execution telemetry")


EventListener = Callable[[AgentLifecycleEvent], None]


class AgentEventBus:
    """Singleton event bus for emitting and subscribing to agent execution events."""

    _instance: Optional[AgentEventBus] = None

    def __new__(cls) -> AgentEventBus:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._listeners: List[EventListener] = []
            cls._instance._events_history: List[AgentLifecycleEvent] = []
        return cls._instance

    def subscribe(self, listener: EventListener) -> None:
        """Register a subscriber to receive all emitted agent events."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: EventListener) -> None:
        """Unregister a subscriber."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def emit(self, event: AgentLifecycleEvent) -> None:
        """Emit an event to all subscribers and append to event history."""
        self._events_history.append(event)
        logger.info(
            "AgentEventBus | %s | agent=%s, campaign=%s, status=%s, latency=%.3fs",
            event.event_type.value,
            event.agent_id,
            event.campaign_id,
            event.status,
            event.latency,
        )
        for listener in self._listeners:
            try:
                listener(event)
            except Exception as exc:
                logger.warning("AgentEventBus | Listener exception: %s", exc)

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
        """Clear all event history."""
        self._events_history.clear()


# Global default instance
event_bus = AgentEventBus()
