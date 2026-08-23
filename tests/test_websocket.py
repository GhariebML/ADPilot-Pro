"""Tests for WebSocket real-time telemetry streaming and debate protocol."""

import pytest
from starlette.testclient import TestClient
from adpilot.api.main import app
from adpilot.core.agent_events import AgentEventType, AgentLifecycleEvent, event_bus
from adpilot.orchestrator.debate import AgentDebateProtocol


def test_websocket_campaign_telemetry_stream():
    """Test connecting to campaign WebSocket and receiving broadcast events."""
    client = TestClient(app)
    campaign_id = "test-ws-campaign-001"

    # Pre-populate history
    event_bus.emit(
        AgentLifecycleEvent(
            event_type=AgentEventType.AGENT_STARTED,
            campaign_id=campaign_id,
            agent_id="strategy_agent",
            status="started",
            latency=0.01,
        )
    )

    with client.websocket_connect(f"/ws/campaigns/{campaign_id}") as websocket:
        # Should receive historical event
        data = websocket.receive_json()
        assert data["campaign_id"] == campaign_id
        assert data["agent_id"] == "strategy_agent"

        # Emit new live event
        event_bus.emit(
            AgentLifecycleEvent(
                event_type=AgentEventType.AGENT_THOUGHT,
                campaign_id=campaign_id,
                agent_id="research_agent",
                status="streaming",
                thought_content="Synthesizing competitor moat vulnerabilities...",
            )
        )

        # Should receive live event
        live_data = websocket.receive_json()
        assert live_data["event_type"] == "agent_thought"
        assert "Synthesizing" in live_data["thought_content"]

        # Test ping/pong
        websocket.send_json({"action": "ping"})
        ack = websocket.receive_json()
        assert ack["type"] == "pong"


@pytest.mark.asyncio
async def test_agent_debate_protocol():
    """Test agent co-reasoning debate protocol execution and consensus formation."""
    protocol = AgentDebateProtocol(max_rounds=2)
    consensus = await protocol.conduct_debate(
        campaign_id="camp-debate-101",
        topic="TOFU vs BOFU Channel Split",
        proposer_agent_id="strategy_agent",
        proposer_proposal="Concentrate 70% budget on LinkedIn Sponsored Content",
        critique_agent_id="competitor_agent",
        critique_concerns=["Competitor is running aggressive Google Search conquesting"],
    )

    assert consensus.consensus_reached is True
    assert consensus.consensus_score >= 0.85
    assert len(consensus.turns) >= 2
    assert "Harmonized Strategic Consensus" in consensus.resolved_action_plan
