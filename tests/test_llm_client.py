import asyncio

import httpx
import openai
import pytest

from app.clients.llm_client import OpenAILLMClient
from app.exceptions import (
    LLMConfigurationError,
    LLMProviderError,
    LLMRateLimitError,
    LLMUnavailableError,
)

from app.clients.llm_client import (
    FakeLLMClient,
    build_llm_client,
    OpenAILLMClient,
    _build_cached_llm_client,
)
from app.config import Settings



def setup_function() -> None:
    """
    每个测试开始前清空 Client Cache,
    防止缓存状态影响其他测试。
    """

    _build_cached_llm_client.cache_clear()

class FailingResponsesAPI:
    """
    代替 AsyncOpenAI.responses。

    create() 被调用时，抛出指定异常。
    """

    def __init__(self, error: Exception) -> None:
        self.error = error

    async def create(self, **kwargs):
        raise self.error


class FailingOpenAISDK:
    """
    代替真正的 AsyncOpenAI Client。
    """

    def __init__(self, error: Exception) -> None:
        self.responses = FailingResponsesAPI(error)


def build_failing_openai_client(
    error: Exception,
) -> OpenAILLMClient:
    client = OpenAILLMClient(
        api_key="test-api-key",
        model_name="test-model",
    )

    # 测试期间替换内部 SDK，
    # 确保不会发送真实网络请求。
    client._client = FailingOpenAISDK(error)

    return client

def test_openai_client_converts_connection_error():
    request = httpx.Request(
        "POST",
        "https://api.openai.com/v1/responses",
    )

    sdk_error = openai.APIConnectionError(
        request=request,
    )

    client = build_failing_openai_client(
        sdk_error
    )

    with pytest.raises(LLMUnavailableError):
        asyncio.run(
            client.generate_response("hello")
        )

def test_openai_client_converts_authentication_error():
    request = httpx.Request(
        "POST",
        "https://api.openai.com/v1/responses",
    )

    response = httpx.Response(
        status_code=401,
        request=request,
    )

    sdk_error = openai.AuthenticationError(
        "Invalid API key",
        response=response,
        body={},
    )

    client = build_failing_openai_client(
        sdk_error
    )

    with pytest.raises(LLMConfigurationError):
        asyncio.run(
            client.generate_response("hello")
        )

def test_openai_client_converts_authentication_error():
    request = httpx.Request(
        "POST",
        "https://api.openai.com/v1/responses",
    )

    response = httpx.Response(
        status_code=401,
        request=request,
    )

    sdk_error = openai.AuthenticationError(
        "Invalid API key",
        response=response,
        body={},
    )

    client = build_failing_openai_client(
        sdk_error
    )

    with pytest.raises(LLMConfigurationError):
        asyncio.run(
            client.generate_response("hello")
        )

def test_openai_client_converts_api_status_error():
    request = httpx.Request(
        "POST",
        "https://api.openai.com/v1/responses",
    )

    response = httpx.Response(
        status_code=500,
        request=request,
    )

    sdk_error = openai.APIStatusError(
        "Provider internal error",
        response=response,
        body={},
    )

    client = build_failing_openai_client(
        sdk_error
    )

    with pytest.raises(LLMProviderError):
        asyncio.run(
            client.generate_response("hello")
        )

def test_build_llm_client_uses_fake_provider():
    """
    配置为 fake 时，应创建 FakeLLMClient。
    """

    settings = Settings(
        llm_provider="fake",
        llm_model="test-fake-model",
    )

    client = build_llm_client(settings)

    assert isinstance(client, FakeLLMClient)
    assert client.model_name == "test-fake-model"

def test_build_llm_client_uses_openai_provider():
    """
    只验证配置能构建 OpenAI Client。

    不发送真实网络请求。
    """

    settings = Settings(
        llm_provider="openai",
        llm_model="test-openai-model",
        llm_api_key="test-api-key",
    )

    client = build_llm_client(settings)

    assert isinstance(client, OpenAILLMClient)
    assert client.model_name == "test-openai-model"


def test_openai_provider_requires_api_key():
    settings = Settings(
        llm_provider="openai",
        llm_model="test-openai-model",
        llm_api_key=None,
    )

    try:
        build_llm_client(settings)

    except LLMConfigurationError as error:
        assert str(error) == (
            "LLM_API_KEY is required "
            "when LLM_PROVIDER is openai"
        )

    else:
        raise AssertionError(
            "Expected ValueError when API key is missing"
        )

def test_build_llm_client_rejects_unknown_provider():
    """
    不支持的 Provider 不应被静默接受。
    """

    settings = Settings(
        llm_provider="unknown-provider",
        llm_model="test-model",
    )

    try:
        build_llm_client(settings)

    except LLMConfigurationError as error:
        assert str(error) == (
            "Unsupported LLM provider: unknown-provider"
        )

    else:
        raise AssertionError(
            "Expected ValueError for unsupported provider"
        )