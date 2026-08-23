import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from adpilot.providers.image_provider import GeminiImageGenerationProvider, ImageGenerationRequest

@pytest.fixture
def mock_request():
    return ImageGenerationRequest(
        campaign_id="test_camp",
        product_name="Test Product",
        product_type="SaaS",
        campaign_goal="Sales",
        target_audience="Devs",
        brand_identity="Blue and White",
        visual_style="Modern",
        platform="LinkedIn",
        aspect_ratio="16:9",
        creative_brief="Test prompt"
    )

def test_initialization_missing_key():
    provider = GeminiImageGenerationProvider(api_key="")
    assert not provider.is_available()

def test_initialization_with_key():
    with patch("adpilot.providers.image_provider.os.environ.get", return_value="fake_api_key_12345"):
        provider = GeminiImageGenerationProvider()
        # It should try to import google.genai, if not installed client is None, but is_available is True
        assert provider.is_available()

@pytest.mark.asyncio
async def test_generate_image_unconfigured(mock_request):
    provider = GeminiImageGenerationProvider(api_key="")
    result = await provider.generate_image(mock_request)
    
    assert result.generation_status == "unconfigured"
    assert result.campaign_id == "test_camp"
    assert "https://placehold.co" in result.generated_image

@pytest.mark.asyncio
async def test_generate_image_success(mock_request):
    provider = GeminiImageGenerationProvider(api_key="fake_key_12345")
    
    # Mocking google-genai client
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_image = MagicMock()
    mock_image.image.image_bytes = b"fake_image_bytes"
    mock_response.generated_images = [mock_image]
    
    mock_client.models.generate_images.return_value = mock_response
    provider.client = mock_client
    
    result = await provider.generate_image(mock_request)
    assert result.generation_status == "generated"
    assert "data:image/jpeg;base64," in result.generated_image

