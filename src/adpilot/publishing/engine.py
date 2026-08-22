"""Publishing Engine: Orchestrates validation, preparation, scheduling, idempotency, retries, and dispatch."""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, List, Optional, Tuple

from ..core.exceptions import ValidationError
from ..schemas.agent_schemas import CampaignContext, MarketingChannel
from .adapters import BasePublishingAdapter, ProviderAdapterFactory
from .audit import PublishingAuditLogger
from .idempotency import IdempotencyStore
from .schemas import (
    ExecutionMode,
    PublishingPayload,
    PublishingReceipt,
    PublishingReport,
    PublishingStatus,
    PublishingValidationResult,
)
from .validator import PublishingValidator

logger = logging.getLogger(__name__)


class PublishingEngine:
    """Enterprise campaign publishing engine."""

    def __init__(
        self,
        validator: Optional[PublishingValidator] = None,
        idemp_store: Optional[IdempotencyStore] = None,
        audit_logger: Optional[PublishingAuditLogger] = None,
        max_retries: int = 3,
    ) -> None:
        self.validator = validator or PublishingValidator()
        self.idempotency_store = idemp_store if idemp_store is not None else IdempotencyStore()
        self.audit_logger = audit_logger or PublishingAuditLogger()
        self.max_retries = max_retries

    async def execute_publishing(
        self,
        context: CampaignContext,
        force_dry_run: bool = False,
        custom_adapters: Optional[Dict[MarketingChannel, BasePublishingAdapter]] = None,
    ) -> Tuple[CampaignContext, PublishingReport]:
        """Executes full publishing workflow across all target campaign channels."""
        # 1. Pre-Flight Approval and Quality Gate Validation
        validation_result: PublishingValidationResult = self.validator.validate_pre_flight(context)
        if not validation_result.is_valid:
            error_summary = "; ".join(validation_result.validation_errors)
            logger.error("PublishingEngine | Cannot publish campaign %s: %s", context.campaign_id, error_summary)
            
            failed_report = PublishingReport(
                campaign_id=context.campaign_id,
                execution_mode=ExecutionMode.DRY_RUN if force_dry_run else ExecutionMode.LIVE,
                total_channels=len(context.channels) if hasattr(context, "channels") else 0,
                successful_dispatches=0,
                failed_dispatches=len(context.channels) if hasattr(context, "channels") else 0,
                receipts=[],
                validation=validation_result,
                summary=f"Pre-flight validation failed: {error_summary}",
            )
            self.audit_logger.log_report(failed_report)
            raise ValidationError(f"Publishing pre-flight validation failed: {error_summary}")

        # 2. Extract Prepared Campaign Elements
        channels = getattr(context, "channels", [MarketingChannel.linkedin])
        headlines = getattr(context.content, "headlines", ["Default Campaign Headline"])
        primary_copy = getattr(context.content, "primary_copy", ["Default body copy"])
        primary_copy_text = primary_copy[0] if isinstance(primary_copy, list) and primary_copy else str(primary_copy)
        ctas = getattr(context.content, "ctas", ["Learn More"])
        
        # Budget and Channel Allocations
        total_budget = getattr(context.budget, "total_budget", 1000.0) if hasattr(context, "budget") else 1000.0
        channel_weights: Dict[str, float] = {}
        if hasattr(context, "optimization") and context.optimization and context.optimization.action_proposal:
            channel_weights = context.optimization.action_proposal.channel_allocations
        
        bid_mult = getattr(context.optimization.action_proposal, "bid_multiplier", 1.0) if hasattr(context, "optimization") and context.optimization and context.optimization.action_proposal else 1.0

        scheduled_for = getattr(context.timeline, "start_date", None) if hasattr(context, "timeline") else None

        # 3. Process Dispatches per Channel
        receipts: List[PublishingReceipt] = []
        is_all_dry_run = True

        for channel in channels:
            # Allocate channel budget share
            weight = channel_weights.get(channel.value, 1.0 / max(1, len(channels)))
            channel_budget = total_budget * weight

            # Build deterministic Idempotency Key
            idemp_key = self.idempotency_store.generate_key(
                campaign_id=context.campaign_id,
                channel=channel.value,
                headlines=headlines,
                primary_copy=primary_copy_text,
                budget=channel_budget,
                scheduled_for=scheduled_for,
            )

            # Check Idempotency Cache
            duplicate = self.idempotency_store.check_duplicate(idemp_key)
            if duplicate:
                receipts.append(duplicate)
                self.audit_logger.log_dispatch(duplicate)
                continue

            # Resolve Adapter
            adapter = (
                custom_adapters.get(channel)
                if custom_adapters and channel in custom_adapters
                else ProviderAdapterFactory.get_adapter_for_channel(channel)
            )

            # Build Channel Payload
            payload = PublishingPayload(
                campaign_id=context.campaign_id,
                channel=channel,
                provider=adapter.provider_type,
                headlines=headlines,
                primary_copy=primary_copy_text,
                ctas=ctas,
                target_audience={"countries": getattr(context.geography, "target_countries", ["US"]) if hasattr(context, "geography") else ["US"]},
                budget_allocation=channel_budget,
                bid_multiplier=bid_mult,
                utm_parameters={
                    "utm_source": channel.value,
                    "utm_medium": "cpc",
                    "utm_campaign": context.campaign_id,
                },
                creative_asset_urls=[],
                scheduled_for=scheduled_for,
                idempotency_key=idemp_key,
            )

            # Execute Dispatch with Exponential Backoff Retries
            receipt = await self._dispatch_with_retries(
                adapter=adapter,
                payload=payload,
                force_dry_run=force_dry_run,
            )

            if not receipt.is_dry_run:
                is_all_dry_run = False

            # Record Success in Idempotency Store
            if receipt.status in [PublishingStatus.PUBLISHED, PublishingStatus.DRY_RUN_PUBLISHED]:
                self.idempotency_store.record_success(idemp_key, receipt)

            # Audit log
            self.audit_logger.log_dispatch(receipt)
            receipts.append(receipt)

        # 4. Construct Final Publishing Report
        successful = sum(1 for r in receipts if r.status in [PublishingStatus.PUBLISHED, PublishingStatus.DRY_RUN_PUBLISHED, PublishingStatus.DUPLICATE_IGNORED])
        failed = sum(1 for r in receipts if r.status == PublishingStatus.FAILED)

        report = PublishingReport(
            campaign_id=context.campaign_id,
            execution_mode=ExecutionMode.DRY_RUN if is_all_dry_run else ExecutionMode.LIVE,
            total_channels=len(channels),
            successful_dispatches=successful,
            failed_dispatches=failed,
            receipts=receipts,
            validation=validation_result,
            summary=f"Successfully dispatched to {successful}/{len(channels)} channels ({'Safe Dry-Run Mode' if is_all_dry_run else 'Live Production'}).",
        )

        self.audit_logger.log_report(report)
        return context, report

    async def _dispatch_with_retries(
        self,
        adapter: BasePublishingAdapter,
        payload: PublishingPayload,
        force_dry_run: bool,
    ) -> PublishingReceipt:
        """Executes adapter dispatch with automatic exponential backoff retries on transient errors."""
        last_error: Optional[Exception] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                receipt = await adapter.publish(payload, dry_run=force_dry_run)
                receipt.attempts = attempt
                return receipt
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "PublishingEngine | Dispatch to %s (channel %s) failed on attempt %d/%d: %s",
                    adapter.provider_type.value,
                    payload.channel.value,
                    attempt,
                    self.max_retries,
                    exc,
                )
                if attempt < self.max_retries:
                    backoff = min(1.0, 0.05 * (2 ** (attempt - 1)))
                    await asyncio.sleep(backoff)

        # Failure handling after retries exhausted
        return PublishingReceipt(
            campaign_id=payload.campaign_id,
            channel=payload.channel,
            provider=adapter.provider_type,
            status=PublishingStatus.FAILED,
            is_dry_run=force_dry_run,
            platform_post_id=None,
            scheduled_for=payload.scheduled_for,
            attempts=self.max_retries,
            idempotency_key=payload.idempotency_key,
            error_message=str(last_error),
            metadata={"error_details": str(last_error), "exhausted_attempts": self.max_retries},
        )
