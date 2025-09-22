# Directory: yt-rag/app/services/embedding.py
import logging
from typing import List
from openai import OpenAI
from ..core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_DASHSCOPE_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

class EmbeddingService:
    """Embeddings via Qwen (DashScope OpenAI-compatible)."""
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.aliyun_api_key,    # 统一用阿里云 Key
            base_url=_DASHSCOPE_BASE
        )
        # 统一从阿里云模型读取
        self.embed_model = settings.aliyun_embed_model

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        try:
            resp = self.client.embeddings.create(
                model=self.embed_model,
                input=texts
            )
            emb = [d.embedding for d in resp.data]
            logger.info(f"Generated embeddings for {len(texts)} texts via Qwen")
            return emb
        except Exception as e:
            logger.error(f"Failed to generate embeddings via Qwen: {e}")
            raise

    async def embed_query(self, query: str) -> List[float]:
        return (await self.embed_texts([query]))[0]

embedding_service = EmbeddingService()
