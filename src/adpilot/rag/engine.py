"""Production RAG Engine orchestrating Ingestion, Chunking, Hybrid Retrieval, Reranking, and Context Assembly."""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional
from langchain_core.documents import Document

from ..services.document_loader import DocumentLoaderService
from ..services.qdrant_store import BaseQdrantStore, QdrantLocalStore
from .bm25 import BM25Index
from .chunker import SemanticChunker
from .epistemic import EpistemicContextBuilder
from .hybrid import HybridRetriever
from .reranker import RerankerEngine
from .schemas import RAGContext, RetrievedChunk

logger = logging.getLogger(__name__)


class ProductionRAGEngine:
    """Enterprise RAG pipeline managing Ingestion, Semantic Chunking, Dense Vector + BM25 Hybrid Retrieval, and Reranking."""

    def __init__(
        self,
        vector_store: Optional[BaseQdrantStore] = None,
        bm25_index: Optional[BM25Index] = None,
        chunker: Optional[SemanticChunker] = None,
        reranker: Optional[RerankerEngine] = None,
    ) -> None:
        self.vector_store = vector_store or QdrantLocalStore(path="./storage/qdrant_rag")
        self.bm25_index = bm25_index or BM25Index()
        self.chunker = chunker or SemanticChunker()
        self.reranker = reranker or RerankerEngine()
        self.hybrid_retriever = HybridRetriever(
            vector_store=self.vector_store,
            bm25_index=self.bm25_index,
        )
        self.all_indexed_documents: List[Document] = []

    async def ingest_text_document(
        self,
        collection_name: str,
        document_name: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """Chunks, embeds, and indexes a raw text document across Dense Vector store and BM25 index."""
        # 1. Semantic Chunking
        chunks = self.chunker.chunk_document(
            text=text,
            document_name=document_name,
            base_metadata=metadata,
        )

        if not chunks:
            return []

        # 2. Add to Vector Store
        await self.vector_store.add_documents(collection_name=collection_name, documents=chunks)

        # 3. Add to BM25 Index
        self.all_indexed_documents.extend(chunks)
        self.bm25_index.index_documents(self.all_indexed_documents)

        logger.info(
            "ProductionRAGEngine | Ingested '%s' into collection '%s' (%d chunks)",
            document_name,
            collection_name,
            len(chunks),
        )
        return chunks

    async def ingest_file(
        self,
        collection_name: str,
        file_path: str,
        document_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """Loads a file from disk, chunks, embeds, and indexes it."""
        doc_loader = DocumentLoaderService()
        doc_name = document_name or file_path.split("/")[-1].split("\\")[-1]

        raw_docs = doc_loader.load_document(file_path)
        combined_text = "\n\n".join(d.page_content for d in raw_docs)
        return await self.ingest_text_document(
            collection_name=collection_name,
            document_name=doc_name,
            text=combined_text,
            metadata=metadata,
        )

    async def retrieve(
        self,
        collection_name: str,
        query: str,
        k: int = 4,
        filter_dict: Optional[Dict[str, Any]] = None,
        user_input: Optional[Dict[str, Any]] = None,
        memory_context: Optional[Dict[str, Any]] = None,
        model_predictions: Optional[Dict[str, Any]] = None,
    ) -> RAGContext:
        """Executes Hybrid Retrieval (Dense + BM25), Cross-Encoder Reranking, and formats Epistemic Context."""
        start_time = time.perf_counter()

        # 1. Hybrid RRF Retrieval
        candidates: List[RetrievedChunk] = await self.hybrid_retriever.retrieve_hybrid(
            collection_name=collection_name,
            query=query,
            k=k * 2,
            filter_dict=filter_dict,
        )

        # 2. Cross-Encoder Reranking
        reranked_chunks: List[RetrievedChunk] = self.reranker.rerank(query=query, candidates=candidates)[:k]

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        # 3. Assemble Epistemic Context
        temp_ctx = RAGContext(
            query=query,
            chunks=reranked_chunks,
            attribution_summary=EpistemicContextBuilder.build_attribution_summary(reranked_chunks),
            retrieval_latency_ms=round(latency_ms, 2),
        )

        formatted_text = EpistemicContextBuilder.format_agent_rag_context(
            rag_context=temp_ctx,
            user_input=user_input,
            memory_context=memory_context,
            model_predictions=model_predictions,
        )
        temp_ctx.formatted_context = formatted_text

        return temp_ctx
