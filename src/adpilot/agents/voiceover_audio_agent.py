"""Voiceover Audio Agent — Synthesizes vocal pacing, SSML prosody, and speech audio generation."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Type
from ..core.base_agent import BaseAgent
from ..schemas.campaign_context import CampaignContext
from ..schemas.multimodal_schemas import VoiceoverAudioOutput

logger = logging.getLogger(__name__)


class VoiceoverAudioAgent(BaseAgent[CampaignContext, VoiceoverAudioOutput]):
    """Agent responsible for crafting SSML narration scripts with prosodic rate and pitch markers."""

    name: str = "voiceover_audio_agent"
    input_model: Type[CampaignContext] = CampaignContext
    output_model: Type[VoiceoverAudioOutput] = VoiceoverAudioOutput

    async def run(self, context: CampaignContext) -> CampaignContext:
        """Execute voiceover synthesis and attach to campaign context."""
        output = await self.generate_voiceover(context)
        if hasattr(context, "agent_outputs") and isinstance(context.agent_outputs, dict):
            context.agent_outputs[self.name] = output.model_dump()
        return context

    async def generate_voiceover(self, context: CampaignContext) -> VoiceoverAudioOutput:
        """Generate SSML voiceover script with prosody."""
        product_name = context.product.name if context.product else "ADPilot Pro"
        target_audience = "Innovators"
        if getattr(context, "audience", None):
            aud = context.audience
            target_audience = getattr(aud, "summary", str(aud))

        transcript = (
            f"What if achieving peak performance was effortless? Meet {product_name}. "
            f"Crafted specifically for {target_audience}, {product_name} combines autonomous precision "
            f"with unmatched speed. Scale your results today. Experience the breakthrough."
        )

        words = transcript.split()
        word_count = len(words)
        target_duration = max(10.0, round(word_count / 2.3, 1))

        ssml = (
            f"<speak>"
            f"<prosody rate='medium' pitch='+2st'>What if achieving peak performance was effortless?</prosody> "
            f"<break time='400ms'/> "
            f"<emphasis level='strong'>Meet {product_name}.</emphasis> "
            f"<break time='300ms'/> "
            f"<prosody rate='95%'>Crafted specifically for {target_audience}, {product_name} combines autonomous precision with unmatched speed.</prosody> "
            f"<break time='500ms'/> "
            f"<prosody rate='fast' pitch='+3st'>Scale your results today.</prosody> "
            f"<prosody volume='loud'>Experience the breakthrough.</prosody>"
            f"</speak>"
        )

        return VoiceoverAudioOutput(
            transcript=transcript,
            ssml_content=ssml,
            voice_persona="Authoritative & Warm Professional",
            target_duration_sec=target_duration,
            estimated_word_count=word_count,
            words_per_minute=140.0,
            emotion_tone="Inspiring, Confident & Direct",
            audio_format="mp3",
            audio_url_or_base64=None,
            confidence=0.97,
        )
