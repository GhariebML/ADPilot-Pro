"""Video Storyboard Agent — Generates structured multi-scene video sequences for motion diffusion synthesis."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Type
from ..core.base_agent import BaseAgent
from ..schemas.campaign_context import CampaignContext
from ..schemas.multimodal_schemas import (
    VideoStoryboardOutput,
    SceneSpecification,
    VideoAspectRatio,
)

logger = logging.getLogger(__name__)


class VideoStoryboardAgent(BaseAgent[CampaignContext, VideoStoryboardOutput]):
    """Agent responsible for crafting dynamic 6-scene video storyboards with visual prompts and motion cues."""

    name: str = "video_storyboard_agent"
    input_model: Type[CampaignContext] = CampaignContext
    output_model: Type[VideoStoryboardOutput] = VideoStoryboardOutput

    async def run(self, context: CampaignContext) -> CampaignContext:
        """Execute storyboard generation and attach to campaign context."""
        output = await self.generate_storyboard(context)
        if hasattr(context, "agent_outputs") and isinstance(context.agent_outputs, dict):
            context.agent_outputs[self.name] = output.model_dump()
        return context

    async def generate_storyboard(self, context: CampaignContext) -> VideoStoryboardOutput:
        """Generate structured video storyboard scenes."""
        product_name = context.product.name if context.product else "ADPilot Enterprise"
        target_audience = "Modern Professionals"
        if getattr(context, "audience", None):
            aud = context.audience
            target_audience = getattr(aud, "summary", str(aud))

        scenes: List[SceneSpecification] = [
            SceneSpecification(
                scene_number=1,
                duration_sec=2.5,
                visual_prompt=f"Dramatic close-up opening shot highlighting the core challenge faced by {target_audience}. Cinematic lighting, depth of field.",
                camera_motion="Slow push in",
                dialogue_or_voiceover=f"Tired of outdated workflows? Discover the next generation with {product_name}.",
                on_screen_text=f"The Future of {product_name}",
                transition="Fast whip pan",
            ),
            SceneSpecification(
                scene_number=2,
                duration_sec=3.0,
                visual_prompt=f"Futuristic holographic interface revealing {product_name} solving real-time bottlenecks with glowing cyan accents.",
                camera_motion="Orbit 360 around centerpiece",
                dialogue_or_voiceover=f"Engineered specifically for {target_audience} to maximize precision and velocity.",
                on_screen_text="Autonomous Precision",
                transition="Cross dissolve",
            ),
            SceneSpecification(
                scene_number=3,
                duration_sec=3.5,
                visual_prompt="Multi-screen split view showing rapid performance gains and upward trending analytics charts.",
                camera_motion="Dynamic zoom out",
                dialogue_or_voiceover="Deliver 10x output with zero manual friction.",
                on_screen_text="10x Performance Boost",
                transition="Glitch transition",
            ),
            SceneSpecification(
                scene_number=4,
                duration_sec=3.0,
                visual_prompt=f"High-energy lifestyle shot of satisfied user experiencing seamless results with {product_name}.",
                camera_motion="Tracking shot left to right",
                dialogue_or_voiceover="Built for those who demand excellence in every campaign.",
                on_screen_text="Proven Results",
                transition="Flash cut",
            ),
            SceneSpecification(
                scene_number=5,
                duration_sec=3.0,
                visual_prompt=f"Premium product showcase with glowing aura and official {product_name} insignia on dark titanium backdrop.",
                camera_motion="Gentle tilt up",
                dialogue_or_voiceover="Experience the power today.",
                on_screen_text=f"Unlock {product_name} Now",
                transition="Fade to emblem",
            ),
        ]

        total_duration = sum(s.duration_sec for s in scenes)

        return VideoStoryboardOutput(
            title=f"{product_name} — High-Conversion Motion Storyboard",
            scenes=scenes,
            total_duration_sec=total_duration,
            aspect_ratio=VideoAspectRatio.PORTRAIT_9_16,
            target_platform="Instagram Reels / TikTok / YouTube Shorts",
            audio_soundtrack_prompt="High-tempo cinematic electronica with driving pulse and triumphant synth chords",
            confidence=0.96,
            metadata={"product_name": product_name, "scene_count": len(scenes)},
        )
