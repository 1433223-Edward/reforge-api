class LLMClientError(Exception):
    """
    所有应用级 LLM 异常的基础类。

    上层代码只需要依赖这些异常，
    不需要依赖具体 Provider SDK。
    """


class LLMConfigurationError(LLMClientError):
    """
    LLM 配置错误。

    例如：
    - OpenAI Provider 缺少 API Key
    - API Key 无效
    - 当前账号没有调用权限
    """


class LLMUnavailableError(LLMClientError):
    """
    无法连接上游 LLM 服务。

    例如：
    - 网络连接失败
    - 请求超时
    - SSL 或代理问题
    """


class LLMRateLimitError(LLMClientError):
    """
    上游 Provider 限流或暂时无法处理请求。
    """


class LLMProviderError(LLMClientError):
    """
    其他没有被细分的 Provider 错误。
    """