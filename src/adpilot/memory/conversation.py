"""ConversationMemory subsystem: Stores multi-turn user directives, human feedback, and agent dialogues."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class DialogueTurn(BaseModel):
    """A single turn in an agent or human interaction session."""
    turn_id: str = Field(default_factory=lambda: f"turn-{uuid4().hex[:8]}")
    session_id: str
    campaign_id: str
    sender: str = Field(..., description="'user', 'human_reviewer', or agent name")
    role: str = Field(default="user", description="'user', 'assistant', 'system'")
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ConversationMemory:
    """Manages conversational dialogue history and human feedback logs across campaign lifecycles."""

    def __init__(self, db: Optional[Any] = None) -> None:
        self.db = db
        self._in_memory_dialogues: Dict[str, List[DialogueTurn]] = {}

    async def add_turn(self, turn: DialogueTurn) -> None:
        """Appends a new interaction turn to conversation history."""
        key = turn.campaign_id
        if key not in self._in_memory_dialogues:
            self._in_memory_dialogues[key] = []
        self._in_memory_dialogues[key].append(turn)

        if self.db is not None:
            try:
                await self.db["dialogue_turns"].insert_one(turn.model_dump(mode="json"))
            except Exception as e:
                logger.warning("ConversationMemory | DB save error: %s", e)

    async def get_history(self, campaign_id: str, limit: int = 20) -> List[DialogueTurn]:
        """Retrieves conversational history for a campaign."""
        if campaign_id in self._in_memory_dialogues:
            return self._in_memory_dialogues[campaign_id][-limit:]

        if self.db is not None:
            try:
                cursor = self.db["dialogue_turns"].find({"campaign_id": campaign_id}).sort("timestamp", 1).limit(limit)
                docs = await cursor.to_list(length=limit)
                turns = []
                for d in docs:
                    d.pop("_id", None)
                    turns.append(DialogueTurn.model_validate(d))
                self._in_memory_dialogues[campaign_id] = turns
                return turns
            except Exception as e:
                logger.warning("ConversationMemory | DB get error: %s", e)

        return []
