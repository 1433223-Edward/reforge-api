from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    POST /chat 的请求模型。

    FastAPI 会使用这个 Model 验证客户端发送的 JSON:
    - 必须包含 message
    - message 必须是字符串
    """

    message: str


class ChatResponse(BaseModel):
    """
    POST /chat 的响应模型。

    它定义了当前接口对客户端承诺的稳定输出结构。
    """

    response: str