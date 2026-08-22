"""Epistemic Context Formatter enforcing strict boundaries between evidence, memory, user input, and model predictions."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .schemas import RAGContext, RetrievedChunk

logger = logging.getLogger(__name__)


class EpistemicContextBuilder:
    """Formats multi-source context with strict epistemological boundaries and source citations."""

    @staticmethod
    def format_agent_rag_context(
        rag_context: RAGContext,
        user_input: Optional[Dict[str, Any]] = None,
        memory_context: Optional[Dict[str, Any]] = None,
        model_predictions: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Constructs an epistemically partitioned prompt context."""
        parts: List[str] = []

        # 1. Ground-Truth User Input
        if user_input:
            parts.append("### 1. [GROUND TRUTH USER INPUT]\n*Strictly immutable campaign specifications provided by the user.*")
            for k, v in user_input.items():
                parts.append(f"- **{k}**: {v}")
            parts.append("")

        # 2. Multi-Tier Memory Recalled Context
        if memory_context:
            parts.append("### 2. [RECALLED ENTERPRISE MEMORY]\n*Historical brand, customer, and campaign knowledge.*")
            for mem_type, items in memory_context.items():
                parts.append(f"#### Memory: {mem_type.upper()}")
                if isinstance(items, list):
                    for item in items:
                        parts.append(f"- {item}")
                elif isinstance(items, dict):
                    for k, v in items.items():
                        parts.append(f"- **{k}**: {v}")
                else:
                    parts.append(f"- {items}")
            parts.append("")

        # 3. Factual Retrieved Evidence (RAG Documents)
        parts.append("### 3. [FACTUAL RETRIEVED EVIDENCE (RAG)]\n*Verified enterprise documentation. Cite source chunks when utilizing these facts.*")
        if not rag_context.chunks:
            parts.append("*No relevant external documentation retrieved for this query.*")
        else:
            for idx, chunk in enumerate(rag_context.chunks, 1):
                p = chunk.provenance
                parts.append(
                    f"#### [Evidence #{idx}] [Doc: {p.document_name} | Section: {p.section_header} | ChunkID: {p.chunk_id} | Score: {p.score:.3f}]\n"
                    f"```text\n{chunk.content}\n```"
                )
        parts.append("")

        # 4. Statistical Model Predictions
        if model_predictions:
            parts.append("### 4. [STATISTICAL MODEL PREDICTIONS]\n*Probabilistic machine learning inferences (not ground truth facts).*")
            for model_name, pred in model_predictions.items():
                parts.append(f"- **{model_name}**: {pred}")
            parts.append("")

        # 5. Anti-Hallucination & Epistemic Rules
        parts.append(
            "### 5. [EPISTEMIC GROUNDING DIRECTIVE]\n"
            "- Treat [GROUND TRUTH USER INPUT] as hard immutable requirements.\n"
            "- Support all factual claims with citations to [FACTUAL RETRIEVED EVIDENCE] using format `[Source: DocName#ChunkID]`.\n"
            "- Do NOT claim unverified assumptions or LLM hypotheses as factual evidence.\n"
            "- Clearly demarcate probabilistic inferences from empirical data."
        )

        return "\n".join(parts)

    @staticmethod
    def build_attribution_summary(chunks: List[RetrievedChunk]) -> List[Dict[str, Any]]:
        """Extracts structured attribution metadata for audit logging."""
        summary = []
        for c in chunks:
            summary.append({
                "document_name": c.provenance.document_name,
                "chunk_id": c.provenance.chunk_id,
                "section_header": c.provenance.section_header,
                "score": c.provenance.score,
                "retrieval_method": c.provenance.retrieval_method.value,
                "timestamp": c.provenance.timestamp,
            })
        return summary
