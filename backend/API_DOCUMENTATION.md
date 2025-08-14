# API Documentation

Complete API reference for the RH Chatbot backend, including all endpoints, request/response schemas, and usage examples.

## Base Information

- **Base URL**: `http://localhost:8000`
- **API Version**: v1
- **Documentation**: `http://localhost:8000/docs` (Swagger UI)


##  Endpoint Details

### **1. Root Endpoint**

#### **GET /** - Application Information

**Description**: Returns basic application information and health status.

**Response**:
```json
{
  "message": "RH Chatbot API",
  "version": "1.0.0",
  "status": "healthy"
}
```



---

### **2. Health Check**

#### **GET /health** - Service Health Status

**Description**: Returns the current health status of the service.

**Response**:
```json
{
  "status": "healthy"
}
```




### **3. Generate Sub-questions**

#### **POST /generate_subquestions/** - Create Focused Sub-questions

**Description**: Generates 3-4 focused sub-questions from a job description using AI analysis.

**Request Schema**:
```json
{
  "description": "string"
}
```

**Response Schema**:
```json
{
  "subquestions": ["string", "string", "string"]
}
```


**Example Request**:
```bash
curl -X POST "http://localhost:8000/generate_subquestions/" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Senior Software Engineer with 5+ years of Python experience, knowledge of Django, React, and AWS. Experience with microservices architecture and CI/CD pipelines."
  }'
```

**Example Response**:
```json
{
  "subquestions": [
    "Python development experience with 5+ years",
    "Django and React framework knowledge",
    "AWS cloud services experience",
    "Microservices architecture and CI/CD experience"
  ]
}
```

**AI Prompt Strategy**:
The service uses a specialized prompt to break down job descriptions:
```
You are an expert in talent acquisition. Separate this job description 
into 3-4 more focused aspects for efficient resume retrieval.
Make sure every single relevant aspect of the query is covered in at least one query.
Only use the information provided in the initial query.
Do not make up any requirements of your own.
```

---

### **4. Retrieve Resumes**

#### **POST /retrieve_resumes/** - Find Matching Resumes

**Description**: Retrieves relevant resumes based on sub-questions using vector similarity search and ranking algorithms.

**Request Schema**:
```json
{
  "subquestions": ["string", "string", "string"]
}
```

**Response Schema**:
```json
{
  "resumes": ["string", "string", "string"]
}
```


**Example Request**:
```bash
curl -X POST "http://localhost:8000/retrieve_resumes/" \
  -H "Content-Type: application/json" \
  -d '{
    "subquestions": [
      "Python development experience with 5+ years",
      "Django and React framework knowledge",
      "AWS cloud services experience"
    ]
  }'
```

**Example Response**:
```json
{
  "resumes": [
    "Applicant ID 123\nJohn Doe\nSenior Software Engineer\n5+ years Python, Django, React, AWS experience...",
    "Applicant ID 456\nJane Smith\nFull Stack Developer\n4 years Python, Django, React, cloud experience...",
    "Applicant ID 789\nBob Johnson\nSoftware Engineer\n3 years Python, Django, AWS experience..."
  ]
}
```

**RAG Process**:
1. **Vector Search**: Each sub-question searches the FAISS vector database
2. **Similarity Scoring**: Documents ranked by cosine similarity
3. **Reciprocal Rank Fusion**: Combines results from multiple queries
4. **Top-K Selection**: Returns top 5 most relevant resumes


### **5. Generate Chat Response**

#### **POST /generate/** - AI Chat Generation

**Description**: Generates contextual AI responses based on retrieved documents, chat history, and user questions.

**Request Schema**:
```json
{
  "question": "string",
  "subquestions": ["string", "string"],
  "history": [
    {
      "question": "string",
      "answer": "string"
    }
  ],
  "docs": ["string", "string"],
  "prompt_cls": "string"
}
```

**Response Schema**:
```json
{
  "message": "string"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/generate/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Which candidate has the strongest Python experience?",
    "subquestions": ["Python development experience with 5+ years"],
    "history": [],
    "docs": ["Applicant ID 123\nJohn Doe\n5+ years Python experience..."],
    "prompt_cls": "retrieve_applicant_jd"
  }'
```

**Example Response**:
```json
{
  "message": "Based on the retrieved resumes, **John Doe (Applicant ID 123)** has the strongest Python experience with 5+ years of development experience. His background shows extensive work with Python frameworks and cloud services, making him the most qualified candidate for this position."
}
```
