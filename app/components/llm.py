from langchain_groq import ChatGroq
from app.config.config import GROQ_API_KEY
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(model_name:str = "llama-3.1-8b-instant", groq_api_key:str = GROQ_API_KEY):
      try:
            logger.info(f"Loading LLM model {model_name}")

            llm = ChatGroq(model=model_name, api_key=groq_api_key,
                           temperature=0.3, max_tokens=256)
            
            logger.info(f"LLM model loaded successfully from Groq")

            return llm
      except Exception as e:
            error_message = CustomException("Failed to load LLM model",e)
            logger.error(f"Error: {error_message}")
            return None
      
