"""Phase 13 — Enterprise Publishing Agent."""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, Optional

from langchain_core.prompts import ChatPromptTemplate

from ..core.agent_events import AgentEventType, AgentLifecycleEvent, event_bus
from ..core.base_agent import BaseAgent
from ..core.exceptions import AgentOutputError, ValidationError
from ..publishing.engine import PublishingEngine
from ..publishing.schemas import ExecutionMode
from ..schemas.agent_schemas import (
    CampaignContext,
    CampaignGoal,
    CampaignInput,
    MarketingChannel,
    PublishingAgentInput,
    PublishingPackage,
    ToneOfVoice,
    UTMParameters,
)

logger = logging.getLogger(__name__)


class PublishingAgent(BaseAgent[PublishingAgentInput, PublishingPackage]):
    """Enterprise Publishing Agent managing the execution boundary to ad platforms."""

    name = "publishing_agent"
    input_model = PublishingAgentInput
    output_model = PublishingPackage

    system_prompt = (
        "You are AdPilot's Campaign Operations and Publishing Manager. Your objective is to package "
        "and dispatch approved campaign assets, copy, strategy, and validated optimizer allocations "
        "to external ad networks with strict pre-flight safety gates, safe dry-run fallback, "
        "and idempotency protection. Return output that matches the PublishingPackage schema."
    )

    def __init__(self, engine: Optional[PublishingEngine] = None) -> None:
        super().__init__()
        self.engine = engine or PublishingEngine()

    def build_prompt(self) -> ChatPromptTemplate:
        """Build the LangChain prompt template for publishing generation."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "human",
                    "Compile and package this campaign for publishing:\n\n"
                    "Campaign Brief:\n{campaign_json}\n\n"
                    "Strategy:\n{strategy_json}\n\n"
                    "Content:\n{content_json}\n\n"
                    "Return only structured data that satisfies the required Pydantic output model.",
                ),
            ]
        )

    async def run(
        self,
        context: CampaignContext,
        force_dry_run: bool = False,
        custom_adapters: Optional[Dict[MarketingChannel, Any]] = None,
    ) -> CampaignContext:
        """Executes pre-flight validation and dispatches campaign to ad platforms."""
        start_time = time.time()
        event_bus.emit(
            AgentLifecycleEvent(
                event_type=AgentEventType.AGENT_STARTED,
                agent_id=self.name,
                campaign_id=context.campaign_id,
                status="started",
            )
        )

        logger.info("PublishingAgent | Commencing execution for campaign %s", context.campaign_id)

        # 1. Validate Input & Optional LLM Generation
        brief_input = context.brief if hasattr(context, "brief") and context.brief else (
            context.to_campaign_input() if hasattr(context, "to_campaign_input") else None
        )
        if brief_input is None:
            brief_input = CampaignInput(
                business_name=context.business.name if hasattr(context, "business") and context.business else "Enterprise",
                product_description=context.product.description if hasattr(context, "product") and context.product else "SaaS Platform",
                target_market="Enterprise",
                budget_usd=context.budget.total_budget if hasattr(context, "budget") and context.budget else 10000.0,
                goals=context.goals if hasattr(context, "goals") and context.goals else [CampaignGoal.lead_generation],
                channels=context.channels if hasattr(context, "channels") and context.channels else [MarketingChannel.linkedin],
                tone_of_voice=context.brand.tone_of_voice if hasattr(context, "brand") and context.brand else ToneOfVoice.professional,
                competitors=[],
                campaign_duration_days=context.timeline.duration_days if hasattr(context, "timeline") and context.timeline else 30,
            )

        agent_input = PublishingAgentInput(
            campaign=brief_input,
            content=context.content if hasattr(context, "content") and context.content else None,
            strategy=context.strategy if hasattr(context, "strategy") and context.strategy else None,
        )
        validated_input = self.validate_input(agent_input)
        prompt = self.build_prompt()

        llm_pkg: Optional[PublishingPackage] = None
        try:
            llm_pkg = await self.call_llm(
                prompt=prompt,
                campaign_json=json.dumps(validated_input.campaign.model_dump(mode="json"), indent=2),
                content_json=json.dumps(validated_input.content.model_dump(mode="json") if validated_input.content else {}, indent=2),
                strategy_json=json.dumps(validated_input.strategy.model_dump(mode="json") if validated_input.strategy else {}, indent=2),
                campaign_id=context.campaign_id,
            )
        except AgentOutputError:
            raise
        except Exception as llm_err:
            logger.info("LLM unavailable for publishing package; using engine extraction: %s", llm_err)

        # 2. Execute publishing through engine (handles validation, idempotency, retries, dry-run adapters)
        report = None
        try:
            context, report = await self.engine.execute_publishing(
                context=context,
                force_dry_run=force_dry_run,
                custom_adapters=custom_adapters,
            )
        except ValidationError:
            if llm_pkg is not None:
                context.publishing = llm_pkg
                context.record_agent_output("publishing_agent", llm_pkg)
                return context
            raise

        # 3. Assemble canonical PublishingPackage
        headlines = llm_pkg.headlines if llm_pkg and llm_pkg.headlines else getattr(context.content, "headlines", [])
        ctas = llm_pkg.ctas if llm_pkg and llm_pkg.ctas else getattr(context.content, "ctas", [])
        targeting = llm_pkg.targeting_criteria if llm_pkg and llm_pkg.targeting_criteria else (
            getattr(context.geography, "target_countries", ["US"]) if hasattr(context, "geography") else ["US"]
        )
        
        budget_allocations: Dict[str, float] = {}
        for r in report.receipts:
            budget_allocations[r.channel.value] = r.metadata.get("simulated_spend", 0.0)

        utm = llm_pkg.utm_parameters if llm_pkg and llm_pkg.utm_parameters else UTMParameters(
            utm_source="adpilot_multi_channel",
            utm_medium="cpc",
            utm_campaign=context.campaign_id,
        )

        pkg = PublishingPackage(
            headlines=headlines,
            ctas=ctas,
            targeting_criteria=targeting,
            budget_allocation=budget_allocations or (llm_pkg.budget_allocation if llm_pkg else {}),
            utm_parameters=utm,
            campaign_metadata=llm_pkg.campaign_metadata if llm_pkg and llm_pkg.campaign_metadata else {
                "campaign_id": context.campaign_id,
                "execution_mode": report.execution_mode.value,
                "total_channels": str(report.total_channels),
                "successful_dispatches": str(report.successful_dispatches),
                "published_at": report.published_at,
            },
            receipts=[r.model_dump() for r in report.receipts],
            is_dry_run=report.execution_mode == ExecutionMode.DRY_RUN,
            execution_mode=report.execution_mode.value,
            published_channels=[r.channel.value for r in report.receipts],
            validation_summary=report.validation.model_dump() if report.validation else None,
        )

        context.publishing = pkg
        context.record_agent_output("publishing_agent", pkg)

        latency = time.time() - start_time
        event_bus.emit(
            AgentLifecycleEvent(
                event_type=AgentEventType.AGENT_COMPLETED,
                agent_id=self.name,
                campaign_id=context.campaign_id,
                status="completed",
                latency=latency,
                metadata={"published_channels": pkg.published_channels, "is_dry_run": pkg.is_dry_run},
            )
        )

        logger.info(
            "PublishingAgent | Completed dispatch for campaign %s (%d channels, Mode: %s)",
            context.campaign_id,
            len(pkg.published_channels),
            pkg.execution_mode,
        )
        return context
