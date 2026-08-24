"""Schemas for multimodal video, voiceover audio, and regulatory compliance extensions."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VideoAspectRatio(str, Enum):
    PORTRAIT_9_16 = "9:16"    # TikTok / Instagram Reels / YouTube Shorts
    LANDSCAPE_16_9 = "16:9"  # YouTube / Desktop Ad
    SQUARE_1_1 = "1:1"        # Feed post


class SceneSpecification(BaseModel):
    """Specification for a single video storyboard scene."""

    scene_number: int = Field(..., ge=1, description="Sequential scene index")
    duration_sec: float = Field(default=3.0, ge=0.5, le=30.0, description="Scene duration in seconds")
    visual_prompt: str = Field(..., description="Diffusion generation visual description")
    camera_motion: str = Field(default="slow zoom in", description="Camera movement (e.g. pan left, tilt up)")
    dialogue_or_voiceover: str = Field(default="", description="Spoken voiceover script for this scene")
    on_screen_text: Optional[str] = Field(default=None, description="Overlay typography text")
    transition: str = Field(default="cut", description="Transition to next scene (e.g. cross dissolve, whip pan)")


class VideoStoryboardOutput(BaseModel):
    """Full storyboard sequence generated for motion video synthesis."""

    title: str = Field(..., description="Video concept title")
    scenes: List[SceneSpecification] = Field(..., min_length=1, description="Ordered scene breakdowns")
    total_duration_sec: float = Field(..., ge=1.0, description="Total video run time")
    aspect_ratio: VideoAspectRatio = Field(default=VideoAspectRatio.PORTRAIT_9_16, description="Frame aspect ratio")
    target_platform: str = Field(default="Instagram Reels / TikTok", description="Primary deployment platform")
    audio_soundtrack_prompt: str = Field(default="Modern upbeat synth with ambient bass", description="Background music cue")
    confidence: float = Field(default=0.92, ge=0.0, le=1.0, description="Agent generation confidence score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Rendering metadata")


class VoiceoverAudioOutput(BaseModel):
    """Vocal narration, SSML formatting, and audio synthesis output."""

    transcript: str = Field(..., description="Plain-text voiceover transcript")
    ssml_content: str = Field(..., description="SSML markup with prosody and break tags")
    voice_persona: str = Field(default="Authoritative & Warm Professional", description="Vocal persona tone")
    target_duration_sec: float = Field(default=15.0, ge=1.0, description="Target narration duration")
    estimated_word_count: int = Field(..., ge=1, description="Word count")
    words_per_minute: float = Field(default=140.0, description="Speaking rate")
    emotion_tone: str = Field(default="Inspiring & Confident", description="Emotional inflection")
    audio_format: str = Field(default="mp3", description="Output audio container")
    audio_url_or_base64: Optional[str] = Field(default=None, description="Generated audio stream or placeholder")
    confidence: float = Field(default=0.94, ge=0.0, le=1.0, description="Confidence score")


class LegalComplianceOutput(BaseModel):
    """Regulatory compliance, FTC disclosures, and brand safety audit report."""

    is_compliant: bool = Field(..., description="Overall legal and brand safety clearance")
    ftc_disclosures_present: bool = Field(default=True, description="Whether required sponsor/ad tags are present")
    gdpr_consent_ready: bool = Field(default=True, description="Whether user tracking claims comply with GDPR/CCPA")
    claim_safety_score: float = Field(default=0.98, ge=0.0, le=1.0, description="Objective truthfulness & safety score")
    flags: List[str] = Field(default_factory=list, description="Identified compliance warnings or flags")
    suggested_disclaimers: List[str] = Field(default_factory=list, description="Required or recommended disclaimer copy")
    confidence: float = Field(default=0.96, ge=0.0, le=1.0, description="Auditor confidence score")
