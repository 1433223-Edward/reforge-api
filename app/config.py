from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):

    app_name: str = "Project Reforge LLM Service"

    external_api_base_url: str = "https://httpbin.org"

    llm_provider: str = "fake"
    llm_model: str = "reforge-fake-v1"
    llm_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    """
    返回缓存后的 Settings 对象。

    应用运行期间通常只需要读取并创建一次配置。
    """

    return Settings()

settings = Settings()