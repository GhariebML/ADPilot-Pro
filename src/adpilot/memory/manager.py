"""MemoryManager orchestrating Multi-Tier Global Memory subsystems."""

from __future__ import annotations

import logging
from typing import Any, Optional

try:
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
except ImportError:
    AsyncIOMotorClient = None  # type: ignore
    AsyncIOMotorDatabase = Any  # type: ignore

from ..core.config import get_config
from .agent import AgentMemory
from .brand import BrandMemory
from .campaign import CampaignMemory
from .conversation import ConversationMemory
from .customer import CustomerMemory
from .execution import ExecutionMemory
from .long_term import LongTermMemory
from .short_term import ShortTermMemory

logger = logging.getLogger(__name__)


class MemoryManager:
    """Central orchestration layer for the multi-tiered AdPilot enterprise memory architecture.
    
    Subsystems:
    - Campaign Memory (campaign-level contexts and outputs)
    - Customer Memory (customer ICPs, buyer personas, objections)
    - Brand Memory (brand voice guidelines, visual rules, approved slogans)
    - Conversation Memory (multi-turn dialogues and human review logs)
    - Execution Memory (pipeline execution records, stage latencies, failure logs)
    - Long-Term Memory (cross-campaign learnings and channel priors)
    - Short-Term Memory (session-level scratchpad)
    - Agent Memory (per-agent run tracking)
    """

    def __init__(self, mongodb_url: Optional[str] = None, db_name: str = "adpilot") -> None:
        self.config = get_config()
        self.mongodb_url = mongodb_url or getattr(self.config, "mongodb_url", "mongodb://localhost:27017")
        self.db: Optional[AsyncIOMotorDatabase] = None

        try:
            if self.mongodb_url and self.mongodb_url.startswith("mongodb"):
                self.client = AsyncIOMotorClient(self.mongodb_url, serverSelectionTimeoutMS=1000)
                self.db = self.client[db_name]
        except Exception as e:
            logger.info("MemoryManager | MongoDB client fallback to local in-memory: %s", e)

        # Initialize all 6 memory subsystems + short-term & agent memory
        self.short_term = ShortTermMemory()
        self.campaign = CampaignMemory(self.db)
        self.customer = CustomerMemory(self.db)
        self.brand = BrandMemory(self.db)
        self.conversation = ConversationMemory(self.db)
        self.execution = ExecutionMemory(self.db)
        self.long_term = LongTermMemory(self.db)
        self.agent = AgentMemory(self.db)

        logger.info("MemoryManager | Multi-tier memory architecture initialized successfully.")
