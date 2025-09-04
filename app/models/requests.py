# Copyright 2024
# Directory: yt-rag/app/models/requests.py

"""
Request models for the RAG API endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """Individual document chunk for seeding."""
    chunk_id: str = Field(..., description="Unique identifier for the chunk")
    source: str = Field(..., description="Source URL or identifier")
    text: str = Field(..., description="Text content of the chunk")


class SeedRequest(BaseModel):
    """Request model for the /seed endpoint."""
    docs: Optional[List[DocumentChunk]] = Field(
        None, 
        description="Optional list of documents to seed. If omitted, uses default documents."
    )


class AnswerRequest(BaseModel):
    """Request model for the /answer endpoint."""
    query: str = Field(..., description="User question to answer")
    top_k: Optional[int] = Field(
        6, 
        ge=1, 
        le=20, 
        description="Number of chunks to retrieve for context"
    )
