# Creative Agent

## 1. Purpose
The **Creative Agent** establishes high-level art direction, visual moodboards, stylistic guidelines, and color harmony palettes for campaign creative production.

## 2. Business Responsibility
Maintains consistent, elevated brand visual aesthetics across multi-channel creative assets.

## 3. Technical Responsibility
Ingests positioning statements and target audience demographics, translates abstract branding attributes into explicit visual styling tokens (lighting, composition, typography, palette), and emits creative briefs.

## 4. Source Code
- `src/adpilot/agents/creative_agent.py`

## 5. Input
- `StrategyAgentOutput` (Positioning, Brand tone)
- `ResearchAgentOutput` (Audience aesthetics)

## 6. Processing Flow
1. Parse brand tone and audience psychographic styling preferences.
2. Select cohesive primary, secondary, and accent color hex codes.
3. Formulate typography pairings and negative space guidelines.
4. Output structured creative styling guidelines for `DesignAgent`.

## 7. Models Used
- Foundation LLM (GPT-4o Router).

## 8. Tools Used
- Brand Style Repository (`src/adpilot/services/design_repo.py`)

## 9. Output
- Styling tokens: Primary `#06B6D4`, Secondary `#8B5CF6`, Background `#030712`, Composition Layouts.

## 10. Downstream Consumers
- `DesignAgent` (uses tokens in text-to-image prompts)
- `CVAgent` (audits generated assets against the palette)

## 11. Error Handling
- Defaults to obsidian dark-theme tokens if brand inputs are empty.

## 12. Validation
- Verifies WCAG color contrast compliance for text/background pairings.

## 13. Corrective Actions
- Replaces low-contrast accent colors with high-visibility equivalents.

## 14. Human-in-the-Loop
- Palette can be edited in the Nano Banana Creative Studio.

## 15. Example Execution
```json
{
  "theme_name": "Obsidian Cyber Intelligence",
  "primary_hex": "#06B6D4",
  "secondary_hex": "#8B5CF6",
  "background_hex": "#030712",
  "typography": "Inter + JetBrains Mono",
  "aesthetic_tone": "Enterprise, Futuristic, Authoritative"
}
```

## 16. Implementation Status
[IMPLEMENTED]
