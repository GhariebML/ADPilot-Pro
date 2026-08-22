"""Publishing adapters package and factory."""

from __future__ import annotations

from typing import Dict, Type

from ...schemas.agent_schemas import MarketingChannel
from ..schemas import ProviderType
from .base import BasePublishingAdapter
from .email import EmailMailchimpAdapter
from .google import GoogleAdsAdapter
from .linkedin import LinkedInAdsAdapter
from .meta import MetaAdsAdapter
from .mock import MockDryRunAdapter

CHANNEL_TO_PROVIDER: Dict[MarketingChannel, ProviderType] = {
    MarketingChannel.facebook: ProviderType.META,
    MarketingChannel.instagram: ProviderType.META,
    MarketingChannel.youtube: ProviderType.GOOGLE_ADS,
    MarketingChannel.linkedin: ProviderType.LINKEDIN,
    MarketingChannel.email: ProviderType.EMAIL_MAILCHIMP,
    MarketingChannel.twitter: ProviderType.BUFFER,
    MarketingChannel.tiktok: ProviderType.META,
    MarketingChannel.snapchat: ProviderType.META,
}

ADAPTER_REGISTRY: Dict[ProviderType, Type[BasePublishingAdapter]] = {
    ProviderType.META: MetaAdsAdapter,
    ProviderType.GOOGLE_ADS: GoogleAdsAdapter,
    ProviderType.LINKEDIN: LinkedInAdsAdapter,
    ProviderType.EMAIL_MAILCHIMP: EmailMailchimpAdapter,
    ProviderType.MOCK_DRY_RUN: MockDryRunAdapter,
}


class ProviderAdapterFactory:
    """Resolves and instantiates external provider adapters."""

    @staticmethod
    def get_adapter_for_channel(
        channel: MarketingChannel,
        force_mock: bool = False,
    ) -> BasePublishingAdapter:
        if force_mock:
            return MockDryRunAdapter()

        provider_type = CHANNEL_TO_PROVIDER.get(channel, ProviderType.MOCK_DRY_RUN)
        adapter_cls = ADAPTER_REGISTRY.get(provider_type, MockDryRunAdapter)
        return adapter_cls()

    @staticmethod
    def get_adapter_for_provider(
        provider: ProviderType,
    ) -> BasePublishingAdapter:
        adapter_cls = ADAPTER_REGISTRY.get(provider, MockDryRunAdapter)
        return adapter_cls()


__all__ = [
    "BasePublishingAdapter",
    "MetaAdsAdapter",
    "GoogleAdsAdapter",
    "LinkedInAdsAdapter",
    "EmailMailchimpAdapter",
    "MockDryRunAdapter",
    "ProviderAdapterFactory",
    "CHANNEL_TO_PROVIDER",
    "ADAPTER_REGISTRY",
]
