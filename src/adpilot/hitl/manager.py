"""HITL Review Manager: Coordinates human-in-the-loop review, approval, rejection, edits, revisions, and overrides."""

from __future__ import annotations

import logging
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import ValidationError
from ..correction.engine import CorrectionEngine
from ..correction.schemas import CorrectionTriggerSource
from ..schemas.agent_schemas import CampaignContext
from .audit import HITLAuditStore, audit_store
from .gates import HITLGates
from .schemas import (
    ApprovalStage,
    HITLAuditRecord,
    HITLDecisionSubmission,
    HITLGateOutput,
    HumanDecisionType,
    HumanReviewRequest,
)

logger = logging.getLogger(__name__)


class HITLReviewManager:
    """Enterprise Human-in-the-Loop review manager."""

    def __init__(
        self,
        audit_store_instance: Optional[HITLAuditStore] = None,
        correction_engine: Optional[CorrectionEngine] = None,
    ) -> None:
        self.audit_store = audit_store_instance or audit_store
        self.correction_engine = correction_engine or CorrectionEngine()
        self.gates = HITLGates()

    def create_review_request(
        self,
        context: CampaignContext,
        stage: ApprovalStage,
    ) -> HumanReviewRequest:
        """Generates a structured review request package for a human reviewer."""
        agent_name, recommendation, risk, summary = self.gates.extract_stage_recommendation(context, stage)

        request = HumanReviewRequest(
            campaign_id=context.campaign_id,
            stage=stage,
            agent_name=agent_name,
            agent_recommendation=recommendation,
            risk_level=risk,
            summary=summary,
        )

        logger.info(
            "HITLReviewManager | Created review request %s for campaign %s, stage %s (Risk: %s)",
            request.request_id,
            context.campaign_id,
            stage.value,
            risk.value,
        )
        return request

    async def process_decision(
        self,
        context: CampaignContext,
        stage: ApprovalStage,
        submission: HITLDecisionSubmission,
        db_session: Optional[AsyncSession] = None,
    ) -> Tuple[CampaignContext, HITLGateOutput]:
        """Processes a human reviewer's decision with strict non-silent audit logging."""
        agent_name, recommendation, risk, _ = self.gates.extract_stage_recommendation(context, stage)

        # 1. Anti-Silent Override Check & Record Construction
        is_override = submission.decision == HumanDecisionType.OVERRIDE
        is_edit = submission.decision == HumanDecisionType.EDIT

        if (is_override or is_edit) and not submission.modified_output:
            raise ValidationError(f"Human decision '{submission.decision.value}' must provide a non-empty modified_output payload.")

        audit_record = HITLAuditRecord(
            user=submission.user,
            campaign_id=context.campaign_id,
            stage=stage,
            agent=agent_name,
            decision=submission.decision,
            previous_output=recommendation,
            modified_output=submission.modified_output,
            reason=submission.reason,
            revision_directives=submission.revision_directives,
            is_override=is_override,
            metadata=submission.metadata,
        )

        # 2. Commit audit record to store
        self.audit_store.record_decision(audit_record)
        if db_session:
            await self.audit_store.persist_to_db(audit_record, db_session)

        # 3. Handle Decision Branches
        updated_context = context
        is_approved = False
        requires_revision = False

        if submission.decision in [HumanDecisionType.APPROVE, HumanDecisionType.FINAL_APPROVAL]:
            logger.info("HITLReviewManager | Stage %s APPROVED by user %s.", stage.value, submission.user)
            is_approved = True

        elif submission.decision == HumanDecisionType.REJECT:
            logger.warning("HITLReviewManager | Stage %s REJECTED by user %s: %s", stage.value, submission.user, submission.reason)
            is_approved = False

        elif submission.decision in [HumanDecisionType.EDIT, HumanDecisionType.OVERRIDE]:
            logger.info(
                "HITLReviewManager | Stage %s %s applied by user %s.",
                stage.value,
                "OVERRIDE" if is_override else "EDIT",
                submission.user,
            )
            # Apply modified output to context
            if submission.modified_output:
                updated_context = self.gates.apply_modification_to_context(
                    context=updated_context,
                    stage=stage,
                    modified_output=submission.modified_output,
                )
            is_approved = True

        elif submission.decision == HumanDecisionType.REQUEST_REVISION:
            logger.info(
                "HITLReviewManager | Stage %s REVISION REQUESTED by user %s: %s",
                stage.value,
                submission.user,
                submission.reason,
            )
            requires_revision = True
            is_approved = False

            # Trigger Phase 11 Correction Engine with revision directives
            combined_feedback = f"{submission.reason}. Directives: {'; '.join(submission.revision_directives)}"
            updated_context, _ = await self.correction_engine.execute_correction_loop(
                context=updated_context,
                trigger_source=CorrectionTriggerSource.HUMAN_REJECTION,
                human_feedback=combined_feedback,
            )

        elif submission.decision == HumanDecisionType.REVIEW:
            logger.info("HITLReviewManager | Stage %s reviewed without state change.", stage.value)
            is_approved = False

        gate_output = HITLGateOutput(
            stage=stage,
            decision=submission.decision,
            approved_by=submission.user,
            approved_at=audit_record.timestamp,
            reason=submission.reason,
            is_approved=is_approved,
            audit_id=audit_record.audit_id,
            requires_revision=requires_revision,
            revision_directives=submission.revision_directives,
            modified_output=submission.modified_output,
        )

        return updated_context, gate_output

    def get_campaign_audit_history(self, campaign_id: str) -> List[HITLAuditRecord]:
        """Fetch all decisions and audit entries recorded for a campaign."""
        return self.audit_store.get_campaign_audits(campaign_id)
