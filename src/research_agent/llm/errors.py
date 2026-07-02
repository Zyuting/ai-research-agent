"""LLM 调用相关的异常层次结构。"""


class LLMError(Exception):
    """LLM 调用基类异常。"""


class LLMConfigurationError(LLMError):
    """API Key / Base URL 等配置错误。"""


class LLMAuthenticationError(LLMError):
    """认证失败（API Key 无效或过期）。"""


class LLMRateLimitError(LLMError):
    """触发频率限制。"""


class LLMBadRequestError(LLMError):
    """请求参数错误（model 不存在、prompt 过长等）。"""


class LLMTemporaryError(LLMError):
    """服务端临时故障，可重试。"""
