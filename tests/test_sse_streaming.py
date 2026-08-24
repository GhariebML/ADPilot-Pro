import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock
from adpilot.core.agent_events import AgentEventBus, AgentLifecycleEvent, AgentEventType
from adpilot.api.sse_stream import sse_event_generator

@pytest.mark.asyncio
async def test_sse_event_generator_connection_and_events():
    mock_request = MagicMock()
    mock_request.is_disconnected = AsyncMock(side_effect=[False, False, True])

    gen = sse_event_generator("test_stream_camp", mock_request)

    # First event is connection event
    first_chunk = await anext(gen)
    assert "connected" in first_chunk
    assert "test_stream_camp" in first_chunk

    # Emit event on bus
    bus = AgentEventBus()
    test_event = AgentLifecycleEvent(
        event_type=AgentEventType.AGENT_STARTED,
        campaign_id="test_stream_camp",
        agent_id="strategy_agent",
        status="started"
    )
    bus.emit(test_event)

    second_chunk = await anext(gen)
    assert "agent_started" in second_chunk
    assert "strategy_agent" in second_chunk

@pytest.mark.asyncio
async def test_sse_event_generator_bus_queue_registration():
    bus = AgentEventBus()
    queue = asyncio.Queue()
    bus.register_campaign_queue("camp_unit_test", queue)

    event = AgentLifecycleEvent(
        event_type=AgentEventType.AGENT_COMPLETED,
        campaign_id="camp_unit_test",
        agent_id="content_agent",
        status="completed"
    )
    bus.emit(event)

    received = await asyncio.wait_for(queue.get(), timeout=2.0)
    assert received.campaign_id == "camp_unit_test"
    assert received.agent_id == "content_agent"

    bus.unregister_campaign_queue("camp_unit_test", queue)
