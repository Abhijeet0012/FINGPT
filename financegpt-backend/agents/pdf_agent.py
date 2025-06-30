import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from typing import List, Dict
from chromadb.config import Settings

class PDFAgent:
    def __init__(self, pdf_directory: str = "brochures"):
        logger.info(f"Initializing PDFAgent with directory: {pdf_directory}")
        self.pdf_directory = pdf_directory
        self.embeddings = OpenAIEmbeddings()
        self.db = None
        self.initialize_db()

    def load_pdfs(self) -> List[str]:
        logger.info("Loading PDF documents")
        documents = []
        for file in os.listdir(self.pdf_directory):
            if file.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, file)
                logger.info(f"Processing PDF file: {pdf_path}")
                loader = PyPDFLoader(pdf_path, mode="page")
                documents.extend(loader.load())
        logger.info(f"Loaded {len(documents)} documents (pages)")
        return documents

    def initialize_db(self):
        logger.info("Initializing database")
        client_settings = Settings(anonymized_telemetry=False)
        if os.path.exists("./chroma_db"):
            logger.info("Loading existing Chroma database")
            self.db = Chroma(
                embedding_function=self.embeddings,
                persist_directory="./chroma_db",
                client_settings=client_settings
            )
        else:
            logger.info("Creating new Chroma database")
            documents = self.load_pdfs()
            logger.info(f"Using {len(documents)} page documents as chunks")
            self.db = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory="./chroma_db",
                client_settings=client_settings
            )

    def query_documents(self, query: str, k: int = 2) -> Dict:
        logger.info(f"Querying documents with: {query}")
        if not self.db:
            logger.error("Database not initialized")
            raise ValueError("Database not initialized")

        retriever = self.db.as_retriever(search_kwargs={"k": k})
        llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        logger.info("Executing query chain")
        response = qa_chain.invoke({"query": query})
        logger.info("Query completed successfully")
        # Log the metadata of each fetched chunk
        for i, doc in enumerate(response['source_documents']):
            logger.info(f"Fetched chunk {i+1}: metadata={doc.metadata}")
        return {
            "answer": response['result'],
            "source_documents": [doc.page_content for doc in response['source_documents']]
        }

    def process_query(self, user_query: str) -> str:
        logger.info(f"Processing user query: {user_query}")
        try:
            results = self.query_documents(user_query)
            
            # Prepare context for summarization
            context = "\n".join(results["source_documents"])
            
            return context
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"Error processing query: {str(e)}"
