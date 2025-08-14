from pydantic import BaseModel
from typing import List

class SubquestionsResponse(BaseModel):
    """Response schema for sub-questions generation."""
    subquestions: List[str]

class ResumesResponse(BaseModel):
    """Response schema for resume retrieval."""
    resumes: List[str]

class ChatResponse(BaseModel):
    """Response schema for chat generation."""
    message: str
