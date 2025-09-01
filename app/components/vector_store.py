from langchain_community.vectorstores import FAISS
import os
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.components.embeddings import get_embedding_model
from app.config.config import DB_FAISS_PATH

logger = get_logger(__name__)

def load_vector_store():
      try:
            embedding_model = get_embedding_model()

            if os.path.exists(DB_FAISS_PATH):
                  logger.info(f"Loading Existing vector store from {DB_FAISS_PATH}")

                  return FAISS.load_local(DB_FAISS_PATH,embedding_model, allow_dangerous_deserialization=True)
            else:
                  logger.warning(f"Vector store not found at {DB_FAISS_PATH}")
      except Exception as e:
            error_message = CustomException("Failed to load vector store",e)
            logger.error(f"Error: {error_message}")
            return None

# Creating new vectorstore function
def save_vector_store(text_chunks):
      try:
            if not text_chunks:
                  raise CustomException("No text chunks were found")
            
            logger.info(f"Creating new vector store with {len(text_chunks)} text chunks")
            embedding_model = get_embedding_model()

            db = FAISS.from_documents(text_chunks,embedding_model)

            logger.info(f"Saving vector store to {DB_FAISS_PATH}")
            db.save_local(DB_FAISS_PATH)
            logger.info(f"Vector store saved sucesfully")
      
      except Exception as e:
            error_message = CustomException("Failed to save vector store",e)
            logger.error(f"Error: {error_message}")
