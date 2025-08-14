from pydantic import BaseModel
from typing import List

class JobDescriptionRequest(BaseModel):
    """Request schema for job description processing."""
    description: str

class QueryRequest(BaseModel):
    """Request schema for resume retrieval."""
    subquestions: List[str]

class ChatRequest(BaseModel):
    """Request schema for chat generation."""
    question: str
    subquestions: List[str]
    history: List[dict]
    docs: List[str]
    prompt_cls: str
