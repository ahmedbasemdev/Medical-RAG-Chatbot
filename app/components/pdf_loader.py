import os
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.common.logger import get_logger
from app.config.config import DATA_PATH,CHUNK_SIZE,CHUNK_OVERLAP
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_pdf_files():
      try:
            if not os.path.exists(DATA_PATH):
                  raise CustomException("Data path does not exist")
            
            logger.info(f"Loading files from {DATA_PATH}")

            loader = DirectoryLoader(DATA_PATH,glob="*.pdf",loader_cls=PyPDFLoader)
            documents = loader.load()
            
            if not documents:
                  logger.warning("No pdfs were found")
            else:
                  logger.info(f"Sucesfully fetched {len(documents)} documents")

            return documents
      except Exception as e:
            error_message = CustomException("Failed to load pdf files",e)
            logger.error(f"Error: {error_message}")
            return []

def create_text_chunks(documents):
      try:
            if not documents:
                  raise CustomException("No documents were found")
            
            logger.info(f"Creating text chunks from {len(documents)} documents")

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)

            text_chunks = text_splitter.split_documents(documents)

            logger.info(f"Sucesfully created {len(text_chunks)} text chunks")

            return text_chunks
      except Exception as e:
            error_message = CustomException("Failed to create text chunks",e)
            logger.error(f"Error: {error_message}")
            return []

