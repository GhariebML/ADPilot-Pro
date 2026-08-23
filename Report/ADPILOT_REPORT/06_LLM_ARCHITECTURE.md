# 06 — LLM Architecture & Prompt Engineering

## 1. Multi-Provider LLM Abstraction Layer
ADPilot Pro implements an enterprise provider-agnostic LLM interface (`LLMProvider`) managed via `LLMProviderFactory` in `src/adpilot/providers/factory.py`. This decouples the agent reasoning logic from specific model vendor APIs, enabling dynamic routing, fallback resiliency, and structured output parsing.

```
                  ┌───────────────────────────────┐
                  │       BaseAgent.call_llm()     │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │      LLMProviderFactory       │
                  └───────┬───────┬───────┬───────┘
                          │       │       │
             ┌────────────┘       │       └────────────┐
             ▼                    ▼                    ▼
┌─────────────────────────┐ ┌───────────┐ ┌─────────────────────────┐
│     OpenAI Provider     │ │ Anthropic │ │     Gemini Provider     │
│       (GPT-4o)          │ │ (Claude)  │ │   (Gemini 1.5/2.5 Pro)  │
└─────────────────────────┘ └───────────┘ └─────────────────────────┘
```

---

## 2. Identity Enforcement & Role Specialization
An agent's role identity is never defined merely by its file name or class name. Instead, ADPilot enforces cognitive boundaries through 4 coupled mechanisms:
1. **System Prompt Directives:** Immutable Markdown prompt templates located in `src/adpilot/prompts/` (e.g., `strategy_agent.md`, `content_agent.md`, `cv_agent.md`) that establish behavioral boundaries, output structures, and domain expertise.
2. **Pydantic Contract Registries:** Every agent registers its input and output schema in `ContractRegistry`.
3. **Structured JSON Output Parsing:** Responses are parsed with Pydantic JSON mode, enforcing deterministic schema compliance and rejecting non-conforming responses.
4. **Deterministic Fallback Handlers:** When LLM endpoints experience latency or outages, agents invoke deterministic heuristic synthesis methods (e.g. `_generate_deterministic_design()`) to prevent pipeline disruption.

---

## 3. Configured Provider Implementations
| Provider | Underlying Class | Primary Role in Fleet | Schema Mode | Status |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI** | `OpenAIProvider` | Strategy, Audience, Research, Content Generation | Pydantic / JSON Object | `[IMPLEMENTED]` |
| **Anthropic** | `AnthropicProvider` | High-complexity Reasoning, Strategy Synthesis | Strict Tool Calling | `[IMPLEMENTED]` |
| **Google Gemini** | `GeminiProvider` / `GeminiImageGenerationProvider` | Multi-Modal Visual Synthesis (Nano Banana) | Native GenAI SDK | `[IMPLEMENTED]` |
