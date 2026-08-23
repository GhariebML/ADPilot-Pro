import pytest
from unittest.mock import patch, MagicMock
from adpilot.orchestrator.simulation_runner import SimulationRunner
from adpilot.schemas.simulation_schemas import CampaignSimulation
from adpilot.core.simulation_store import simulation_store

@pytest.fixture
def mock_simulation():
    sim = CampaignSimulation(
        campaign_id="test-camp",
        campaign_input={
            "product_name": "Test",
            "product_type": "SaaS",
            "budget": 10000
        }
    )
    simulation_store.save(sim)
    return sim

@pytest.mark.asyncio
async def test_simulation_runner_initialization(mock_simulation):
    runner = SimulationRunner(mock_simulation.simulation_id)
    assert runner.simulation_id == mock_simulation.simulation_id
