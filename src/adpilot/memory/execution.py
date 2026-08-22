"""ExecutionMemory subsystem: Tracks runtime pipeline executions, step latencies, retries, and errors."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class StageExecutionRecord(BaseModel):
    """Telemetry record for a single pipeline stage execution."""
    record_id: str = Field(default_factory=lambda: f"exec-{uuid4().hex[:8]}")
    campaign_id: str
    stage_name: str
    agent_name: str
    status: str = Field(default="completed", description="'started', 'completed', 'failed', 'retrying'")
    latency_ms: float = 0.0
    attempt: int = 1
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ExecutionMemory:
    """Stores and analyzes pipeline execution metrics and operational failure histories."""

    def __init__(self, db: Optional[Any] = None) -> None:
        self.db = db
        self._in_memory_records: Dict[str, List[StageExecutionRecord]] = {}

    async def record_stage(self, record: StageExecutionRecord) -> None:
        """Appends a stage execution telemetry record."""
        key = record.campaign_id
        if key not in self._in_memory_records:
            self._in_memory_records[key] = []
        self._in_memory_records[key].append(record)

        if self.db is not None:
            try:
                await self.db["execution_records"].insert_one(record.model_dump(mode="json"))
            except Exception as e:
                logger.warning("ExecutionMemory | DB save error: %s", e)

    async def get_execution_history(self, campaign_id: str) -> List[StageExecutionRecord]:
        """Retrieves all execution steps for a campaign."""
        if campaign_id in self._in_memory_records:
            return self._in_memory_records[campaign_id]

        if self.db is not None:
            try:
                cursor = self.db["execution_records"].find({"campaign_id": campaign_id}).sort("timestamp", 1)
                docs = await cursor.to_list(length=100)
                records = []
                for d in docs:
                    d.pop("_id", None)
                    records.append(StageExecutionRecord.model_validate(d))
                self._in_memory_records[campaign_id] = records
                return records
            except Exception as e:
                logger.warning("ExecutionMemory | DB get error: %s", e)

        return []
