import os

from app.components.pdf_loader import load_pdf_files,create_text_chunks
from app.components.vector_store import save_vector_store
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import DB_FAISS_PATH

logger = get_logger(__name__)

def process_store_pdfs():
      try:
            logger.info("Starting the data loading process")
            documents = load_pdf_files()
            text_chunks = create_text_chunks(documents)

            save_vector_store(text_chunks)

            logger.info("Data loading process completed successfully")
      except Exception as e:
            error_message = CustomException("Failed to process and store pdfs",e)
            logger.error(f"Error: {error_message}")
            return None
      
if __name__ == "__main__":
      process_store_pdfs()
