import pytest
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.agents.video_storyboard_agent import VideoStoryboardAgent
from adpilot.agents.voiceover_audio_agent import VoiceoverAudioAgent
from adpilot.agents.legal_compliance_agent import LegalComplianceAgent
from adpilot.schemas.multimodal_schemas import (
    VideoStoryboardOutput,
    VoiceoverAudioOutput,
    LegalComplianceOutput,
)


@pytest.fixture
def sample_context():
    return CampaignContextBuilder.from_brief(
        {
            "business_name": "Apex AI Cloud",
            "product_description": "Autonomous multi-agent marketing operating system for enterprise scaling.",
            "target_market": "Enterprise CMOs and Growth Directors",
            "budget_usd": 10000,
            "goals": ["lead_generation", "brand_awareness"],
            "channels": ["instagram", "youtube", "linkedin"],
            "tone_of_voice": "authoritative",
        },
        campaign_id="camp-multimodal-test",
    )


@pytest.mark.asyncio
async def test_video_storyboard_agent_execution(sample_context):
    agent = VideoStoryboardAgent()
    output = await agent.generate_storyboard(sample_context)

    assert isinstance(output, VideoStoryboardOutput)
    assert len(output.scenes) >= 3
    assert output.total_duration_sec > 0
    assert output.confidence >= 0.90

    # Also verify full run() lifecycle
    updated_context = await agent.run(sample_context)
    assert agent.name in updated_context.agent_outputs


@pytest.mark.asyncio
async def test_voiceover_audio_agent_execution(sample_context):
    agent = VoiceoverAudioAgent()
    output = await agent.generate_voiceover(sample_context)

    assert isinstance(output, VoiceoverAudioOutput)
    assert "<speak>" in output.ssml_content
    assert "</speak>" in output.ssml_content
    assert output.estimated_word_count > 0
    assert output.target_duration_sec > 0
    assert output.confidence >= 0.90

    # Also verify full run() lifecycle
    updated_context = await agent.run(sample_context)
    assert agent.name in updated_context.agent_outputs


@pytest.mark.asyncio
async def test_legal_compliance_agent_execution(sample_context):
    agent = LegalComplianceAgent()
    output = await agent.audit_compliance(sample_context)

    assert isinstance(output, LegalComplianceOutput)
    assert output.is_compliant is True
    assert output.ftc_disclosures_present is True
    assert len(output.suggested_disclaimers) > 0
    assert output.claim_safety_score >= 0.95

    # Also verify full run() lifecycle
    updated_context = await agent.run(sample_context)
    assert agent.name in updated_context.agent_outputs
