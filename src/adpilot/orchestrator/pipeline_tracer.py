"""Phase 16 — Master Pipeline Execution Tracer & Observability System.

Tracks for every single Agent in the pipeline:
- INPUT: Input parameters, brief data, upstream context
- PROCESSING: Specific algorithmic/heuristic methods executed
- MODEL: ML/LLM/Statistical models invoked (with versioning)
- OUTPUT: Structured results, deliverables, decisions
- CONFIDENCE: Quantitative confidence level (0.0 to 1.0)
- EVIDENCE: Verifiable citations to RAG documents, dataset priors, or live telemetry
- CORRECTIVE ACTION: Quality gate directives and remediation tasks
- LATENCY: Execution runtime in milliseconds
- STATUS: 'started', 'completed', 'failed', 'retrying', 'corrected'
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class StageTraceRecord(BaseModel):
    """Detailed observability trace record for an individual pipeline stage."""
    trace_id: str = Field(default_factory=lambda: f"tr-{uuid4().hex[:8]}")
    stage_number: int
    stage_name: str
    agent_name: str
    input_summary: Dict[str, Any] = Field(default_factory=dict)
    processing_details: str
    model_name: str
    output_summary: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    evidence: List[str] = Field(default_factory=list)
    corrective_actions: List[str] = Field(default_factory=list)
    latency_ms: float = 0.0
    status: str = "completed"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PipelineTraceLog(BaseModel):
    """Holistic trace log capturing the entire end-to-end campaign execution."""
    campaign_id: str
    industry_archetype: str
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    finished_at: Optional[str] = None
    total_latency_ms: float = 0.0
    stages: List[StageTraceRecord] = Field(default_factory=list)
    overall_status: str = "running"
    rag_retrievals_count: int = 0
    memory_lookups_count: int = 0
    corrections_count: int = 0
    human_decisions_count: int = 0


class PipelineExecutionTracer:
    """Manages recording, formatting, and persisting execution traces for pipeline observability."""

    def __init__(self, campaign_id: str, industry_archetype: str = "saas") -> None:
        self.log = PipelineTraceLog(
            campaign_id=campaign_id,
            industry_archetype=industry_archetype,
        )

    def record_stage_trace(
        self,
        stage_number: int,
        stage_name: str,
        agent_name: str,
        input_summary: Dict[str, Any],
        processing_details: str,
        model_name: str,
        output_summary: Dict[str, Any],
        confidence: float,
        evidence: Optional[List[str]] = None,
        corrective_actions: Optional[List[str]] = None,
        latency_ms: float = 0.0,
        status: str = "completed",
    ) -> StageTraceRecord:
        """Records a new stage trace into the holistic pipeline log."""
        record = StageTraceRecord(
            stage_number=stage_number,
            stage_name=stage_name,
            agent_name=agent_name,
            input_summary=input_summary,
            processing_details=processing_details,
            model_name=model_name,
            output_summary=output_summary,
            confidence=round(confidence, 3),
            evidence=evidence or [],
            corrective_actions=corrective_actions or [],
            latency_ms=round(latency_ms, 2),
            status=status,
        )
        self.log.stages.append(record)
        self.log.total_latency_ms += record.latency_ms

        logger.info(
            "PipelineExecutionTracer | Stage %02d [%s] -> %s (Model: %s, Latency: %.2fms, Conf: %.2f)",
            stage_number,
            stage_name,
            status.upper(),
            model_name,
            latency_ms,
            confidence,
        )
        return record

    def finalize(self, overall_status: str = "success") -> PipelineTraceLog:
        """Marks pipeline trace as complete."""
        self.log.finished_at = datetime.now(timezone.utc).isoformat()
        self.log.overall_status = overall_status
        return self.log

    def format_markdown_trace(self) -> str:
        """Renders human-readable markdown execution trace matching user requirements."""
        lines = [
            f"# Master Pipeline Execution Trace: `{self.log.campaign_id}`",
            f"**Industry Archetype:** {self.log.industry_archetype.upper()}  ",
            f"**Execution Status:** `{self.log.overall_status.upper()}`  ",
            f"**Total Latency:** {self.log.total_latency_ms:.2f} ms  ",
            f"**Executed Stages:** {len(self.log.stages)}  ",
            "",
            "---",
            "",
        ]

        for s in self.log.stages:
            lines.extend([
                f"### Stage {s.stage_number:02d}: {s.stage_name} (`{s.agent_name}`)",
                f"- **STATUS:** `{s.status.upper()}`",
                f"- **LATENCY:** {s.latency_ms:.2f} ms",
                f"- **MODEL:** `{s.model_name}`",
                f"- **CONFIDENCE:** {s.confidence:.2f}",
                f"- **PROCESSING:** {s.processing_details}",
                "- **INPUT:**",
                "```json",
                f"{s.input_summary}",
                "```",
                "- **OUTPUT:**",
                "```json",
                f"{s.output_summary}",
                "```",
                f"- **EVIDENCE:** {', '.join(s.evidence) if s.evidence else 'N/A'}",
                f"- **CORRECTIVE ACTION:** {', '.join(s.corrective_actions) if s.corrective_actions else 'None'}",
                "",
            ])

        return "\n".join(lines)
