"""Legacy orchestration alias module forwarding to the canonical adpilot.orchestrator."""

from __future__ import annotations

import logging
from ..orchestrator.orchestrator import CampaignOrchestrator
from ..orchestrator.master_orchestrator import MasterOrchestrator
from ..orchestrator.planner import CampaignPlanner

logger = logging.getLogger(__name__)

Orchestrator = CampaignOrchestrator

__all__ = [
    "Orchestrator",
    "CampaignOrchestrator",
    "MasterOrchestrator",
    "CampaignPlanner",
]
