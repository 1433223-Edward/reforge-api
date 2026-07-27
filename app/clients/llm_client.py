import logging
import openai

from fastapi import Depends, HTTPException
from app.config import Settings, get_settings
from functools import lru_cache
from openai import AsyncOpenAI
from app.exceptions import (
    LLMConfigurationError,
    LLMProviderError,
    LLMRateLimitError,
    LLMUnavailableError,
)

logger = logging.getLogger(__name__)

class LLMClient:
    """
    所有 LLM Client 的基础接口。

    Endpoint 只需要知道：
    给 generate_response() 一条消息，
    Client 会返回一条字符串回复。

    具体模型提供商如何实现，由子类负责。
    """

    async def generate_response(
        self,
        message: str,
    ) -> str:
        """
        异步生成模型回复。

        真实 Client 后续会在这里等待外部 LLM API。
        """
        raise NotImplementedError


class FakeLLMClient(LLMClient):
    """
    当前开发阶段使用的假 LLM Client。

    它不访问真实网络，也不消耗模型额度。
    作用是帮助我们验证完整的应用调用链。
    """
    def __init__(self, model_name: str) -> None:
        # 当前只是保存配置，后续真实 Client 会真正使用模型名。
        self.model_name = model_name

    async def generate_response(
        self,
        message: str,
    ) -> str:
        return f"Fake AI response to: {message}"


# 当前应用默认使用的 Client 实例。
# 后续接入真实 Provider 时，可以替换具体实现。

class OpenAILLMClient(LLMClient):
    """
    使用 OpenAI Responses API 的真实异步 Client。

    该类负责隐藏：
    - OpenAI SDK
    - API Key
    - 模型配置
    - Provider Response 对象
    """

    def __init__(
        self,
        api_key: str,
        model_name: str,
    ) -> None:
        self.model_name = model_name

        # AsyncOpenAI 内部负责异步 HTTP 通信。
        self._client = AsyncOpenAI(
            api_key=api_key,
        )

    async def generate_response(
        self,
        message: str,
    ) -> str:
        """
        将用户消息发送给真实模型，并返回纯文本。
        """
        try:
            response = await self._client.responses.create(
                model=self.model_name,
                instructions=(
                    "You are a concise and helpful assistant."
                ),
                input=message,
            )

            return response.output_text
        
        except (
            openai.AuthenticationError,
            openai.PermissionDeniedError,
        ) as error:
            # API Key 无效或当前账号没有权限，
            # 对 /chat 用户而言，这是服务器配置问题。
            raise LLMConfigurationError(
                "OpenAI authentication or permission failed"
            ) from error

        except openai.RateLimitError as error:
            # Provider 返回 429。
            raise LLMRateLimitError(
                "OpenAI rate limit reached"
            ) from error

        except openai.APIConnectionError as error:
            # APITimeoutError 也是 APIConnectionError 的子类，
            # 所以连接错误和超时都会进入这里。
            raise LLMUnavailableError(
                "OpenAI connection failed"
            ) from error

        except openai.APIStatusError as error:
            # 其他由上游 4xx / 5xx 状态触发的错误。
            # request_id 可以帮助服务器侧定位问题，
            # 但不直接返回给客户端。
            raise LLMProviderError(
                "OpenAI API returned "
                f"status {error.status_code}; "
                f"request_id={error.request_id}"
            ) from error

        except openai.APIError as error:
            # 兜底处理其他 OpenAI SDK API 异常。
            raise LLMProviderError(
                "Unexpected OpenAI SDK error"
            ) from error


@lru_cache
def _build_cached_llm_client(
    provider: str,
    model_name: str,
    api_key: str | None,
) -> LLMClient:
    """
    根据纯配置值创建并缓存 Client。

    缓存可以避免每个请求都重新创建 SDK Client,
    从而复用底层连接资源。
    """

    normalized_provider = provider.strip().lower()

    if normalized_provider == "fake":
        return FakeLLMClient(
            model_name=model_name,
        )

    if normalized_provider == "openai":
        if not api_key or not api_key.strip():
            raise LLMConfigurationError(
                "LLM_API_KEY is required "
                "when LLM_PROVIDER is openai"
            )

        return OpenAILLMClient(
            api_key=api_key.strip(),
            model_name=model_name,
        )

    raise LLMConfigurationError(
        f"Unsupported LLM provider: {provider}"
    )

def build_llm_client(
    settings: Settings,
) -> LLMClient:
    """
    将结构化 Settings 转换成具体 LLM Client。
    """

    return _build_cached_llm_client(
        provider=settings.llm_provider,
        model_name=settings.llm_model,
        api_key=settings.llm_api_key,
    )

def get_llm_client(
    settings: Settings = Depends(get_settings),
) -> LLMClient:
    """
    构建 LLM Client。

    配置错误发生在 Dependency Resolution 阶段，
    因此需要在这里转换成稳定的 HTTP Response。
    """

    try:
        return build_llm_client(settings)

    except LLMConfigurationError as error:
        logger.exception(
            "LLM Client configuration failed"
        )

        raise HTTPException(
            status_code=500,
            detail="LLM service configuration error",
        ) from error