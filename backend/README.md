# Backend - RH Chatbot using RAG Fusion

> **📖 Main Project Documentation**: See the [main README](../README.md) for complete project overview and Docker setup instructions.

AI-powered HR assistant backend for resume analysis and job matching using RAG (Retrieval-Augmented Generation).

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment variables:**
   Create a `.env` file:
   ```env
   HUGGINGFACE_API_KEY=your_huggingface_token
   GROQ_API_KEY=your_groq_api_key
   ```

3. **Run the application:**
   ```bash
   python -m app.main
   ```

4. **Access the API:**
   - **API**: http://localhost:8000
   - **Interactive Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

## Documentation

- **[Services Documentation](./SERVICES_DOCUMENTATION.md)** - Backend services architecture and implementation details
- **[API Documentation](./API_DOCUMENTATION.md)** - Complete API reference with examples

## Architecture Overview

### **High-Level Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Services   │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Groq)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Vector DB     │
                       │   (FAISS)       │
                       └─────────────────┘
```

### **Core Components**
- **FastAPI Application**: RESTful API server
- **RAG Pipeline**: Document retrieval and AI generation
- **Vector Database**: FAISS for similarity search
- **AI Integration**: Groq for LLM inference

## Data Flow

1. **Job Description Input** → AI generates focused sub-questions
2. **Sub-questions** → Vector search retrieves relevant resumes
3. **Retrieved Documents** → AI analyzes and generates responses
4. **Response** → Structured output to frontend

## Project Structure

```
backend/
├── app/
│   ├── api/endpoints.py          # API route handlers
│   ├── core/config.py            # Configuration management
│   ├── schemas/                  # Request/response models
│   ├── services/                 # Business logic services
│   └── main.py                   # Application entry point
├── Dockerfile                    # Container configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Configuration

### **Environment Variables**
| Variable | Description | Required |
|----------|-------------|----------|
| `HUGGINGFACE_API_KEY` | HuggingFace API token for models | Yes |
| `GROQ_API_KEY` | Groq API key for LLM inference | Yes |

### **Default Settings**
- **Port**: 8000
- **Host**: 0.0.0.0
- **CORS**: http://localhost:3000
- **Model**: llama3-8b-8192
- **Embeddings**: thenlper/gte-large

## Related Documentation

- **[Main Project README](../README.md)** - Complete project overview and Docker setup
- **[Frontend Documentation](../frontend/README.md)** - React application structure


