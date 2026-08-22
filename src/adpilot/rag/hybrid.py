"""Hybrid retrieval engine combining Dense Vector Search and BM25 via Reciprocal Rank Fusion (RRF)."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from langchain_core.documents import Document

from .bm25 import BM25Index
from .schemas import (
    EpistemicType,
    RetrievalMethod,
    RetrievedChunk,
    SourceProvenance,
)

logger = logging.getLogger(__name__)


class HybridRetriever:
    """Combines semantic vector embeddings and sparse BM25 keyword search using Reciprocal Rank Fusion."""

    def __init__(
        self,
        vector_store: Any,
        bm25_index: Optional[BM25Index] = None,
        dense_weight: float = 0.6,
        bm25_weight: float = 0.4,
        rrf_k: int = 60,
    ) -> None:
        self.vector_store = vector_store
        self.bm25_index = bm25_index or BM25Index()
        self.dense_weight = dense_weight
        self.bm25_weight = bm25_weight
        self.rrf_k = rrf_k

    async def retrieve_hybrid(
        self,
        collection_name: str,
        query: str,
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedChunk]:
        """Executes dense vector search and BM25 lexical search in parallel, fusing results via RRF."""
        # 1. Dense Vector Search
        dense_docs = []
        try:
            res = await self.vector_store.similarity_search(
                collection_name=collection_name,
                query=query,
                k=k * 2,
                filter=filter_dict or None,
            )
            dense_docs = res if res is not None else []
        except Exception as e:
            logger.warning("HybridRetriever | Dense search error: %s; relying on BM25", e)
            dense_docs = []

        # 2. Sparse BM25 Search
        def bm25_filter(doc: Document) -> bool:
            if not filter_dict:
                return True
            return all(doc.metadata.get(k) == v for k, v in filter_dict.items())

        bm25_results = self.bm25_index.search(query=query, k=k * 2, filter_fn=bm25_filter)

        # 3. Reciprocal Rank Fusion (RRF)
        # Map chunk_id / content -> doc, dense_rank, bm25_rank
        fused_scores: Dict[str, float] = {}
        doc_registry: Dict[str, Document] = {}

        # Dense ranking
        for rank, doc in enumerate(dense_docs):
            cid = doc.metadata.get("chunk_id") or doc.page_content[:50]
            doc_registry[cid] = doc
            fused_scores[cid] = fused_scores.get(cid, 0.0) + (self.dense_weight / (self.rrf_k + rank + 1))

        # BM25 ranking
        for rank, (doc, _) in enumerate(bm25_results):
            cid = doc.metadata.get("chunk_id") or doc.page_content[:50]
            doc_registry[cid] = doc
            fused_scores[cid] = fused_scores.get(cid, 0.0) + (self.bm25_weight / (self.rrf_k + rank + 1))

        # Sort by composite RRF score
        sorted_cids = sorted(fused_scores.keys(), key=lambda cid: fused_scores[cid], reverse=True)[:k]

        retrieved_chunks: List[RetrievedChunk] = []
        for cid in sorted_cids:
            doc = doc_registry[cid]
            score = fused_scores[cid]

            provenance = SourceProvenance(
                document_name=doc.metadata.get("document_name", "enterprise_knowledge"),
                chunk_id=doc.metadata.get("chunk_id", cid),
                collection_name=collection_name,
                score=round(score, 5),
                retrieval_method=RetrievalMethod.HYBRID_RRF,
                section_header=doc.metadata.get("section_header", "General"),
                metadata=doc.metadata,
            )

            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_id=provenance.chunk_id,
                    content=doc.page_content,
                    provenance=provenance,
                    epistemic_type=EpistemicType.RETRIEVED_EVIDENCE,
                )
            )

        logger.info(
            "HybridRetriever | Query '%s' retrieved %d candidates via RRF (Dense: %d, BM25: %d)",
            query[:40],
            len(retrieved_chunks),
            len(dense_docs),
            len(bm25_results),
        )
        return retrieved_chunks
