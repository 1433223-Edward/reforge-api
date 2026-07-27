from fastapi.testclient import TestClient
import pytest
from app.clients.llm_client import LLMClient, get_llm_client
from app.main import app
from app.exceptions import (
    LLMConfigurationError,
    LLMProviderError,
    LLMRateLimitError,
    LLMUnavailableError,
)

client = TestClient(app)

class StubLLMClient(LLMClient):
    """
    测试专用 LLM Client。

    它返回固定、可预测的结果，
    不访问任何真实网络或模型服务。
    """

    async def generate_response(self, message: str) -> str:
        return f"Stub response: {message}"

class ErrorLLMClient(LLMClient):
    """
    调用时抛出指定应用级异常。
    """

    def __init__(self, error: Exception) -> None:
        self.error = error

    async def generate_response(
        self,
        message: str,
    ) -> str:
        raise self.error

def override_llm_with_error(
    error: Exception,
) -> None:
    def provider() -> LLMClient:
        return ErrorLLMClient(error)

    app.dependency_overrides[get_llm_client] = (
        provider
    )

def override_get_llm_client() -> LLMClient:
    """
    测试期间提供 StubLLMClient。
    """

    return StubLLMClient()

@pytest.fixture(autouse=True)
def override_llm_dependency():
    """
    test_chat.py 中的每个测试都使用 Stub Client。

    这样测试不会受到：
    - .env 当前 Provider
    - API Key
    - 真实网络
    - OpenAI 服务状态
    的影响。
    """

    app.dependency_overrides[get_llm_client] = (
        override_get_llm_client
    )

    yield

    # 只删除本测试设置的 Override，
    # 不要误删其他测试可能使用的 Override。
    app.dependency_overrides.pop(
        get_llm_client,
        None,
    )

def test_chat_maps_llm_unavailable_to_502():
    override_llm_with_error(
        LLMUnavailableError(
            "Internal connection information"
        )
    )

    response = client.post(
        "/chat",
        json={
            "message": "hello",
        },
    )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "LLM service unavailable",
    }

    # 内部错误信息不能泄露给客户端。
    assert "Internal connection information" not in (
        response.text
    )

def test_chat_maps_llm_configuration_error_to_500():
    override_llm_with_error(
        LLMConfigurationError(
            "Invalid secret configuration"
        )
    )

    response = client.post(
        "/chat",
        json={
            "message": "hello",
        },
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "LLM service configuration error",
    }

    assert "Invalid secret configuration" not in (
        response.text
    )

def test_chat_maps_llm_provider_error_to_502():
    override_llm_with_error(
        LLMProviderError(
            "Provider internal response"
        )
    )

    response = client.post(
        "/chat",
        json={
            "message": "hello",
        },
    )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "LLM service failed",
    }

def test_chat_success():
    """
    正常消息应返回 200 和稳定的 ChatResponse。
    """

    app.dependency_overrides[get_llm_client] = (
        override_get_llm_client
        )

    try:

        response = client.post(
            "/chat",
            json={
                "message": "hello",
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "response": "Stub response: hello",
        }
    finally:
        app.dependency_overrides.clear()


def test_chat_strips_surrounding_whitespace():
    """
    Endpoint 应删除消息首尾空格，
    避免把无意义空白传入后续 LLM 调用链。
    """

    app.dependency_overrides[get_llm_client] = (
        override_get_llm_client
    )

    try:
        response = client.post(
            "/chat",
            json={
                "message": "   hello   ",
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "response": "Stub response: hello",
        }

    finally:
        app.dependency_overrides.clear()

def test_chat_missing_message_returns_422():
    """
    缺少必填字段属于 Request Model 验证失败，
    应由 FastAPI 和 Pydantic 返回 422。
    """

    response = client.post(
        "/chat",
        json={},
    )

    assert response.status_code == 422


def test_chat_blank_message_returns_400():
    """
    空白消息的结构和类型正确，但业务上无效，
    因此应返回 400。
    """

    response = client.post(
        "/chat",
        json={
            "message": "   ",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Message cannot be blank",
    }