"""Phase 15 — Production RAG & Epistemic Provenance Schemas."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class RetrievalMethod(str, Enum):
    """Method used to retrieve knowledge candidates."""
    DENSE_VECTOR = "dense_vector"
    BM25_LEXICAL = "bm25_lexical"
    HYBRID_RRF = "hybrid_rrf"
    CROSS_ENCODER_RERANK = "cross_encoder_rerank"


class EpistemicType(str, Enum):
    """Epistemological classification of knowledge provided to agents."""
    USER_INPUT = "user_input"
    MEMORY = "memory"
    RETRIEVED_EVIDENCE = "retrieved_evidence"
    MODEL_PREDICTION = "model_prediction"
    LLM_REASONING = "llm_reasoning"


class SourceProvenance(BaseModel):
    """Authoritative source provenance attached to every retrieved passage."""
    source_id: str = Field(default_factory=lambda: f"src-{uuid4().hex[:8]}")
    document_name: str = Field(..., description="Name or URI of the original document")
    chunk_id: str = Field(..., description="Unique chunk identifier")
    collection_name: str = Field(default="enterprise_knowledge")
    score: float = Field(..., description="Relevance score (0.0 to 1.0 or RRF score)")
    retrieval_method: RetrievalMethod = Field(default=RetrievalMethod.HYBRID_RRF)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    section_header: Optional[str] = Field(default=None, description="Document section/heading if available")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RetrievedChunk(BaseModel):
    """A retrieved knowledge passage with verified provenance and epistemic classification."""
    chunk_id: str
    content: str
    provenance: SourceProvenance
    epistemic_type: EpistemicType = Field(default=EpistemicType.RETRIEVED_EVIDENCE)


class RAGContext(BaseModel):
    """Context assembled for an agent query with full provenance tracking."""
    query: str
    chunks: List[RetrievedChunk] = Field(default_factory=list)
    formatted_context: str = Field(default="", description="Markdown formatted context for LLM prompt")
    attribution_summary: List[Dict[str, Any]] = Field(default_factory=list)
    retrieval_latency_ms: float = 0.0
    metrics: Dict[str, float] = Field(default_factory=dict)
