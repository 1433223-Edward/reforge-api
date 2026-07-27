from typing import Any

import httpx

from app.config import settings


def fetch_external_data() -> dict[str, Any]:
    # Client（客户端对象）负责向外部 HTTP 服务发送请求。
    #
    # 使用 with：
    # 请求完成后，HTTP Client 会被正常关闭，
    # 避免连接等资源长期处于未释放状态。
    #
    # timeout=5.0：
    # 最多等待约 5 秒。
    # 外部服务不能无限期拖住当前后端请求。
    with httpx.Client(timeout=5.0) as client:
        response = client.get(
            # 使用 Settings 中的 Base URL，
            # 再组合当前需要访问的具体路径。
            f"{settings.external_api_base_url}/get",

            # params 会被 HTTPX 编码为 Query Parameters（查询参数）。
            #
            # 最终请求大致类似：
            # GET /get?source=reforge
            params={"source": "reforge"},
        )

        # 如果上游返回 4xx 或 5xx，
        # raise_for_status() 会抛出 HTTPStatusError。
        #
        # 注意：
        # HTTPX 收到一个 HTTP 响应，并不代表请求业务上成功。
        # 例如 404 和 500 也都是有效的 HTTP 响应。
        response.raise_for_status()

        # response.json() 会把 JSON Response Body
        # 解析为 Python 数据结构。
        data = response.json()

        # 当前先返回我们后续 Endpoint 真正需要的数据。
        #
        # 不直接把完整上游响应原样公开给客户端，
        # 避免当前 API 与第三方响应结构产生过强耦合。
        return {
            "source": data["args"]["source"],
            "upstream_status": response.status_code,
        }