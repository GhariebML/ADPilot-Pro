"""BrandMemory subsystem: Stores and recalls persistent brand voice, visual identity, and messaging rules."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class BrandProfile(BaseModel):
    """Authoritative enterprise brand identity and guideline specification."""
    brand_id: str
    brand_name: str
    tone_of_voice: str = Field(default="professional", description="e.g. 'professional', 'bold', 'technical'")
    brand_voice_guidelines: str = ""
    brand_colors: List[str] = Field(default_factory=list)
    approved_slogans: List[str] = Field(default_factory=list)
    messaging_pillars: List[str] = Field(default_factory=list)
    prohibited_keywords: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BrandMemory:
    """Manages persistent brand guidelines and voice invariants across all campaigns."""

    def __init__(self, db: Optional[Any] = None) -> None:
        self.db = db
        self._in_memory_store: Dict[str, BrandProfile] = {}

    async def save_brand_profile(self, profile: BrandProfile) -> None:
        """Stores or updates brand specifications."""
        self._in_memory_store[profile.brand_id] = profile
        if self.db is not None:
            try:
                await self.db["brand_profiles"].update_one(
                    {"brand_id": profile.brand_id},
                    {"$set": profile.model_dump(mode="json")},
                    upsert=True,
                )
            except Exception as e:
                logger.warning("BrandMemory | DB save error: %s; in-memory copy preserved", e)

    async def get_brand_profile(self, brand_id: str) -> Optional[BrandProfile]:
        """Retrieves a brand profile by ID."""
        if brand_id in self._in_memory_store:
            return self._in_memory_store[brand_id]

        if self.db is not None:
            try:
                doc = await self.db["brand_profiles"].find_one({"brand_id": brand_id})
                if doc:
                    doc.pop("_id", None)
                    profile = BrandProfile.model_validate(doc)
                    self._in_memory_store[brand_id] = profile
                    return profile
            except Exception as e:
                logger.warning("BrandMemory | DB get error: %s", e)

        return None
