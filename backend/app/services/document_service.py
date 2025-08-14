import pandas as pd
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class DocumentRetrieverService:
    """Service for document retrieval and RAG operations."""
    
    def __init__(self, df: pd.DataFrame, vectorstore):
        self.df = df
        self.vectorstore = vectorstore
        self.meta_data = {}

    def reciprocal_rank_fusion(self, results: list[list], k: int = 60) -> list:
        """Apply reciprocal rank fusion to combine multiple search results."""
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

    def __retrieve_docs_id__(self, question: str, k: int = 50) -> dict:
        """Retrieve document IDs with similarity scores."""
        docs_score = self.vectorstore.similarity_search_with_score(question, k=k)
        docs_score_dict = {str(doc.metadata["ID"]): score for doc, score in docs_score}
        return docs_score_dict

    def retrieve_id_and_rerank(self, subquestion_list: list) -> list:
        """Retrieve and rerank documents based on multiple sub-questions."""
        document_rank_list = []
        for subquestion in subquestion_list:
            doc_scores = self.__retrieve_docs_id__(subquestion, settings.RAG_K_THRESHOLD)
            document_rank_list.append(doc_scores)
        reranked_documents = self.reciprocal_rank_fusion(document_rank_list)
        return reranked_documents

    def retrieve_documents_with_id(self, doc_id_with_score: dict, threshold: int = 5) -> list:
        """Retrieve documents by ID with formatting."""
        id_resume_dict = dict(zip(self.df[settings.ID_COLUMN].astype(str), self.df[settings.CONTENT_COLUMN]))
        retrieved_ids = list(sorted(doc_id_with_score, key=doc_id_with_score.get, reverse=True))[:threshold]
        retrieved_documents = [id_resume_dict[id] for id in retrieved_ids]
        
        for i in range(len(retrieved_documents)):
            retrieved_documents[i] = f"Applicant ID {retrieved_ids[i]}\n{retrieved_documents[i]}"
        
        return retrieved_documents

    def retrieve_applicant_id(self, id_list: list) -> list:
        """Retrieve resumes by specific applicant IDs."""
        retrieved_resumes = []
        for id in id_list:
            try:
                resume = self.df[self.df[settings.ID_COLUMN].astype(str) == id].iloc[0][settings.CONTENT_COLUMN]
                retrieved_resumes.append(resume)
            except Exception as e:
                logger.error(f"Error retrieving resume for ID {id}: {e}")
                continue
        return retrieved_resumes
