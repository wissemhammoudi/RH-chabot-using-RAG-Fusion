# Services Documentation

This document provides detailed information about the backend services architecture, implementation details, and how they work together.

## 🏗️ Service Architecture Overview

The backend follows a **Service-Oriented Architecture** pattern where each service has a single responsibility and communicates through well-defined interfaces.

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    API      │  │   Schemas   │  │    Core     │        │
│  │ Endpoints   │  │ Validation  │  │   Config    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  ChatBot    │  │ Document    │  │   Vector    │        │
│  │  Service    │  │ Retriever   │  │  Database   │        │
│  │             │  │  Service    │  │  Service    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Core Services

### **1. Configuration Service (`app/core/config.py`)**

**Purpose**: Centralized application configuration and environment variable management.

**Responsibilities**:
- Load environment variables from `.env` file
- Provide typed configuration values
- Centralize all application settings
- Ensure configuration consistency across services

**Key Configuration Categories**:
```python
# API Configuration
API_V1_STR: str = "/api/v1"
PROJECT_NAME: str = "RH Chatbot API"
VERSION: str = "1.0.0"

# Server Configuration
HOST: str = "0.0.0.0"
PORT: int = 8000
DEBUG: bool = True

# AI Model Configuration
GROQ_MODEL: str = "llama3-8b-8192"
EMBEDDING_MODEL: str = "thenlper/gte-large"

# RAG Configuration
RAG_K_THRESHOLD: int = 5
CHUNK_SIZE: int = 400
CHUNK_OVERLAP: int = 50
```

**Usage in Services**:
```python
from app.core.config import settings

# Access configuration values
api_key = settings.GROQ_API_KEY
model_name = settings.GROQ_MODEL
```

## 🤖 AI Services

### **2. ChatBot Service (`app/services/chatbot_service.py`)**

**Purpose**: Handle all AI interactions and chat generation using Groq API.

**Responsibilities**:
- Generate sub-questions from job descriptions
- Create contextual chat responses
- Manage AI model interactions
- Handle prompt engineering
- Error handling for AI service failures

**Key Methods**:

#### **`generate_subquestions(question: str) -> list`**
Generates focused sub-questions from a job description.

**Prompt Strategy**:
```python
system_message = """
    You are an expert in talent acquisition. Separate this job description 
    into 3-4 more focused aspects for efficient resume retrieval.
    Make sure every single relevant aspect of the query is covered in at least one query.
    Only use the information provided in the initial query. 
    Do not make up any requirements of your own.
"""
```

**Output Format**: List of 3-4 focused sub-questions

#### **`generate_message(question, docs, history, prompt_cls, joblist) -> str`**
Generates contextual responses based on retrieved documents and chat history.

**Prompt Classes**:
- `"retrieve_applicant_jd"`: For candidate selection scenarios
- `"default"`: For general resume analysis

**Context Integration**:
- Combines retrieved documents with job requirements
- Incorporates chat history for continuity
- Uses different system prompts based on context

**Error Handling**:
```python
try:
    response = self.client.chat.completions.create(...)
    return response.choices[0].message.content
except Exception as e:
    logger.error(f"Error generating message: {e}")
    return ""
```

## 📚 Document Processing Services

### **3. Document Retriever Service (`app/services/document_service.py`)**

**Purpose**: Manage RAG operations, document retrieval, and ranking algorithms.

**Responsibilities**:
- Implement reciprocal rank fusion for document ranking
- Retrieve documents by similarity scores
- Format and structure retrieved documents
- Handle document metadata and scoring

**Key Methods**:

#### **`reciprocal_rank_fusion(results: list[list], k: int = 60) -> list`**
Combines multiple search results using reciprocal rank fusion algorithm.

**Algorithm**:
```python
fused_scores = {}
for docs in results:
    for rank, doc in enumerate(docs):
        doc_str = json.dumps(doc)
        if doc_str not in fused_scores:
            fused_scores[doc_str] = 0
        fused_scores[doc_str] += 1 / (rank + k)
```

**Benefits**:
- Combines results from multiple sub-questions
- Reduces bias towards single search queries
- Improves overall retrieval quality

#### **`retrieve_id_and_rerank(subquestion_list: list) -> list`**
Retrieves documents for each sub-question and applies reranking.

**Process**:
1. Search for each sub-question individually
2. Collect similarity scores
3. Apply reciprocal rank fusion
4. Return reranked results

#### **`retrieve_documents_with_id(doc_id_with_score: dict, threshold: int = 5) -> list`**
Formats retrieved documents with applicant IDs.

**Formatting**:
```python
for i in range(len(retrieved_documents)):
    retrieved_documents[i] = f"Applicant ID {retrieved_ids[i]}\n{retrieved_documents[i]}"
```

### **4. Vector Database Service (`app/services/vector_service.py`)**

**Purpose**: Manage embeddings, vector store operations, and document processing pipeline.

**Responsibilities**:
- Initialize HuggingFace models and embeddings
- Load and process CSV data
- Create and manage FAISS vector store
- Handle document chunking and vectorization

**Initialization Process**:
```python
def _initialize_services(self):
    """Initialize HuggingFace login and load data."""
    try:
        login(token=settings.HUGGINGFACE_API_KEY)
        self._load_data()
        self._setup_embedding_model()
        self._create_vectorstore()
    except Exception as e:
        logger.error(f"Error initializing vector database service: {e}")
        raise
```

**Document Processing Pipeline**:
1. **Data Loading**: Read CSV with pandas
2. **Document Loading**: Use LangChain DataFrameLoader
3. **Text Splitting**: RecursiveCharacterTextSplitter with configurable chunk size
4. **Vectorization**: Create embeddings using Sentence Transformers
5. **Storage**: Store in FAISS vector database

**Chunking Strategy**:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,      # 400 characters
    chunk_overlap=settings.CHUNK_OVERLAP  # 50 characters
)
```

**Benefits**:
- Maintains context between chunks
- Optimizes for retrieval accuracy
- Configurable for different document types

## 🔄 Service Communication

### **Service Dependencies**

```
VectorDatabaseService
        ↓
DocumentRetrieverService
        ↓
ChatBotService
        ↓
API Endpoints
```

### **Data Flow Between Services**

1. **VectorDatabaseService** initializes and provides:
   - DataFrame with resume data
   - FAISS vector store for similarity search

2. **DocumentRetrieverService** uses vector store to:
   - Search for relevant documents
   - Apply ranking algorithms
   - Return formatted results

3. **ChatBotService** receives:
   - Retrieved documents from DocumentRetrieverService
   - Generates AI responses using Groq

4. **API Endpoints** orchestrate:
   - Service interactions
   - Request/response handling
   - Error management

## 🧪 Service Testing

### **Testing Strategy**

Each service can be tested independently:

```python
# Test ChatBot Service
def test_chatbot_service():
    service = ChatBotService()
    result = service.generate_subquestions("Software Engineer")
    assert len(result) > 0

# Test Document Retriever Service
def test_document_service():
    # Mock vector store and DataFrame
    service = DocumentRetrieverService(mock_df, mock_vectorstore)
    result = service.retrieve_documents_with_id({"1": 0.9})
    assert len(result) > 0
```

### **Mocking Dependencies**

```python
# Mock external services
@patch('app.services.chatbot_service.Groq')
def test_chatbot_with_mock_groq(mock_groq):
    mock_groq.return_value.chat.completions.create.return_value.choices = [
        Mock(message=Mock(content="Test response"))
    ]
    # Test service logic
```

## 📊 Service Monitoring

### **Health Checks**

Each service should implement health check methods:

```python
class ChatBotService:
    def health_check(self) -> dict:
        try:
            # Test Groq API connection
            return {"status": "healthy", "groq_api": "connected"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

### **Logging Strategy**

```python
import logging

logger = logging.getLogger(__name__)

class DocumentRetrieverService:
    def retrieve_documents(self, query: str):
        logger.info(f"Retrieving documents for query: {query}")
        try:
            # ... retrieval logic
            logger.info(f"Retrieved {len(results)} documents")
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise
```

## 🔧 Service Configuration

### **Environment Variables**

| Service | Variable | Purpose |
|---------|----------|---------|
| ChatBot | `GROQ_API_KEY` | Groq API authentication |
| Vector | `HUGGINGFACE_API_KEY` | Model access token |
| All | `DEBUG` | Enable debug logging |

### **Service-Specific Settings**

```python
# ChatBot Service Settings
GROQ_MODEL: str = "llama3-8b-8192"

# Vector Service Settings
EMBEDDING_MODEL: str = "thenlper/gte-large"
CHUNK_SIZE: int = 400
CHUNK_OVERLAP: int = 50

# Document Service Settings
RAG_K_THRESHOLD: int = 5
```

## 🚀 Service Extension

### **Adding New Services**

1. **Create service file** in `app/services/`
2. **Implement service class** with clear responsibilities
3. **Add to API endpoints** if needed
4. **Update configuration** if required
5. **Add health checks** and logging

### **Service Interface Pattern**

```python
from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def health_check(self) -> dict:
        pass
    
    @abstractmethod
    def process(self, data: any) -> any:
        pass
```

## 🔒 Service Security

### **Input Validation**

All services use Pydantic schemas for validation:

```python
from app.schemas.requests import JobDescriptionRequest

def process_job_description(job: JobDescriptionRequest):
    # Pydantic automatically validates input
    description = job.description
    # Process validated data
```

### **Error Handling**

Services implement secure error handling:

```python
try:
    result = external_api_call()
    return result
except Exception as e:
    logger.error(f"Service error: {e}")
    # Don't expose internal details
    raise HTTPException(status_code=500, detail="Service unavailable")
```

## 📈 Performance Optimization

### **Service-Level Caching**

```python
from functools import lru_cache

class VectorDatabaseService:
    @lru_cache(maxsize=128)
    def get_embedding_model(self):
        # Cache model loading
        return SentenceTransformer(settings.EMBEDDING_MODEL)
```

### **Async Operations**

Services can be extended with async support:

```python
class ChatBotService:
    async def generate_message_async(self, question: str):
        # Async implementation for better performance
        pass
```

---

**Next**: Check the [API Documentation](./API_DOCUMENTATION.md) for endpoint details and usage examples.
