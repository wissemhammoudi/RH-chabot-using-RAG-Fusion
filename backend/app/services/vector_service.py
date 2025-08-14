import pandas as pd
import logging
from huggingface_hub import login
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.document_loaders import DataFrameLoader
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorDatabaseService:
    """Service for managing vector database operations."""
    
    def __init__(self):
        self.embedding_model = None
        self.vectorstore = None
        self.df = None
        self._initialize_services()
    
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
    
    def _load_data(self):
        """Load CSV data into pandas DataFrame."""
        try:
            self.df = pd.read_csv(settings.DATA_FILE_PATH)
            logger.info(f"Loaded data from {settings.DATA_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def _setup_embedding_model(self):
        """Setup the embedding model for text vectorization."""
        try:
            # Load sentence transformer model
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            
            # Setup LangChain embeddings
            self.langchain_embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                multi_process=True,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )
            logger.info(f"Embedding model {settings.EMBEDDING_MODEL} loaded successfully")
        except Exception as e:
            logger.error(f"Error setting up embedding model: {e}")
            raise
    
    def _create_vectorstore(self):
        """Create FAISS vector store from documents."""
        try:
            # Load documents
            loader = DataFrameLoader(self.df, page_content_column=settings.CONTENT_COLUMN)
            documents = loader.load()
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE, 
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            document_chunks = text_splitter.split_documents(documents)
            
            # Create vector store
            self.vectorstore = FAISS.from_documents(
                document_chunks, 
                self.langchain_embeddings, 
                distance_strategy=DistanceStrategy.COSINE
            )
            logger.info(f"Vector store created with {len(document_chunks)} chunks")
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get the loaded DataFrame."""
        return self.df
    
    def get_vectorstore(self):
        """Get the FAISS vector store."""
        return self.vectorstore
