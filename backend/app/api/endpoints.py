from fastapi import APIRouter, HTTPException, Depends
from app.schemas.requests import JobDescriptionRequest, QueryRequest, ChatRequest
from app.schemas.responses import SubquestionsResponse, ResumesResponse, ChatResponse
from app.services.chatbot_service import ChatBotService
from app.services.document_service import DocumentRetrieverService
from app.services.vector_service import VectorDatabaseService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
vector_service = VectorDatabaseService()
chatbot_service = ChatBotService()
document_service = DocumentRetrieverService(
    vector_service.get_dataframe(), 
    vector_service.get_vectorstore()
)

@router.post("/generate_subquestions/", response_model=SubquestionsResponse)
async def generate_subquestions(job: JobDescriptionRequest):
    """Generate sub-questions from a job description."""
    try:
        subquestions = chatbot_service.generate_subquestions(job.description)
        if not subquestions:
            raise HTTPException(status_code=500, detail="Failed to generate sub-questions")
        return SubquestionsResponse(subquestions=subquestions)
    except Exception as e:
        logger.error(f"Error in generate_subquestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrieve_resumes/", response_model=ResumesResponse)
async def retrieve_resumes(request: QueryRequest):
    """Retrieve resumes based on sub-questions."""
    try:
        if not request.subquestions:
            raise HTTPException(status_code=400, detail="Sub-questions are required")

        retrieved_ids = document_service.retrieve_id_and_rerank(request.subquestions)
        document_service.meta_data["retrieved_docs_with_scores"] = retrieved_ids
        retrieved_resumes = document_service.retrieve_documents_with_id(dict(retrieved_ids))
        
        return ResumesResponse(resumes=retrieved_resumes)
    except Exception as e:
        logger.error(f"Error in retrieve_resumes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/", response_model=ChatResponse)
async def generate_message(request: ChatRequest):
    """Generate a chat message based on context and history."""
    try:
        if not request.subquestions:
            raise HTTPException(status_code=400, detail="Sub-questions are required")
        
        message = chatbot_service.generate_message(
            request.question,
            request.docs,
            request.history,
            request.prompt_cls,
            request.subquestions
        )
        
        if not message:
            raise HTTPException(status_code=500, detail="Failed to generate message")
        
        return ChatResponse(message=message)
    except Exception as e:
        logger.error(f"Error in generate_message: {e}")
        raise HTTPException(status_code=500, detail=str(e))
