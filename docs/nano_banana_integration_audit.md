# Nano Banana (Gemini) Integration Audit

## 1. Current Architecture
- **Design Agent**: Located at src/adpilot/agents/design_agent.py. It currently generates creative briefs, deterministic placeholder images (https://placehold.co), and delegates generation to an ImageGenerationProvider.
- **Image Provider Abstraction**: Located at src/adpilot/providers/image_provider.py. Includes ImageGenerationProvider and a NanoBananaProviderAdapter which currently mocks generation to a fictional API (pi.nanobanana.ai/v1).
- **Nano Banana Studio UI**: Located at rontend/src/components/CreativeStudioView.tsx. Uses hardcoded Unsplash image URLs and mock data.
- **Agent Orchestration**: src/adpilot/orchestrator/pipeline_runner.py drives the workflow, calling the Design Agent after Strategy and Content agents.
- **Data Models**: Pydantic models in src/adpilot/schemas/agent_schemas.py and campaign_context.py dictate data flow.

## 2. Existing Reusable Components
- **Agent Abstraction**: BaseAgent handles standard logging, tracing, and metadata event emission.
- **Image Provider Interface**: ImageGenerationProvider acts as the interface, we just need to build a new GeminiImageGenerationProvider implementation.
- **Model Loader / DB**: Existing ArtifactRegistry and MemoryManager can be used to store final assets.
- **HITL Manager**: src/adpilot/hitl/manager.py handles approvals, preventing immediate publication.
- **Environment config**: .env and src/adpilot/config.py.

## 3. Missing Components
- **Gemini SDK**: The google-genai Python package is not in equirements.txt or pyproject.toml.
- **ImageGenerationRequest & Response Schemas**: Provider-agnostic DTOs for the exact contract requested by the user.
- **Creative Evaluator**: An automated step post-generation to check for brand/campaign alignment before sending to HITL.
- **Frontend Live Data**: CreativeStudioView.tsx needs to bind to real data from the backend instead of static mock arrays.

## 4. Integration Risks
- Modifying the DesignAgentOutput schema without updating downstream consumers (CVAgent, Hitl, Publisher).
- Synchronous calls to Gemini image generation might time out the pipeline runner. Must ensure async usage.
- Handling Gemini's rate limits and content safety filter blockages gracefully.

## 5. Recommended Implementation Path
1. **Define Contracts**: Update src/adpilot/schemas/agent_schemas.py or image_provider.py with ImageGenerationRequest and ImageGenerationResponse.
2. **Install SDK**: Add google-genai to project dependencies.
3. **Implement Gemini Provider**: Create GeminiImageGenerationProvider in image_provider.py.
4. **Update Design Agent**: Refactor DesignAgent to generate ImageGenerationRequest from CampaignContext and invoke the Gemini provider.
5. **Implement Validation**: Add CreativeEvaluator to validate alignment and manage the retry loop.
6. **Update HITL & Asset Registry**: Store generated images into the existing registry.
7. **Refactor UI**: Update CreativeStudioView.tsx and backend API (src/adpilot/api/main.py) to expose the actual images.
8. **Testing**: Add mock tests and optionally integration tests.
