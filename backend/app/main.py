from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import login
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.document_loaders import DataFrameLoader
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from groq import Groq
import faiss
import json
import sys
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
load_dotenv()

# Define Pydantic models for request bodies
class JobDescription(BaseModel):
    description: str

class QueryRequest(BaseModel):
    subquestions: list
class chatRequest(BaseModel):
    question : str
    subquestions: list
    history : list
    docs :list
    prompt_cls : str
    

# Initialize FastAPI app
app = FastAPI()
# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this based on your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)
# Initialize Hugging Face login and set up variables
login(token=os.getenv("HuggingFace_API_KEY"))

EMBEDDING_MODEL = "thenlper/gte-large"

def load_embedding_model(model_name: str):
    return SentenceTransformer(model_name)

embedding_model = load_embedding_model(EMBEDDING_MODEL)

# Load data and initialize vector store
df = pd.read_csv('./chat.csv')
loader = DataFrameLoader(df, page_content_column="content")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
documents = loader.load()
document_chunks = text_splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    multi_process=True,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

KNOWLEDGE_VECTOR_DATABASE = FAISS.from_documents(
    document_chunks, embedding_model, distance_strategy=DistanceStrategy.COSINE
)

sys.dont_write_bytecode = True
RAG_K_THRESHOLD = 5

class ChatBot:
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate_subquestions(self, question: str):
        system_message = """
            You are an expert in talent acquisition. Separate this job description into 3-4 more focused aspects for efficient resume retrieval.
            Make sure every single relevant aspect of the query is covered in at least one query. You may choose to remove irrelevant information that doesn't contribute to finding resumes.
            Only use the information provided in the initial query. Do not make up any requirements of your own.
            Put each result in one line, separated by a linebreak.
        """

        user_message = f"""
            Generate 3 to 4 distinct sub-queries based on this initial job description:
            {question}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ]
            )
            result = response.choices[0].message.content.split("\n")
            return [subq.strip() for subq in result if subq.strip()]
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def generate_message(self, question: str, docs: list, history: list, prompt_cls: str, joblist: list):
        context = "\n\n".join(docs)  # Ensure documents are strings
        job = "\n\n".join(joblist)
        if prompt_cls == "retrieve_applicant_jd":
            system_message = """
                You are an expert in talent acquisition who helps determine the best candidate among multiple suitable resumes.
                Use the following pieces of context to determine the best resume given a job description.
                Provide detailed explanations for the best resume choice.
                Use the applicant ID to refer to resumes in your response.
                If you don't know the answer, just say that you don't know; do not try to make up an answer.
            """

            user_message = f"""
                Context:
                {context}
                Job Requirement:
                {job}

                Question:
                {question}
            """
        else:
            system_message = """
                You are an expert in talent acquisition who helps analyze resumes for effective resume screening.
                Use the provided context and chat history to answer the question.
                Do not mention that chat history is provided in your response.
                If you don't know the answer, just say that you don't know; do not try to make up an answer.
            """

            user_message = f"""
                Chat History:
                {history}

                Context:
                {context}

                Question:
                {question}
            """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

class DocumentRetriever:
    def __init__(self, df, vectorstore):
        self.df = df
        self.vectorstore = vectorstore
        self.meta_data = {}

    def reciprocal_rank_fusion(self, results: list[list], k=60):
        fused_scores = {}
        for docs in results:
            for rank, doc in enumerate(docs):
                doc_str = json.dumps(doc)
                if doc_str not in fused_scores:
                    fused_scores[doc_str] = 0
                fused_scores[doc_str] += 1 / (rank + k)

        reranked_results = [
            (json.loads(doc), score)
            for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        ]
        return reranked_results

    def __retrieve_docs_id__(self, question: str, k=50):
        docs_score = self.vectorstore.similarity_search_with_score(question, k=k)
        docs_score_dict = {str(doc.metadata["ID"]): score for doc, score in docs_score}
        return docs_score_dict

    def retrieve_id_and_rerank(self, subquestion_list: list):
        document_rank_list = []
        for subquestion in subquestion_list:
            doc_scores = self.__retrieve_docs_id__(subquestion, RAG_K_THRESHOLD)
            document_rank_list.append(doc_scores)
        reranked_documents = self.reciprocal_rank_fusion(document_rank_list)
        return reranked_documents

    def retrieve_documents_with_id(self, doc_id_with_score: dict, threshold=5):
        id_resume_dict = dict(zip(self.df["ID"].astype(str), self.df["content"]))
        retrieved_ids = list(sorted(doc_id_with_score, key=doc_id_with_score.get, reverse=True))[:threshold]
        retrieved_documents = [id_resume_dict[id] for id in retrieved_ids]
        for i in range(len(retrieved_documents)):
            retrieved_documents[i] = "Applicant ID " + retrieved_ids[i] + "\n" + retrieved_documents[i]
        return retrieved_documents

    def retrieve_applicant_id(self, id_list: list):
        retrieved_resumes = []
        for id in id_list:
            try:
                resume = self.df[self.df["ID"].astype(str) == id].iloc[0]["content"]
                retrieved_resumes.append(resume)
            except:
                return []
        return retrieved_resumes

# Initialize ChatBot and DocumentRetriever instances
api_key = os.getenv("GROQ_API_KEY")
model = 'llama3-8b-8192'
chatbot = ChatBot(api_key=api_key, model=model)
retriever = DocumentRetriever(df, KNOWLEDGE_VECTOR_DATABASE)

@app.post("/generate_subquestions/")
async def generate_subquestions(job: JobDescription):
    subquestions = chatbot.generate_subquestions(job.description)
    if not subquestions:
        raise HTTPException(status_code=500, detail="Failed to generate sub-questions")
    return {"subquestions": subquestions}

@app.post("/retrieve_resumes/")
async def retrieve_resumes(request: QueryRequest):
    subquestions = request.subquestions
    if not subquestions:
        raise HTTPException(status_code=400, detail="Sub-questions are required")

    retrieved_ids = retriever.retrieve_id_and_rerank(subquestions)
    retriever.meta_data["retrieved_docs_with_scores"] = retrieved_ids
    retrieved_resumes = retriever.retrieve_documents_with_id(dict(retrieved_ids))
    return {"resumes": retrieved_resumes}
@app.post("/generate/")
async def generate_message(request: chatRequest):
    subquestions = request.subquestions
    history = request.history
    question = request.question
    docs = request.docs
    prompt_cls =request.prompt_cls
    if not subquestions:
        raise HTTPException(status_code=400, detail="Sub-questions are required")
    message = chatbot.generate_message(question,docs,history,prompt_cls,subquestions)
    if not message:
        raise HTTPException(status_code=500, detail="Failed to generate message")
    return {"message": message}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
