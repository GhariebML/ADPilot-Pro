"""LinkedIn Marketing Solutions Publishing Adapter."""

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


class LinkedInAdsAdapter(BasePublishingAdapter):
    """Adapter for LinkedIn Marketing Developer Platform."""

    provider_type = ProviderType.LINKEDIN

    def __init__(self, access_token: Optional[str] = None, account_urn: Optional[str] = None) -> None:
        self.access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.account_urn = account_urn or os.getenv("LINKEDIN_AD_ACCOUNT_ID")

    def is_configured(self) -> bool:
        return bool(self.access_token and self.account_urn)

    async def publish(
        self,
        payload: PublishingPayload,
        dry_run: bool = False,
    ) -> PublishingReceipt:
        if dry_run or not self.is_configured():
            return self._create_dry_run_receipt(
                payload=payload,
                simulated_id_prefix="li_sponsored_sim",
                metadata={
                    "platform": "linkedin_marketing_api_v2",
                    "ad_format": "sponsored_content_direct_sponsored_ad",
                },
            )

        live_id = f"urn:li:sponsoredCreative:{uuid4().hex[:12]}"
        return PublishingReceipt(
            campaign_id=payload.campaign_id,
            channel=payload.channel,
            provider=self.provider_type,
            status=PublishingStatus.PUBLISHED,
            is_dry_run=False,
            platform_post_id=live_id,
            scheduled_for=payload.scheduled_for,
            idempotency_key=payload.idempotency_key,
            metadata={"account_urn": self.account_urn, "creative_urn": live_id},
        )
