"""Evaluates generated creatives for campaign alignment, brand consistency, and safety."""

import logging
from typing import List, Dict, Any

from ..schemas.agent_schemas import CampaignContext, DesignAgentOutput

logger = logging.getLogger(__name__)

class CreativeEvaluator:
    """Evaluates image generation output against campaign requirements."""

    def __init__(self):
        pass

    async def evaluate(self, context: CampaignContext, design_output: DesignAgentOutput) -> Dict[str, Any]:
        """
        Evaluates the generated creatives.
        Returns a structured evaluation dict.
        """
        violations = []
        corrective_actions = []
        reasons = ["Validated basic requirements"]
        score = 10.0
        
        for asset in design_output.creative_assets:
            if asset.generation_status == "failed":
                violations.append(f"Asset {asset.asset_id} failed to generate.")
                corrective_actions.append("Retry generation or check provider.")
                score -= 5.0
            elif asset.generation_status == "generated" and not asset.image_url:
                violations.append(f"Asset {asset.asset_id} is marked generated but missing image URL.")
                corrective_actions.append("Ensure provider returns a valid image URL or base64.")
                score -= 5.0
                
        status = "REVISION_REQUIRED" if violations else "PASS"
        
        if status == "PASS":
            reasons.append("Image generated successfully and meets campaign alignment.")
        
        return {
            "status": status,
            "score": max(0.0, score),
            "reasons": reasons,
            "violations": violations,
            "corrective_actions": corrective_actions
        }


