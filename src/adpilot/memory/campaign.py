"""CampaignMemory for storing and retrieving holistic CampaignContext."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

from ..schemas.agent_schemas import CampaignContext

logger = logging.getLogger(__name__)


class CampaignMemory:
    """Manages loading and saving the holistic CampaignContext."""

    def __init__(self, db: Optional[Any] = None, collection_name: str = "campaign_contexts") -> None:
        self.db = db
        self.collection_name = collection_name
        self._in_memory_store: Dict[str, CampaignContext] = {}

    async def get(self, campaign_id: str) -> Optional[CampaignContext]:
        """Retrieve the campaign context."""
        if campaign_id in self._in_memory_store:
            return self._in_memory_store[campaign_id]

        if self.db is not None:
            try:
                collection = self.db[self.collection_name]
                doc = await collection.find_one({"campaign_id": campaign_id})
                if not doc or "context_json" not in doc:
                    return None
                data = json.loads(doc["context_json"])
                ctx = CampaignContext.model_validate(data)
                self._in_memory_store[campaign_id] = ctx
                return ctx
            except Exception as e:
                logger.warning("CampaignMemory | DB get error: %s", e)

        return None

    async def save(self, campaign_id: str, context: CampaignContext) -> None:
        """Save the campaign context."""
        self._in_memory_store[campaign_id] = context
        if self.db is not None:
            try:
                collection = self.db[self.collection_name]
                data_json = json.dumps(context.model_dump(mode="json"))
                await collection.update_one(
                    {"campaign_id": campaign_id},
                    {"$set": {"context_json": data_json}},
                    upsert=True,
                )
            except Exception as e:
                logger.warning("CampaignMemory | DB save error: %s", e)
