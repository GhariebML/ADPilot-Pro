# 21 — Current System Limitations

## 1. Technical & Architecture Limitations
* **In-Memory Simulation State:** The current simulation store uses in-memory dictionary storage (`simulation_store.py`); restarting the backend drops active simulation telemetry.
* **RL Policy Environment:** PPO policy updates currently operate against a simulated marketing environment rather than real-time live ad spend APIs.

---

## 2. Data & Model Limitations
* **Zero-Shot Vision Gating:** Computer Vision evaluation relies on general CLIP-ViT regression models rather than custom fine-tuned ad conversion vision models.
* **Rate Limits on Free-Tier APIs:** Commercial generative image models require paid API tier quotas to sustain high-frequency continuous batch generation.
