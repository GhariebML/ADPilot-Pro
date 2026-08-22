"""Tests for application configuration, settings validation, and environment modes."""

from adpilot.core.config import AdPilotConfig, clear_config_cache, get_config


def test_default_config():
    """Verify default configuration values."""
    clear_config_cache()
    config = get_config()

    assert config.app_name == "ADPilot Pro"
    assert config.app_version == "2.0.0"
    assert config.api_v1_prefix == "/api/v1"
    assert config.api_legacy_prefix == "/api"
    assert config.db_pool_size == 5
    assert config.redis_max_connections == 10
    assert config.correlation_id_header == "X-Request-ID"


def test_environment_normalization():
    """Verify environment strings are case-insensitive and trimmed."""
    config = AdPilotConfig(ENVIRONMENT="  PRODUCTION  ")
    assert config.environment == "production"
    assert config.is_production is True
    assert config.is_testing is False

    test_config = AdPilotConfig(ENVIRONMENT="test")
    assert test_config.is_testing is True
    assert test_config.is_production is False


def test_production_validation_warnings():
    """Verify validation warnings are emitted for missing production keys."""
    prod_config = AdPilotConfig(
        ENVIRONMENT="production",
        ADPILOT_API_KEY="",
        DATABASE_URL="sqlite+aiosqlite:///./test.db",
        OPENAI_API_KEY="",
        OPENROUTER_API_KEY="",
        ANTHROPIC_API_KEY="",
        HF_TOKEN="",
    )

    warnings = prod_config.validate_environment()
    assert any("ADPILOT_API_KEY" in w for w in warnings)
    assert any("SQLite" in w for w in warnings)
    assert any("LLM provider" in w for w in warnings)


def test_development_validation_no_strict_warnings():
    """Verify development mode does not require production-only secrets."""
    dev_config = AdPilotConfig(ENVIRONMENT="development")
    warnings = dev_config.validate_environment()
    assert len(warnings) == 0
