# Appendix B — Master Model Registry

Catalog of all machine learning, deep learning, reinforcement learning, and generative models in ADPilot Pro.

| Model Identifier | Category | Framework | Checkpoint Location | Input Shape / Type | Output Spec | Consuming Agent | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`gpt-4o`** | LLM | OpenAI API | Cloud Endpoint | Token Sequence | JSON Schema | Strategy, Content | `[IMPLEMENTED]` |
| **`claude-3-5-sonnet`**| LLM | Anthropic API | Cloud Endpoint | Token Sequence | JSON Schema | Research, Strategy | `[IMPLEMENTED]` |
| **`gemini-3.1-flash-image`**| GenVision | Google GenAI SDK | Cloud Endpoint | Multi-Modal Prompt | JPEG / Base64 Data URL | Design Agent | `[IMPLEMENTED]` |
| **`bge-small-en-v1.5`** | Embedding | FastEmbed | Local Engine | Text String | 384-dim Float Vector | RAG Service | `[IMPLEMENTED]` |
| **`aesthetic_score.pkl`**| Custom ML | Scikit-Learn | `research/models/design/` | `[brightness, contrast]` | Score $[0.0, 10.0]$ | Design Agent | `[IMPLEMENTED]` |
| **`analytics_model.onnx`**| Deep ML | ONNXRuntime | `research/models/analytics/` | Float Tensor (1, 8) | CTR, CPA, ROAS Floats | Analytics Agent | `[IMPLEMENTED]` |
| **`brand_voice_classifier.pkl`**| NLP ML | Scikit-Learn | `research/models/content/` | TF-IDF Token Vector | Probability $[0.0, 1.0]$ | Content Evaluator | `[IMPLEMENTED]` |
| **`ctr_predictor.pkl`** | Custom ML | Random Forest | `research/models/content/` | Feature Vector (1, 6) | Expected CTR % | Content Agent | `[IMPLEMENTED]` |
| **`compliance_classifier.pkl`**| Vision ML | SVM | `research/models/cv/` | Feature Vector (1, 4) | Boolean Pass/Fail | CV Agent | `[IMPLEMENTED]` |
| **`ppo_policy_net.pt`** | RL Policy | PyTorch | `research/models/rl/` | State Vector (1, 12) | Action Delta Vector (1, 3)| PPO Optimizer | `[PARTIAL]` |
