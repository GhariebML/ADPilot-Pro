# 10 — Computer Vision & Creative Quality Gating

## 1. Multi-Modal Vision Architecture
ADPilot Pro establishes a dual-engine visual intelligence architecture, strictly separating the **Generative Vision Engine** from the independent **Computer Vision Quality Gate**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      1. GENERATIVE VISION ENGINE                            │
│  Design Agent ──> Gemini Nano Banana (`google-genai` models.generate_content)│
│  Generates Native Multi-Format Creatives (16:9, 1:1, 4:5, 9:16)              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Raw Image URL / Base64 Data URL
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    2. COMPUTER VISION QUALITY GATE (CV Agent)               │
│                                                                             │
│  ┌────────────────────────┐ ┌───────────────────────┐ ┌───────────────────┐ │
│  │  Zero-Shot CLIP-ViT    │ │   WCAG Accessibility  │ │ Text Density Area │ │
│  │  Aesthetic Regression  │ │  Contrast Ratio Check │ │   Occupancy Check │ │
│  └───────────┬────────────┘ └───────────┬───────────┘ └─────────┬─────────┘ │
│              │ Score (0-10)             │ Ratio (e.g. 14.2:1)   │ % Density │
│              └──────────────────────────┼───────────────────────┘           │
│                                         ▼                                   │
│                        Weighted Quality Score Calculation                   │
│                                         │                                   │
│                                         ▼                                   │
│                        Decision: PASS or REVISION_REQUIRED                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Visual Quality Standards & Mathematical Thresholds
* **CLIP-ViT Aesthetic Score:** Evaluates visual harmony, lighting, and composition against trained human preference vectors. Threshold: $\text{Score} \ge 8.5/10$.
* **WCAG AAA Contrast Ratio:** Measures luminosity contrast between typography and background pixels:
  $$C = \frac{L_1 + 0.05}{L_2 + 0.05} \ge 7.0:1 \; (\text{AAA Certified})$$
* **Text Density Ceiling:** Ad images with text area occupancy $> 20\%$ trigger an automated revision prompt to reduce copy clutter.
