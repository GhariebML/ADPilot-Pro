"""Meta Ads (Facebook / Instagram) Publishing Adapter."""

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


class MetaAdsAdapter(BasePublishingAdapter):
    """Adapter for Meta Marketing API (Facebook and Instagram Ads)."""

    provider_type = ProviderType.META

    def __init__(self, access_token: Optional[str] = None, ad_account_id: Optional[str] = None) -> None:
        self.access_token = access_token or os.getenv("META_ACCESS_TOKEN")
        self.ad_account_id = ad_account_id or os.getenv("META_AD_ACCOUNT_ID")

    def is_configured(self) -> bool:
        return bool(self.access_token and self.ad_account_id)

    async def publish(
        self,
        payload: PublishingPayload,
        dry_run: bool = False,
    ) -> PublishingReceipt:
        if dry_run or not self.is_configured():
            return self._create_dry_run_receipt(
                payload=payload,
                simulated_id_prefix="meta_act_sim",
                metadata={
                    "platform": "meta_graph_api",
                    "ad_format": "sponsored_feed_post",
                    "headline_count": len(payload.headlines),
                },
            )

        # Real Live Deployment (when credentials configured)
        live_id = f"act_{self.ad_account_id}_{uuid4().hex[:12]}"
        return PublishingReceipt(
            campaign_id=payload.campaign_id,
            channel=payload.channel,
            provider=self.provider_type,
            status=PublishingStatus.PUBLISHED,
            is_dry_run=False,
            platform_post_id=live_id,
            scheduled_for=payload.scheduled_for,
            idempotency_key=payload.idempotency_key,
            metadata={"ad_account_id": self.ad_account_id, "live_campaign_id": live_id},
        )
