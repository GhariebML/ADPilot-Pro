"""Base provider adapter interface for campaign publishing."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
from uuid import uuid4

from ..schemas import (
    ProviderType,
    PublishingPayload,
    PublishingReceipt,
    PublishingStatus,
)

logger = logging.getLogger(__name__)


class BasePublishingAdapter(ABC):
    """Abstract base class for all external advertising and publishing adapters."""

    provider_type: ProviderType

    @abstractmethod
    def is_configured(self) -> bool:
        """Checks whether the necessary API credentials exist in the environment."""
        pass

    @abstractmethod
    async def publish(
        self,
        payload: PublishingPayload,
        dry_run: bool = False,
    ) -> PublishingReceipt:
        """Dispatches the prepared campaign payload to the platform or returns a dry-run receipt."""
        pass

    def _create_dry_run_receipt(
        self,
        payload: PublishingPayload,
        simulated_id_prefix: str = "dryrun",
        metadata: Dict[str, Any] | None = None,
    ) -> PublishingReceipt:
        """Constructs an explicit, transparent dry-run receipt."""
        simulated_id = f"{simulated_id_prefix}_{payload.channel.value}_{uuid4().hex[:8]}"
        meta = metadata or {}
        meta["dry_run_reason"] = "Safe dry-run execution (real advertising credentials unconfigured or dry-run requested)"
        meta["simulated_spend"] = payload.budget_allocation

        logger.info(
            "PublishingAdapter [%s] | Executed SAFE DRY-RUN for channel '%s' (Campaign: %s, SimID: %s)",
            self.provider_type.value,
            payload.channel.value,
            payload.campaign_id,
            simulated_id,
        )

        return PublishingReceipt(
            campaign_id=payload.campaign_id,
            channel=payload.channel,
            provider=self.provider_type,
            status=PublishingStatus.DRY_RUN_PUBLISHED,
            is_dry_run=True,
            platform_post_id=simulated_id,
            scheduled_for=payload.scheduled_for,
            idempotency_key=payload.idempotency_key,
            metadata=meta,
        )
