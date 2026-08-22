"""LongTermMemory for semantic cross-campaign memory and knowledge base."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from ..schemas.memory_schemas import MemoryRecord

logger = logging.getLogger(__name__)


class LongTermMemory:
    """Manages long-term cross-campaign knowledge, channel priors, and winning strategic patterns."""

    def __init__(self, db: Optional[Any] = None) -> None:
        self.db = db
        self._in_memory_records: List[MemoryRecord] = []

    async def add_memory(
        self,
        campaign_id: str,
        agent_name: str,
        memory_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store a new long-term memory."""
        record = MemoryRecord(
            campaign_id=campaign_id,
            agent_name=agent_name,
            memory_type=memory_type,
            content=content,
            metadata=metadata or {},
        )
        self._in_memory_records.append(record)

        if self.db is not None:
            try:
                collection = self.db["memories"]
                await collection.insert_one(record.model_dump(mode="json"))
            except Exception as e:
                logger.warning("LongTermMemory | DB insert error: %s", e)

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Searches long-term memories by keyword or recency."""
        query_lower = query.lower()
        matched = []
        for rec in reversed(self._in_memory_records):
            if query_lower in rec.content.lower() or query_lower in rec.memory_type.lower():
                matched.append(rec.model_dump(mode="json"))
            if len(matched) >= limit:
                break

        if not matched and self._in_memory_records:
            matched = [r.model_dump(mode="json") for r in self._in_memory_records[-limit:]]

        if self.db is not None and not matched:
            try:
                collection = self.db["memories"]
                cursor = collection.find().sort("created_at", -1).limit(limit)
                docs = await cursor.to_list(length=limit)
                for d in docs:
                    d.pop("_id", None)
                return docs
            except Exception as e:
                logger.warning("LongTermMemory | DB search error: %s", e)

        return matched
