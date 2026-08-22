"""Retrieval Evaluation Engine benchmarking Precision@K, Recall@K, MRR, and Hybrid gains."""

from __future__ import annotations

import logging
from typing import Dict, List
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class RetrievalEvalQuery(BaseModel):
    """Ground truth evaluation test case."""
    query: str
    relevant_doc_names: List[str]
    relevant_keywords: List[str] = Field(default_factory=list)


class MethodEvaluationResult(BaseModel):
    """Evaluation metrics for a specific retrieval strategy."""
    method_name: str
    precision_at_k: float
    recall_at_k: float
    mrr: float
    hit_rate: float
    avg_latency_ms: float


class RAGEvaluationReport(BaseModel):
    """Comprehensive comparative retrieval benchmark report."""
    total_queries: int
    k: int
    results_by_method: Dict[str, MethodEvaluationResult]
    summary: str


class RetrievalEvaluator:
    """Computes ranking metrics (Precision@K, Recall@K, MRR, HitRate) to evaluate retrieval quality."""

    def __init__(self, k: int = 3) -> None:
        self.k = k

    def evaluate_results(
        self,
        method_name: str,
        eval_cases: List[RetrievalEvalQuery],
        retrieved_results: List[List[str]],  # List of retrieved document names per query
        latencies_ms: List[float],
    ) -> MethodEvaluationResult:
        """Evaluates a batch of retrieved candidate lists against ground-truth test cases."""
        total_queries = len(eval_cases)
        if total_queries == 0:
            return MethodEvaluationResult(
                method_name=method_name,
                precision_at_k=0.0,
                recall_at_k=0.0,
                mrr=0.0,
                hit_rate=0.0,
                avg_latency_ms=0.0,
            )

        precisions = []
        recalls = []
        reciprocal_ranks = []
        hits = 0

        for query_case, retrieved in zip(eval_cases, retrieved_results):
            top_k_retrieved = retrieved[:self.k]
            relevant_set = set(query_case.relevant_doc_names)

            # Precision@K
            matched = [doc for doc in top_k_retrieved if doc in relevant_set]
            p_k = len(matched) / max(1, len(top_k_retrieved))
            precisions.append(p_k)

            # Recall@K
            r_k = len(matched) / max(1, len(relevant_set))
            recalls.append(r_k)

            # MRR (Mean Reciprocal Rank)
            first_rank = None
            for rank, doc in enumerate(top_k_retrieved, 1):
                if doc in relevant_set:
                    first_rank = rank
                    break
            
            if first_rank:
                reciprocal_ranks.append(1.0 / first_rank)
                hits += 1
            else:
                reciprocal_ranks.append(0.0)

        avg_p = round(sum(precisions) / total_queries, 4)
        avg_r = round(sum(recalls) / total_queries, 4)
        avg_mrr = round(sum(reciprocal_ranks) / total_queries, 4)
        hit_rate = round(hits / total_queries, 4)
        avg_latency = round(sum(latencies_ms) / max(1, len(latencies_ms)), 2)

        return MethodEvaluationResult(
            method_name=method_name,
            precision_at_k=avg_p,
            recall_at_k=avg_r,
            mrr=avg_mrr,
            hit_rate=hit_rate,
            avg_latency_ms=avg_latency,
        )
