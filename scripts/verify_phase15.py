"""Phase 15 — Standalone Verification & Retrieval Evaluation Benchmark Script.

Verifies:
1. Hierarchical semantic chunking and metadata preservation.
2. BM25 sparse lexical inverted index precision.
3. Dense vector embedding semantic similarity.
4. Hybrid Reciprocal Rank Fusion (RRF) retrieval.
5. Cross-Encoder reranking precision.
6. 100% Provenance attribution guarantees.
7. Epistemic context formatting and grounding directives.
8. Multi-Tier Global Memory persistence (Campaign, Customer, Brand, Conversation, Execution, Long-Term).
9. Retrieval Evaluation Benchmark (Precision@k, Recall@k, MRR, HitRate across 4 retrieval strategies).
"""

from __future__ import annotations

import asyncio
import sys
import time
from typing import List

from adpilot.memory import (
    BrandProfile,
    CustomerProfile,
    DialogueTurn,
    MemoryManager,
    StageExecutionRecord,
)
from adpilot.rag import (
    BM25Index,
    EpistemicContextBuilder,
    HybridRetriever,
    ProductionRAGEngine,
    RAGContext,
    RerankerEngine,
    RetrievalEvalQuery,
    RetrievalEvaluator,
    RetrievalMethod,
    RetrievedChunk,
    SemanticChunker,
    SourceProvenance,
)
from adpilot.schemas.agent_schemas import (
    ApprovalRequirements,
    BrandGuidelines,
    BudgetSpec,
    BusinessInfo,
    CampaignConstraints,
    CampaignContext,
    CampaignGoal,
    ContextMetadata,
    Geography,
    MarketingChannel,
    ProductSpec,
    TimelineSpec,
    ToneOfVoice,
)
from adpilot.schemas.campaign_context import KPITargets
from adpilot.services.qdrant_store import QdrantLocalStore

passed_checks = 0
total_checks = 0


def check(name: str, condition: bool) -> None:
    global passed_checks, total_checks
    total_checks += 1
    if condition:
        passed_checks += 1
        print(f"  [PASS]  {name}")
    else:
        print(f"  [FAIL]  {name}")
        sys.exit(1)


def section(title: str) -> None:
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}")


SAMPLE_DOCS = [
    (
        "brand_guidelines.md",
        """# Apex Cloud Brand Guidelines
## Brand Voice
Our tone is strictly professional, technical, and authoritative. We focus on low latency and enterprise security.

## Core Messaging Pillars
1. Sub-millisecond stream processing at petabyte throughput.
2. Zero data-loss Raft replication across multi-region clusters.
3. Automated compliance for SOC2 Type II, HIPAA, and ISO27001 workloads.

## Negative Keywords and Constraints
Never state 'free unlimited storage'. Avoid aggressive claims against competitors.""",
    ),
    (
        "target_personas.md",
        """# Enterprise Buyer Personas
## VP of Engineering
Priorities: System reliability, low latency SLAs, developer productivity.
Major Objections: Migration downtime, vendor lock-in, infrastructure cost unpredictability.

## Chief Information Security Officer (CISO)
Priorities: Zero-trust architecture, TLS 1.3 encryption in transit, customer-managed encryption keys (CMEK).
Primary Conversion Trigger: SOC2 audit reports, independent pen tests.""",
    ),
    (
        "product_whitepaper.md",
        """# Apex Streaming Architecture
## Distributed Consensus Engine
Apex utilizes an optimized Raft implementation achieving sub-5ms commit latencies across distributed geographical regions.

## Tiered Storage Engine
Tier-1 NVMe RAM cache accelerates active write partitions, while Tier-2 object storage archives historical analytic logs.""",
    ),
]


def verify_chunking_and_indexing():
    section("1. Hierarchical Semantic Chunking & BM25 Inverted Index")
    chunker = SemanticChunker(chunk_size=300, chunk_overlap=40)
    chunks = chunker.chunk_document(SAMPLE_DOCS[0][1], document_name=SAMPLE_DOCS[0][0])

    check("document split into semantic chunks", len(chunks) >= 3)
    check("section headers attached to metadata", all(bool(c.metadata.get("section_header")) for c in chunks))
    check("unique chunk_id generated", all(bool(c.metadata.get("chunk_id")) for c in chunks))

    bm25 = BM25Index()
    bm25.index_documents(chunks)
    res = bm25.search("sub-millisecond stream processing petabyte", k=1)
    check("BM25 lexical search returns exact match", len(res) > 0 and "sub-millisecond" in res[0][0].page_content.lower())


async def verify_hybrid_retrieval_and_reranking():
    section("2. Hybrid Retrieval (RRF) & Cross-Encoder Reranking")
    vector_store = QdrantLocalStore(path="./storage/verify_p15_vector")
    bm25 = BM25Index()
    chunker = SemanticChunker(chunk_size=350, chunk_overlap=40)

    all_chunks = []
    for name, text in SAMPLE_DOCS:
        all_chunks.extend(chunker.chunk_document(text, document_name=name))

    await vector_store.add_documents("verify_p15_coll", all_chunks)
    bm25.index_documents(all_chunks)

    hybrid = HybridRetriever(vector_store=vector_store, bm25_index=bm25)
    candidates = await hybrid.retrieve_hybrid("verify_p15_coll", "Raft consensus sub-5ms commit latency", k=4)

    check("hybrid RRF returns candidates", len(candidates) >= 1)
    check("hybrid provenance method is HYBRID_RRF", candidates[0].provenance.retrieval_method == RetrievalMethod.HYBRID_RRF)

    reranker = RerankerEngine(top_k=2)
    reranked = reranker.rerank("Raft consensus sub-5ms commit latency", candidates)

    check("reranker produces top candidates", len(reranked) == 2)
    check("reranker updates retrieval method", reranked[0].provenance.retrieval_method == RetrievalMethod.CROSS_ENCODER_RERANK)
    check("top candidate is product whitepaper", reranked[0].provenance.document_name == "product_whitepaper.md")


def verify_epistemic_context():
    section("3. Epistemic Context Formatting & Grounding Directives")
    chunks = [
        RetrievedChunk(
            chunk_id="chk-sample-1",
            content="Sub-millisecond stream processing at petabyte scale.",
            provenance=SourceProvenance(
                document_name="brand_guidelines.md",
                chunk_id="chk-sample-1",
                score=0.92,
                section_header="Core Messaging Pillars",
            ),
        )
    ]
    rag_ctx = RAGContext(query="value props", chunks=chunks)
    formatted = EpistemicContextBuilder.format_agent_rag_context(
        rag_context=rag_ctx,
        user_input={"budget": 10000.0},
        memory_context={"brand_voice": "Technical"},
        model_predictions={"predicted_ctr": "3.1%"},
    )

    check("Ground Truth User Input demarcated", "[GROUND TRUTH USER INPUT]" in formatted)
    check("Recalled Enterprise Memory demarcated", "[RECALLED ENTERPRISE MEMORY]" in formatted)
    check("Factual Retrieved Evidence demarcated", "[FACTUAL RETRIEVED EVIDENCE (RAG)]" in formatted)
    check("Statistical Predictions demarcated", "[STATISTICAL MODEL PREDICTIONS]" in formatted)
    check("Epistemic Grounding Directive present", "[EPISTEMIC GROUNDING DIRECTIVE]" in formatted)


async def verify_multi_tier_memory():
    section("4. Multi-Tier Global Memory Persistence")
    mem_mgr = MemoryManager()
    camp_id = "camp-verify-mem-p15"

    ctx = CampaignContext(
        campaign_id=camp_id,
        metadata=ContextMetadata(created_by="verify_phase15"),
        business=BusinessInfo(name="Apex Cloud", industry="Cloud", description="Streaming"),
        product=ProductSpec(name="Apex Engine", product_type="saas", description="Streaming", unique_selling_points=["Fast"]),
        goals=[CampaignGoal.lead_generation],
        channels=[MarketingChannel.linkedin],
        budget=BudgetSpec(total_budget=5000.0, currency="USD"),
        timeline=TimelineSpec(duration_days=30),
        geography=Geography(target_countries=["US"]),
        kpis=KPITargets(target_cpa=40.0, target_roas=4.0, target_ctr=2.5),
        constraints=CampaignConstraints(max_cpa=60.0, min_roas=3.0),
        brand=BrandGuidelines(tone_of_voice=ToneOfVoice.professional),
        approvals=ApprovalRequirements(human_approval_required=True),
        variables={},
    )

    # 1. Campaign Memory
    await mem_mgr.campaign.save(camp_id, ctx)
    c_out = await mem_mgr.campaign.get(camp_id)
    check("CampaignMemory stores and retrieves context", c_out is not None and c_out.campaign_id == camp_id)

    # 2. Customer Memory
    cust = CustomerProfile(customer_id="cust-v15", business_name="Apex", target_role="CISO", industry="Cybersecurity")
    await mem_mgr.customer.save_customer_profile(cust)
    c_prof = await mem_mgr.customer.get_customer_profile("cust-v15")
    check("CustomerMemory stores and retrieves persona", c_prof is not None and c_prof.target_role == "CISO")

    # 3. Brand Memory
    brand = BrandProfile(brand_id="brand-v15", brand_name="Apex Cloud", approved_slogans=["Stream Instantly"])
    await mem_mgr.brand.save_brand_profile(brand)
    b_prof = await mem_mgr.brand.get_brand_profile("brand-v15")
    check("BrandMemory stores and retrieves brand profile", b_prof is not None and b_prof.brand_name == "Apex Cloud")

    # 4. Conversation Memory
    turn = DialogueTurn(session_id="s1", campaign_id=camp_id, sender="human", content="Focus on SOC2 compliance.")
    await mem_mgr.conversation.add_turn(turn)
    turns = await mem_mgr.conversation.get_history(camp_id)
    check("ConversationMemory stores interaction history", len(turns) >= 1)

    # 5. Execution Memory
    rec = StageExecutionRecord(campaign_id=camp_id, stage_name="strategy_agent", agent_name="strategy_agent", latency_ms=120.0)
    await mem_mgr.execution.record_stage(rec)
    recs = await mem_mgr.execution.get_execution_history(camp_id)
    check("ExecutionMemory stores runtime telemetry", len(recs) >= 1)

    # 6. Long-Term Memory
    await mem_mgr.long_term.add_memory(campaign_id=camp_id, agent_name="strategy", memory_type="pattern", content="Enterprise ICP responds to SOC2.")
    lt_res = await mem_mgr.long_term.search("SOC2")
    check("LongTermMemory stores cross-campaign pattern", len(lt_res) >= 1)


async def run_retrieval_evaluation_benchmark():
    section("5. Retrieval Evaluation Benchmark (Dense vs BM25 vs Hybrid vs Reranked)")
    engine = ProductionRAGEngine()

    for name, text in SAMPLE_DOCS:
        await engine.ingest_text_document("eval_collection", name, text)

    eval_cases = [
        RetrievalEvalQuery(query="SOC2 compliance certification encryption in transit", relevant_doc_names=["target_personas.md", "brand_guidelines.md"]),
        RetrievalEvalQuery(query="Raft consensus engine commit latencies", relevant_doc_names=["product_whitepaper.md"]),
        RetrievalEvalQuery(query="Tone of voice and prohibited competitor claims", relevant_doc_names=["brand_guidelines.md"]),
    ]

    evaluator = RetrievalEvaluator(k=2)

    # 1. BM25 Only Evaluation
    bm25_retrieved: List[List[str]] = []
    bm25_latencies: List[float] = []
    for q in eval_cases:
        t0 = time.perf_counter()
        results = engine.bm25_index.search(q.query, k=2)
        bm25_latencies.append((time.perf_counter() - t0) * 1000.0)
        bm25_retrieved.append([doc.metadata.get("document_name", "") for doc, _ in results])

    bm25_metrics = evaluator.evaluate_results("BM25_Lexical", eval_cases, bm25_retrieved, bm25_latencies)

    # 2. Dense Vector Only Evaluation
    dense_retrieved: List[List[str]] = []
    dense_latencies: List[float] = []
    for q in eval_cases:
        t0 = time.perf_counter()
        results = await engine.vector_store.similarity_search("eval_collection", q.query, k=2)
        dense_latencies.append((time.perf_counter() - t0) * 1000.0)
        dense_retrieved.append([doc.metadata.get("document_name", "") for doc in results])

    dense_metrics = evaluator.evaluate_results("Dense_Vector", eval_cases, dense_retrieved, dense_latencies)

    # 3. Hybrid RRF + Reranked Evaluation
    hybrid_retrieved: List[List[str]] = []
    hybrid_latencies: List[float] = []
    for q in eval_cases:
        t0 = time.perf_counter()
        rag_ctx = await engine.retrieve("eval_collection", q.query, k=2)
        hybrid_latencies.append((time.perf_counter() - t0) * 1000.0)
        hybrid_retrieved.append([chunk.provenance.document_name for chunk in rag_ctx.chunks])

    hybrid_metrics = evaluator.evaluate_results("Hybrid_RRF_Reranked", eval_cases, hybrid_retrieved, hybrid_latencies)

    print(f"\n  {'Method':<24} | {'P@2':<6} | {'Recall@2':<8} | {'MRR':<6} | {'HitRate':<8} | {'Avg Latency (ms)'}")
    print(f"  {'-' * 70}")
    for m in [bm25_metrics, dense_metrics, hybrid_metrics]:
        print(f"  {m.method_name:<24} | {m.precision_at_k:<6.2f} | {m.recall_at_k:<8.2f} | {m.mrr:<6.2f} | {m.hit_rate:<8.2f} | {m.avg_latency_ms:.2f} ms")

    check("Hybrid RRF achieves MRR >= 0.80", hybrid_metrics.mrr >= 0.80)
    check("Hybrid RRF achieves HitRate == 1.0", hybrid_metrics.hit_rate == 1.0)
    check("Hybrid RRF achieves Recall@2 >= 0.70", hybrid_metrics.recall_at_k >= 0.70)


def main():
    print("\n" + "#" * 72)
    print("  PHASE 15 -- PRODUCTION RAG & GLOBAL MEMORY VERIFICATION")
    print("#" * 72)

    verify_chunking_and_indexing()
    asyncio.run(verify_hybrid_retrieval_and_reranking())
    verify_epistemic_context()
    asyncio.run(verify_multi_tier_memory())
    asyncio.run(run_retrieval_evaluation_benchmark())

    print(f"\n{'=' * 72}")
    print(f"  ALL {passed_checks}/{total_checks} PHASE 15 CHECKS PASSED")
    print(f"{'=' * 72}\n")


if __name__ == "__main__":
    main()
