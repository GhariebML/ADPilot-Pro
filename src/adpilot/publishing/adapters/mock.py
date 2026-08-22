"""Deterministic Mock / Dry Run Publishing Adapter."""

from __future__ import annotations

from ..schemas import (
    ProviderType,
    PublishingPayload,
    PublishingReceipt,
)
from .base import BasePublishingAdapter


class MockDryRunAdapter(BasePublishingAdapter):
    """Deterministic Mock adapter for safe testing and dry-run demonstrations."""

    provider_type = ProviderType.MOCK_DRY_RUN

    def __init__(self, simulate_network_failure: bool = False) -> None:
        self.simulate_network_failure = simulate_network_failure

    def is_configured(self) -> bool:
        return True

    async def publish(
        self,
        payload: PublishingPayload,
        dry_run: bool = False,
    ) -> PublishingReceipt:
        if self.simulate_network_failure:
            raise ConnectionError("Simulated transient socket timeout during provider dispatch.")

        return self._create_dry_run_receipt(
            payload=payload,
            simulated_id_prefix="mock_dryrun",
            metadata={"adapter": "MockDryRunAdapter", "simulated": True},
        )
