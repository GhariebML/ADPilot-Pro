# System Configuration & Environment Variables

**Status:** [IMPLEMENTED]  
**Config Loader:** `src/adpilot/core/config.py` (Pydantic `BaseSettings`)  

---

## 1. Environment Variables Matrix

| Variable Name | Type | Default Value | Description |
|---|---|---|---|
| `ENVIRONMENT` | `str` | `development` | Runtime environment (`development`, `production`, `test`) |
| `LLM_PROVIDER` | `str` | `openai` | Active primary LLM provider (`openai`, `anthropic`, `openrouter`, `ollama`) |
| `OPENAI_API_KEY` | `SecretStr` | `None` | Authentication secret for OpenAI API |
| `OPENAI_MODEL` | `str` | `gpt-4o` | Model identifier for OpenAI calls |
| `ANTHROPIC_API_KEY` | `SecretStr` | `None` | Authentication secret for Anthropic API |
| `ANTHROPIC_MODEL` | `str` | `claude-3-5-sonnet-20241022` | Model identifier for Anthropic calls |
| `OPENROUTER_API_KEY`| `SecretStr` | `None` | Gateway API key for OpenRouter |
| `REDIS_URL` | `str` | `redis://localhost:6379/0` | Connection URI for Redis cache & task worker |
| `QDRANT_URL` | `str` | `http://localhost:6333` | Vector database host URL |
| `DATABASE_URL` | `str` | `sqlite:///./data/adpilot.db` | SQLAlchemy relational database URI |
| `TEMPERATURE` | `float` | `0.2` | Creativity ceiling for foundation LLMs |
| `HITL_STRICT_MODE` | `bool` | `true` | Enforces human review on high-risk actions |
| `EMBEDDING_MODEL` | `str` | `BAAI/bge-small-en-v1.5` | FastEmbed dense embedding model |
| `LOG_LEVEL` | `str` | `INFO` | Application log verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
