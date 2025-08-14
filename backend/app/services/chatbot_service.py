from groq import Groq
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ChatBotService:
    """Service for handling AI chat interactions."""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
    
    def generate_subquestions(self, question: str) -> list:
        """Generate sub-questions from a job description."""
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
            logger.error(f"Error generating sub-questions: {e}")
            return []

    def generate_message(self, question: str, docs: list, history: list, prompt_cls: str, joblist: list) -> str:
        """Generate a chat message based on context and history."""
        context = "\n\n".join(docs) 
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
            logger.error(f"Error generating message: {e}")
            return ""
