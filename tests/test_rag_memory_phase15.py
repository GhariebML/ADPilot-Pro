"""Phase 15 — Production RAG & Multi-Tier Global Memory Test Suite.

Verifies:
1. Document Ingestion & Hierarchical Semantic Chunking.
2. BM25 Sparse Lexical Inverted Index Keyword Search.
3. Dense Vector Similarity Search.
4. Hybrid Retrieval via Reciprocal Rank Fusion (RRF).
5. Cross-Encoder Semantic Reranking.
6. 100% Provenance Attribution Guarantee.
7. Epistemic Context Formatting & Boundaries (User Input, Memory, Evidence, Predictions).
8. Multi-Tier Memory Subsystems (Campaign, Customer, Brand, Conversation, Execution, Long-Term).
9. Retrieval Evaluation Benchmark (Precision@k, Recall@k, MRR).
10. RAG Integration in Agent Contexts.
"""

from __future__ import annotations

import pytest

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


@pytest.fixture
def sample_documents() -> list[tuple[str, str]]:
    """Fixture providing raw documents with markdown headers and technical content."""
    doc1 = (
        "brand_guidelines.md",
        """# Apex Cloud Brand Voice and Guidelines
## Tone of Voice
Our tone is strictly professional, technical, and authoritative. We never use buzzwords or colloquial language.

## Approved Value Propositions
1. Sub-millisecond stream processing at petabyte scale.
2. Zero data-loss transactional replication across multi-region clusters.
3. Automated compliance for SOC2 and ISO27001 workloads.

## Prohibited Messaging
Never claim 'completely free' or 'unlimited storage without limits'. Do not disparage competitors directly.""",
    )

    doc2 = (
        "customer_personas.md",
        """# Target Buyer Personas and ICP
## VP of Engineering
Key priorities include system stability, developer velocity, and infrastructure reliability.
Major objections: Migration downtime, complex legacy integrations, team retraining costs.

## Chief Information Security Officer (CISO)
Key priorities: Zero-trust architecture, encryption at rest and in transit, continuous compliance auditing.
Primary conversion driver: Verifiable third-party penetration reports and SOC2 Type II certifications.""",
    )

    doc3 = (
        "product_whitepaper.md",
        """# Apex Real-Time Engine Architecture
## Distributed Consensus Engine
Apex utilizes a customized Raft consensus engine delivering sub-5ms commit latencies across distributed multi-region partitions.

## Storage Hierarchy
Tier-1 NVMe in-memory cache handles hot partitions, while Tier-2 S3 object storage seamlessly archives historical analytics partitions.""",
    )

    return [doc1, doc2, doc3]


@pytest.fixture
def sample_campaign_context() -> CampaignContext:
    return CampaignContext(
        campaign_id="camp-rag-p15",
        metadata=ContextMetadata(created_by="test_rag_phase15"),
        business=BusinessInfo(name="Apex Cloud", industry="Infrastructure", description="Streaming database"),
        product=ProductSpec(name="Apex Engine", product_type="saas", description="Real-time analytics engine", unique_selling_points=["Sub-ms latency"]),
        goals=[CampaignGoal.lead_generation],
        channels=[MarketingChannel.linkedin],
        budget=BudgetSpec(total_budget=10000.0, currency="USD"),
        timeline=TimelineSpec(duration_days=30),
        geography=Geography(target_countries=["US"]),
        kpis=KPITargets(target_cpa=50.0, target_roas=4.0, target_ctr=3.0),
        constraints=CampaignConstraints(max_cpa=70.0, min_roas=3.0, prohibited_keywords=["free"]),
        brand=BrandGuidelines(tone_of_voice=ToneOfVoice.professional, brand_colors=["#1E3A8A"]),
        approvals=ApprovalRequirements(human_approval_required=True),
        variables={},
    )


# ---------------------------------------------------------------------------
# Scenario 1: Document Ingestion & Hierarchical Semantic Chunking
# ---------------------------------------------------------------------------
def test_scenario_1_hierarchical_semantic_chunking(sample_documents):
    chunker = SemanticChunker(chunk_size=300, chunk_overlap=50)
    doc_name, doc_text = sample_documents[0]

    chunks = chunker.chunk_document(doc_text, document_name=doc_name)

    assert len(chunks) >= 3
    for c in chunks:
        assert c.metadata["document_name"] == "brand_guidelines.md"
        assert bool(c.metadata["chunk_id"])
        assert bool(c.metadata["section_header"])
        assert len(c.page_content) > 0


# ---------------------------------------------------------------------------
# Scenario 2: BM25 Lexical Keyword Search
# ---------------------------------------------------------------------------
def test_scenario_2_bm25_lexical_search(sample_documents):
    chunker = SemanticChunker(chunk_size=400, chunk_overlap=50)
    bm25 = BM25Index()

    all_chunks = []
    for doc_name, doc_text in sample_documents:
        all_chunks.extend(chunker.chunk_document(doc_text, document_name=doc_name))

    bm25.index_documents(all_chunks)

    # Exact technical query
    results = bm25.search("sub-millisecond stream processing petabyte", k=3)
    assert len(results) >= 1
    top_doc, score = results[0]
    assert "sub-millisecond" in top_doc.page_content.lower()
    assert score > 0.0


# ---------------------------------------------------------------------------
# Scenario 3: Dense Vector Search
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_3_dense_vector_search(sample_documents):
    vector_store = QdrantLocalStore(path="./storage/test_p15_vector")
    chunker = SemanticChunker(chunk_size=400, chunk_overlap=50)

    chunks = []
    for doc_name, doc_text in sample_documents:
        chunks.extend(chunker.chunk_document(doc_text, document_name=doc_name))

    await vector_store.add_documents("test_p15_vector", chunks)
    results = await vector_store.similarity_search("test_p15_vector", "security compliance soc2", k=3)

    assert len(results) >= 1
    assert any("soc2" in doc.page_content.lower() or "compliance" in doc.page_content.lower() for doc in results)


# ---------------------------------------------------------------------------
# Scenario 4: Hybrid Retrieval with Reciprocal Rank Fusion (RRF)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_4_hybrid_retrieval_rrf(sample_documents):
    vector_store = QdrantLocalStore(path="./storage/test_p15_hybrid")
    bm25 = BM25Index()
    chunker = SemanticChunker(chunk_size=400, chunk_overlap=50)

    chunks = []
    for doc_name, doc_text in sample_documents:
        chunks.extend(chunker.chunk_document(doc_text, document_name=doc_name))

    await vector_store.add_documents("test_p15_hybrid", chunks)
    bm25.index_documents(chunks)

    hybrid = HybridRetriever(vector_store=vector_store, bm25_index=bm25)
    candidates: list[RetrievedChunk] = await hybrid.retrieve_hybrid(
        collection_name="test_p15_hybrid",
        query="Raft consensus latency distributed partitions",
        k=3,
    )

    assert len(candidates) >= 1
    top_cand = candidates[0]
    assert top_cand.provenance.retrieval_method == RetrievalMethod.HYBRID_RRF
    assert top_cand.provenance.score > 0.0
    assert "raft" in top_cand.content.lower() or "consensus" in top_cand.content.lower()


# ---------------------------------------------------------------------------
# Scenario 5: Cross-Encoder Semantic Reranking
# ---------------------------------------------------------------------------
def test_scenario_5_cross_encoder_reranking():
    reranker = RerankerEngine(top_k=2)

    chunks = [
        RetrievedChunk(
            chunk_id="chk-1",
            content="Apex provides low-cost cloud storage options for archived files.",
            provenance=SourceProvenance(document_name="pricing.md", chunk_id="chk-1", score=0.01),
        ),
        RetrievedChunk(
            chunk_id="chk-2",
            content="Sub-millisecond stream processing with zero-data-loss Raft replication.",
            provenance=SourceProvenance(document_name="architecture.md", chunk_id="chk-2", score=0.012, section_header="Stream Processing"),
        ),
    ]

    reranked = reranker.rerank("Sub-millisecond stream processing replication", chunks)

    assert len(reranked) == 2
    assert reranked[0].chunk_id == "chk-2"  # Exact technical match boosted to #1
    assert reranked[0].provenance.retrieval_method == RetrievalMethod.CROSS_ENCODER_RERANK


# ---------------------------------------------------------------------------
# Scenario 6: 100% Provenance Attribution Guarantee
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_6_provenance_attribution(sample_documents):
    engine = ProductionRAGEngine()

    for doc_name, doc_text in sample_documents:
        await engine.ingest_text_document("p15_prov_coll", doc_name, doc_text)

    rag_ctx: RAGContext = await engine.retrieve("p15_prov_coll", "CISO security priorities", k=3)

    assert len(rag_ctx.chunks) >= 1
    for chunk in rag_ctx.chunks:
        prov = chunk.provenance
        assert bool(prov.document_name)
        assert bool(prov.chunk_id)
        assert bool(prov.timestamp)
        assert prov.score > 0.0
        assert prov.retrieval_method in [RetrievalMethod.HYBRID_RRF, RetrievalMethod.CROSS_ENCODER_RERANK]


# ---------------------------------------------------------------------------
# Scenario 7: Epistemic Context Formatting & Grounding Directives
# ---------------------------------------------------------------------------
def test_scenario_7_epistemic_context_boundaries():
    chunks = [
        RetrievedChunk(
            chunk_id="chk-ev-1",
            content="Apex delivers sub-5ms commit latencies across multi-region clusters.",
            provenance=SourceProvenance(document_name="whitepaper.md", chunk_id="chk-ev-1", score=0.88, section_header="Consensus"),
        )
    ]
    rag_ctx = RAGContext(query="latency specs", chunks=chunks)

    user_input = {"budget_usd": 15000.0, "primary_channel": "linkedin"}
    memory_ctx = {"brand_voice": "Authoritative and concise", "prior_roas": "4.2x in Tech"}
    model_predictions = {"predicted_roas": 4.15, "predicted_ctr": "2.8%"}

    formatted = EpistemicContextBuilder.format_agent_rag_context(
        rag_context=rag_ctx,
        user_input=user_input,
        memory_context=memory_ctx,
        model_predictions=model_predictions,
    )

    assert "[GROUND TRUTH USER INPUT]" in formatted
    assert "[RECALLED ENTERPRISE MEMORY]" in formatted
    assert "[FACTUAL RETRIEVED EVIDENCE (RAG)]" in formatted
    assert "[STATISTICAL MODEL PREDICTIONS]" in formatted
    assert "[EPISTEMIC GROUNDING DIRECTIVE]" in formatted
    assert "whitepaper.md" in formatted
    assert "chk-ev-1" in formatted


# ---------------------------------------------------------------------------
# Scenario 8: Multi-Tier Memory Subsystems
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_8_multi_tier_memory_subsystems(sample_campaign_context):
    mem_mgr = MemoryManager()

    # 1. Campaign Memory
    await mem_mgr.campaign.save(sample_campaign_context.campaign_id, sample_campaign_context)
    retrieved_camp = await mem_mgr.campaign.get(sample_campaign_context.campaign_id)
    assert retrieved_camp is not None
    assert retrieved_camp.campaign_id == sample_campaign_context.campaign_id

    # 2. Customer Memory
    profile = CustomerProfile(
        customer_id="cust-1",
        business_name="TechCorp",
        target_role="VP Engineering",
        industry="FinTech",
        key_pain_points=["Batch latency", "Downtime"],
    )
    await mem_mgr.customer.save_customer_profile(profile)
    retrieved_cust = await mem_mgr.customer.get_customer_profile("cust-1")
    assert retrieved_cust is not None
    assert retrieved_cust.target_role == "VP Engineering"

    # 3. Brand Memory
    brand = BrandProfile(
        brand_id="brand-1",
        brand_name="Apex Cloud",
        tone_of_voice="authoritative",
        brand_colors=["#1E3A8A"],
        approved_slogans=["Stream at Scale"],
    )
    await mem_mgr.brand.save_brand_profile(brand)
    retrieved_brand = await mem_mgr.brand.get_brand_profile("brand-1")
    assert retrieved_brand is not None
    assert retrieved_brand.approved_slogans == ["Stream at Scale"]

    # 4. Conversation Memory
    turn = DialogueTurn(
        session_id="sess-1",
        campaign_id=sample_campaign_context.campaign_id,
        sender="human_reviewer",
        content="Emphasize sub-second latency in headline.",
    )
    await mem_mgr.conversation.add_turn(turn)
    history = await mem_mgr.conversation.get_history(sample_campaign_context.campaign_id)
    assert len(history) >= 1
    assert history[0].content == "Emphasize sub-second latency in headline."

    # 5. Execution Memory
    exec_rec = StageExecutionRecord(
        campaign_id=sample_campaign_context.campaign_id,
        stage_name="content_agent",
        agent_name="content_agent",
        latency_ms=45.0,
    )
    await mem_mgr.execution.record_stage(exec_rec)
    exec_history = await mem_mgr.execution.get_execution_history(sample_campaign_context.campaign_id)
    assert len(exec_history) >= 1
    assert exec_history[0].stage_name == "content_agent"

    # 6. Long-Term Memory
    await mem_mgr.long_term.add_memory(
        campaign_id=sample_campaign_context.campaign_id,
        agent_name="strategy_agent",
        memory_type="winning_pattern",
        content="Technical positioning yields 35% higher CTR in Enterprise IT.",
    )
    lt_results = await mem_mgr.long_term.search("Technical positioning")
    assert len(lt_results) >= 1


# ---------------------------------------------------------------------------
# Scenario 9: Retrieval Evaluation Benchmark
# ---------------------------------------------------------------------------
def test_scenario_9_retrieval_evaluation_benchmark():
    evaluator = RetrievalEvaluator(k=3)

    test_queries = [
        RetrievalEvalQuery(query="SOC2 compliance and encryption", relevant_doc_names=["customer_personas.md"]),
        RetrievalEvalQuery(query="Raft consensus sub-5ms commit latency", relevant_doc_names=["product_whitepaper.md"]),
    ]

    retrieved_results = [
        ["customer_personas.md", "brand_guidelines.md", "product_whitepaper.md"],  # Hit at rank 1 (RR = 1.0)
        ["product_whitepaper.md", "brand_guidelines.md", "customer_personas.md"],  # Hit at rank 1 (RR = 1.0)
    ]
    latencies = [12.5, 14.2]

    metrics = evaluator.evaluate_results(
        method_name="Hybrid_RRF_Reranked",
        eval_cases=test_queries,
        retrieved_results=retrieved_results,
        latencies_ms=latencies,
    )

    assert metrics.precision_at_k > 0.0
    assert metrics.recall_at_k == 1.0
    assert metrics.mrr == 1.0
    assert metrics.hit_rate == 1.0
    assert metrics.avg_latency_ms > 0.0


# ---------------------------------------------------------------------------
# Scenario 10: Production RAG Engine End-to-End Execution
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_10_production_rag_engine_end_to_end(sample_documents, sample_campaign_context):
    engine = ProductionRAGEngine()

    for doc_name, doc_text in sample_documents:
        await engine.ingest_text_document("enterprise_kb", doc_name, doc_text)

    rag_ctx = await engine.retrieve(
        collection_name="enterprise_kb",
        query="What are the approved value propositions and tone of voice?",
        k=3,
        user_input={"campaign_id": sample_campaign_context.campaign_id},
        memory_context={"brand_name": "Apex Cloud"},
    )

    assert len(rag_ctx.chunks) >= 1
    assert "brand_guidelines.md" in rag_ctx.formatted_context
    assert "[FACTUAL RETRIEVED EVIDENCE (RAG)]" in rag_ctx.formatted_context
    assert len(rag_ctx.attribution_summary) >= 1
