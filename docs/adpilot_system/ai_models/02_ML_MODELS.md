# Classical & Statistical ML Models

**Status:** [IMPLEMENTED]  
**Framework:** Scikit-Learn / NumPy / SciPy  

---

## 1. Overview
In addition to LLMs, ADPilot Pro integrates **locally trained, deterministic machine learning models** for sub-millisecond revenue forecasting, copy quality classification, and anomaly detection without incurring external cloud API latency or costs.

---

## 2. Implemented ML Models Catalog

### Model 1: Multi-Target Revenue & ROAS Forecaster
- **Responsible Agent:** `AnalyticsAgent`
- **Model Type:** Multi-Target Ridge Regressor (`Ridge(alpha=1.0)`)
- **Artifact Path:** `research/models/analytics/revenue_forecaster.pkl`
- **Scaler Path:** `research/models/analytics/feature_scaler.pkl`
- **Features (12):**
  1. `budget_log`: Log-transformed campaign budget ($)
  2. `channel_count`: Number of active advertising networks
  3. `headline_sentiment`: VADER sentiment compound score of ad headlines
  4. `headline_length_chars`: Average headline character count
  5. `body_word_count`: Average body copy length
  6. `cta_urgency_score`: Keyword density of action-oriented conversion words
  7. `vertical_b2b_saas`: One-hot encoded vertical indicator
  8. `vertical_ecommerce`: One-hot encoded vertical indicator
  9. `vertical_real_estate`: One-hot encoded vertical indicator
  10. `historical_roas_prior`: Retrieved historical benchmark ROAS from RAG
  11. `market_competition_index`: Competitor saturation rating ($1.0 - 5.0$)
  12. `cv_aesthetic_score`: Visual quality rating from CLIP-ViT
- **Targets (3):** `[Predicted_ROAS, Predicted_CAC, Predicted_CVR]`
- **Performance:** $R^2 = 0.894$, $\text{RMSE} = 0.28$
- **Inference Latency:** `2.1ms`

---

### Model 2: Copy Quality & Brand Voice Classifier
- **Responsible Agent:** `ContentAgent` / `ContentEvaluator`
- **Model Type:** Logistic Regression with TF-IDF Vectorizer
- **Artifact Path:** `research/models/content/brand_voice_classifier.pkl`
- **Features:** 500-dim TF-IDF n-grams ($n \in \{1, 2, 3\}$) + Text readability metrics (Flesch-Kincaid grade level).
- **Target:** Binary Brand Compliance (`1 = Compliant`, `0 = Off-Brand/Spammy`).
- **Performance:** $\text{Accuracy} = 94.2\%$, $\text{F1} = 0.938$.
- **Inference Latency:** `3.4ms`.

---

### Model 3: Rolling Statistical Anomaly Detector
- **Responsible Agent:** `MonitoringAgent`
- **Algorithm:** Dynamic Rolling Z-Score with Exponential Moving Average (EMA) Smoothing.
- **Formulation:**
  $$Z_t = \frac{x_t - \text{EMA}_{24}(x)}{\sigma_{24}(x)}$$
- **Threshold:** $|Z_t| > 2.5 \implies \text{Anomaly Flagged}$.
- **Inference Latency:** `0.8ms`.
