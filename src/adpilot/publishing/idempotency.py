"""Idempotency store: Guarantees duplicate publish prevention."""

from __future__ import annotations

import hashlib
import json
import logging
import threading
from typing import Dict, Optional

from .schemas import PublishingReceipt, PublishingStatus

logger = logging.getLogger(__name__)


class IdempotencyStore:
    """Thread-safe idempotency registry tracking publishing dispatch keys."""

    def __init__(self) -> None:
        self._cache: Dict[str, PublishingReceipt] = {}
        self._lock = threading.Lock()

    @staticmethod
    def generate_key(
        campaign_id: str,
        channel: str,
        headlines: list[str],
        primary_copy: str,
        budget: float,
        scheduled_for: Optional[str] = None,
    ) -> str:
        """Computes a deterministic SHA-256 signature for the publish payload."""
        payload_data = {
            "campaign_id": campaign_id,
            "channel": channel,
            "headlines": sorted(headlines),
            "primary_copy": primary_copy.strip(),
            "budget": round(budget, 2),
            "scheduled_for": scheduled_for or "",
        }
        serialized = json.dumps(payload_data, sort_keys=True)
        raw_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return f"idemp-{raw_hash[:16]}"

    def check_duplicate(self, key: str) -> Optional[PublishingReceipt]:
        """Returns existing cached receipt if key was already published, otherwise None."""
        with self._lock:
            cached = self._cache.get(key)
            if cached:
                logger.warning(
                    "IdempotencyStore | Duplicate publish detected for key '%s'. Returning cached receipt.",
                    key,
                )
                duplicate_receipt = cached.model_copy()
                duplicate_receipt.status = PublishingStatus.DUPLICATE_IGNORED
                duplicate_receipt.metadata["duplicate_ignored"] = True
                return duplicate_receipt
            return None

    def record_success(self, key: str, receipt: PublishingReceipt) -> None:
        """Stores successful dispatch receipt in idempotency registry."""
        with self._lock:
            self._cache[key] = receipt

    def clear(self) -> None:
        """Clears cached keys (for testing resets)."""
        with self._lock:
            self._cache.clear()


# Default singleton
idempotency_store = IdempotencyStore()
