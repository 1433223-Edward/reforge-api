import app.main as main_module
from fastapi.testclient import TestClient
import httpx
from app.main import app
import pytest
from fastapi import HTTPException

# TestClient 直接连接 FastAPI Application。
# 测试时通常不需要单独启动 Uvicorn。
client = TestClient(main_module.app)


# def test_external_check_success(monkeypatch):
#     """
#     验证外部服务正常时：
#     /external-check 返回 200 和预期 JSON。
#     """

#     def fake_fetch_external_data():
#         # 这是测试替身，不访问真实互联网。
#         # 我们只模拟 external_client 正常返回结果的情况。
#         return {
#             "source": "reforge",
#             "upstream_status": 200,
#         }

#     # main.py 中实际使用的是：
#     # main_module.fetch_external_data
#     #
#     # 因此测试期间将这个名字临时替换成假函数。
#     monkeypatch.setattr(
#         main_module,
#         "fetch_external_data",
#         fake_fetch_external_data,
#     )

#     # 像浏览器一样访问 API，但请求直接进入 FastAPI app。
#     response = client.get("/external-check")

#     # 验证 HTTP 状态码。
#     assert response.status_code == 200

#     # 验证响应 JSON 的完整内容。
#     assert response.json() == {
#         "source": "reforge",
#         "upstream_status": 200,
#     }

def test_external_check_success():
    """
    验证外部依赖成功时,Endpoint 返回稳定的响应。
    """

    def fake_get_external_data() -> dict:
        # 测试不访问真实网络,直接提供确定结果。
        return {
            "upstream_status": 200,
        }

    # 告诉 FastAPI：
    # 当应用需要 get_external_data 时,
    # 测试期间改用 fake_get_external_data。
    app.dependency_overrides[main_module.get_external_data] = (
        fake_get_external_data
    )

    try:
        response = client.get("/external-check")

        assert response.status_code == 200
        assert response.json() == {
            "source": "reforge",
            "upstream_status": 200,
        }

    finally:
        # 测试结束后清除 Override，避免污染其他测试。
        app.dependency_overrides.clear()

def test_get_external_data_converts_httpx_error_to_502(
    monkeypatch,
):
    """
    验证底层网络错误会在 Dependency 层
    转换成稳定的 HTTPException 502。
    """

    def fake_fetch_external_data():
        raise httpx.ConnectError(
            "Simulated connection failure"
        )

    monkeypatch.setattr(
        main_module,
        "fetch_external_data",
        fake_fetch_external_data,
    )

    with pytest.raises(HTTPException) as captured_exception:
        main_module.get_external_data()

    assert captured_exception.value.status_code == 502
    assert captured_exception.value.detail == (
        "External service request failed"
    )



# def test_external_check_failure_returns_502(monkeypatch):
#     """
#     验证外部服务访问失败时：
#     内部 HTTPX 异常被转换成稳定的 502 Response。
#     """

#     def fake_fetch_external_data():
#         # 不需要真的断网。
#         # 假函数直接模拟 HTTPX 连接失败。
#         raise httpx.ConnectError("Simulated connection failure")

#     monkeypatch.setattr(
#         main_module,
#         "fetch_external_data",
#         fake_fetch_external_data,
#     )

#     response = client.get("/external-check")

#     assert response.status_code == 502

#     assert response.json() == {
#         "detail": "External service request failed",
#     }