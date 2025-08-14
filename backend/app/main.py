import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.dont_write_bytecode = True

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered HR assistant for resume analysis and job matching"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="")

@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "message": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT
    )
