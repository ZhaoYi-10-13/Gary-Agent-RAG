# Directory: Gary-Agent-RAG/app/core/config.py
from typing import Literal, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # -------- Supabase --------
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_anon_key: str = Field(..., env="SUPABASE_ANON_KEY")
    supabase_service_role_key: str = Field(..., env="SUPABASE_SERVICE_ROLE_KEY")

    # -------- Provider --------
    ai_provider: Literal["openai", "anthropic", "aliyun"] = Field(default="aliyun", env="AI_PROVIDER")

    # -------- 阿里云通义千问--------
    aliyun_api_key: str = Field(..., env="ALIYUN_API_KEY")
    aliyun_chat_model: str = Field(default="qwen-plus", env="ALIYUN_CHAT_MODEL")
    aliyun_embed_model: str = Field(default="text-embedding-v4", env="ALIYUN_EMBED_MODEL")

    #保留 OpenAI/Anthropic 字段以兼容老逻辑
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_chat_model: str = Field(default="", env="OPENAI_CHAT_MODEL")
    openai_embed_model: str = Field(default="", env="OPENAI_EMBED_MODEL")

    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    anthropic_chat_model: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_CHAT_MODEL")

    # -------- App / RAG --------
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    default_top_k: int = Field(default=6)
    chunk_size: int = Field(default=400)
    chunk_overlap: int = Field(default=60)
    temperature: float = Field(default=0.1)
    embedding_dimensions: int = Field(default=1024)

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

def get_settings() -> Settings:
    return settings
