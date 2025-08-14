# RH Chatbot using RAG Fusion

AI-powered HR assistant for resume analysis and job matching using Retrieval-Augmented Generation (RAG).

##  Quick Start

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/wissemhammoudi/RH-chabot-using-RAG-Fusion
cd RH-chabot-using-RAG-Fusion

# Copy environment variables
cp env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Project Overview

This project consists of two main components:

- **Frontend**: React-based chatbot interface with modern UI/UX
- **Backend**: FastAPI-powered AI service with RAG capabilities

### **Architecture**
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

##  Documentation

### **Frontend Documentation**
- **[Frontend README](./frontend/README.md)** - React application structure and development guide

### **Backend Documentation**
- **[Backend README](./backend/README.md)** - Backend overview and quick start
- **[Services Documentation](./backend/SERVICES_DOCUMENTATION.md)** - Backend services architecture
- **[API Documentation](./backend/API_DOCUMENTATION.md)** - Complete API reference

##   Docker Setup

### **Prerequisites**
- Docker and Docker Compose installed
- Environment variables configured

### **Environment Variables**
Copy `env.example` to `.env` and fill in your API keys:

```bash
cp env.example .env
```

Required variables:
```env
# Backend API Keys
HUGGINGFACE_API_KEY=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
```

### **Start Services**
```bash
# Start all services
docker-compose up -d

```

## Project Structure

```
RH-chabot-using-RAG-Fusion/
├── frontend/                    # React application
│   ├── src/                    # Source code
│   ├── README.md               # Frontend documentation
│   └── package.json            # Dependencies
├── backend/                     # FastAPI application
│   ├── app/                    # Application code
│   ├── README.md               # Backend documentation
│   ├── SERVICES_DOCUMENTATION.md # Services architecture
│   ├── API_DOCUMENTATION.md    # API reference
│   └── requirements.txt        # Python dependencies
├── docker-compose.yml          # Service orchestration
├── env.example                 # Environment variables template
└── README.md                   # This file
```
