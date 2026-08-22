# Design Agent

## 1. Purpose
The **Design Agent** formulates visual composition rules, defines platform aspect ratios (1:1 Feed, 9:16 Story, 16:9 Landscape), establishes color palettes, and constructs high-converting text-to-image prompts (e.g., DALL-E 3 / Midjourney / Stable Diffusion).

## 2. Business Responsibility
Ensures brand visual identity is upheld across creative assets while formulating prompts designed to maximize audience attention and click-through rates.

## 3. Technical Responsibility
Ingests `ContentAgentOutput` and `StrategyAgentOutput`, extracts brand styling tokens from memory, generates prompt specifications with lighting, camera angle, and layout metadata, and emits `DesignAgentOutput`.

## 4. Source Code
- `src/adpilot/agents/design_agent.py`
- System Prompt: `src/adpilot/prompts/design_system_prompt.md`

## 5. Input
- **Schema:** `ContentAgentOutput` (Ads, headlines, visual hooks)
- Brand Guidelines (Color hexes, logo placement, aesthetic tone)

## 6. Processing Flow
1. Parse each ad creative and identify its target platform format (e.g., Meta Carousel, LinkedIn Feed, Story).
2. Load brand color hex codes and design guardrails from Brand Memory.
3. Call GPT-4o to engineer image generation prompts with explicit compositional hierarchy.
4. Pass generated concepts to `CVAgent` for zero-shot contrast and aesthetic pre-validation.

## 7. Models Used
- Foundation LLM: OpenAI GPT-4o Router (Prompt Engineering).
- Image Generation Engine: DALL-E 3 / Nano Banana Mock Image Service (`src/adpilot/services/image_service.py`).

## 8. Tools Used
- Image Service (`src/adpilot/services/image_service.py`)
- Brand Style Repository (`src/adpilot/services/design_repo.py`)

## 9. Output
- **Schema:** `DesignAgentOutput`
  - `visual_concepts: List[VisualConcept]` (Concept Name, Mood, Composition)
  - `image_prompts: List[ImagePrompt]` (Platform, AspectRatio, Detailed Prompt, Negative Prompt)
  - `brand_rules: Dict[str, str]` (Hex Codes, Typography, Safe Zones)

## 10. Downstream Consumers
- `CVAgent` (scores prompt visual outputs against contrast standards)
- `PublishingAgent` (attaches rendered images to ad campaigns)

## 11. Error Handling
- Safe fallback prompt templates if LLM prompt generator emits unsupported syntax.

## 12. Validation
- Verifies exact aspect ratio strings (`1:1`, `16:9`, `9:16`) and valid hex color formats (`#RRGGBB`).

## 13. Corrective Actions
- If `CVAgent` flags contrast $< 7:1$, adjusts background brightness values in prompt.

## 14. Human-in-the-Loop
- Designers can review, regenerate, or download assets in the Creative Studio view.

## 15. Example Execution
```json
{
  "visual_concepts": [
    {
      "name": "Neural Command Center",
      "mood": "Futuristic, sleek, authoritative",
      "primary_hex": "#06B6D4",
      "secondary_hex": "#030712"
    }
  ],
  "image_prompts": [
    {
      "platform": "LINKEDIN",
      "aspect_ratio": "1:1",
      "prompt": "Ultra-modern glassmorphism dashboard floating over dark midnight obsidian background. Glowing cyan and purple neural network nodes displaying marketing analytics metrics.",
      "negative_prompt": "blurry, low quality, cluttered text, distorted graphics"
    }
  ]
}
```

## 16. Implementation Status
[IMPLEMENTED]
