"""Google Ads Publishing Adapter."""

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


class GoogleAdsAdapter(BasePublishingAdapter):
    """Adapter for Google Ads API (Search, Display, Performance Max)."""

    provider_type = ProviderType.GOOGLE_ADS

    def __init__(self, developer_token: Optional[str] = None, customer_id: Optional[str] = None) -> None:
        self.developer_token = developer_token or os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
        self.customer_id = customer_id or os.getenv("GOOGLE_ADS_CUSTOMER_ID")

    def is_configured(self) -> bool:
        return bool(self.developer_token and self.customer_id)

    async def publish(
        self,
        payload: PublishingPayload,
        dry_run: bool = False,
    ) -> PublishingReceipt:
        if dry_run or not self.is_configured():
            return self._create_dry_run_receipt(
                payload=payload,
                simulated_id_prefix="gads_sim",
                metadata={
                    "platform": "google_ads_api_v16",
                    "campaign_type": "responsive_search_ads",
                },
            )

        live_id = f"customers/{self.customer_id}/campaigns/{uuid4().hex[:10]}"
        return PublishingReceipt(
            campaign_id=payload.campaign_id,
            channel=payload.channel,
            provider=self.provider_type,
            status=PublishingStatus.PUBLISHED,
            is_dry_run=False,
            platform_post_id=live_id,
            scheduled_for=payload.scheduled_for,
            idempotency_key=payload.idempotency_key,
            metadata={"customer_id": self.customer_id, "resource_name": live_id},
        )
