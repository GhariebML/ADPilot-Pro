# Production Model Registry

**Status:** [IMPLEMENTED]  

---

## 1. Unified Model Registry Table

| Model Identifier | Intelligence Type | Responsible Agent | Input Schema | Output Schema | Training Method | Inference Latency | Production Status |
|---|---|---|---|---|---|---|---|
| **`ppo_policy.pt`** | Reinforcement Learning | `OptimizationAgent` | 12-dim continuous state $\mathbf{s}_t$ | 4-dim Dirichlet $\boldsymbol{\alpha}$ parameters | PyTorch PPO (Actor-Critic) | `15.8ms` | **[IMPLEMENTED]** |
| **`revenue_forecaster.pkl`** | Classical ML | `AnalyticsAgent` | 12-dim scaled feature vector | Vector $[\text{ROAS}, \text{CAC}, \text{CVR}]$ | Scikit-Learn Multi-Target Ridge | `2.1ms` | **[IMPLEMENTED]** |
| **`brand_voice_classifier.pkl`** | Classical NLP | `ContentAgent` | 500-dim TF-IDF n-grams | Quality Score $[0, 10]$ & binary label | Scikit-Learn Logistic Regression | `3.4ms` | **[IMPLEMENTED]** |
| **`creative_quality_regressor.pkl`** | Zero-Shot Vision | `CVAgent` | 512-dim CLIP-ViT B/32 embeddings | Aesthetic Quality $[0.0, 10.0]$ | Scikit-Learn Linear Head | `4.8ms` | **[IMPLEMENTED]** |
| **`bge-small-en-v1.5`** | Dense Embeddings | `RAG / Memory` | Text Chunks ($\le 512$ tokens) | 384-dim normalized dense vector | Pre-trained FastEmbed BGE | `23.3ms` | **[IMPLEMENTED]** |
| **`gpt-4o`** | Foundation LLM | `Strategy / Planner / Competitor` | Structured Pydantic prompt | Typed JSON contract response | Cloud API (OpenAI) | `1,420ms` | **[IMPLEMENTED]** |
| **`claude-3-5-sonnet`** | Foundation LLM | `Research / Content Copy` | Structured Pydantic prompt | Typed JSON contract response | Cloud API (Anthropic) | `1,980ms` | **[IMPLEMENTED]** |

---

## 2. Model Storage Locations

```text
research/models/
├── analytics/
│   ├── revenue_forecaster.pkl        # Scikit-Learn Multi-Target Ridge Regressor
│   └── feature_scaler.pkl            # StandardScaler transformer
├── content/
│   └── brand_voice_classifier.pkl    # Scikit-Learn TF-IDF + Logistic Regressor
├── cv/
│   └── creative_quality_regressor.pkl# CLIP-ViT visual quality scoring weights
└── optimizer/
    └── ppo_policy.pt                 # PyTorch Actor-Critic neural policy network
```
