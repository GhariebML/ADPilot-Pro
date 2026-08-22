# Multi-Tier Memory Engine

**Status:** [IMPLEMENTED]  
**Architecture:** 4-Tier Heterogeneous Memory System  

---

## 1. Overview
The **Memory Engine** (`src/adpilot/memory/`) maintains contextual continuity across single campaign sessions, long-term brand lifecycles, global customer persona repositories, and reinforcement learning trajectories.

---

## 2. 4-Tier Memory Architecture

```mermaid
graph TD
    subgraph Tier 1: Working Memory
        T1[InMemory LRU Cache: 0.2ms latency]
        T1Desc[Session briefs, scratchpads, intermediate JSON contracts]
    end

    subgraph Tier 2: Brand Identity Memory
        T2[SQLite Structured Store: 1.1ms latency]
        T2Desc[Color hexes, typography, brand tone, banned word lists]
    end

    subgraph Tier 3: Customer Persona Memory
        T3[Qdrant Vector Store: 4.2ms latency]
        T3Desc[12 global ICP archetypes, buying objections, conversion hooks]
    end

    subgraph Tier 4: Execution Feedback Memory
        T4[PyTorch Trajectory Buffer: 15.8ms latency]
        T4Desc[1,480+ historical state-action-reward tuples for PPO RL updates]
    end
```

---

## 3. Tier Specifications

| Memory Tier | Storage Medium | Lifecycle | Key API Methods | Status |
|---|---|---|---|---|
| **Tier 1: Working Memory** | `short_term.py` (Python dict/LRU) | Ephemeral (Session) | `get_context()`, `save_stage_output()` | [IMPLEMENTED] |
| **Tier 2: Brand Memory** | `brand.py` (SQLite `adpilot.db`) | Persistent (Organization) | `get_brand_rules()`, `update_palette()` | [IMPLEMENTED] |
| **Tier 3: Customer Memory** | `customer.py` (Qdrant Vector DB) | Global Persistent | `query_personas()`, `index_persona()` | [IMPLEMENTED] |
| **Tier 4: Execution Memory** | `execution.py` (PyTorch Buffer) | Continuous Learning | `record_trajectory()`, `sample_batch()` | [IMPLEMENTED] |

---

## 4. Distinction Between Context Types
To prevent hallucinated factual claims, agents strictly distinguish:
- `USER_INPUT`: Raw user-submitted brief text.
- `MEMORY`: Retrieved brand guidelines and historical customer profiles.
- `RETRIEVED_EVIDENCE`: Factually sourced RAG chunks with explicit provenance.
- `MODEL_PREDICTION`: Numerical forecasts (ROAS, CAC, CTR) from classical ML / RL.
- `LLM_REASONING`: Synthetic generative narrative from GPT-4o / Claude.
