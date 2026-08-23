# 07 — Custom Machine Learning Models

## 1. Custom Model Registry
Beyond commercial LLM APIs, ADPilot Pro integrates specialized custom machine learning models trained on domain-specific advertising datasets. These models reside in `research/models/` and are loaded during inference via `ModelLoader`.

| # | Model Name | Model Artifact Path | Type / Architecture | Consuming Agent | Input Features | Output Target | Purpose | Status |
|---|---|---|---|---|---|---|---|---|
| **1** | **Aesthetic Score Regressor** | `research/models/design/aesthetic_score.pkl` | Gradient Boosted Regressor | `DesignAgent` | Brightness, Contrast, Color Dominance | Aesthetic Score $[0.0, 10.0]$ | Predicts creative visual appeal score prior to dispatch | `[IMPLEMENTED]` |
| **2** | **Analytics ONNX Model** | `research/models/analytics/analytics_model.onnx` | Deep Neural Net (ONNX) | `AnalyticsAgent` | Impressions, Spend, Audience Size, CPC | Predicted CTR, CPA, ROAS | High-speed serialized performance forecasting | `[IMPLEMENTED]` |
| **3** | **Brand Voice Classifier** | `research/models/content/brand_voice_classifier.pkl` | TF-IDF + Logistic Regression | `ContentEvaluator` | Text Token n-grams | Tone Alignment Probability $[0.0, 1.0]$ | Verifies copy adheres to brand tone guidelines | `[IMPLEMENTED]` |
| **4** | **CTR Predictor** | `research/models/content/ctr_predictor.pkl` | Random Forest Regressor | `ContentAgent` | Headline Length, Sentiment, Reading Ease | Expected CTR (%) | Ranks copy variants by expected conversion impact | `[IMPLEMENTED]` |
| **5** | **CV Compliance Classifier** | `research/models/cv/compliance_classifier.pkl` | Support Vector Machine (SVM) | `CVAgent` | Text Area %, Color Ratio, Contrast | Compliance Pass/Fail Flag | Enforces ad platform policy rules | `[IMPLEMENTED]` |
| **6** | **Lead Scoring Model** | `research/models/analytics/lead_scoring_model.pkl` | XGBoost Classifier | `AnalyticsAgent` | Industry, Company Size, Intent Score | Lead Quality Score $[0, 100]$ | Estimates expected sales qualification rate | `[IMPLEMENTED]` |
| **7** | **Revenue Forecaster** | `research/models/analytics/revenue_forecaster.pkl` | Ridge Regression / Time-Series | `AnalyticsAgent` | Historical ROAS, Channel Budget | Predicted Incremental Revenue ($) | Models 30-day revenue trajectory | `[IMPLEMENTED]` |

---

## 2. Model Loading & Inference Architecture
Models are dynamically loaded through a thread-safe singleton cache in `src/adpilot/core/model_loader.py`:

```
Agent Execution Request
         │
         ▼
┌────────────────────────────────┐
│   ModelLoader.load_model()     │ ──> Checks in-memory cache
└────────┬──────────────┬────────┘
         │ (Hit)        │ (Miss)
         ▼              ▼
 In-Memory Checkpoint  Deserialize from `research/models/` (.pkl / .onnx)
         │              │
         └──────┬───────┘
                ▼
  Inference Pipeline Execution (Scikit / ONNXRuntime)
                │
                ▼
  Predictive Output Injected into Agent Context
```
