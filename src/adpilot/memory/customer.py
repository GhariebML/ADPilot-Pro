"""CustomerMemory subsystem: Stores and recalls customer ICPs, personas, and buyer insights."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class CustomerProfile(BaseModel):
    """Structured customer persona profile and ICP definition."""
    customer_id: str
    business_name: str
    target_role: str = Field(..., description="e.g. 'VP Engineering', 'CISO', 'Head of Growth'")
    industry: str
    company_size: str = Field(default="Enterprise (500+)")
    key_pain_points: List[str] = Field(default_factory=list)
    common_objections: List[str] = Field(default_factory=list)
    preferred_channels: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CustomerMemory:
    """Manages persistent recall and indexing of customer personas and target audience insights."""

    def __init__(self, db: Optional[Any] = None) -> None:
        self.db = db
        self._in_memory_store: Dict[str, CustomerProfile] = {}

    async def save_customer_profile(self, profile: CustomerProfile) -> None:
        """Stores or updates a customer profile."""
        self._in_memory_store[profile.customer_id] = profile
        if self.db is not None:
            try:
                await self.db["customer_profiles"].update_one(
                    {"customer_id": profile.customer_id},
                    {"$set": profile.model_dump(mode="json")},
                    upsert=True,
                )
            except Exception as e:
                logger.warning("CustomerMemory | DB save error: %s; in-memory copy preserved", e)

    async def get_customer_profile(self, customer_id: str) -> Optional[CustomerProfile]:
        """Retrieves a customer profile by ID."""
        if customer_id in self._in_memory_store:
            return self._in_memory_store[customer_id]

        if self.db is not None:
            try:
                doc = await self.db["customer_profiles"].find_one({"customer_id": customer_id})
                if doc:
                    doc.pop("_id", None)
                    profile = CustomerProfile.model_validate(doc)
                    self._in_memory_store[customer_id] = profile
                    return profile
            except Exception as e:
                logger.warning("CustomerMemory | DB get error: %s", e)

        return None

    async def query_personas(self, industry: Optional[str] = None, role: Optional[str] = None) -> List[CustomerProfile]:
        """Searches customer personas by industry or target role."""
        matches = []
        for prof in self._in_memory_store.values():
            if industry and prof.industry.lower() != industry.lower():
                continue
            if role and role.lower() not in prof.target_role.lower():
                continue
            matches.append(prof)
        return matches
