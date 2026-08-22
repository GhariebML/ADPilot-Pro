# Vector Database & Embeddings Architecture

**Status:** [IMPLEMENTED]  
**Vector Engine:** Qdrant (`qdrant-client`) / FastEmbed BGE  
**Storage Path:** `storage/qdrant_rag/` (Persistent disk) or In-Memory Local fallback  

---

## 1. Overview
ADPilot Pro uses **Qdrant** as its primary vector store for RAG evidence retrieval and Customer Persona memory indexing.

---

## 2. Vector Collection Specifications

| Collection Name | Vector Dimension | Distance Metric | Managed Content |
|---|---|---|---|
| `adpilot_rag_knowledge` | 384-d Dense | Cosine Similarity | B2B SaaS playbooks, ad copy guidelines, competitor dossiers |
| `customer_personas` | 384-d Dense | Cosine Similarity | 12 Global buyer persona archetypes and objection patterns |
| `creative_embeddings` | 512-d Dense | Cosine Similarity | CLIP-ViT visual embeddings of benchmark ad creatives |

---

## 3. Embedding Pipeline (`src/adpilot/services/embedding_service.py`)

- **Model:** `BAAI/bge-small-en-v1.5` (via `fastembed`)
- **Normalized Vectors:** All output tensors are L2-normalized:
  $$\|\mathbf{v}\|_2 = 1.0 \implies \text{CosineSimilarity}(\mathbf{u}, \mathbf{v}) = \mathbf{u} \cdot \mathbf{v}$$
- **Batch Processing:** Chunks are embedded in parallel batches of 32 vectors.
- **Latency:** `23.3ms` per query embedding.
