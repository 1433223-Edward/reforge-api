from typing import Any
import httpx
import logging
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from app.config import settings
from app.external_client import fetch_external_data
from app.schemas import ChatRequest, ChatResponse
from app.clients.llm_client import LLMClient, get_llm_client
from app.exceptions import (
    LLMConfigurationError,
    LLMProviderError,
    LLMRateLimitError,
    LLMUnavailableError,
)
# 配置基础 Logging。
#
# level=logging.INFO：
# 表示 INFO 以及更严重的日志级别都允许输出。
#
# 当前只做最小配置。
# 暂时不加入文件日志、日志轮转、JSON Formatter 等复杂内容。
logging.basicConfig(level=logging.INFO)

# __name__ 是当前 Python Module（模块）的名称。
#
# 当前文件是 app/main.py，
# 当它作为 app.main 被导入时，__name__ 通常是 "app.main"。
#
# 使用模块名创建 Logger，可以帮助我们判断：
# “这条日志来自项目中的哪个模块？”
logger = logging.getLogger(__name__)

class MessageRequest(BaseModel):message: str

class MessageResponse(BaseModel):message: str

class ExternalCheckResponse(BaseModel):
    # 我们传给上游服务并由上游返回的来源标记。
    source: str

    # 上游服务返回的 HTTP Status Code。
    upstream_status: int
# 从 Settings Object 读取应用名称。
#
# 这里不再把 "Project Reforge API" 直接硬编码在应用创建代码中。
app = FastAPI(title=settings.app_name)

def process_message(message: str) -> str:
    # 这是一个最小的“业务处理函数”。
    #
    # 当前只是为了制造一个可控的失败场景，
    # 后续真正调用 LLM API 时，类似的 Service Function
    # 可能因为网络、认证、超时等原因失败。
    if message == "explode":
        # ValueError 是 Python 内置异常类型之一。
        #
        # 这里故意抛出异常，用于训练 Exception Handling。
        raise ValueError("Simulated processing failure")

    return message

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/echo", response_model=MessageResponse)
def echo_message(request: MessageRequest) -> MessageResponse:
    # strip() 会移除字符串两端的空白字符。
    #
    # 例如：
    # "  hello  ".strip() -> "hello"
    # "     ".strip()      -> ""
    #
    # 因此：
    # not request.message.strip()
    # 用于判断 message 是否只包含空白字符。
    if not request.message.strip():
    # HTTPException 用来主动终止当前请求，
    # 并返回一个明确的 HTTP Error Response。
    #
    # 这里使用 400，因为：
    # 请求的 JSON 结构和字段类型是合法的，
    # 但 message 的内容违反了当前 Endpoint 的业务规则。
        raise HTTPException(
        status_code=400,
        detail="Message cannot be blank",
        )
    
    try:
        # 这里调用一个可能抛出异常的内部函数。
        processed_message = process_message(request.message)

    except ValueError:
        # logger.exception() 应该在 except block（异常捕获块）中使用。
        #
        # 它会记录：
        # 1. 我们提供的日志消息
        # 2. 当前正在处理的 Exception 信息
        # 3. Stack Trace（堆栈追踪）
        #
        # Stack Trace 能帮助开发者定位：
        # 异常经过了哪些函数调用，以及最终在哪里发生。
        logger.exception("Message processing failed")

        # 客户端仍然只收到稳定、适合公开的错误信息。
        # 内部 Stack Trace 不直接放进 HTTP Response。
        raise HTTPException(
            status_code=500,
            detail="Message processing failed",
        )

    logger.info("Message processed successfully")

    return MessageResponse(message=processed_message)

def get_external_data() -> dict:
    """
    调用外部服务，并把底层 HTTPX 异常转换为稳定的 HTTP 响应。

    该函数作为 FastAPI Dependency:
    - 成功时返回外部服务数据
    - 失败时记录内部日志并返回 502
    """
    try:
        return fetch_external_data()

    except httpx.HTTPError:
        logger.exception("External API request failed")

        raise HTTPException(
            status_code=502,
            detail="External service request failed",
        )

@app.get(
    "/external-check",
    response_model=ExternalCheckResponse,
)
def external_check(
    external_data: dict = Depends(get_external_data),
):
    """
    返回外部服务检查结果。

    Endpoint 只负责把依赖提供的数据转换成 API Response,
    不直接处理底层 HTTP 通信。
    """
    return ExternalCheckResponse(
        source="reforge",
        upstream_status=external_data["upstream_status"],
    )

# def external_check() -> ExternalCheckResponse:
#     try:
#         # 调用我们自己的外部服务访问函数。
#         #
#         # Endpoint 不需要知道 HTTP 请求的所有细节；
#         # 它只需要使用 external_client 提供的结果。
#         result = fetch_external_data()

#     except httpx.HTTPError:
#         # HTTPError 是 HTTPX 多种 HTTP 相关异常的共同父类。
#         #
#         # 当前先统一处理：
#         # - 网络连接失败
#         # - 超时
#         # - 上游返回错误状态
#         #
#         # 后续会通过实验观察，再决定是否需要细分。
#         logger.exception("External API request failed")

#         # 502 Bad Gateway：
#         # 当前服务器作为中间层调用上游服务，
#         # 但没有从上游获得可正常使用的结果。
#         raise HTTPException(
#             status_code=502,
#             detail="External service request failed",
#         )

#     # FastAPI 会在运行 Endpoint 前调用 fetch_external_data，
#     # 再把返回结果注入 result。
#     # 不直接把任意 dict 传出去，
#     # 而是显式建立当前 API 承诺的 Response Model。
#     return ExternalCheckResponse(
#         source=result["source"],
#         upstream_status=result["upstream_status"],
#     )

@app.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest,
         llm_client: LLMClient = Depends(get_llm_client),
         ) -> ChatResponse:
    """
    接收用户消息，并返回当前最小 Echo Response。

    本 Checkpoint 先验证完整 API 链路。
    后续会把回复生成逻辑替换为 LLM Client。
    """

    # Pydantic 已经保证 message 是字符串。
    # 这里删除首尾空白，再检查它是否具有实际内容。
    cleaned_message = request.message.strip()

    if not cleaned_message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be blank",
        )

    # 日志只记录请求已经进入，不记录完整用户内容，
    # 为后续避免敏感数据泄露保留良好习惯。
    logger.info("Chat request received")

    try:
        generated_response = (
            await llm_client.generate_response(
                cleaned_message
            )
        )

    except LLMConfigurationError as error:
        logger.exception(
            "LLM runtime configuration failed"
        )

        raise HTTPException(
            status_code=500,
            detail="LLM service configuration error",
        ) from error

    except LLMRateLimitError as error:
        logger.exception(
            "LLM Provider rate limit reached"
        )

        raise HTTPException(
            status_code=503,
            detail="LLM service temporarily unavailable",
        ) from error

    except LLMUnavailableError as error:
        logger.exception(
            "LLM Provider connection failed"
        )

        raise HTTPException(
            status_code=502,
            detail="LLM service unavailable",
        ) from error

    except LLMProviderError as error:
        logger.exception(
            "LLM Provider request failed"
        )

        raise HTTPException(
            status_code=502,
            detail="LLM service failed",
        ) from error

    return ChatResponse(
        response=generated_response,
    )