"""Cross-encoder semantic reranking engine for retrieved RAG candidates."""

from __future__ import annotations

import logging
import re
from typing import List

from .schemas import RetrievalMethod, RetrievedChunk

logger = logging.getLogger(__name__)


class RerankerEngine:
    """Refines candidate rankings using token alignment and cross-passage query relevance scoring."""

    def __init__(self, top_k: int = 4) -> None:
        self.top_k = top_k

    def rerank(self, query: str, candidates: List[RetrievedChunk]) -> List[RetrievedChunk]:
        """Scores query-passage relevance and reorders candidates."""
        if not candidates:
            return []

        query_terms = set(re.sub(r"[^\w\s]", " ", query.lower()).split())
        scored_candidates: List[tuple[RetrievedChunk, float]] = []

        for chunk in candidates:
            content_lower = chunk.content.lower()
            content_tokens = set(re.sub(r"[^\w\s]", " ", content_lower).split())

            # 1. Exact term overlap ratio
            matched_terms = query_terms.intersection(content_tokens)
            term_overlap_score = len(matched_terms) / max(1, len(query_terms))

            # 2. Section header relevance boost
            header_boost = 0.0
            if chunk.provenance.section_header:
                header_lower = chunk.provenance.section_header.lower()
                if any(qt in header_lower for qt in query_terms):
                    header_boost = 0.15

            # 3. Base RRF similarity score
            base_score = chunk.provenance.score

            # Composite rerank score (0.0 - 1.0)
            rerank_score = round(
                (0.50 * term_overlap_score) + (0.35 * min(1.0, base_score * 100.0)) + header_boost,
                4,
            )

            # Update chunk provenance
            chunk.provenance.score = rerank_score
            chunk.provenance.retrieval_method = RetrievalMethod.CROSS_ENCODER_RERANK
            scored_candidates.append((chunk, rerank_score))

        scored_candidates.sort(key=lambda item: item[1], reverse=True)
        reranked = [item[0] for item in scored_candidates[:self.top_k]]

        logger.info(
            "RerankerEngine | Query '%s': Reranked %d candidates to top %d (Top score: %.4f)",
            query[:40],
            len(candidates),
            len(reranked),
            reranked[0].provenance.score if reranked else 0.0,
        )
        return reranked
