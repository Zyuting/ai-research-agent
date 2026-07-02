"""LLM error hierarchy — maps provider-specific errors to domain exceptions."""


class LLMError(Exception):
    """Base exception for all LLM-related errors."""


class LLMConfigurationError(LLMError):
    """Missing or invalid configuration (API key, base URL, etc.)."""


class LLMAuthenticationError(LLMError):
    """Authentication failure — invalid or expired API key."""


class LLMRateLimitError(LLMError):
    """Rate limit exceeded."""


class LLMBadRequestError(LLMError):
    """Invalid request — unsupported model, context length exceeded, etc."""


class LLMTemporaryError(LLMError):
    """Transient server error — safe to retry."""
