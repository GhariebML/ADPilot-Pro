"""Content quality, relevance, keyword coverage, brand compliance, and anti-hallucination evaluator."""

from __future__ import annotations

import logging
import re
from typing import List, Optional, Set

from ..schemas.agent_schemas import (
    ContentEvaluationMetric,
    ContentEvaluationReport,
    ToneOfVoice,
)
from ..schemas.campaign_context import BrandGuidelines, CampaignContext, ProductType
from ..services.model_loader import ModelLoader

logger = logging.getLogger(__name__)

# Heuristic patterns for hallucination and extreme unsupported claims
UNSUPPORTED_PATTERNS = [
    r"\b1000%\s*(?:roi|return|growth)\b",
    r"\b(?:undisputed|undisputable)\s*#?1\b",
    r"\bguaranteed\s*(?:millions|wealth|cure|instant)\b",
    r"\bworld'?s\s*only\s*flawless\b",
    r"\bzero\s*risk\s*guaranteed\b",
    r"\bmagical(?:ly)?\s*(?:solves?|fixes?)\b",
]


class ContentEvaluator:
    """Evaluates marketing content quality, strategic relevance, keyword coverage, and brand safety."""

    def __init__(self) -> None:
        self.model_loader = ModelLoader()
        self._ml_model = None
        self._ml_tokenizer = None
        self._load_ml_components()

    def _load_ml_components(self) -> None:
        try:
            self._ml_model = self.model_loader.load_model("research/models/content/content_model.pkl")
            self._ml_tokenizer = self.model_loader.load_model("research/models/content/tokenizer.pkl")
        except Exception as exc:
            logger.warning("ContentEvaluator | ML model initialization failed: %s", exc)

    def evaluate(
        self,
        headlines: List[str],
        primary_copy: List[str],
        descriptions: List[str],
        ctas: List[str],
        target_keywords: List[str],
        context: Optional[CampaignContext] = None,
        brand_guidelines: Optional[BrandGuidelines] = None,
        product_type: Optional[ProductType] = None,
        expected_tone: Optional[ToneOfVoice] = None,
    ) -> ContentEvaluationReport:
        """Run comprehensive multi-dimensional evaluation on generated content."""
        all_text = " ".join(headlines + primary_copy + descriptions + ctas).lower()

        # 1. ML Content Quality Prediction
        ml_prediction: Optional[float] = None
        if self._ml_model is not None and self._ml_tokenizer is not None and (headlines or primary_copy):
            sample_text = headlines[0] if headlines else primary_copy[0]
            try:
                vec = self._ml_tokenizer.transform([sample_text])
                ml_prediction = float(self._ml_model.predict(vec)[0])
            except Exception as e:
                logger.debug("ML inference error during evaluation: %s", e)

        # 2. Content Quality Score (0 - 100)
        quality_score, quality_details = self._evaluate_content_quality(
            headlines, primary_copy, descriptions, ctas, ml_prediction
        )

        # 3. Strategic Relevance Score (0 - 100)
        relevance_score, relevance_details = self._evaluate_relevance(
            all_text, context, product_type
        )

        # 4. Keyword Coverage
        keyword_score, covered_kw, missing_kw, kw_details = self._evaluate_keyword_coverage(
            all_text, target_keywords
        )

        # 5. Brand Compliance
        brand_score, brand_details = self._evaluate_brand_compliance(
            all_text, context, brand_guidelines, expected_tone
        )

        # 6. Hallucination / Unsupported Claim Risk (0 = no risk, 100 = extreme risk)
        hallucination_score, flagged_claims, hall_details = self._evaluate_hallucinations(
            all_text, headlines + primary_copy
        )

        metrics = [
            ContentEvaluationMetric(
                name="content_quality",
                score=quality_score,
                passed=quality_score >= 70.0,
                details=quality_details,
            ),
            ContentEvaluationMetric(
                name="relevance",
                score=relevance_score,
                passed=relevance_score >= 70.0,
                details=relevance_details,
            ),
            ContentEvaluationMetric(
                name="keyword_coverage",
                score=keyword_score,
                passed=keyword_score >= 50.0,
                details=kw_details,
            ),
            ContentEvaluationMetric(
                name="brand_compliance",
                score=brand_score,
                passed=brand_score >= 80.0,
                details=brand_details,
            ),
            ContentEvaluationMetric(
                name="hallucination_risk",
                score=hallucination_score,
                passed=hallucination_score <= 25.0,
                details=hall_details,
            ),
        ]

        passed_gate = all(
            [
                quality_score >= 60.0,
                relevance_score >= 60.0,
                brand_score >= 70.0,
                hallucination_score <= 30.0,
            ]
        )

        return ContentEvaluationReport(
            content_quality_score=round(quality_score, 2),
            relevance_score=round(relevance_score, 2),
            keyword_coverage_score=round(keyword_score, 2),
            brand_compliance_score=round(brand_score, 2),
            hallucination_risk_score=round(hallucination_score, 2),
            ml_quality_prediction=round(ml_prediction, 4) if ml_prediction is not None else None,
            covered_keywords=covered_kw,
            missing_keywords=missing_kw,
            detected_unsupported_claims=flagged_claims,
            passed_quality_gate=passed_gate,
            metrics=metrics,
        )

    def _evaluate_content_quality(
        self,
        headlines: List[str],
        primary_copy: List[str],
        descriptions: List[str],
        ctas: List[str],
        ml_prediction: Optional[float],
    ) -> tuple[float, str]:
        score = 80.0
        findings = []

        if not headlines:
            score -= 20.0
            findings.append("Missing headlines.")
        elif len(headlines) >= 2:
            score += 5.0

        if not primary_copy:
            score -= 25.0
            findings.append("Missing primary copy blocks.")
        else:
            # Check length: reward rich, multi-paragraph enterprise copy
            avg_words = sum(len(p.split()) for p in primary_copy) / len(primary_copy)
            if avg_words >= 35:
                score += 10.0
            elif avg_words < 15:
                score -= 10.0
                findings.append("Primary copy is too terse for enterprise conversion.")

        if not ctas:
            score -= 15.0
            findings.append("Missing CTA variants.")

        if ml_prediction is not None:
            # Scale regression prediction to positive score adjustment
            if ml_prediction > 0:
                score = min(100.0, score + 2.0)

        score = max(0.0, min(100.0, score))
        details = "; ".join(findings) if findings else "Copy exhibits robust depth, length, and structured CTAs."
        return score, details

    def _evaluate_relevance(
        self,
        all_text: str,
        context: Optional[CampaignContext],
        product_type: Optional[ProductType],
    ) -> tuple[float, str]:
        score = 75.0
        findings = []

        if context and context.brief:
            biz_name = context.brief.business_name.lower()
            if biz_name in all_text:
                score += 10.0
            else:
                findings.append(f"Business name '{context.brief.business_name}' not mentioned.")

            if context.brief.goals:
                goal_words = [g.value.replace("_", " ") for g in context.brief.goals]
                if any(gw in all_text for gw in goal_words):
                    score += 5.0

        if product_type:
            prod_indicators = {
                ProductType.saas: ["platform", "software", "cloud", "workflow", "api", "integration", "dashboard", "scale"],
                ProductType.physical: ["quality", "material", "crafted", "durable", "shipping", "product"],
                ProductType.service: ["consulting", "expert", "service", "tailored", "support", "dedicated"],
                ProductType.real_estate: ["property", "estate", "residence", "luxury", "sqft", "location", "view"],
            }
            indicators = prod_indicators.get(product_type, [])
            if any(ind in all_text for ind in indicators):
                score += 10.0

        score = max(0.0, min(100.0, score))
        details = "; ".join(findings) if findings else "Content strongly aligns with product type and objectives."
        return score, details

    def _evaluate_keyword_coverage(
        self, all_text: str, target_keywords: List[str]
    ) -> tuple[float, List[str], List[str], str]:
        if not target_keywords:
            return 100.0, [], [], "No target keywords specified."

        covered: List[str] = []
        missing: List[str] = []

        for kw in target_keywords:
            clean_kw = kw.strip().lower()
            # Check for direct keyword or root words
            if clean_kw in all_text or any(token in all_text for token in clean_kw.split() if len(token) > 4):
                covered.append(kw)
            else:
                missing.append(kw)

        coverage_ratio = len(covered) / len(target_keywords) if target_keywords else 1.0
        score = coverage_ratio * 100.0
        details = f"Covered {len(covered)}/{len(target_keywords)} target keywords ({score:.1f}% coverage)."
        return score, covered, missing, details

    def _evaluate_brand_compliance(
        self,
        all_text: str,
        context: Optional[CampaignContext],
        brand_guidelines: Optional[BrandGuidelines],
        expected_tone: Optional[ToneOfVoice],
    ) -> tuple[float, str]:
        score = 90.0
        findings = []

        prohibited: Set[str] = set()
        if brand_guidelines and hasattr(brand_guidelines, "prohibited_keywords"):
            prohibited.update(kw.lower() for kw in brand_guidelines.prohibited_keywords)
        if context and context.brand and hasattr(context.brand, "prohibited_keywords"):
            prohibited.update(kw.lower() for kw in context.brand.prohibited_keywords)
        if context and hasattr(context, "constraints") and context.constraints and hasattr(context.constraints, "prohibited_keywords"):
            prohibited.update(kw.lower() for kw in context.constraints.prohibited_keywords)

        for bad_word in prohibited:
            if bad_word in all_text:
                score -= 30.0
                findings.append(f"Prohibited brand keyword detected: '{bad_word}'.")

        # Tone checks
        tone = expected_tone or (context.brand.tone_of_voice if context and context.brand else None)
        if tone == ToneOfVoice.authoritative:
            if "!" in all_text and all_text.count("!") > 5:
                score -= 5.0
                findings.append("Excessive exclamation points for authoritative tone.")
        elif tone == ToneOfVoice.friendly:
            score += 5.0

        score = max(0.0, min(100.0, score))
        details = "; ".join(findings) if findings else "Fully compliant with brand voice and tone guidelines."
        return score, details

    def _evaluate_hallucinations(
        self, all_text: str, copy_items: List[str]
    ) -> tuple[float, List[str], str]:
        risk_score = 0.0
        flagged: List[str] = []

        for pattern in UNSUPPORTED_PATTERNS:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                risk_score += 25.0
                for m in matches:
                    flagged.append(f"Unsupported claim: '{m}'")

        risk_score = max(0.0, min(100.0, risk_score))
        details = f"Detected {len(flagged)} unsubstantiated claims." if flagged else "No unsupported or hyperbolic claims detected."
        return risk_score, flagged, details
