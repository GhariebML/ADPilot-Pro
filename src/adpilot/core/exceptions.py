"""Custom exception hierarchy for AdPilot.

Collecting custom domain errors in a single module keeps traceback handling tidy,
provides clear semantic meaning, and translates cleanly into RFC 7807 Problem Details.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class AdPilotError(Exception):
    """Base-class for all AdPilot-specific errors."""

    def __init__(
        self,
        message: str = "An unexpected error occurred in AdPilot.",
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}


# Alias for backward compatibility
AdPilotException = AdPilotError


class ConfigurationError(AdPilotError):
    """Raised on mis-configuration of an agent or environment."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="CONFIGURATION_ERROR",
            details=details,
        )


class DatabaseConnectionError(AdPilotError):
    """Raised when a database connection or query fails."""

    def __init__(self, message: str = "Database connection error.", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            status_code=503,
            error_code="DATABASE_ERROR",
            details=details,
        )


class RedisConnectionError(AdPilotError):
    """Raised when Redis connection or operations fail."""

    def __init__(self, message: str = "Redis connection error.", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            status_code=503,
            error_code="REDIS_ERROR",
            details=details,
        )


class DependencyError(AdPilotError):
    """Raised when a critical external dependency is unhealthy."""

    def __init__(self, dependency: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=f"Dependency '{dependency}' error: {message}",
            status_code=503,
            error_code="DEPENDENCY_ERROR",
            details={"dependency": dependency, **(details or {})},
        )


class EntityNotFoundError(AdPilotError):
    """Raised when a requested entity (campaign, task, user, asset) is not found."""

    def __init__(self, entity_type: str, entity_id: str) -> None:
        super().__init__(
            message=f"{entity_type} with ID '{entity_id}' was not found.",
            status_code=404,
            error_code="ENTITY_NOT_FOUND",
            details={"entity_type": entity_type, "entity_id": entity_id},
        )


class AuthenticationError(AdPilotError):
    """Raised when authentication credentials are missing or invalid."""

    def __init__(self, message: str = "Invalid or missing authentication credentials.") -> None:
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_FAILED",
        )


class AuthorizationError(AdPilotError):
    """Raised when an authenticated user lacks required roles/permissions."""

    def __init__(self, message: str = "Access forbidden for current user role.") -> None:
        super().__init__(
            message=message,
            status_code=403,
            error_code="PERMISSION_DENIED",
        )


class ValidationError(AdPilotError):
    """Raised when business input validation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class SchemaValidationError(AdPilotError):
    """Raised when invalid config or schema data is detected."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            status_code=422,
            error_code="SCHEMA_VALIDATION_ERROR",
            details=details,
        )


class AgentOutputError(AdPilotError):
    """Raised when an agent produces data that fails ``output_model`` validation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            status_code=502,
            error_code="AGENT_OUTPUT_ERROR",
            details=details,
        )


class AgentInputValidationError(AdPilotError):
    """Raised when the supplied input data does not match ``input_model``."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            status_code=422,
            error_code="AGENT_INPUT_ERROR",
            details=details,
        )


class AgentExecutionError(AdPilotError):
    """Raised while an agent is executing for an unexpected reason."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="AGENT_EXECUTION_ERROR",
            details=details,
        )


class QualityGateFailureError(AdPilotError):
    """Raised when campaign quality gate fails after maximum retries."""

    def __init__(self, score: float, threshold: float, hints: Optional[list[str]] = None) -> None:
        super().__init__(
            message=f"Campaign quality score {score:.1f} failed to reach threshold {threshold:.1f}.",
            status_code=422,
            error_code="QUALITY_GATE_FAILED",
            details={"score": score, "threshold": threshold, "hints": hints or []},
        )


class ProviderError(AdPilotError):
    """Raised when an LLM provider fails."""

    def __init__(self, provider: str, message: str) -> None:
        super().__init__(
            message=f"LLM Provider '{provider}' error: {message}",
            status_code=502,
            error_code="PROVIDER_ERROR",
            details={"provider": provider},
        )
