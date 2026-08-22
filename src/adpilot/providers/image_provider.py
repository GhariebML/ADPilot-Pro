"""Image Generation Provider abstraction and NanoBanana adapter."""

from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ImageGenerationResult(BaseModel):
    """Result of an image generation request."""

    status: str = Field(..., description="'generated', 'unconfigured', 'failed', 'placeholder'")
    image_url: Optional[str] = Field(default=None, description="URL of generated image if available")
    placeholder_url: str = Field(default="https://placehold.co/1200x628.png", description="Safe fallback URL")
    provider_name: str = Field(default="nanobanana")
    error_message: Optional[str] = Field(default=None, description="Detailed error or configuration message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Generation metadata (dimensions, seed, latency)")


class ImageGenerationProvider(ABC):
    """Abstract interface for multi-modal visual generative AI providers."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider credentials and network endpoints are configured."""
        raise NotImplementedError

    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1200,
        height: int = 628,
        brand_colors: Optional[List[str]] = None,
        style: str = "photorealistic",
    ) -> ImageGenerationResult:
        """Execute image generation or return unconfigured status with safe placeholder."""
        raise NotImplementedError


class NanoBananaProviderAdapter(ImageGenerationProvider):
    """Adapter for the NanoBanana Image Generation API.

    Strictly complies with system policy:
    - If API key / endpoint is configured in environment, executes actual API calls.
    - If unconfigured, explicitly reports missing credentials and does NOT fake successful generation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("NANOBANANA_API_KEY")
        self.base_url = base_url or os.environ.get("NANOBANANA_BASE_URL", "https://api.nanobanana.ai/v1")

    def is_available(self) -> bool:
        """Returns True only when valid API credentials exist."""
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1200,
        height: int = 628,
        brand_colors: Optional[List[str]] = None,
        style: str = "photorealistic",
    ) -> ImageGenerationResult:
        """Generate image via NanoBanana if available, otherwise return unconfigured status."""
        placeholder_url = f"https://placehold.co/{width}x{height}.png?text={prompt[:24].replace(' ', '+')}"

        if not self.is_available():
            logger.info("NanoBananaProvider | API credentials not configured (NANOBANANA_API_KEY missing). Using unconfigured placeholder.")
            return ImageGenerationResult(
                status="unconfigured",
                image_url=None,
                placeholder_url=placeholder_url,
                provider_name="nanobanana",
                error_message="NanoBanana credentials not configured in environment (NANOBANANA_API_KEY is not set).",
                metadata={
                    "width": width,
                    "height": height,
                    "style": style,
                    "configured": False,
                },
            )

        # Real NanoBanana API call when configured
        try:
            import httpx
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "prompt": prompt,
                "negative_prompt": negative_prompt or "blurry, low quality, artifacts",
                "width": width,
                "height": height,
                "style": style,
                "color_palette": brand_colors or [],
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{self.base_url}/generate", json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    image_url = data.get("image_url") or data.get("url")
                    return ImageGenerationResult(
                        status="generated",
                        image_url=image_url,
                        placeholder_url=placeholder_url,
                        provider_name="nanobanana",
                        metadata=data,
                    )
                else:
                    return ImageGenerationResult(
                        status="failed",
                        image_url=None,
                        placeholder_url=placeholder_url,
                        provider_name="nanobanana",
                        error_message=f"NanoBanana API error {response.status_code}: {response.text}",
                        metadata={"status_code": response.status_code},
                    )
        except Exception as exc:
            logger.error("NanoBananaProvider | Generation exception: %s", exc)
            return ImageGenerationResult(
                status="failed",
                image_url=None,
                placeholder_url=placeholder_url,
                provider_name="nanobanana",
                error_message=str(exc),
                metadata={"error": str(exc)},
            )
