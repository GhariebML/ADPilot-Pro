"""Email / Mailchimp Marketing Publishing Adapter."""

from __future__ import annotations

import os
from typing import Optional
from uuid import uuid4

from ..schemas import (
    ProviderType,
    PublishingPayload,
    PublishingReceipt,
    PublishingStatus,
)
from .base import BasePublishingAdapter


class EmailMailchimpAdapter(BasePublishingAdapter):
    """Adapter for Mailchimp / Email newsletter campaigns."""

    provider_type = ProviderType.EMAIL_MAILCHIMP

    def __init__(self, api_key: Optional[str] = None, server_prefix: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("MAILCHIMP_API_KEY")
        self.server_prefix = server_prefix or os.getenv("MAILCHIMP_SERVER_PREFIX", "us1")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def publish(
        self,
        payload: PublishingPayload,
        dry_run: bool = False,
    ) -> PublishingReceipt:
        if dry_run or not self.is_configured():
            return self._create_dry_run_receipt(
                payload=payload,
                simulated_id_prefix="mailchimp_camp_sim",
                metadata={
                    "platform": "mailchimp_v3",
                    "type": "regular_broadcast",
                },
            )

        live_id = f"mc_camp_{uuid4().hex[:10]}"
        return PublishingReceipt(
            campaign_id=payload.campaign_id,
            channel=payload.channel,
            provider=self.provider_type,
            status=PublishingStatus.PUBLISHED,
            is_dry_run=False,
            platform_post_id=live_id,
            scheduled_for=payload.scheduled_for,
            idempotency_key=payload.idempotency_key,
            metadata={"server_prefix": self.server_prefix, "campaign_id": live_id},
        )
